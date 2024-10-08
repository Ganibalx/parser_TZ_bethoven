# Тестовое задание #
***
## Описание ##
Без применения каких-либо фреймворков (например scrapy)
необходимо написать MVP многопоточного парсера интернет-магазина 
[Бетховен](https://www.bethowen.ru/). 


Парсер должен уметь собирать информацию о товарах и ценах. Информация должна содержать: город, код и наименование товара, цены (регулярные и акционные) и информацию о наличии по каждому из вариантов товара (например фасовка: 2.5кг или 12кг) в ТТ (торговой точке / магазине).

Сбор должен выполняться по всем товарам во всех категориях, содержать информацию о наличии товаров в выбранной ТТ.

В итоге файл сбора будет содержать информацию о ценах и наличию по ассортименту той ТТ, на сбор которой будет настроен парсер. Информация о наличии должна содержать флаг наличия (есть в наличии / нет в наличии) и информацию о фактическом остатке в ТТ (если такую информация можно получить из API источника).

## Нюансы ##
- Нужно предусмотреть обработку ошибок получения ответа на запросы.
- Плюсом будет исчерпывающий Readme, наличие возможности запускать парсер как по всем категориям, так и по конкретным задаваемым, а также удобство настройки работы парсера (выбор числа потоков, города, адреса ТТ, категорий сбора).

## Инструкция по исползованию ##
Установка библиотек


```python -m pip install -r requirements.txt```

Запуск

```python main.py```