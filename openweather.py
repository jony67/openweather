# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 20:12:09 2020
Получение сведений о текущей погоде и прогнозе с использованием бесплатного
ключа API сайта OpenWeather (https://openweathermap.org/)
@author: sutyamov
"""
import requests
import json
import datetime
import pandas as pd
###############################################################################
# Исходные данные
###############################################################################
key   = 'API KEY'
city  = 'Москва'
#city=input('Введите город: ')
lat   = 54.71
long  = 20.51
lang  = 'ru'
units = 'metric'  # единицы измерения: standard, metric, imperial
###############################################################################
# Сведения о текущей погоде
###############################################################################
#------------------------------------------------------------------------------
# Доступные URL API для текущей погоды (Current weather API):
#------------------------------------------------------------------------------    
# - по городу:
#'https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}'
#'https://api.openweathermap.org/data/2.5/weather?q={city name},{state code}&appid={API key}'
#'https://api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}'
#'https://api.openweathermap.org/data/2.5/weather?id={city id}&appid={API key}'
# - по географическим координатам:
#'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}'
# - по zip-коду:
#'https://api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API key}'
# - для нескольких городов в прямоугольной области координат:
#'https://api.openweathermap.org/data/2.5/box/city?bbox={bbox}&appid={API key}'
# - для нескольких городов в окружности:
#'https://api.openweathermap.org/data/2.5/box/city?bbox={bbox}&appid={API key}'
# - для нескольких городов по ID:
#'https://api.openweathermap.org/data/2.5/group?id={id,..,id}&appid={API key}'
#------------------------------------------------------------------------------
# Функция проверки статуса ответа на запрос
#------------------------------------------------------------------------------
def status_response(response):
    if response.status_code == 200:
        print('Получен ответ 200. Статус - OK.\n')
        return True
    if response.status_code == 401:
        print('Получен ответ 401. Авторизация не произведена, проверьте API-ключ!\n')
        return False    
    if response.status_code == 403:
        print('Получен ответ 403. Доступ на сервер закрыт для данного API!\n')
        return False        
    if response.status_code == 404:
        print('Получен ответ 404. Город не существует, сервер недоступен или неправильный URL!\n')        
        return False             
#------------------------------------------------------------------------------
# Функция перевода градусов в румбы
#------------------------------------------------------------------------------
def wind_direction(deg):
    if (deg > 0 and deg <= 11.25) or (deg > 348.75 and deg <= 0): return 'С,'        
    elif deg > 11.25 and deg <= 33.75: return 'СCВ,'        
    elif deg > 33.75 and deg <= 56.25: return 'СВ,'        
    elif deg > 56.25 and deg <= 78.75: return 'ВСВ,'        
    elif deg > 78.75 and deg <= 101.25: return 'В,'           
    elif deg > 101.25 and deg <= 146.25: return 'ВЮВ,'        
    elif deg > 146.25 and deg <= 168.75: return 'ЮВ,'            
    elif deg > 168.75 and deg <= 191.25: return 'ЮЮВ,'        
    elif deg > 191.25 and deg <= 213.75: return 'Ю,'            
    elif deg > 213.75 and deg <= 236.25: return 'ЮЮЗ,'       
    elif deg > 236.25 and deg <= 258.75: return 'ЮЗ,'        
    elif deg > 258.75 and deg <= 281.25: return 'ЗЮЗ,'        
    elif deg > 281.25 and deg <= 303.75: return 'З,'        
    elif deg > 303.75 and deg <= 326.25: return 'ЗСЗ,'        
    elif deg > 326.25 and deg <= 348.75: return 'СЗ,'        
    elif deg > 0 and deg <= 150.25: return 'ССЗ,'        
    else: return 'недоступно'        
#------------------------------------------------------------------------------
# Функция вывода текущей погоды для выбранного города
#------------------------------------------------------------------------------
def сurrent_weather(obj_txt):
    current_weather=json.loads(obj_txt)
    with open("current_weather.json", "w") as write_file:
        json.dump(current_weather, write_file, indent=3)
    print('1. Координаты города:')
    print('- широта: ', current_weather['coord']['lat'])
    print('- долгота: ', current_weather['coord']['lon'])
    print('2. Погода:')
    print('- описание: ', current_weather['weather'][0]['description'])    
    print('3. Температура:')
    print('- сейчас: ', round(current_weather['main']['temp']), u'\u2103') 
    print('- ощущается как: ', round(current_weather['main']['feels_like']), u'\u2103')
    print('4. Атмосферное давление: ', round(current_weather['main']['pressure']/1.333), 'мм рт.ст.')    
    print('5. Видимость: ', current_weather['visibility'], 'м') 
    print('6. Ветер: ', wind_direction(current_weather['wind']['deg']), current_weather['wind']['speed'], 'м/с', )    
    print('7. Влажность: ', current_weather['main']['humidity'], '%')      
    print('9. Облачность: ', current_weather['clouds']['all'], '%')  
###############################################################################
# Пример получения сведений о текущей погоде по имени города:
#------------------------------------------------------------------------------    
print('Текущий прогноз погоды для выбранного города (Москва):')
url = 'https://api.openweathermap.org/data/2.5/weather/?q=%s&lang=%s&units=%s&appid=%s' % (city,lang,units,key)
response_town = requests.get(url)
if status_response(response_town):
    сurrent_weather(response_town.text)
###############################################################################
# Весь прогноз погоды одним вызовом (One Call API). Доступно:
# - текущая погода;
# - минутный прогноз на 1 час;
# - почасовой прогноз на 48 часов;
# - ежедневный прогноз погоды на 7 дней;
# - глобальные погодные оповещения;
# - исторические данные о погоде за предыдущие 5 дней.
###############################################################################
# Функция вывода 48-часового прогноза погоды (дата-время, температура,
# давление, скорость ветра) одним вызовом с использованием библиотеки
# для анализа данных Pandas
#------------------------------------------------------------------------------
def all_weather(obj_txt): 
    all_weather=json.loads(obj_txt)
    with open("all_weather.json", "w") as write_file:
        json.dump(all_weather, write_file, indent=3)        
    data = pd.read_json(obj_txt)
    df = pd.DataFrame()
    df['Дата,время'] = data['hourly'].apply(lambda x: datetime.datetime.fromtimestamp(x['dt']))
    df['Темп., \u2103'] = data['hourly'].apply(lambda x: round(x['temp']))
    df['Давл., мм рт.ст.'] = data['hourly'].apply(lambda x: round(x['pressure']/1.333))
    df['Ветер, м/с'] = data['hourly'].apply(lambda x: round(x['wind_speed']/1.333))    
    print(df)
#------------------------------------------------------------------------------
# Пример получения 48-часового прогноза (температура, давление, скорость ветра):
#------------------------------------------------------------------------------
# exclude - исключить данные из ответа (если необходимо):
# - current   # Текущая погода
# - minutely  # Минутный прогноз на 1 час
# - hourly    # Почасовой прогноз на 48 часов
# - daily     # Ежедневный прогноз погоды на 7 дней
# - alerts    # Глобальные погодные оповещения
#------------------------------------------------------------------------------
print('\nВесь прогноз погоды одним вызовом для местоположения\nlat=54.71, long=20.51 (г. Калининград):')
#url = 'https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&lang=%s&units=%s&appid=%s'% (lat, long, lang, units, key)
exclude = 'current,minutely,daily,alerts'
url = 'https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=%s&lang=%s&units=%s&appid=%s'% (lat, long, exclude, lang, units, key)
#------------------------------------------------------------------------------
response_all = requests.get(url) 
if status_response(response_all):
    all_weather(response_all.text)
        
    
    
    
    
    
    
    
    
    