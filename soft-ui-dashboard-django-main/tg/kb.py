from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import emoji
from .TextConfig import Links as link

class inlinekb():
    async def check_subkb_allf(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        b2 = KeyboardButton(text='⚡Поделиться контактом', request_contact=True)
        res = kb.add(b2)
        return res
    async def check_subkb_ct(self):
        kb = InlineKeyboardMarkup()

        b1 = InlineKeyboardButton(text='💬Подписаться', url=link.channel_url)
        b2 = InlineKeyboardButton(text='🔥Проверить подписку', callback_data='check_sub')
        res = kb.add(b1).add(b2)
        return res

    async def homekb(self):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text=emoji.emojize(":bust_in_silhouette:")+"Профиль", callback_data='get_profile')
        b2 = InlineKeyboardButton(text=emoji.emojize(":check_mark_button:")+'Сделать рассылку', callback_data='make_send')
        b3 = InlineKeyboardButton(text=emoji.emojize(":shopping_cart:")+'Магазин', callback_data='shop')
        b4 = InlineKeyboardButton(text=emoji.emojize(":smiling_face_with_sunglasses:")+'О сервисе', callback_data='about')
        b5 = InlineKeyboardButton(text=emoji.emojize(":red_heart:")+'Тех поддержка', callback_data='support')
        b6 = InlineKeyboardButton(text=emoji.emojize(":bomb:")+'Партнерка', callback_data='partners')
        b7 = InlineKeyboardButton(text=emoji.emojize(":bell:")+'Отзывы', url=link.feedbacklink)
        res = kb.add(b2).row(b1, b3).row(b6, b7, b4).add(b5)
        return res

    async def make_send_kb(self):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text=emoji.emojize(":high_voltage:")+"Новая ЦА",
                                  callback_data='new_aud')
        b2 = InlineKeyboardButton(text=emoji.emojize(":bust_in_silhouette:") + "Существующая ЦА",
                                  callback_data='my_aud')
        b3 = InlineKeyboardButton(text=emoji.emojize(":fire:") + "Наша ЦА" + emoji.emojize(":fire:"),
                                  callback_data='our_aud')
        b4 = InlineKeyboardButton(text=emoji.emojize(":shopping_cart:")+'Магазин', callback_data='shop')
        b5 = InlineKeyboardButton(text=emoji.emojize(":BACK_arrow:") + "Назад",
                                  callback_data='home')
        res = kb.row(b1, b2).add(b3).row(b4, b5)
        return res
    # Новая Ца

    # Существующая ца

    # Не\существующая Ца

    # Наша Ца

    # Категории

    # Подтверждение сообщения

    async def profilekb(self):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text=emoji.emojize(":shopping_cart:") + 'Магазин', callback_data='shop')
        b2 = InlineKeyboardButton(text=emoji.emojize(":bomb:") + 'Партнерка', callback_data='partners')
        b3 = InlineKeyboardButton(text=emoji.emojize(":BACK_arrow:") + "Назад",
                                  callback_data='home')
        res = kb.row(b1, b2).add(b3)
        return res

    async def aboutkb(self):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text=emoji.emojize(":BACK_arrow:") + "Назад",
                                  callback_data='home')
        res = kb.add(b1)
        return res

    async def supportkb(self):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text=emoji.emojize(":bust_in_silhouette:") + "Перейти в чат",
                                  url=link.supportlink)
        b2 = InlineKeyboardButton(text=emoji.emojize(":BACK_arrow:") + "Назад",
                                  callback_data='home')
        res = kb.add(b1, b2)
        return res

    async def parnerkb(self):
        kb = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton(text=emoji.emojize(":money_bag:") + "Порядок вывода средств",
                                  callback_data='keep_money')
        b2 = InlineKeyboardButton(text=emoji.emojize(":shopping_cart:") + 'Реферальный магазин', callback_data='ref_shop')
        b3 = InlineKeyboardButton(text=emoji.emojize(":BACK_arrow:") + "Назад",
                                  callback_data='home')
        res = kb.row(b1, b3)
        return res

    async def shopkb(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton(text=emoji.emojize(":confounded_face:") + "Домой" + emoji.emojize(":crying_cat:"))
        res = kb.add(b1)
        return res
