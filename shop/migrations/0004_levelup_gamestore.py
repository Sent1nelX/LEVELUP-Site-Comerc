from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order_card_last_four_order_payment_method'),
    ]

    operations = [
        # Product: material → developer
        migrations.RenameField(
            model_name='product',
            old_name='material',
            new_name='developer',
        ),
        # Product: gender → age_rating
        migrations.RenameField(
            model_name='product',
            old_name='gender',
            new_name='age_rating',
        ),
        migrations.AlterField(
            model_name='product',
            name='age_rating',
            field=models.CharField(
                choices=[
                    ('pegi3',  'PEGI 3'),
                    ('pegi7',  'PEGI 7'),
                    ('pegi12', 'PEGI 12'),
                    ('pegi16', 'PEGI 16'),
                    ('pegi18', 'PEGI 18'),
                ],
                default='pegi12',
                max_length=10,
            ),
        ),
        # ProductVariant: size → platform
        migrations.RenameField(
            model_name='productvariant',
            old_name='size',
            new_name='platform',
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='platform',
            field=models.CharField(
                choices=[
                    ('ps5',    'PlayStation 5'),
                    ('xsx',    'Xbox Series X'),
                    ('ps4',    'PlayStation 4'),
                    ('xone',   'Xbox One'),
                    ('switch', 'Nintendo Switch'),
                    ('pc',     'PC (Steam/Epic)'),
                ],
                max_length=10,
            ),
        ),
        # ProductVariant: color → edition
        migrations.RenameField(
            model_name='productvariant',
            old_name='color',
            new_name='edition',
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='edition',
            field=models.CharField(
                choices=[
                    ('standard', 'Standard Edition'),
                    ('deluxe',   'Deluxe Edition'),
                    ('ultimate', 'Ultimate Edition'),
                    ('gold',     'Gold Edition'),
                ],
                default='standard',
                max_length=20,
            ),
        ),
        # Update unique_together
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together={('product', 'platform', 'edition')},
        ),
    ]
