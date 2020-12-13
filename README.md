Пример работы с API OpenWetherMap на Python (https://openweathermap.org). 
Получение сведений о текущей погоде и прогнозе с использованием бесплатного ключа API сайта OpenWeather (https://openweathermap.org/)

1. Доступные URL API для текущей погоды (Current weather API):
 - по городу:
'https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}'
'https://api.openweathermap.org/data/2.5/weather?q={city name},{state code}&appid={API key}'
'https://api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}'
'https://api.openweathermap.org/data/2.5/weather?id={city id}&appid={API key}'
 - по географическим координатам:
'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}'
 - по zip-коду:
'https://api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API key}'
 - для нескольких городов в прямоугольной области координат:
'https://api.openweathermap.org/data/2.5/box/city?bbox={bbox}&appid={API key}'
 - для нескольких городов в окружности:
'https://api.openweathermap.org/data/2.5/box/city?bbox={bbox}&appid={API key}'
 - для нескольких городов по ID:
'https://api.openweathermap.org/data/2.5/group?id={id,..,id}&appid={API key}'

2. Весь прогноз погоды одним вызовом (One Call API). Доступно:
 - текущая погода;
 - минутный прогноз на 1 час;
 - почасовой прогноз на 48 часов;
 - ежедневный прогноз погоды на 7 дней;
 - глобальные погодные оповещения;
 - исторические данные о погоде за предыдущие 5 дней.

Пример URL API:
'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&lang={language}&units={units}&appid={API key}'
