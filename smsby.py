# Для использования из инициализации класса
import sys
import urllib
import requests


class SMSBY:
    __token = ''
    __api_url = ''
    __api_url_dict = {'by': 'https://app.sms.by/api/v1/'}

    __by_gate_url = 'https://app.sms.by/'
    

    """
    Инициализация класса 
    Args:
        token: Токен для отправки сообщения  
        country_code: Код страны 'by' Беларусь и 'ru' Россия  соответственно выбирается гейт для отправки 
        https://app.sms.by/ 
        
    """

    def __init__(self, token, country_code):
        if token:
            self.__token = token
            if country_code:
                self.__api_url = self.__api_url_dict.get(country_code)
                if self.__api_url == '':
                    print("Неверно указан код страны - завершаю процесс!")
                    sys.exit()
            else:
                print("Неверно указан код для инициализации гейта API - завершаю процесс!")
                sys.exit()
        else:
            print(
                "Код токена не указан. No Token specified. Вы можете получить его здесь: " + self.__by_gate_url + "user-api/token");
            sys.exit()

    """
    Отправка запроса общая внутренняя функция для работы с API 
    Args:
        command: Команда, а на самом деле часть URL для отправки запроса 
        h_params: Набор отправляемых параметров
    Returns:
        Пример ответа: {}
    """

    def __send_request(self, command, h_params: object = {}):
        url = self.__api_url + command + '?token=' + self.__token
        if command:
            if h_params:
                url += "&" + urllib.parse.urlencode(h_params)
            try:
                response = requests.post(url)
                json_response = response.json()
            except Exception:
                print("Something wrong happen")
                json_response = []
            else:
                print("Command perform successfully")
            finally:
                print("All done")
                return json_response

    """
    Метод-обёртка для команды sendQuickSms
    Отправляет сообщение пользователям и используется для разовых рассылок 
    
    Args:
        message: Само сообщение (кириллица или татиница)
        phone: Телефон
    Returns:
        Возвращает ответ:
            {"sms_id":2204968,"status":"NEW"}
    """

    def send_quick_sms(self, message, phone):
        command = 'sendQuickSms'
        h_params = {'message': message, 'phone': phone}
        return self.__send_request(command, h_params)

    """
    Метод-обёртка для команды getBalance
    Получение остатка на балансе
    Args:
        message_id: ID сообщения
        phone: Телефон
    Returns:
        Возвращает ответ:
             {"status":"OK","currency":"RUR","result":[{"balance":"2.86600","viber_balance":"0.00000"}]}
    """

    def get_balance(self):
        command = 'getBalance'
        return self.__send_request(command)

    """
    Получение лимита на отправку сообщений - зависит от баланса
    Returns:
        Возвращает словарь с примерным количеством возможно отправленных сообщений: {"limit":141}
    """

    def get_limit(self):
        command = 'getLimit'
        return self.__send_request(command)

    """
    Получение альфаимен.
    
    Returns:
        This is a description of what is returned.
    """

    def get_alphanames(self):
        command = 'getAlphanames'
        return self.__send_request(command)

    """
    Метод-обёртка для команды getAlphaNameId
    Args:
        name: Название альфаимени.
    Returns:
        Пример ответа: {"id":1111}
    """

    def get_alphaname_id(self, name: str):
        h_params = {'name': name}
        command = 'getAlphanames'
        return self.__send_request(command, h_params)

    """
    Создание сообщения для рассылки
    Args:
        message: Текст сообщения.
        alphaname_id: Алфаимя ID (число или строка)
    Returns:
        Возвращает словарь: {'status': 'ok', 'parts': 1, 'len': 18, 'message_id': 49409, 
        'alphaname': 'system', 'time': 0}
    """

    def create_sms_message(self, message, alphaname_id=''):
        h_params = {'message': message}
        if alphaname_id:
            h_params['alphaname_id'] = alphaname_id
        command = 'createSmsMessage'
        response = self.__send_request(command, h_params)
        return response

    """
    Получение сообщения по его ID
    Args:
        message_id: ID сообщения
    Returns:
        Возвращает словарь:{"error":"not found"}
    """

    def check_sms_message_status(self, message_id: int):
        h_params = {'message_id': str(message_id)}
        command = 'checkSMSMessageStatus'
        response = self.__send_request(command, h_params)
        return response

    """
    Метод-обёртка для команды getMessagesList
    Получение списка всех сообщений
    
    Returns:
        Возвращает словарь:
        {
            "result":[
                {"message_id":2564327,"message":"68755","parts":1,"d_create":"2021-03-22 11:32:32","status":"moderated"},
                {"message_id":2564580,"message":"37271","parts":1,"d_create":"2021-03-22 11:32:32","status":"moderated"}
            ]
        }
    """

    def get_message_list(self):
        command = 'getMessagesList'
        response = self.__send_request(command)
        return response

    """
    Метод-обёртка для команды sendSms
    Отправляет сообщение пользователям по его ID и телефону
    Args:
        message_id: ID сообщения
        phone: Телефон
    Returns:
        Возвращает ответ:
            {"sms_id":2204968,"status":"NEW"}
    """

    def send_sms(self, message_id: int, phone: str):
        h_params = {'message_id': str(message_id), 'phone': phone}
        command = 'sendSms'
        response = self.__send_request(command, h_params)
        return response

    """
    Метод-обёртка для команды checkSMS
    Получение статусов SMS сообщений
    Args:
        sms_id: ID сообщения
    Returns:
        Возвращает ответ:
             {"sms_id":2204968,"delivered":1616064780}
             {"sms_id":2204968,"sent":1616064780}
    """

    def check_sms(self, sms_id: str):
        h_params = {'sms_id': str(sms_id)}
        command = 'checkSMS'
        response = self.__send_request(command, h_params)
        return response

    """
    Метод-обёртка для команды createPasswordObject
    Создание объекта пароля
    
    Args:
        type_id: Может принимать следующие значения: 
                 letters - только буквы латинского алфавита, 
                 numbers - только цифры, 
                 both - смешанный тип
        object_len: Длина пароля от 1 до 16
    Returns:
        Возвращает ответ:
             {
              "result": {
                "password_object_id": 243
              }
            }
    """

    def create_password_object(self, type_id='both', object_len=10):
        h_params = {'type_id': type_id, 'len': object_len}
        command = 'createPasswordObject'
        response = self.__send_request(command, h_params)
        return response

    """
    Метод-обёртка для команды getPasswordObjects
    Получение всех созданных объектов паролей
    Returns:
        Возвращает ответ:
             {
              "result": [
                {
                  "id": 232,
                  "type_id": "both",
                  "len": 5,
                  "d_create": "2021-03-18 10:53:39"
                },
                {
                  "id": 272,
                  "type_id": "both",
                  "len": 6,
                  "d_create": "2021-03-19 11:03:39"
                }
              ]
            }
    """

    def get_password_objects(self):
        command = 'getPasswordObjects'
        response = self.__send_request(command)
        return response

    """
    Метод-обёртка для команды getPasswordObject
    Получение информации по объекту пароля
    Args:
        object_id: ID объекта возвращаемое из createPasswordObject
    Returns:
        Возвращает ответ:
             {
              "result": {
                "id": 248,
                "type_id": "both",
                "len": 4,
                "d_create": "2021-03-20 14:50:11"
              }
            }
    """

    def get_password_object(self, object_id):
        h_params = {'id': object_id}
        command = 'getPasswordObjects'
        response = self.__send_request(command, h_params)
        return response

    """
    Метод-обёртка для команды editPasswordObject
    Редактирование информации по объекту пароля
    Args:
        object_id: ID объекта возвращаемое из createPasswordObject
        type_id: Может принимать следующие значения: 
                    letters - только буквы латинского алфавита, 
                    numbers - только цифры, 
                    both - смешанный тип
        object_len: Длина пароля от 1 до 16
    Returns:
        Возвращает ответ:
             {
               "result": "1"
             }
    """

    def edit_password_object(self, object_id, object_len, type_id='both'):
        h_params = {'id': object_id, 'type_id': type_id, 'len': object_len}
        command = 'getPasswordObjects'
        response = self.__send_request(command, h_params)
        return response

    """
    Метод-обёртка для команды deletePasswordObject
    Удаление объекта пароля
    Args:
        object_id: ID объекта возвращаемое из createPasswordObject
    Returns:
        Возвращает ответ:
             {
              "result": {
                "id": 248,
                "type_id": "both",
                "len": 4,
                "d_create": "2021-03-20 14:50:11"
              }
            }
    """

    def delete_password_object(self, object_id):
        h_params = {'id': object_id}
        command = 'deletePasswordObject'
        response = self.__send_request(command, h_params)
        return response

    """
    Метод-обёртка для команды sendSmsMessageWithCode
    Отправить SMS с кодом подтверждения (sendSmsMessageWithCode)
    Args:
        password_object_id: ID объекта возвращаемое из createPasswordObject
        phone: Номер телефона
        message: сообщение должно обязательно содержать переменную для подстановки %CODE%) 
                 Например: message = Ваш пароль: %CODE%
        alphaname_id: смотрите использование Альфа-имен
    Returns:
        Возвращает ответ:
             {
              "status": "ok",
              "parts": 1,
              "len": 21,
              "sms_id": 2208471,
              "code": "GAYXILYZOX"
            }
    """

    def send_sms_message_with_code(self, password_object_id, phone, message, alphaname_id=''):
        if (alphaname_id):
            h_params = {'password_object_id': password_object_id, 'phone': phone, 'message': message, 'alphaname_id': alphaname_id}
        else:
            h_params = {'password_object_id': password_object_id, 'phone': phone, 'message': message}
        command = 'sendSmsMessageWithCode'
        response = self.__send_request(command, h_params)
        return response
