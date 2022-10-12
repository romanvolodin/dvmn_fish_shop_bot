# Продаём рыбу в Telegram

Это Telegram-бот для продажи рыбы.

## Требования

Для запуска вам понадобится:

- Python 3.6 или выше
- [Redis](https://redis.io/), в качестве базы данных.
- Магазин с товарами в [Elastic Path](https://www.elasticpath.com/). Продукты в магазине проще и понятней добавлять через `Catalog (legacy)`.
- Необходимо зарегистрировать бота и получить токен для доступа к API Телеграма. Подробная инструкция [как зарегистрировать бота](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram/)

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
EP_ACCESS_TOKEN=365289d32d452b1473a1b94f83cd425b
TG_TOKEN=57871874:AAH4n9lBfH1iz8DsKx6Vle40qx710f4
DATABASE_PASSWORD=redispass
DATABASE_HOST=localhost
DATABASE_PORT=6379
```

## Запуск

Запустите бота в терминале:

```sh
python bot.py
```

В случае успешного старта скрипт ничего не выводит и запускает бесконечный цикл. Остановить можно командой `Ctrl+C`.

## Цели проекта

Код написан в учебных целях — для курса по Python на сайте [Devman](https://dvmn.org/modules/chat-bots/)