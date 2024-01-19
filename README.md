## Это учебный проект онлайн-магазина, разработанный в фреймворке Django.


## Навыки:
- Создание web-приложения в Django;
- Работа с ORM (создание/обновление модели, миграция в БД);
- Использование базовых шаблонов и подшаблонов, шаблонных тэгов и фильтров;
- Создание контроллеров (views) на основе FBV и CBV;
- Применение Django-forms;
- Настройка работы с пользователями сервиса (регистрация, верификация, авторизация);
- Разграничение прав доступа пользователей;

## Для запуска проекта необходимо:

1. Клонируйте репозиторий
```bash
  git glone git@github.com:VladimirKovaliev/19.2_homework_django.git
```
2. Активируйте в нём виртуальное оружение, установите зависимости
```bash
  python source/bin/activate
```
```bash
  python -m pip install -r requirements.txt 
```
3. Укажите свои данные в env.example

4. Выполните миграции
```bash
  ./manage.py makemigrations –dry-run
```
```bash
(если происходит ошибка, то пропишите 
'chmod u+rwx manage.py' и попробуйте выполнить миграции снова)
```

5. Запустите проект
```bash
    python manage.py runserver
```

![Sansanimated-1](https://github.com/VladimirKovaliev/19.2_homework_django/assets/142924160/91a91cf8-3565-4526-990d-6327ed81cfad)



