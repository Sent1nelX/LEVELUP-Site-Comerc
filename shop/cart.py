from decimal import Decimal

from django.shortcuts import get_object_or_404

from .models import Product, ProductVariant


CART_SESSION_KEY = "cart"


def _get_cart_data(session):
    cart = session.get(CART_SESSION_KEY)
    if cart is None:
        cart = {"items": {}}
        session[CART_SESSION_KEY] = cart
    return cart


def add_to_cart(session, product_id, quantity=1, variant_id=None):
    cart = _get_cart_data(session)
    key = f"{product_id}:{variant_id or 'no-variant'}"
    item = cart["items"].get(key)

    if item:
        item["quantity"] += quantity
    else:
        cart["items"][key] = {
            "product_id": product_id,
            "variant_id": variant_id,
            "quantity": quantity,
        }

    session.modified = True


def update_cart_item(session, key, quantity):
    cart = _get_cart_data(session)
    if key not in cart["items"]:
        return

    if quantity <= 0:
        cart["items"].pop(key, None)
    else:
        cart["items"][key]["quantity"] = quantity

    session.modified = True


def remove_cart_item(session, key):
    cart = _get_cart_data(session)
    cart["items"].pop(key, None)
    session.modified = True


def clear_cart(session):
    session[CART_SESSION_KEY] = {"items": {}}
    session.modified = True


def get_cart_items(session):
    cart = _get_cart_data(session)
    items = []
    total = Decimal("0.00")

    for key, row in cart["items"].items():
        product = get_object_or_404(Product, id=row["product_id"], is_active=True)
        variant = None
        if row.get("variant_id"):
            variant = get_object_or_404(ProductVariant, id=row["variant_id"], product=product)

        quantity = max(1, int(row["quantity"]))
        unit_price = product.final_price
        subtotal = unit_price * quantity
        total += subtotal

        items.append(
            {
                "key": key,
                "product": product,
                "variant": variant,
                "quantity": quantity,
                "unit_price": unit_price,
                "subtotal": subtotal,
            }
        )

    return items, total


def cart_items_count(session):
    cart = _get_cart_data(session)
    return sum(max(0, int(row.get("quantity", 0))) for row in cart["items"].values())
