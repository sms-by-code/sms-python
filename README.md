# sms-python
Простой способ отправить смс на Python

Методы класса SMSBY
init - Инициализация класса необходимо передать token и код страны
send_quick_sms - Отправка "быстрого" СМС без его
get_balance - Получение информации по балансу счета
get_limit - Получение примерного лимита на отправление сообщений
get_alphanames - Получение альфаимен (подписей отправителя)
get_alphaname_id - Получение информации по конкретному альфаимени
create_sms_message - Создание SMS сообщения (для массовой рассылки)
check_sms_message_status - Получение информации статуса сообщения
get_message_list - Получение списка всех сообщений
send_sms - Отправка сообщения (массовая рассылка)
check_sms - Проверка статуса сообщений
create_password_object - Создание объекта пароля
get_password_objects - Получение всех созданных объектов паролей
get_password_object - Получение информации по объекту пароля
edit_password_object - Редактирование информации по объекту пароля
delete_password_object - Удаление объекта пароля
send_sms_message_with_code - Отправить SMS с кодом подтверждения (sendSmsMessageWithCode)

Подключение класса SMSBY
Подключение стандартно для python3

from smsby import SMSBY
Далее по коду:

sms = SMSBY('xxxxxxxx', 'by')

respond = sms.get_balance()
print('Ответ на метод getBalance:')
где, xxxxxxxx токен sms из вашего личного кабинета

Для python2 библиотека (класс) не подходит
