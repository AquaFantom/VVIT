import requests

s_city = "Moscow, RU"
appid = "5bfad62df07cc2b9575aef567923605e"
res = requests.get('http://api.openweathermap.org/data/2.5/weather',
                   params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print('Погода сейчас:')
print('Скорость ветра:', data['wind']['speed'], 'м/с\nВидимость:',
      data['visibility'], 'м')

