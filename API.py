import requests

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

