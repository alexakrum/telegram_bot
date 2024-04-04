from bot_settings import bot
import sqlite
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import random
from datetime import datetime


def register_welcome_handlers():
    # commands
    bot.register_message_handler(welcome, commands=['start'])
    bot.register_message_handler(welcome, commands=['menu'])
    bot.register_message_handler(list_variants, commands=['list'])
    # regexp
    bot.register_message_handler(send_products_keyboard, regexp='Перейти к товарам')
    bot.register_message_handler(send_personal_area, regexp='Вход в личный кабинет')
    bot.register_message_handler(welcome, regexp='Назад')
    bot.register_message_handler(send_manager, regexp='Обратная связь')
    bot.register_message_handler(send_we, regexp='О нас')

    # callback
    bot.register_callback_query_handler(send_user_id_and_names, lambda call: call.data.startswith('show_'))
    bot.register_callback_query_handler(send_products_keyboard_edit, lambda call: call.data.startswith('back_to_categories'))
    bot.register_callback_query_handler(delete_message, lambda call: call.data.startswith('back'))
    bot.register_callback_query_handler(send_products_list, lambda call: call.data.startswith('send_'))
    bot.register_callback_query_handler(send_product_info, lambda call: call.data.startswith('product_info_'))
    bot.register_callback_query_handler(send_order_process, lambda call: call.data.startswith('order_'))
    bot.register_callback_query_handler(send_Dark_academy_process, lambda call: call.data.startswith('Dark_academy'))
    bot.register_callback_query_handler(send_Сottagecore_process, lambda call: call.data.startswith('Сottagecore'))
    bot.register_callback_query_handler(send_Grunge_process, lambda call: call.data.startswith('Grunge'))
    bot.register_callback_query_handler(send_Y2K_process, lambda call: call.data.startswith('Y2K'))
    bot.register_callback_query_handler(send_Coquette_process, lambda call: call.data.startswith('Coquette'))
    bot.register_callback_query_handler(send_Shoes_process, lambda call: call.data.startswith('raz1'))
    bot.register_callback_query_handler(send_Trousers_process, lambda call: call.data.startswith('raz2'))
    bot.register_callback_query_handler(send_Skirt_process, lambda call: call.data.startswith('raz3'))
    bot.register_callback_query_handler(send_Blouse_process, lambda call: call.data.startswith('raz4'))
    bot.register_callback_query_handler(send_Top_process, lambda call: call.data.startswith('raz5'))
    bot.register_callback_query_handler(send_size_process, lambda call: call.data.startswith('22'))





def send_order_process(call):
    model = call.data[6:]
    now = datetime.now()
    order_number = 1
    sqlite.insert_order_to_base(model, call.from_user.id, now, "оплачено", "в обработке", order_number)
    sqlite.insert_order_to_orders_cache(order_number, call.from_user.id, "в обработке")

    # bot.answer_callback_query(call.from_user.id, )
    bot.answer_callback_query(call.id, "Заказ оформлен, с вами свяжутся в телеграме.", show_alert=True)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def send_product_info(call):
    name = call.data[13:]
    description, price, image = sqlite.get_description_by_name(name)
    file = open(f'images/{image}', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"Купить {price} ₽", callback_data=f"order_{name}"))
    markup.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back_to_categories"))
    bot.send_photo(call.from_user.id, file, description, reply_markup=markup)


def send_products_list(call):
    category = call.data[5:]
    products = sqlite.get_products_by_category(category)
    markup = InlineKeyboardMarkup()
    for product in products:
        markup.add(InlineKeyboardButton(text=f"{product[0]}", callback_data=f'product_info_{product[0]}'))
    markup.add(InlineKeyboardButton(text="Назад", callback_data='back_to_categories'))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def send_products_keyboard_edit(call):
    send_products_keyboard(call, edit=True)


def send_products_keyboard(message, edit=False):
    image = open(f'images/{random.randint(1, 3)}.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Dark academy", callback_data="Dark_academy"))
    markup.add(InlineKeyboardButton(text="Сottagecore", callback_data="Сottagecore"))
    markup.add(InlineKeyboardButton(text="Grunge", callback_data="Grunge"))
    markup.add(InlineKeyboardButton(text="Y2K", callback_data="Y2K"))
    markup.add(InlineKeyboardButton(text="Coquette", callback_data="Coquette"))
    text = "SubCultureSearsh\n Просто выберите стиль"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)


def send_Dark_academy_process(message, edit=False):
    name = message.data
    image = open(f'images/4.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Обувь", callback_data=f"raz1{name}_Shoes"))
    markup.add(InlineKeyboardButton(text="Брюки", callback_data=f"raz2{name}_Trousers"))
    markup.add(InlineKeyboardButton(text="Юбка", callback_data=f"raz3{name}_Skirt"))
    markup.add(InlineKeyboardButton(text="Топ", callback_data=f"raz4{name}_Blouse"))
    text = "Выберите какая одежда вам нужна"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)

def send_Сottagecore_process(message, edit=False):
    name = message.data
    image = open(f'images/5.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Обувь", callback_data=f"raz1{name}_Shoes"))
    markup.add(InlineKeyboardButton(text="Брюки", callback_data=f"raz2{name}_Trousers"))
    markup.add(InlineKeyboardButton(text="Юбка", callback_data=f"raz3{name}_Skirt"))
    markup.add(InlineKeyboardButton(text="Топ", callback_data=f"raz4{name}_Blouse"))
    text = "Выберите какая одежда вам нужна"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)


def send_Grunge_process(message, edit=False):
    image = open(f'images/6.jpg', 'rb')
    name = message.data
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Обувь", callback_data=f"raz1{name}_Shoes"))
    markup.add(InlineKeyboardButton(text="Брюки", callback_data=f"raz2{name}_Trousers"))
    markup.add(InlineKeyboardButton(text="Юбка", callback_data=f"raz3{name}_Skirt"))
    markup.add(InlineKeyboardButton(text="Топ", callback_data=f"raz5{name}_Top"))
    text = "Выберите какая одежда вам нужна"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)

def send_Y2K_process(message, edit=False):
    image = open(f'images/7.jpg', 'rb')
    name = message.data
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Обувь", callback_data=f"raz1{name}_Shoes"))
    markup.add(InlineKeyboardButton(text="Брюки", callback_data=f"raz2{name}_Trousers"))
    markup.add(InlineKeyboardButton(text="Юбка", callback_data=f"raz3{name}_Skirt"))
    markup.add(InlineKeyboardButton(text="Топ", callback_data=f"raz5{name}_Top"))
    text = "Выберите какая одежда вам нужна"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)

def send_Coquette_process(message, edit=False):
    image = open(f'images/8.jpg', 'rb')
    name = message.data
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Обувь", callback_data=f"raz1{name}_Shoes"))
    markup.add(InlineKeyboardButton(text="Брюки", callback_data=f"raz2{name}_Trousers"))
    markup.add(InlineKeyboardButton(text="Юбка", callback_data=f"raz3{name}_Skirt"))
    markup.add(InlineKeyboardButton(text="Топ", callback_data=f"raz5{name}_Top"))
    text = "Выберите какая одежда вам нужна"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)

def send_Shoes_process(message, edit=False):
    name = message.data[4:]
    image = open(f'images/{name}.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="37", callback_data=f"22_{name}"))
    markup.add(InlineKeyboardButton(text="38", callback_data=f"22_{name}"))
    text = "Выберите размер обуви"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)

def send_Trousers_process(message, edit=False):
    name = message.data[4:]
    image = open(f'images/{name}.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="44", callback_data=f"22_{name}"))
    markup.add(InlineKeyboardButton(text="46", callback_data=f"22_{name}"))
    text = "Выберите размер одежды"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)
def send_Skirt_process(message, edit=False):
    name = message.data[4:]
    image = open(f'images/{name}.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="44", callback_data=f"22_{name}"))
    markup.add(InlineKeyboardButton(text="46", callback_data=f"22_{name}"))
    text = "Выберите размер одежды"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)
def send_Blouse_process(message, edit=False):
    name = message.data[4:]
    image = open(f'images/{name}.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="44", callback_data=f"22_{name}"))
    markup.add(InlineKeyboardButton(text="46", callback_data=f"22_{name}"))
    text = "Выберите размер одежды"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)
def send_Top_process(message, edit=False):
    name = message.data[4:]
    image = open(f'images/{name}.jpg', 'rb')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="44", callback_data=f"22_{name}"))
    markup.add(InlineKeyboardButton(text="46", callback_data=f"22_{name}"))
    text = "Выберите размер одежды"
    if not edit:
        bot.send_photo(message.from_user.id, image, text, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)



def send_size_process(message, edit=False):
    name = message.data[3:]
    price = sqlite.get_description_by_name(name+".jpg")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=f"Купить {price} рублей", callback_data=f"order_{name}"))
    markup.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back_to_categories"))
    bot.send_message(message.from_user.id, "После покупки с вами свяжется менеджер" , reply_markup=markup)

def send_manager(message):
    text = '[Если что-то пошло не так пишите сюда](https://t.me/alexaAIII)'
    bot.send_message(message.from_user.id, text, parse_mode='markdown')

def send_we(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Перейти к товарам"), KeyboardButton(text="О нас"))
    markup.add(KeyboardButton(text="Личный кабинет"),KeyboardButton(text="Обратная связь"))
    bot.send_message(message.from_user.id, "SCS – это инновационная компания, специализирующаяся на персонализированном подборе одежды различных стилей для клиентов. Мы объединяем опыт профессиональных стилистов и современны технологии для создания уникальных образов, отвечающих индивидуальным предпочтениям и потребностям каждого клиента. \nМы стремимся помочь нашим клиентам выразить свою уникальность и стиль через моду, делая процесс выбора одежды легким, приятным и индивидуальным.\n \nКонтактная информация: \nАдрес: ул. Модная, 1, г. Стильград. \nТелефон: +7 (XXX) XXX-XX-XX \nЭлектронная почта: info@scs.com. \n \nБудем рады помочь вам создать неповторимый образ!", reply_markup=markup)

def send_personal_area(message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Заказы"), KeyboardButton(text="Возврат"), KeyboardButton(text="Написать специалисту"))
    markup.add(KeyboardButton(text="История покупок"), KeyboardButton(text="Назад"))
    bot.send_message(message.from_user.id, "Вы вошли в личный кабинет!", reply_markup=markup)


def delete_message(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def welcome(message):
    sqlite.insert_user(message.from_user.id, message.from_user.first_name)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text="Перейти к товарам"), KeyboardButton(text="О нас"), KeyboardButton(text="Обратная связь"))
    markup.add(KeyboardButton(text="Личный кабинет"))
    bot.send_message(message.from_user.id,"Привет! Готовы погрузиться в мир стиля и моды?\n "
                                          "Давай подберем тебе идеальный лук, который выразит твою индивидуальность и стиль!"
                     ,reply_markup=markup)


def list_variants(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="user_id", callback_data='show_users_id'),
               InlineKeyboardButton(text="names", callback_data='show_names'))

    bot.send_message(message.from_user.id, "Выбери формат списка: ", reply_markup=markup)


def send_user_id_and_names(call):
    data = call.data[5:]
    user_data = sqlite.get_user_id_and_name()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Назад", callback_data='back'))
    text = f"*Список пользователей:*\n"
    number = 1
    for user_id, name in user_data:
        if data == 'users_id':
            text += f"{number}) {str(user_id)}\n"
        elif data == 'names':
            text += f"{number}) {name}\n"
        number += 1
    bot.send_message(call.from_user.id, text, parse_mode='markdown', reply_markup=markup)

