from User import user
import telebot
import serializer


#
# 1. сериялизатор
# 2. Админ панельч
#


TOKEN = '1737697318:AAGk5-yqnQXmew0eGdYX2dp_JPXRtezJQKA'
bot = telebot.TeleBot(TOKEN)
users = {}

messageToIgnore = ['cb_Обновить', 'start', 'help', 'cookie']
buttonWords = ["cb_Обновить", "cb_Двойное обновление", "cb_Тройное обновление", "cb_Квадробновление", "cb_Безумие", "cb_Заебал обновлять", "cb_Мозги обнови себе"]


# Handle all other messages.





@bot.message_handler(func=lambda message: isMessageToIgnore(message),
                     content_types=['audio', 'photo', 'voice', 'video', 'document',
                                    'text', 'location', 'contact', 'sticker'])
def default_command(message):
    pass


def isMessageToIgnore(message):
    flag = False
    if message.text[0] != '/':
        flag = True
    print(message.text)
    return flag


def userExists(userID):
    return userID in users


def findExistsUser(userID):
    return users[userID]


def printUsers():
    for x in users:
        print(x)


@bot.callback_query_handler(func=lambda message: message.data in buttonWords)
def callback_query(message):
    nextWord = buttonWords[(buttonWords.index(message.data) + 1) % len(buttonWords)][3:]
    updateResults(message, nextWord)



@bot.message_handler(commands='infa')
def sendInfaReses(message):
    try:
        dayInf = message.text.split()[1]
        users[message.from_user.id].setDayInf(dayInf)
        bot.send_message(message.from_user.id,users[message.from_user.id].getInfa())
    except:
        pass



# TODO
def updateResults(message, word):
    bot.edit_message_text(users[message.from_user.id].getMyResults(), message.from_user.id, message.message.message_id, parse_mode="Markdown", reply_markup=getMarkup(word))


@bot.message_handler(commands=['start', 'help'])
def greetings(message):
    bot.send_message(message.from_user.id,
                     """Чтобы получить результаты, введите "/cookie" и значение cookie с сайта check ege. Пример: /cookie 123456789""",
                     parse_mode="Markdown")


def sendResultsToUser(tgID, buttonWord):
    bot.send_message(tgID, users[tgID].getMyResults(), parse_mode='Markdown', reply_markup=getMarkup(buttonWord))


def getMarkup(word):
    callword = 'cb_' + word
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(telebot.types.InlineKeyboardButton(word, callback_data=callword))
    return markup


@bot.message_handler(commands='cookie')
def addNewUser(message):
    try:
        cookie = message.text.split()[1]
        if len(cookie) != 200:
            bot.reply_to(message, 'Это не куки блять!!!')
        users[message.from_user.id] = user(cookie, message.from_user.id)
        serializer.save_obj(users, "users")
        sendResultsToUser(message.from_user.id, "Обновить")
    except:
        bot.reply_to(message, 'Cookie не был получен, соблюдай пример из /start')


if __name__ == "__main__":
    try:
        users = serializer.load_obj("users")
    except:
        pass
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)



