from django.db import models
#import django.db.models.options as options
#options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

class Users(models.Model):
    time = models.DateTimeField(
        verbose_name='Дата и время регистрации (UTC)',
        auto_now_add=True,
        null=True
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Telegram ID',
        unique=True,
        null=True
    )
    username = models.CharField(
        verbose_name='Ник',
        max_length=30,
        null=True
    )
    firstname = models.CharField(
        verbose_name='Имя',
        max_length=30,
        null=True
    )
    lastname = models.CharField(
        verbose_name='Фамилия',
        max_length=30,
        null=True
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=30,
        null=True
    )

    def __str__(self):
        return f'{self.external_id}'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

class Items(models.Model):
    name = models.CharField(
        verbose_name='Название товара',
        max_length=100,
        null=True
    )
    price = models.PositiveBigIntegerField(
        verbose_name='Цена товара (в копейках, не меньше 10000)',
        null=True
    )
    description = models.CharField(
        verbose_name='Описание товара',
        max_length=100,
        null=True
    )
    volume = models.PositiveBigIntegerField(
        verbose_name='Кол-во сообщений',
        null=True
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class PaymentHistory(models.Model):
    time = models.DateTimeField(
        verbose_name='Дата и время транзакци (UTC)',
        auto_now_add=True,
        null=True
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Telegram ID',
        unique=False,
        null=True
    )
    summ = models.PositiveBigIntegerField(
        verbose_name='Сумма',
        null=True
    )
    comment = models.CharField(
        verbose_name='Комментарий',
        max_length=100,
        null=True
    )

    def __str__(self):
        return f'{self.external_id}', f'{self.summ}'

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

class Profiles(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Telegram ID',
        unique=True,
        null=True
    )
    ref_count = models.PositiveIntegerField(
        verbose_name='Рефералы',
        default=0
    )
    sub_ref_count = models.PositiveBigIntegerField(
        verbose_name='Суб-рефералы',
        default=0
    )
    items_count = models.PositiveBigIntegerField(
        verbose_name='Сообщения',
        default=0
    )
    wallet = models.PositiveBigIntegerField(
        verbose_name='Кошелёк',
        default=0
    )

    def __int__(self):
        return self.ref_count, self.sub_ref_count, self.items_count, self.wallet

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class ReferalBase(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Telegram ID',
        unique=True,
        null=True
    )
    from_who = models.PositiveIntegerField(
        verbose_name='Кто пригласил',
        null=True
    )
    referals = models.ManyToManyField(Users)

    def get_refs(self):
        return [Users.external_id for Users in self.referals.all()]


    class Meta:
        verbose_name = 'Рферал'
        verbose_name_plural = 'Рефералы'

class Audiences(models.Model):
    username = models.CharField(
        verbose_name='Ник клиента',
        max_length=100,
        null=True
    )
    external_id = models.PositiveIntegerField(
        verbose_name='Telegram ID владельца базы',
        unique=True,
        null=True
    )
    name = models.CharField(
        verbose_name='Название базы',
        max_length=100,
        null=True
    )
    category = models.CharField(
        verbose_name='Категория базы',
        max_length=100,
        null=True
    )
    time = models.DateTimeField(
        verbose_name='Дата и время последнего сообщения (UTC)',
        auto_now_add=False,
        null=True
    )

    def base_list(self):
        return self.list

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'