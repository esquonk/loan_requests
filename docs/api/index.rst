Использование API
=================

    API для работы с заявками используется протокол `REST <https://ru.wikipedia.org/wiki/REST>`_.

Точки доступа API
=================

.. toctree::
   :maxdepth: 1

   request_type
   request


Аутентификация
==============
    Аутентификация в системе возможна двумя способами:

    * HTTP Basic Auth
    * OAuth2

    Чтобы получить `access_token` для oauth2, нужно выплонить запрос на адрес:

    .. http:post:: /o/token/

        В запросе должны передаваться параметры в формате x-www-form-urlencoded:

        :param grant_type: `password`,
        :param username: имя пользователя
        :param password: пароль
        :param client_id: client_id
        :param client_secret: client_secret

    Пример запроса с помощью `curl`::

        curl -X POST -d "grant_type=password&client_id=<client_id>&client_password=<client_password>&username=<user_name>&password=<password>" http://<server_name>/o/token/
