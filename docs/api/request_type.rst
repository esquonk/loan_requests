API для типов заявок
====================

.. http:get:: /api/request_type/

    Запросить типы заявок на кредит.
    Возвращает json-массив объектов заявок.

.. http:get:: /api/request_type/(int:id)/

    Запросить информацию об одном типе заявки.

    :>json int id: идентификатор
    :>json string title: название
    :>json array fields: json-массив с описанием полей заявки

    **Содержимое массива fields:**

    :>json int id: идентификатор
    :>json boolean required: признак обязательного пола
    :>json string field_group: название группы полей. При отправки заявки обязательно к заполнению хотя бы одно поле из группы.
    :>json string field.name: имя поля
    :>json string field.title: нзвание поля
    :>json string field.description: описание поля
    :>json string field.type: тип поля


