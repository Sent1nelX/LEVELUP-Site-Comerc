from django.contrib import admin

from .models import Category, ContactRequest, Order, OrderItem, Product, ProductImage, ProductVariant


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "age_rating",
        "developer",
        "price",
        "discount_percent",
        "is_featured",
        "is_active",
    )
    list_filter = ("category", "age_rating", "is_featured", "is_active")
    search_fields = ("name", "description", "developer")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVariantInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("item_title", "quantity", "unit_price", "variant")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "city", "total_amount", "payment_method", "card_last_four", "status", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("full_name", "phone", "email", "address")
    inlines = [OrderItemInline]


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "topic", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "phone", "topic", "message")
    readonly_fields = ("name", "email", "phone", "topic", "message", "created_at")
    list_editable = ("status",)
    ordering = ("-created_at",)


admin.site.site_header = "LEVELUP Admin"
admin.site.site_title = "LEVELUP"
admin.site.index_title = "Управление магазином LEVELUP"
