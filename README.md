# Задание 1. Сервер времени - Вариант 2
Разработать веб приложение (напр через интерфейс wsgi) реализующее аналог сервиса time.is и предоставляющее работу с временными зонами на базе библиотеки tz
1) Веб приложение по запросу GET / отдает текущее время во временной зоне сервера в формате html
2) по запросу GET /<tz name> отдает текущее время в запрошенной зоне в формате html
3) по запросу POST /api/v1/time - отдает в формате json текущее время в зоне определенной параметром tz(если нет - то зона сервера)
4) по запросу POST /api/v1/date- отдает в формате json текущую дату в зоне определенной параметром tz(если нет - то зона сервера)

5) по запросу POST /api/v1/datediff- отдает в формате json время между датами определенными параметрами start и end (каждый - это json формата {"date":"12.20.2021 22:21:05", "tz": "EST"} или {"date":"12:30pm 2020-12-01", "tz": "Europe/Moscow"}, tz - опциональна).

# Запустите сервер WSGI
Откройте терминал и запустите WSGI-приложение:
```
python server.py
```
Output
```
Server running at http://127.0.0.1:8000/
```
# Запустите тесты API
Откройте другой терминал. Запустите тестовый скрипт:
```
python test.py
```
Output
```
Testing GET /
<h1>Current Server Time: 2025-01-08 17:51:38 +0700</h1>

Testing GET /<tz_name>
Time in Europe/London: <h1>Current Time in Europe/London: 2025-01-08 10:51:38 +0000</h1>
Time in Asia/Ho_Chi_Minh: <h1>Current Time in Asia/Ho_Chi_Minh: 2025-01-08 17:51:38 +0700</h1>
Time in America/New_York: <h1>Current Time in America/New_York: 2025-01-08 05:51:38 -0500</h1>

Testing POST /api/v1/time
{'time': '2025-01-08 19:51:38', 'tz': 'Asia/Tokyo'}

Testing POST /api/v1/date
{'date': '2025-01-08', 'tz': 'UTC'}

Testing POST /api/v1/datediff
{'difference': '24 days, 23:04:00'}
```
