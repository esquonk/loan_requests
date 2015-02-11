API для работы с заявками
=========================

.. http:get:: /api/request/

    Запросить список заявок.

.. http:get:: /api/request/(int:id)/

    Запросить информацию о заявке.

    :>json int id: идентификатор
    :>json string user: имя пользователя, создавшего заявку
    :>json int request_type: идентификатор :doc:`типа заявки </api/request_type>`
    :>json object content: поля заявки

.. http:post:: /api/request/

    Создать новую заявку.

    :<json int request_type: идентификатор :doc:`типа заявки </api/request_type>`
    :<json object content: поля заявки.

    **Поля заявки**

    Поле `content` в запросе должно содержать json-объект, где именам полей соответствуют их значения.
    Имена и типы полей зависят от типа заявки.

.. http:put:: /api/request/(int:id)/
.. http:patch:: /api/request/(int:id)/

    Изменить завку.

    :<json int request_type: идентификатор :doc:`типа заявки </api/request_type>`
    :<json object content: поля заявки.

.. http:delete:: /api/request/(int:id)/

    Удалить завку.