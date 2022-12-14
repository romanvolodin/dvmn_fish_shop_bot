# Продаём рыбу в Telegram

Это Telegram-бот для продажи рыбы.

## Требования

Для запуска вам понадобится:

- Python 3.6 или выше
- [Redis](https://redis.io/), в качестве базы данных.
- Магазин с товарами в [Elastic Path](https://www.elasticpath.com/). Продукты в магазине проще и понятней добавлять через `Catalog (legacy)`.
- Необходимо зарегистрировать бота и получить токен для доступа к API Телеграма. Подробная инструкция [как зарегистрировать бота](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram/)

## Заполнение магазина

В магазине есть основные сущности:

- Продукт - оно же товар, тут всё понятно.
- Книга цен - это некий набор цен на товары. Например, может быть книга с обычными ценами и книга со сниженными ценами для акций.
- Конфигурация - здесь важно создать иерархию (по сути - категории) товаров. Для бота я просто добавил товары в корневой элемент иерархии (нажимаешь на название категории (root в данном случае) и плюсиками добавляешь товары в категорию).
- Каталог - это способ разделить товары по смыслу. Каталог - это комбинация категорий и книги цен. Пример: в Питере у нас большой магазин, делаем отдельный каталог со всеми товарами и ценами чуть выше. Для Петрозаводска отдельный каталог - продаем только избранные товары и цены ставим чуть ниже.

Порядок заполнения магазина:

- Создаем книгу цен (просто задаем имя книги).
- Создаем товары. Из необязательных полей указываем описание товара и переключаем Product Status, чтобы товар стал активным. При указании цены выбираем нужную книгу. Важно указать количество доступных товаров (Inventory ⟶ Increment нужное количество).
- Создаем иерархию. Задаем имя и накидываем продукты.
- Создаем каталог.

Пока не понимаю порядок заполнения товаров/книги цен. С одной стороны без книги нельзя добавить цену товара. С другой стороны надо добавить товары в книгу цен, ибо именно цены, указанные в книге, отображаются при получении данных через API. И, как выяснилось, прописываются в карточке товара, даже если ранее прописал цену вручную.

**Важно:** каталог надо опубликовать, чтобы получить доступ к товарам через API.

## Подготовка

Скачайте код с GitHub. Установите зависимости:

```sh
pip install -r requirements.txt
```

Сгенерируйте ключ приложения (Application Key) в Elastic Path. Для этого перейдите `Settings → Application Keys` и нажмите `Create`. Имя ключа может быть любое. Сохраните CLIENT_ID и CLIENT_SECRET, они понадобятся для получения токена к API Elastic Path.

## Переменные окружения

Настройки берутся из переменных окружения. Чтобы их определить, создайте файл `.env` в корне проекта и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Пример:

```env
EP_CLIENT_ID=e04ae87f8788327940c5279f356d193a9b6f
EP_CLIENT_SECRET=cf71c07b8c32360ba975ce9b42c0bd4083
EP_PRICEBOOK_ID=19a013-03df-42da-8dfg-9414dfd633b0
TG_TOKEN=57871874:AAH4n9lBfH1iz8DsKx6Vle40qx710f4
DATABASE_PASSWORD=redispass
DATABASE_HOST=localhost
DATABASE_PORT=6379
```

## Запуск

Запуск Redis через Docker:

```sh
docker run --name fish-bot-redis --rm redis:alpine

```

Контейнер будет удален после остановки, данные не сохранятся (нужен volume для этого).
Пароль в данной конфигурации не нужен (должен быть пустой строкой).

Запустите бота в терминале:

```sh
python bot.py
```

В случае успешного старта скрипт ничего не выводит и запускает бесконечный цикл. Остановить можно командой `Ctrl+C`.

## Цели проекта

Код написан в учебных целях — для курса по Python на сайте [Devman](https://dvmn.org/modules/chat-bots/)
