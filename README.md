# Виртуальная среда:
#### Создание виртуальной среды:
`python3 -m venv env`
#### Активация виртуальной среды:
`source env/bin/activate`
#### Отключение:
`deactivate`

## Запуск приложения:
`python app.py`

# О боте:
1. **"Предоставление информации"**
	Бот создан как информатор для продуктовых команд или для фирм, оказывающим услуги или продающим товары
2. **"Гибкость"**
	Взаимодействие с ботом строится через меню благодаря, динамически создаваемым, кнопкам. Подробности в п.п. "Типы кнопок"
3. **"Простота"**
	Для наполнения базового функционала и управления не требуется взаимодействовать с БД и тем более обращаться к коду приложения

# Типы кнопок:
1. **"Подкатегория"**
	Кнопка, продолжающая ветвление. Пункт меню который позволяет задавать вложенные кнопки и создавать иерархическую структуру информационного поля бота
2. **"Финальная кнопка"**
	Кнопка, отдающая заданный текст без возможности продолжения ветвления
3. **"Подкатегория с заголовком"**
	Кнопка, отдающая заданный текст и позволяет задавать вложенные кнопки и создавать иерархическую структуру информационного поля бота
4. **"Добавить кнопку"**
	Создание кнопок доступно администраторам бота, которые перечислены в `./.env (ADMINS=502000003,0565656589)` по нажатию кнопки. Кнопка доступна только администраторам
5. **"Назад"**
	Возвращает на предыдущий пункт меню
