import logging
import threading
import concurrent.futures
import asyncio
from django.core.management.base import BaseCommand
from aiogram import types, Bot, Dispatcher, executor
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters.builtin import CommandStart, IsSenderContact
from aiogram.utils.deep_linking import get_start_link
from django.conf import settings
from ...models import Users, Items, PaymentHistory, Profiles, ReferalBase, Audiences
from ...kb import inlinekb
from ...TextConfig import Texts as textconf
from ...TextConfig import Links as link



init = Bot(token=settings.TOKEN_BOT, parse_mode=types.ParseMode.MARKDOWN)
bot = Dispatcher(init)

logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    help = 'bot'

    def handle(self, *args, **options):
        return ''

async def run_thread(func, *args):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        res = await loop.run_in_executor(
            pool, func, *args
        )
    return res

def check_user(id, username, first_name, last_name):
    account, _ = Users.objects.get_or_create(
        external_id=id,
        defaults={
            'username': username,
            'firstname': first_name,
            'lastname': last_name,
        }
    )
    refbase, _ = ReferalBase.objects.get_or_create(
        external_id=id
    )
    profile, _ = Profiles.objects.get_or_create(
        external_id=id
    )

def pay_refer(chat, cost):
    r = ReferalBase.objects.get(external_id=chat).from_who
    if bool(r):
        profile_referer = Profiles.objects.get(external_id=r)
        profile_referer.wallet = int(profile_referer.wallet) + ((int(cost)//100)*10)//100
        profile_referer.save()
        s_r = ReferalBase.objects.get(external_id=r).from_who
        if bool(s_r):
            profile_sub_referer = Profiles.objects.get(external_id=s_r)
            profile_sub_referer.wallet = int(profile_sub_referer.wallet) + ((int(cost)//100)*4)//100
            profile_sub_referer.save()

def check_refer(deep, chat):
    r = bool(ReferalBase.objects.filter(external_id=deep))
    if r:
        l = ReferalBase.objects.get(external_id=chat)
        l.from_who = deep
        l.save()
        listt = ReferalBase.objects.get(external_id=deep)
        ref = Users.objects.get(external_id=chat)
        listt.referals.add(ref)
        listt.save()
        c = Profiles.objects.get(external_id=deep)
        c.ref_count = c.ref_count + 1
        c.save()
        cs = ReferalBase.objects.get(external_id=deep).from_who
        if bool(cs):
            csf = Profiles.objects.get(external_id=cs)
            csf.sub_ref_count = csf.sub_ref_count + 1
            csf.save()
    else:
        init.send_message(chat_id=chat, text=textconf.errormes)

def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False

def check_phone(chat):
    if Users.objects.get(external_id=chat).phone_number:
        return True
    else:
        return False

def up_phone(chat, number):
    ph = Users.objects.get(external_id=chat)
    ph.phone_number = number
    ph.save()

def user_profile(chat):
    data_ref = Profiles.objects.get(external_id=chat).ref_count
    data_sub_ref = Profiles.objects.get(external_id=chat).sub_ref_count
    data_item = Profiles.objects.get(external_id=chat).items_count
    data_wallet = Profiles.objects.get(external_id=chat).wallet
    res = data_item, data_ref, data_sub_ref, data_wallet
    print(res)
    return res

def items_name(id):
    names_list = Items.objects.values_list('name', flat=True)
    return names_list[id]

def items_count():
    count = Items.objects.all().count()
    return count

async def items_count_data_gen(count):
    i = 0
    while i <= (count-1):
        name = await run_thread(items_name, i)
        i += 1
        yield name

def items_data(name):
    print(name)
    price = Items.objects.get(name=name).price
    description = Items.objects.get(name=name).description
    volume = Items.objects.get(name=name).volume
    pack = types.LabeledPrice(label=name, amount=price)
    res = description, pack, volume
    return res

def up_volume(chat, volume):
    vol = Profiles.objects.get(external_id=chat)
    vol.items_count = int(vol.items_count) + int(volume)
    vol.save()

def create_transaction(chat, cost):
    trans = PaymentHistory(external_id=chat, summ=cost)
    trans.save()


@bot.message_handler(CommandStart())
async def welcome(message: types.Message):
    try:
        kb = await inlinekb.homekb(message)
        kb_decline_q = await inlinekb.check_subkb_allf(message)
        kb_decline_w = await inlinekb.check_subkb_ct(message)
        await run_thread(check_user, message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
        deep = message.get_args()
        print(deep, message.chat.id)
        if bool(deep):
            if int(deep) == int(message.chat.id):
                await message.answer(textconf.refererr)
            else:
                await run_thread(check_refer, deep, message.chat.id)
        chat = message.chat.id
        phone_acc = await run_thread(check_phone, chat)
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=message.chat.id)
        if check_sub_channel(stat):
            if phone_acc:
                await message.answer(textconf.welcomemes.format(
                    firstname=message.chat.first_name
                ))
                await message.answer(textconf.startmessage, reply_markup=kb)
        if check_sub_channel(stat) == False:
            if phone_acc:
                await message.answer(textconf.channel_invite_ct, reply_markup=kb_decline_w)
        if check_sub_channel(stat):
            if phone_acc == False:
                await message.answer(textconf.channel_invite_st, reply_markup=kb_decline_q)
        if check_sub_channel(stat) == False:
            if phone_acc == False:
                await message.answer(textconf.channel_invite_af, reply_markup=kb_decline_q)
    except Exception as e:
        print(e)
        await message.answer(textconf.errormes)

@bot.message_handler(IsSenderContact(True), content_types='contact')
async def add_phone(message: types.Message):
    print(message)
    await run_thread(up_phone, message.chat.id, message.contact.phone_number)
    d = types.ReplyKeyboardRemove()
    kh = await inlinekb.homekb(message)
    kb = await inlinekb.check_subkb_ct(message)
    stat = await init.get_chat_member(chat_id=link.channel_id, user_id=message.chat.id)
    await init.send_message(chat_id=message.chat.id, text=textconf.phone_accept, reply_markup=d)
    if check_sub_channel(stat):
        await message.answer(textconf.welcomemes.format(
            firstname=message.chat.first_name
        ))
        await message.answer(textconf.startmessage, reply_markup=kh)
    if check_sub_channel(stat) == False:
        await init.send_message(chat_id=message.chat.id, text=textconf.channel_invite_ct, reply_markup=kb)

@bot.message_handler(IsSenderContact(False), content_types='contact')
async def invalid_contact(message: types.Message):
    await message.answer('Это не твой контантакт, давай еще раз попробуем')

@bot.message_handler(content_types=['text'])
async def exit(message: types.Message):
    if 'Домой' in message.text:
        d = types.ReplyKeyboardRemove()
        kb = await inlinekb.homekb(message)
        await message.answer(textconf.comebackmes, reply_markup=d)
        await message.answer(textconf.startmessage, reply_markup=kb)

@bot.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await init.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')
    chat = message.chat.id
    price = pmnt['total_amount']
    item_volume = pmnt['invoice_payload']
    print(pmnt)
    print(chat)
    # Логирование
    await run_thread(create_transaction, chat, price)

    # Математика
    await run_thread(pay_refer, chat, price)

    # Присвоение
    await run_thread(up_volume, chat, item_volume)


    d = types.ReplyKeyboardRemove()
    kb = await inlinekb.homekb(message)
    await message.answer(textconf.successful_payment.format(
        total_amount=message.successful_payment.total_amount//100,
        currency=message.successful_payment.currency
    ), reply_markup=d)
    await message.answer(textconf.startmessage, reply_markup=kb)

@bot.callback_query_handler(lambda call: True)
async def callback_check(call: types.CallbackQuery):
    if call.data == 'check_sub':
        kb_decline_q = await inlinekb.check_subkb_allf(call.data)
        kb = await inlinekb.homekb(call.data)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        chat = call.message.chat.id
        phone_acc = await run_thread(check_phone, chat)
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        if check_sub_channel(stat):
            if phone_acc:
                await call.message.answer(textconf.welcomemes.format(
                    firstname=call.message.chat.first_name
                ))
                await call.message.edit_text(textconf.startmessage, reply_markup=kb)
        if check_sub_channel(stat) == False:
            if phone_acc:
                await call.message.edit_text(textconf.sub_decline+textconf.channel_invite_ct, reply_markup=kb_decline_w)
        if check_sub_channel(stat):
            if phone_acc == False:
                await call.message.answer(textconf.channel_invite_st, reply_markup=kb_decline_q)
        if check_sub_channel(stat) == False:
            if phone_acc == False:
                await call.message.answer(textconf.channel_invite_af, reply_markup=kb_decline_q)

    if call.data == 'home':
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        if check_sub_channel(stat):
            kb = await inlinekb.homekb(call.data)
            await call.message.edit_text(textconf.startmessage, reply_markup=kb)
        else:
            await call.message.edit_text(textconf.sub_decline + textconf.channel_invite_ct, reply_markup=kb_decline_w)

    if call.data == 'get_profile':
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        if check_sub_channel(stat):
            data = await run_thread(user_profile, call.message.chat.id)
            kb = await inlinekb.profilekb(call.data)
            await call.message.edit_text(textconf.profiletext.format(
                chat_id=call.message.chat.id,
                username=call.message.chat.username,
                mescount=data[0],
                refcount=data[1],
                subrefcount=data[2],
                balance=data[3]
            ), reply_markup=kb)
        else:
            await call.message.edit_text(textconf.sub_decline + textconf.channel_invite_ct, reply_markup=kb_decline_w)

    if call.data == 'make_send':
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        if check_sub_channel(stat):
            kb = await inlinekb.make_send_kb(call.data)
            data = await run_thread(user_profile, call.message.chat.id)
            await call.message.edit_text(textconf.sendinstuct.format(
                mescount=data[0]
            ), reply_markup=kb)
        else:
            await call.message.edit_text(textconf.sub_decline + textconf.channel_invite_ct, reply_markup=kb_decline_w)

    if call.data == 'shop':
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        if check_sub_channel(stat):
            kb = await inlinekb.shopkb(call.data)
            await call.message.answer(text='Выберите предпочитаемый пакет:', reply_markup=kb)
            count = await run_thread(items_count)
            names = await run_thread(items_count_data_gen, count)
            assert names.__aiter__() is names
            async for i in names:
                nick = i
                item_data = await run_thread(items_data, nick)
                await call.bot.send_invoice(
                    call.message.chat.id,
                    title=nick,
                    description=item_data[0],
                    provider_token=settings.PAYMENT_TOKEN_YOO,
                    currency='rub',
                    is_flexible=False,  # True если конечная цена зависит от способа доставки
                    prices=[item_data[1]],
                    start_parameter=item_data[2],
                    payload=item_data[2]
                )
        else:
            await call.message.edit_text(textconf.sub_decline + textconf.channel_invite_ct, reply_markup=kb_decline_w)

    if call.data == 'about':
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        if check_sub_channel(stat):
            kb = await inlinekb.aboutkb(call.data)
            await call.message.edit_text(textconf.abouttext, reply_markup=kb)
        else:
            await call.message.edit_text(textconf.sub_decline + textconf.channel_invite_ct, reply_markup=kb_decline_w)

    if call.data == 'support':
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        if check_sub_channel(stat):
            kb = await inlinekb.supportkb(call.data)
            await call.message.edit_text(textconf.supporttext, reply_markup=kb)
        else:
            await call.message.edit_text(textconf.sub_decline + textconf.channel_invite_ct, reply_markup=kb_decline_w)

    if call.data == 'partners':
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        if check_sub_channel(stat):
            data = await run_thread(user_profile, call.message.chat.id)
            referal_link = await get_start_link(payload=call.message.chat.id)
            kb = await inlinekb.parnerkb(call.data)
            await call.message.edit_text(textconf.partertext.format(
                refcount=data[1],
                subrefcount=data[2],
                balance=data[3],
                referal_link=referal_link
            ), reply_markup=kb)
        else:
            await call.message.edit_text(textconf.sub_decline + textconf.channel_invite_ct, reply_markup=kb_decline_w)

    if call.data == 'keep_money':
        stat = await init.get_chat_member(chat_id=link.channel_id, user_id=call.message.chat.id)
        kb_decline_w = await inlinekb.check_subkb_ct(call.data)
        if check_sub_channel(stat):
            kb = await inlinekb.aboutkb(call.data)
            await call.message.edit_text(textconf.keep_money, reply_markup=kb)
        else:
            await call.message.edit_text(textconf.sub_decline + textconf.channel_invite_ct, reply_markup=kb_decline_w)


WEBHOOK_HOST = '92.255.110.178'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './targetproject.crt'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './targetproject.key'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_PATH = '/'

WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_URL_PATH}"

# webhook = await init.get_webhook_info()
#
# # If URL is bad
# if webhook.url != WEBHOOK_URL:
#     # If URL doesnt match current - remove webhook
#     if not webhook.url:
#         await init.delete_webhook()
#
#     # Set new URL for webhook
#     await init.set_webhook(WEBHOOK_URL, certificate=open(WEBHOOK_SSL_CERT, 'rb'))
#     # If you want to use free certificate signed by LetsEncrypt you need to set only URL without sending certificate.

executor.start_polling(bot, skip_updates=True, timeout=3)