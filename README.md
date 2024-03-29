# Dash-apps

Здесь будут выложены работы веб-приложений на основе Dash (python)

## Geocoder
Приложение, которое определяет координаты для списка мест. Алгоритм действий:

1. Загрузить файл с местами (записанными в колонке `name`) в форматах `csv` или `excel`
2. Подождать
3. Получить таблицу с координатами и всеми соответствующими местами из алгоритма геокодера OSM (если место не найдено, то в таблице будут пустые значения)
4. Получить карту с найденными местами
5. Скачать готовый файл с координатами.

### Установка
#### Скачать данные

Клонирование репозитория

```
git clone https://github.com/yupest/dash-apps.git
```
Или кликнуть на `Code` -> `Download ZIP` чтобы скачать архив. После чего извлечь данные.

#### Установка зависимостей

Запустить консоль `python`. Перейти в папку `Geocoder`. При необходимости прописать полный путь (`cd D:/.../.../Geocoder`)
```
cd Geocoder 
pip install -r requirements.txt
```
### Использование

1. Подготовить файл в формате `csv` или `excel` с колонкой `name`, в которой содержится список мест.
2. Запуск приложение осуществляется также в консоли `python`
```
python geocoder.py
```
3. После чего нужно открыть страницу (`localhost:8050`): 
```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "geocoder" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```
![](https://github.com/yupest/dash-apps/blob/main/Geocoder/geocoder_example.gif?raw=true)

## [НТО.Визуализация](https://github.com/yupest/dash-apps/tree/main/nto.visualization)
Приложение предназначено для знакомства с визуализацией данных, созданием дашборда. Позволяет:

1. Загрузить файл в форматах `csv` или `excel`
2. Создать визуализации в разделе `Визуализация`:
- Столбчатая диаграмма
- Линейная диаграмма
- Диаграмма рассеяния
- Круговая диаграмма
- Облако слов
- Текстовое описание и настройка названия дашборда
4. Автоматически отобразить дашборд: перетащить и масштабировать блоки с визуализациями

Подробнее: https://youtube.com/playlist?list=PL6LiR0TiNuAK7wExhS8UZfUNrWHOMorHF&si=hWFNRedbuXX6D27s

Сервис выложен: https://yupest.pythonanywhere.com/

### Установка
#### Клонирование репозитория

```
git clone https://github.com/yupest/dash-apps.git
```
Или кликнуть на `Code` -> `Download ZIP` чтобы скачать архив. После чего извлечь данные.

#### Установка зависимостей

Запустить консоль `python`. Перейти в папку `nto.visualization`. При необходимости прописать полный путь (`cd D:/.../.../nto.visualization`)
```
cd nto.visualization 
pip install -r requirements.txt
```
