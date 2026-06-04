from decimal import Decimal

from django.core.management.base import BaseCommand

from shop.models import Category, Product, ProductImage, ProductVariant


class Command(BaseCommand):
    help = "Seed database with demo game store data"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing catalog data")

    def handle(self, *args, **options):
        if options["reset"]:
            ProductVariant.objects.all().delete()
            ProductImage.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing catalog data removed."))

        categories = {
            "action": Category.objects.get_or_create(
                slug="action", defaults={"name": "Action", "description": "Экшн-игры", "sort_order": 1}
            )[0],
            "rpg": Category.objects.get_or_create(
                slug="rpg", defaults={"name": "RPG", "description": "Ролевые игры", "sort_order": 2}
            )[0],
            "strategy": Category.objects.get_or_create(
                slug="strategy", defaults={"name": "Strategy", "description": "Стратегии", "sort_order": 3}
            )[0],
            "sports": Category.objects.get_or_create(
                slug="sports", defaults={"name": "Sports", "description": "Спортивные игры", "sort_order": 4}
            )[0],
            "horror": Category.objects.get_or_create(
                slug="horror", defaults={"name": "Horror", "description": "Хорроры и выживание", "sort_order": 5}
            )[0],
            "ps5": Category.objects.get_or_create(
                slug="ps5-games", defaults={"name": "PS5", "description": "Эксклюзивы PlayStation 5", "sort_order": 6}
            )[0],
            "nintendo": Category.objects.get_or_create(
                slug="nintendo", defaults={"name": "Nintendo", "description": "Игры для Nintendo Switch", "sort_order": 7}
            )[0],
            "pc": Category.objects.get_or_create(
                slug="pc-games", defaults={"name": "PC Games", "description": "Игры для PC", "sort_order": 8}
            )[0],
        }

        products_data = [
            {
                "name": "GTA VI",
                "slug": "gta-vi",
                "category": categories["action"],
                "description": "Долгожданное продолжение легендарной серии. Открытый мир нового поколения, захватывающий сюжет и бесконечные возможности.",
                "developer": "Rockstar Games",
                "age_rating": Product.AgeRating.PEGI18,
                "price": Decimal("29990"),
                "discount_percent": 0,
                "is_featured": True,
                "images": [
                    "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=1200&auto=format&fit=crop",
                ],
                "variants": [
                    ("ps5", "standard", 15),
                    ("ps5", "deluxe", 8),
                    ("xsx", "standard", 12),
                    ("xsx", "deluxe", 6),
                ],
            },
            {
                "name": "Elden Ring: Nightreign",
                "slug": "elden-ring-nightreign",
                "category": categories["rpg"],
                "description": "Новая глава легендарной вселенной от FromSoftware. Мрачный открытый мир, жестокие боссы и глубокая ролевая система.",
                "developer": "FromSoftware / Bandai Namco",
                "age_rating": Product.AgeRating.PEGI16,
                "price": Decimal("24990"),
                "discount_percent": 10,
                "is_featured": True,
                "images": [
                    "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200&auto=format&fit=crop",
                ],
                "variants": [
                    ("ps5", "standard", 20),
                    ("ps5", "deluxe", 10),
                    ("xsx", "standard", 15),
                    ("pc", "standard", 25),
                ],
            },
            {
                "name": "Cyberpunk 2077: Phantom Liberty",
                "slug": "cyberpunk-2077-phantom-liberty",
                "category": categories["rpg"],
                "description": "Night City ждёт. Расширенное издание с дополнением Phantom Liberty и полным обновлением 2.0. Лучший опыт игры в Cyberpunk 2077.",
                "developer": "CD Projekt RED",
                "age_rating": Product.AgeRating.PEGI18,
                "price": Decimal("14990"),
                "discount_percent": 20,
                "is_featured": True,
                "images": [
                    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1200&auto=format&fit=crop",
                ],
                "variants": [
                    ("ps5", "standard", 18),
                    ("xsx", "standard", 14),
                    ("pc", "standard", 30),
                    ("pc", "ultimate", 12),
                ],
            },
            {
                "name": "FIFA 26",
                "slug": "fifa-26",
                "category": categories["sports"],
                "description": "Новый сезон — новые возможности. Улучшенная физика мяча, реалистичная анимация игроков и обновлённый режим карьеры.",
                "developer": "EA Sports",
                "age_rating": Product.AgeRating.PEGI3,
                "price": Decimal("19990"),
                "discount_percent": 0,
                "is_featured": False,
                "images": [
                    "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=1200&auto=format&fit=crop",
                ],
                "variants": [
                    ("ps5", "standard", 25),
                    ("ps5", "ultimate", 10),
                    ("xsx", "standard", 20),
                    ("xsx", "ultimate", 8),
                    ("pc", "standard", 35),
                ],
            },
            {
                "name": "Resident Evil 9",
                "slug": "resident-evil-9",
                "category": categories["horror"],
                "description": "Самая страшная часть серии. Новый главный герой, атмосфера абсолютного ужаса и переработанная механика выживания.",
                "developer": "Capcom",
                "age_rating": Product.AgeRating.PEGI18,
                "price": Decimal("22990"),
                "discount_percent": 5,
                "is_featured": True,
                "images": [
                    "https://images.unsplash.com/photo-1504701954957-2010ec3bcec1?w=1200&auto=format&fit=crop",
                ],
                "variants": [
                    ("ps5", "standard", 12),
                    ("ps5", "deluxe", 6),
                    ("xsx", "standard", 10),
                ],
            },
            {
                "name": "Civilization VII",
                "slug": "civilization-vii",
                "category": categories["strategy"],
                "description": "Постройте величайшую цивилизацию в истории. Новая эра пошаговых стратегий с переработанной дипломатией и военной системой.",
                "developer": "Firaxis Games / 2K",
                "age_rating": Product.AgeRating.PEGI12,
                "price": Decimal("17990"),
                "discount_percent": 15,
                "is_featured": False,
                "images": [
                    "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=1200&auto=format&fit=crop",
                ],
                "variants": [
                    ("pc", "standard", 40),
                    ("pc", "deluxe", 18),
                    ("pc", "ultimate", 10),
                ],
            },
            {
                "name": "The Legend of Zelda: Echoes of Wisdom",
                "slug": "zelda-echoes-of-wisdom",
                "category": categories["nintendo"],
                "description": "Принцесса Зельда стала главным героем. Уникальная механика копирования предметов и существ открывает бесконечные тактические возможности.",
                "developer": "Nintendo",
                "age_rating": Product.AgeRating.PEGI7,
                "price": Decimal("18990"),
                "discount_percent": 0,
                "is_featured": True,
                "images": [
                    "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?w=1200&auto=format&fit=crop",
                ],
                "variants": [
                    ("switch", "standard", 22),
                ],
            },
            {
                "name": "Marvel's Spider-Man 3",
                "slug": "spider-man-3",
                "category": categories["ps5"],
                "description": "Питер Паркер и Майлз Моралес вновь вместе. Расширенный Нью-Йорк, новые злодеи и невероятный свинг на паутине.",
                "developer": "Insomniac Games / Sony",
                "age_rating": Product.AgeRating.PEGI16,
                "price": Decimal("26990"),
                "discount_percent": 0,
                "is_featured": True,
                "images": [
                    "https://images.unsplash.com/photo-1608889476518-738c9b1dcb40?w=1200&auto=format&fit=crop",
                ],
                "variants": [
                    ("ps5", "standard", 18),
                    ("ps5", "deluxe", 9),
                    ("ps5", "ultimate", 4),
                ],
            },
        ]

        created_products = 0
        for data in products_data:
            product, created = Product.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "category": data["category"],
                    "description": data["description"],
                    "developer": data["developer"],
                    "age_rating": data["age_rating"],
                    "price": data["price"],
                    "discount_percent": data["discount_percent"],
                    "is_featured": data["is_featured"],
                    "is_active": True,
                },
            )
            if not created:
                product.name = data["name"]
                product.category = data["category"]
                product.description = data["description"]
                product.developer = data["developer"]
                product.age_rating = data["age_rating"]
                product.price = data["price"]
                product.discount_percent = data["discount_percent"]
                product.is_featured = data["is_featured"]
                product.is_active = True
                product.save()

            product.images.all().delete()
            for index, image_url in enumerate(data["images"]):
                ProductImage.objects.create(
                    product=product,
                    image_url=image_url,
                    is_primary=index == 0,
                    alt_text=product.name,
                )

            product.variants.all().delete()
            for platform, edition, stock in data["variants"]:
                ProductVariant.objects.create(
                    product=product,
                    sku=f"{product.slug}-{platform}-{edition}".upper().replace(" ", "-"),
                    platform=platform,
                    edition=edition,
                    stock=stock,
                )

            if created:
                created_products += 1

        self.stdout.write(self.style.SUCCESS(f"Seed completed. Created products: {created_products}"))
