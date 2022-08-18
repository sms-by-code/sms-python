from smsby import SMSBY

sms = SMSBY('YOUR-TOKEN-HERE', 'by')
respond = sms.get_balance()
print('Ответ на метод getBalance:')
print(respond)
respond = sms.get_limit()
print('Ответ на метод getLimit:')
print(respond)
print("Создаем новое сообщение")
respond = sms.create_sms_message('Тестовое сообщение! Привет от Горыныча!')
print(respond)
message_id = respond['message_id']
print("Отправляем новое сообщение")

# todo необходимо поставить свой телефон вместо +7916xxxxxxxx
respond = sms.send_sms(message_id, '+7916xxxxxxxx')
print('Ответ на метод sendSms:')
print(respond)

# Парольная часть
print('Создаем пароль:')
respond = sms.create_password_object('both', 10);
print(respond)
password_object_id = respond['result']['password_object_id']

print('Проверяем созданные пароли')
respond = sms.get_password_objects();
print(respond)

# todo необходимо поставить свой телефон вместо +7916xxxxxxxx
print('Посылаем sms с кодом:')
respond = sms.send_sms_message_with_code(password_object_id, '+7916', 'Ваш пароль: %CODE%')
print(respond)
