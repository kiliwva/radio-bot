# Telegram-магазин цифровых услуг (Radio Bot)

Готовый проект Telegram-бота с inline-кнопками + административная веб-панель + Telegram Web App.

## Что реализовано

- Каталог товаров в боте:
  - Telegram Stars
  - Аренда NFT
  - Аренда виртуальных номеров
  - Telegram Premium
- Оформление заказа с выбором платежки (Pally / Platega / CryptoBot / FreeKassa)
- Система тикетов
- Stars баланс и генерация чеков
- Админ-панель:
  - просмотр пользователей, заказов, тикетов
  - блокировка/разблокировка пользователей
  - перевод заказов по статусам
  - включение/выключение каждой платежной системы
- Telegram Web App витрина
- Аналитика:
  - топ пользователей по покупкам Stars
  - калькулятор прибыли

## Структура

```text
app/
  bot/
    handlers/
    keyboards/
    main.py
  services/
  web/
    templates/
    static/
    main.py
  config.py
  database.py
run_bot.py
run_web.py
tests/
```

## Запуск

1. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Создать `.env`:
   ```env
   BOT_TOKEN=ваш_токен
   WEBAPP_URL=https://ваш-домен/webapp
   DATABASE_URL=sqlite:///./radio_bot.db
   ```
3. Запуск веб-панели:
   ```bash
   python run_web.py
   ```
4. Запуск бота:
   ```bash
   python run_bot.py
   ```

## Команды бота

- `/start` — главное меню
- `/ticket Тема | Текст` — создать тикет
- `/topup <amount>` — пополнить Stars баланс (демо)
- `/check <amount>` — создать чек из Stars
