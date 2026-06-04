from decimal import Decimal

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    class AgeRating(models.TextChoices):
        PEGI3  = "pegi3",  "PEGI 3"
        PEGI7  = "pegi7",  "PEGI 7"
        PEGI12 = "pegi12", "PEGI 12"
        PEGI16 = "pegi16", "PEGI 16"
        PEGI18 = "pegi18", "PEGI 18"

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    developer = models.CharField(max_length=120, blank=True)
    age_rating = models.CharField(max_length=10, choices=AgeRating.choices, default=AgeRating.PEGI12)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        if not self.discount_percent:
            return self.price
        discount = (Decimal(self.discount_percent) / Decimal("100")) * self.price
        return (self.price - discount).quantize(Decimal("0.01"))

    @property
    def primary_image_url(self):
        image = self.images.filter(is_primary=True).first() or self.images.first()
        return image.image_url if image else ""


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image_url = models.URLField(max_length=800)
    alt_text = models.CharField(max_length=220, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Изображение игры"
        verbose_name_plural = "Изображения игр"

    def __str__(self):
        return f"{self.product.name} | image"


class ProductVariant(models.Model):
    PLATFORM_CHOICES = [
        ("ps5",    "PlayStation 5"),
        ("xsx",    "Xbox Series X"),
        ("ps4",    "PlayStation 4"),
        ("xone",   "Xbox One"),
        ("switch", "Nintendo Switch"),
        ("pc",     "PC (Steam/Epic)"),
    ]

    EDITION_CHOICES = [
        ("standard", "Standard Edition"),
        ("deluxe",   "Deluxe Edition"),
        ("ultimate", "Ultimate Edition"),
        ("gold",     "Gold Edition"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(max_length=64, unique=True)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    edition = models.CharField(max_length=20, choices=EDITION_CHOICES, default="standard")
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["product", "platform", "edition"]
        unique_together = ("product", "platform", "edition")
        verbose_name = "Вариант игры"
        verbose_name_plural = "Варианты игр"

    def __str__(self):
        return f"{self.product.name} | {self.get_platform_display()} | {self.get_edition_display()}"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW        = "new",        "Новый"
        PROCESSING = "processing", "В обработке"
        DONE       = "done",       "Завершен"
        CANCELED   = "canceled",   "Отменен"

    class PaymentMethod(models.TextChoices):
        CARD = "card", "Оплата картой"
        CASH = "cash", "Оплата при получении"

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=32)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=220)
    comment = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    card_last_four = models.CharField(max_length=4, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} — {self.full_name}"

    def recalculate_total(self):
        self.total_amount = sum(
            (item.subtotal for item in self.items.all()), start=Decimal("0.00")
        )
        self.save(update_fields=["total_amount"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    item_title = models.CharField(max_length=220)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.item_title} x {self.quantity}"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price


class ContactRequest(models.Model):
    class Status(models.TextChoices):
        NEW      = "new",      "Новая"
        IN_WORK  = "in_work",  "В работе"
        DONE     = "done",     "Обработана"

    name    = models.CharField(max_length=120, verbose_name="Имя")
    email   = models.EmailField(verbose_name="Email")
    phone   = models.CharField(max_length=32, blank=True, verbose_name="Телефон")
    topic   = models.CharField(max_length=180, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    status  = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW, verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка с контактов"
        verbose_name_plural = "Заявки с контактов"

    def __str__(self):
        return f"#{self.id} {self.name} — {self.topic}"
