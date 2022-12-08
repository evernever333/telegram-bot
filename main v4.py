import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
 
bot = telebot.TeleBot('1461155136:AAEvea1W9Gk7f7fp1JX0y94QDgLqqATfPxs')

def holidays(holiday_date_text, holiday_name_text):  # прописываем парсинг в начале, чтобы не заходить на сайт при каждом новом запросе от пользователя
    url = 'https://www.timeanddate.com/holidays/un/2021'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    table = soup.find_all('table')[0]
    holiday_name = table.find_all('a')

    for i in range(0, len(holiday_name)):
        holiday_name_text.append(holiday_name[i].get_text())

    holiday_date = table.find_all('th')
    for i in range(3, len(holiday_date)):
        holiday_date_text.append(holiday_date[i].get_text())
    return holiday_name_text, holiday_date_text


holiday_name_text = []
holiday_date_text = []
holidays(holiday_date_text, holiday_name_text)

bot = telebot.TeleBot('1461155136:AAEvea1W9Gk7f7fp1JX0y94QDgLqqATfPxs')


@bot.message_handler(commands=["start"])  # прописываем ответ на команду /start
def start_reply(message):
    bot.send_message(message.chat.id,
                     'Привет! Этот бот может проверить есть ли какой-нибудь интернациональный '
                     'прадзник в определенную дату. Чтобы начать проверку нажми "/check". Если хочешь узнать откуда этот бот черпает информацию, нажми  "/info"')

@bot.message_handler(commands=["info"]) # прописываем ответ на команду /info
def info_reply(message):
    bot.send_message(message.chat.id,
                     'Наш главный ресурс - это сайт timeanddate.com .'
                     ' Пока что мы не используем другие ресурсы, но можем начать это делать в ближайшем будушем, так что следите за обновлениями бота!')

date_number = ''
# задаем пустые значения, которые позже будем зполнять ответами на наши сообщения
date_month = ''

result = ''
userfriendly_date_month = ''




@bot.message_handler(content_types=['text'])
def handling_date(message):

    if message.text == '/check': # прописываем ответ на команду /check
        bot.send_message(message.from_user.id,
                         'Укажи число, которое хочешь проверить.')

        bot.register_next_step_handler(message, get_date_number)
    else:
        pass


def get_date_number(message): #функция для сохранения ответа числа, которое вводит пользователь
    global date_number
    date_number = message.text # сохраняем ввод
    try:
        message.text = int(message.text)

        if (int(message.text) > 0) and (int(message.text < 32)):
            pass

        else:
            bot.send_message(message.from_user.id,
                             'Кажется числа, что ты ввел не соответствуют формату! Число должно быть от 1 до 31. Попробуй еще раз, нажав /check ')
            return None

    except ValueError:
        bot.send_message(message.from_user.id,
                         'Кажется то, что ты ввел не соответствует формату! Ты должен ввести число месяца. Попробуй еще раз, нажав /check ')
        return None

    bot.send_message(message.from_user.id,
                     'Отлично! Теперь напиши три первых буквы месяца проверяемой даты. ')
    bot.register_next_step_handler(message, get_date_month)
    message.text == message.text.lower()




def get_date_month(message): #функция для сохранения ответа месяца, которое вводит пользователь
    global date_month
    date_month = message.text

    if (date_month == 'янв') or (date_month == 'фев') or (date_month == 'мар') or (date_month == 'апр') or (date_month == 'май')\
            or (date_month == 'июн') or (date_month == 'июл') or (date_month == 'авг') or (date_month == 'сен') or (date_month == 'окт')\
            or (date_month == 'ноя') or (date_month == 'дек'):
        pass

    else:
        bot.send_message(message.from_user.id,
                         'Формат месяца, что ты ввел, не подходит. Не забывай, нужно ввести три первых буквы месяца. Попробуй начать заново - для этого нажми /check ')
        return None

    # теперь делаем финальную проверку перед поиском информации.
    # Переспрашиваем все ли правильно пользователь ввел.
    keyboard = types.InlineKeyboardMarkup()  # добавляем в код нашу клавиатуру
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # создаем кнопку «Да»
    keyboard.add(key_yes)  # добавляем кнопку в наш чат
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    full_date = date_number + ' ' + date_month

    if date_month == 'янв':
        userfriendly_date_month = 'Января'
    elif date_month == 'фев':
        userfriendly_date_month = 'Февраля'
    elif date_month == 'мар':
        userfriendly_date_month = 'Марта'
    elif date_month == 'апр':
        userfriendly_date_month = 'Апреля'
    elif date_month == 'май':
        userfriendly_date_month = 'Мая'
    elif date_month == 'июн':
        userfriendly_date_month = 'Июня'
    elif date_month == 'июл':
        userfriendly_date_month = 'Июля'
    elif date_month == 'авг':
        userfriendly_date_month = 'Августа'
    elif date_month == 'сен':
        userfriendly_date_month = 'Сентября'
    elif date_month == 'окт':
        userfriendly_date_month = 'Октбяря'
    elif date_month == 'ноя':
        userfriendly_date_month = 'Ноября'
    elif date_month == 'дек':
        userfriendly_date_month = 'Декабря'

    userfriendly_full_date = str(date_number) + ' ' + str(userfriendly_date_month)
    question = f'Финальная проверка. Ты хочешь узнать какие праздники есть по данной дате: ' \
               f'{userfriendly_full_date} , все правильно?'  #задаем вопрос, чтобы пользователь подтвердил свой запрос

    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)  # напишем код, чтобы при нажатии на кнопку хоть что-то происходило
    def callback_worker(call):
        if call.data == "yes":
            bot.send_message(call.message.chat.id,
                             'Проверяю данную дату. Одну секунду. ')
            res = ''
            for j in range(0, len(holiday_date_text)):
                if holiday_date_text[j] == full_date:
                    res = holiday_name_text[j]


            result = res
            result = str(result)

            if res == '':
                bot.send_message(call.message.chat.id,
                                 'Извини, я не нашел никакого праздника по указанной дате. Попробуй другую дату. Чтобы это сделать нажми /check')
            else:
                bot.send_message(call.message.chat.id, f'{result}')

        elif call.data == "no":
            bot.send_message(call.message.chat.id,
                             'О нет! Тебе придется вернуться в начало, чтобы назначить дату заново. Чтобы это сделать, нажми "/check"')







if __name__ == '__main__':
    bot.infinity_polling()
