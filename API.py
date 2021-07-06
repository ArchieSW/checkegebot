import requests
from operator import itemgetter

cookies = {
    'Participant': 'FEA3039FF9CE6EC9A2CAD4008586180CDC5CAC1A50D697BB9553C4283563D6D03113F2200AEC1926AC88EEB4310347947AEBC1A44299120445CC13FBA9AF2102CCC1B9FCABA5FBCC2D85272D36513942333F1011695916A5570310B6C1A6B3B0BAA3EE42',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://checkege.rustest.ru/exams',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

def getResults(participant):
    cookies['Participant'] = participant
    response = requests.get('http://checkege.rustest.ru/api/exam', headers=headers, cookies=cookies, verify=True)
    try:
        data = response.json()
#        print(data)
    except:
        pass
    results = {exam["Subject"]:exam['TestMark'] for exam in data["Result"]['Exams'] }
    if results['Сочинение'] == 1:
        results['Сочинение'] = 'Зачет'
    else:
        results['Сочинение'] = 'Незачет'

    return results

def getTwoAns(outi):
    try:
        return outi[outi.index('[', 1) + 1: outi.index(']')].replace('"', '')
    except:
        pass
def get25Ans(stri):
    stri = stri.replace('}', "{").split('{')
    anses = []
    for x in stri:
        if getTwoAns(x) != None and getTwoAns(x) != ',':
            anses.append(getTwoAns(x))
    return anses
def getInfaResults(participant, day):
    cookies['Participant'] = participant
    try:

        response = requests.get('http://checkege.rustest.ru/api/exam/' + day, headers=headers, cookies=cookies, verify=True)
        answers = response.json()
        answers = answers["Answers"]['Answers']
        answers.sort(key=itemgetter("Number"))
        out = {}
        for x in answers:
            out[x['Number']] = [x['Answer'], x['Mark']]
        out[17][0] = getTwoAns(out[17][0])
        out[18][0] = getTwoAns(out[18][0])
        out[20][0] = getTwoAns(out[20][0])
        out[27][0] = getTwoAns(out[27][0])
        out[26][0] = getTwoAns(out[26][0])
        out[25][0] = get25Ans(out[25][0])
        parsed = "Номер Ваш ответ Балл\n"
        for x in out:
            if x != 25:
                parsed += str(x) + ' ' + out[x][0] + ' ' + str(out[x][1]) + '\n'
            else:
                parsed += str(x) + ' ' + str(out[x][0]) + ' ' + str(out[x][1]) + '\n'
        return parsed
    except:
        return 'Данные не были получены'