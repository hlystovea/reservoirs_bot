# Reservoirs Bot
Telegram бот проекта «Водохранилища ГЭС России»

![Static Badge](https://img.shields.io/badge/hlystovea-reservoirs_bot-reservoirs_bot)
![GitHub top language](https://img.shields.io/github/languages/top/hlystovea/reservoirs_bot)
![GitHub](https://img.shields.io/github/license/hlystovea/reservoirs_bot)
![GitHub Repo stars](https://img.shields.io/github/stars/hlystovea/reservoirs_bot)
![GitHub issues](https://img.shields.io/github/issues/hlystovea/reservoirs_bot)

[Бот](https://t.me/reservoirs_bot) предоставляет удобный интерфейс для отображения информации о гидрологической обстановке на водохранилищах ГЭС России. Также у проекта есть [веб-версия](https://github.com/hlystovea/reservoirs_web).

![gif](https://media.giphy.com/media/IhxXpF9H1nhcQHYsTP/giphy.gif)

## Установка (Linux)
У вас должен быть установлен [Docker Compose](https://docs.docker.com/compose/)

1. Клонирование репозитория 

```git clone https://github.com/hlystovea/reservoirs_bot.git```

2. Переход в директорию reservoirs_web

```cd reservoirs_bot```

3. Создание файла с переменными окружения

```cp env.example .env```

4. Заполнение файла .env своими переменными

```nano .env```

5. Запуск проекта

```sudo docker compose up -d```

## Поддержка
Если у вас возникли сложности или вопросы по использованию проекта, создайте 
[обсуждение](https://github.com/hlystovea/reservoirs_bot/issues/new/choose) в данном репозитории или напишите в [Telegram](https://t.me/hlystovea).

