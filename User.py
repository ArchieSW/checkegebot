from API import getResults
import datetime
class user:
    cookie = ''
    tgID = 0
    def __init__(self, cookie, tgID):
        self.cookie = cookie
        self.tgID = tgID

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
        return message
