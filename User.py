import API
from API import getResults
import datetime
class user:
    cookie = ''
    tgID = 0
    dayInf = ''
    def __init__(self, cookie, tgID):
        self.cookie = cookie
        self.tgID = tgID


    def setDayInf(self, day):
        if day == '24':
            self.dayInf = 19
        elif day == '25':
            self.dayInf = 372


    def getMyResults(self):
        message = '*Текущие результаты:* \n'
        results = getResults(self.cookie)
        currentTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        message += 'Обновлено в ' + currentTime + '\n'
        message += '\n'
        for x in results:
            if x != "Сочинение":
                message += x + ' — ' + '*' + str(results[x]) + ' баллов *' + '\n'
            else:
                message += x + ' — ' + '*' + str(results[x]) + '*' + '\n'
        message += 'Чтобы получить свои баллы за информатику введите "/infa {день в котором был написал 24/25}". Пример "/infa 24"'
        return message


    def getInfa(self):
        return API.getInfaResults(self.cookie, str(self.dayInf))