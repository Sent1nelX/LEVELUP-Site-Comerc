import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Установить новый пароль для пользователя whoispluha
user = User.objects.get(username='whoispluha')
user.set_password('Goldi1234')
user.save()

print(f'✅ Пароль для {user.username} успешно изменён на: Goldi1234')
print('Теперь сможешь войти в админку http://127.0.0.1:8090/admin/')
