import requests

s_city = "Moscow, RU"
appid = "5bfad62df07cc2b9575aef567923605e"
res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                   params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print('Прогноз погоды на неделю:')
for i in data['list']:
    print('Дата и время:', i['dt_txt'],'\nСкорость ветра:', i['wind']['speed'], 'м/с\nВидимость:', i['visibility'], 'м')
    print('-----------------------------')
