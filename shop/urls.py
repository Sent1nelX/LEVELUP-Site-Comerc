from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("about/", views.about, name="about"),
    path("delivery/", views.delivery, name="delivery"),
    path("faq/", views.faq, name="faq"),
    path("contacts/", views.contacts, name="contacts"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("product/<slug:slug>/add/", views.add_to_cart_view, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/update/", views.cart_update_view, name="cart_update"),
    path("cart/remove/", views.cart_remove_view, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/success/", views.order_success, name="order_success"),
]
