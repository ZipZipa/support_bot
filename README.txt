#Создание виртаальной среды 
python3 -m venv env
#Активация вертуально среды 
source env/bin/activate
#Отключение 
deactivate



Запуск приложения: 
python app.py

{"id": "155454188941853375", 
"from": {"id": 36194498, "is_bot": false, "first_name": "M", "last_name": "M", "username": "mmc021", "language_code": "ru"},
"message": {"message_id": 1197, "from": {"id": 5041994394, "is_bot": true, "first_name": "Бот поддержки ДОПС", "username": "dopssup_bot"},
"chat": {"id": 36194498, "first_name": "M", "last_name": "M", "username": "mmc021", "type": "private"},
"date": 1648393518, 
"edit_date": 1648393562, 
"text": "Смотри, что у нас есть",
"reply_markup": 
    {"inline_keyboard": 
        [[{
        "text": "ПСИ", 
        "callback_data": "show_menu:0:ПСИ"},
        {"text": "ПРОМ", "callback_data": "show_menu:0:ПРОМ"}], [{"text": "ИФТ", "callback_data": "show_menu:0:ИФТ"}, {"text": "НТ", "callback_data": "show_menu:0:НТ"}], [{"text": "Назад", "callback_data": "show_menu:0:0"}]]}}, "chat_instance": "3187156444270727489", "data": "show_menu:0:ПСИ"} {"inline_keyboard": [[{"text": "EФС", "callback_data": "show_menu:1:EФС"}, {"text": "ППРБ", "callback_data": "show_menu:5:ППРБ"}]]}
