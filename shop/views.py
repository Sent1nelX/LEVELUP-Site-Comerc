from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import (
    add_to_cart,
    clear_cart,
    get_cart_items,
    remove_cart_item,
    update_cart_item,
)
from .forms import CheckoutForm, ContactForm
from .models import Category, ContactRequest, Order, OrderItem, Product, ProductVariant


def home(request):
    featured_products = (
        Product.objects.filter(is_active=True, is_featured=True)
        .select_related("category")
        .prefetch_related("images")[:8]
    )
    new_arrivals = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related("images")[:8]
    )
    categories = Category.objects.all()

    lookbook_items = [
        {
            "title": "Action",
            "subtitle": "Адреналин и динамика",
            "image": "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=1200&auto=format&fit=crop",
        },
        {
            "title": "RPG",
            "subtitle": "Огромные открытые миры",
            "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200&auto=format&fit=crop",
        },
        {
            "title": "Sports",
            "subtitle": "Лучшие спортивные симуляторы",
            "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=1200&auto=format&fit=crop",
        },
    ]

    return render(
        request,
        "shop/home.html",
        {
            "featured_products": featured_products,
            "new_arrivals": new_arrivals,
            "categories": categories,
            "lookbook_items": lookbook_items,
        },
    )


def catalog(request):
    query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "")
    selected_platform = request.GET.get("platform", "")
    selected_age_rating = request.GET.get("age_rating", "")
    selected_sort = request.GET.get("sort", "new")
    in_stock_only = request.GET.get("in_stock", "0") == "1"

    min_price_raw = request.GET.get("min_price", "").strip()
    max_price_raw = request.GET.get("max_price", "").strip()

    products = Product.objects.filter(is_active=True).select_related("category").prefetch_related(
        "variants", "images"
    )

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(developer__icontains=query)
        )

    if selected_category:
        products = products.filter(category__slug=selected_category)

    valid_age_ratings = {choice[0] for choice in Product.AgeRating.choices}
    if selected_age_rating in valid_age_ratings:
        products = products.filter(age_rating=selected_age_rating)

    valid_platforms = {choice[0] for choice in ProductVariant.PLATFORM_CHOICES}
    if selected_platform in valid_platforms:
        products = products.filter(variants__platform=selected_platform)

    if in_stock_only:
        products = products.filter(variants__stock__gt=0)

    if min_price_raw:
        try:
            min_price = Decimal(min_price_raw)
            products = products.filter(price__gte=min_price)
        except InvalidOperation:
            min_price_raw = ""

    if max_price_raw:
        try:
            max_price = Decimal(max_price_raw)
            products = products.filter(price__lte=max_price)
        except InvalidOperation:
            max_price_raw = ""

    products = products.distinct()

    sort_map = {
        "new": ["-created_at"],
        "popular": ["-is_featured", "-created_at"],
        "price_asc": ["price"],
        "price_desc": ["-price"],
        "name": ["name"],
    }
    products = products.order_by(*sort_map.get(selected_sort, sort_map["new"]))

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "shop/catalog.html",
        {
            "products": page_obj.object_list,
            "page_obj": page_obj,
            "categories": Category.objects.all(),
            "query": query,
            "selected_category": selected_category,
            "selected_platform": selected_platform,
            "selected_age_rating": selected_age_rating,
            "selected_sort": selected_sort,
            "in_stock_only": in_stock_only,
            "min_price": min_price_raw,
            "max_price": max_price_raw,
            "platform_choices": ProductVariant.PLATFORM_CHOICES,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related("variants", "images"), slug=slug, is_active=True
    )
    related_products = (
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(id=product.id)
        .prefetch_related("images")[:4]
    )

    platform_map = dict(ProductVariant.PLATFORM_CHOICES)
    edition_map = dict(ProductVariant.EDITION_CHOICES)
    available_platforms = sorted(
        {platform_map.get(v.platform, v.platform) for v in product.variants.all()}
    )
    available_editions = sorted(
        {edition_map.get(v.edition, v.edition) for v in product.variants.all()}
    )

    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "available_platforms": available_platforms,
            "available_editions": available_editions,
        },
    )


@require_POST
def add_to_cart_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    quantity = max(1, int(request.POST.get("quantity", 1)))
    variant_id = request.POST.get("variant_id") or None

    if product.variants.exists() and not variant_id:
        messages.error(request, "Выберите платформу и издание перед добавлением в корзину.")
        return redirect("shop:product_detail", slug=product.slug)

    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
        if variant.stock < quantity:
            messages.error(request, "Недостаточно товара на складе.")
            return redirect("shop:product_detail", slug=product.slug)

    add_to_cart(
        request.session,
        product_id=product.id,
        quantity=quantity,
        variant_id=variant.id if variant else None,
    )
    messages.success(request, "Игра добавлена в корзину.")
    return redirect("shop:cart")


def cart_view(request):
    items, total = get_cart_items(request.session)
    return render(request, "shop/cart.html", {"items": items, "total": total})


@require_POST
def cart_update_view(request):
    key = request.POST.get("key", "")
    quantity = int(request.POST.get("quantity", 1))
    update_cart_item(request.session, key, quantity)
    messages.success(request, "Корзина обновлена.")
    return redirect("shop:cart")


@require_POST
def cart_remove_view(request):
    key = request.POST.get("key", "")
    remove_cart_item(request.session, key)
    messages.success(request, "Позиция удалена из корзины.")
    return redirect("shop:cart")


def checkout(request):
    items, total = get_cart_items(request.session)
    if not items:
        messages.info(request, "Корзина пуста.")
        return redirect("shop:catalog")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                for item in items:
                    if item["variant"] and item["variant"].stock < item["quantity"]:
                        messages.error(
                            request,
                            f"Недостаточно на складе: {item['product'].name} ({item['variant']}).",
                        )
                        return redirect("shop:cart")

                payment_method = form.cleaned_data.get("payment_method", "cash")
                card_last_four = ""

                if payment_method == "card":
                    card_number = form.cleaned_data.get("card_number", "").replace(" ", "").strip()
                    card_holder = form.cleaned_data.get("card_holder", "").strip()
                    card_expiry = form.cleaned_data.get("card_expiry", "").strip()
                    card_cvv = form.cleaned_data.get("card_cvv", "").strip()

                    if not card_number:
                        messages.error(request, "Пожалуйста, введите номер карты.")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})
                    if not card_holder:
                        messages.error(request, "Пожалуйста, введите имя владельца карты.")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})
                    if not card_expiry:
                        messages.error(request, "Пожалуйста, введите срок действия карты.")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})
                    if not card_cvv:
                        messages.error(request, "Пожалуйста, введите CVV код.")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})
                    if not card_number.isdigit():
                        messages.error(request, "Номер карты должен содержать только цифры.")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})
                    if len(card_number) not in [13, 14, 15, 16, 17, 18, 19]:
                        messages.error(request, f"Номер карты должен содержать 13-19 цифр (введено {len(card_number)}).")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})
                    if not card_cvv.isdigit():
                        messages.error(request, "CVV код должен содержать только цифры.")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})
                    if len(card_cvv) not in [3, 4]:
                        messages.error(request, f"CVV код должен содержать 3-4 цифры (введено {len(card_cvv)}).")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})
                    if "/" not in card_expiry or len(card_expiry) != 5:
                        messages.error(request, "Срок действия должен быть в формате MM/YY.")
                        return render(request, "shop/checkout.html", {"items": items, "total": total, "form": form})

                    card_last_four = card_number[-4:]

                order = Order.objects.create(
                    full_name=form.cleaned_data["full_name"],
                    phone=form.cleaned_data["phone"],
                    email=form.cleaned_data["email"],
                    city=form.cleaned_data["city"],
                    address=form.cleaned_data["address"],
                    comment=form.cleaned_data["comment"],
                    total_amount=Decimal("0.00"),
                    payment_method=payment_method,
                    card_last_four=card_last_four,
                )

                for item in items:
                    product = item["product"]
                    variant = item["variant"]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        variant=variant,
                        item_title=product.name,
                        quantity=item["quantity"],
                        unit_price=item["unit_price"],
                    )
                    if variant:
                        variant.stock -= item["quantity"]
                        variant.save(update_fields=["stock"])

                order.recalculate_total()

            clear_cart(request.session)
            return redirect("shop:order_success", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(
        request, "shop/checkout.html", {"items": items, "total": total, "form": form}
    )


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_success.html", {"order": order})


def about(request):
    return render(
        request,
        "shop/about.html",
        {
            "stats": [
                {"value": "500+", "label": "Игр в каталоге"},
                {"value": "6",    "label": "Платформ"},
                {"value": "24ч",  "label": "Доставка по городу"},
            ]
        },
    )


def delivery(request):
    return render(request, "shop/delivery.html")


def faq(request):
    questions = [
        {
            "question": "Физическая или цифровая копия — что лучше?",
            "answer": "Физическая копия — это диск, который можно перепродать или дать другу. Цифровая — удобнее: скачивается сразу после оплаты, не занимает место на полке.",
        },
        {
            "question": "Как быстро приходят цифровые ключи?",
            "answer": "Цифровые ключи отправляются автоматически на email сразу после подтверждения оплаты. Обычно в течение нескольких минут.",
        },
        {
            "question": "Можно ли вернуть игру?",
            "answer": "Физические копии принимаем в течение 14 дней при сохранении оригинальной запечатанной упаковки. Цифровые ключи возврату не подлежат после активации.",
        },
        {
            "question": "Как отследить заказ?",
            "answer": "После отправки физического заказа мы присылаем трек-номер курьерской службы на email. Отслеживание доступно на сайте курьера.",
        },
        {
            "question": "Есть ли игры для старых консолей (PS4, Xbox One)?",
            "answer": "Да, в нашем каталоге есть игры для PS4 и Xbox One. Используйте фильтр по платформе в каталоге.",
        },
        {
            "question": "Работаете ли вы с оптом?",
            "answer": "Да, для оптовых закупок оставьте заявку через страницу контактов. Обсудим условия индивидуально.",
        },
    ]
    return render(request, "shop/faq.html", {"questions": questions})


def contacts(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactRequest.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data.get("phone", ""),
                topic=form.cleaned_data["topic"],
                message=form.cleaned_data["message"],
            )
            messages.success(request, "Спасибо! Мы получили сообщение и скоро свяжемся с вами.")
            return redirect("shop:contacts")
    else:
        form = ContactForm()

    stores = [
        {
            "city": "Алматы",
            "address": "пр. Абая, 109В",
            "work_time": "Пн–Вс: 10:00–22:00",
        },
        {
            "city": "Астана",
            "address": "пр. Республики, 33",
            "work_time": "Пн–Вс: 10:00–21:00",
        },
    ]

    return render(request, "shop/contacts.html", {"form": form, "stores": stores})
