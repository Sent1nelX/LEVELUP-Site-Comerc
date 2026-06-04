from .cart import cart_items_count


def cart_summary(request):
    return {
        "cart_count": cart_items_count(request.session),
    }
