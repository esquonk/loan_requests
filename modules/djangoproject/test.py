# coding: utf-8
from __future__ import unicode_literals

import base64
import json
from django.contrib.auth.models import User, Group

from django.test import TestCase, Client
from django.utils.http import urlencode
from loan_requests.models import RequestType, RequestField, RequestTypeField, RequestFieldChoice, Request


def http_auth(username, password):
    return {
        'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('{}:{}'.format(username, password)),
        }


class RequestTest(TestCase):
    def setUp(self):
        rt = RequestType.objects.create(title='Автокредит')
        RequestTypeField.objects.create(
            request_type=rt,
            field=RequestField.objects.create(field_type='string', name='last_name', title='Фамилия'),
            required=True
        )
        RequestTypeField.objects.create(
            request_type=rt,
            field=RequestField.objects.create(field_type='string', name='first_name', title='Имя'),
            required=False
        )
        RequestTypeField.objects.create(
            request_type=rt,
            field=RequestField.objects.create(field_type='date', name='birth_date', title='Дата рождения'),
            required=False
        )
        car_type_field=RequestField.objects.create(field_type='string', name='car_type', title='Тип авто')
        RequestTypeField.objects.create(
            request_type=rt,
            field=car_type_field,
            required=True
        )
        RequestTypeField.objects.create(
            request_type=rt,
            field=RequestField.objects.create(field_type='string', name='phone1', title='Телефон 1'),
            field_group='phone',
            required=False
        )
        RequestTypeField.objects.create(
            request_type=rt,
            field=RequestField.objects.create(field_type='string', name='phone2', title='Телефон 2'),
            field_group='phone',
            required=False
        )
        RequestTypeField.objects.create(
            request_type=rt,
            field=RequestField.objects.create(field_type='inn', name='inn', title='ИНН'),
            required=False
        )

        RequestFieldChoice.objects.create(field=car_type_field, text='Новая')
        RequestFieldChoice.objects.create(field=car_type_field, text='Старая')

        User.objects.create_user(username='common_user1', password='123')
        User.objects.create_user(username='common_user2', password='123')
        bank_user = User.objects.create_user(username='bank_user', password='123')
        g = Group.objects.get(name='Сотрудники банка')
        g.user_set.add(bank_user)
        User.objects.create_superuser(username='super_user', email='nobody@example.com', password='123')

    def test_rq_type_api(self):
        c = Client(**http_auth('common_user1', '123'))
        res = c.get('/api/request_type/')
        res_obj = json.loads(res.content)
        self.assertEqual(len(res_obj), 1)
        self.assertEqual(res_obj[0]['title'], 'Автокредит')

        res = c.post('/api/request_type/', {
            'title': 'qweqweqwe'
        })
        self.assertJSONEqual(res.content, '''{"detail":"Method 'POST' not allowed."}''')

    def test_request_submit_errors(self):
        rt_id = RequestType.objects.get(title='Автокредит').id

        c = Client(**http_auth('common_user1', '123'))

        res = c.post('/api/request/', json.dumps({
            'request_type': rt_id,
            'content': {

            }
        }), content_type="application/json")
        res_obj = json.loads(res.content)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(res_obj['content']['car_type']), 1)
        self.assertEqual(len(res_obj['content']['last_name']), 1)

        res = c.post('/api/request/', json.dumps({
            'request_type': rt_id,
            'content': {
                'car_type': 'Новая',
                'last_name': 'Иванов',
            }
        }), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertIn('Обязательно для заполнения хотя бы одно из полей', res.content.decode('utf-8'))

        res = c.post('/api/request/', json.dumps({
            'request_type': rt_id,
            'content': {
                'car_type': 'Новая',
                'last_name': 'Иванов',
                'phone1': '123',
                'inn': '123',

            }
        }), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertIn('Неправильный формат ИНН', res.content.decode('utf-8'))

        res = c.post('/api/request/', json.dumps({
            'request_type': rt_id,
            'content': {
                'car_type': 'Новая',
                'last_name': 'Иванов',
                'phone1': '123',
                'birth_date': 'wqewrqwer',

            }
        }), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertIn('YYYY[-MM[-DD]]', res.content.decode('utf-8'))

    def test_request_submit_access(self):
        rt_id = RequestType.objects.get(title='Автокредит').id
        req_data = {
            'request_type': rt_id,
            'content': {
                'last_name': 'Иванов',
                'car_type': 'Новая',
                'phone2': '123',
                'inn': '1234567890',
            }
        }

        c = Client()

        def make_request(username, password):
            res = c.post('/api/request/',
                         json.dumps(req_data),
                         content_type="application/json",
                         **http_auth(username, password))
            self.assertEqual(res.status_code, 201)
            res_obj = json.loads(res.content)
            req_id = res_obj['id']
            return req_id

        req_id = make_request('common_user1', '123')

        res = c.get('/api/request/{}/'.format(req_id), **http_auth('common_user1', '123'))
        self.assertEqual(res.status_code, 200)

        res = c.get('/api/request/{}/'.format(req_id), **http_auth('common_user2', '123'))
        self.assertEqual(res.status_code, 404)

        res = c.get('/api/request/{}/'.format(req_id), **http_auth('bank_user', '123'))
        self.assertEqual(res.status_code, 200)

        res = c.get('/api/request/{}/'.format(req_id), **http_auth('super_user', '123'))
        self.assertEqual(res.status_code, 200)

        res = c.delete('/api/request/{}/'.format(req_id), **http_auth('common_user2', '123'))
        self.assertEqual(res.status_code, 404)

        res = c.delete('/api/request/{}/'.format(req_id), **http_auth('bank_user', '123'))
        self.assertEqual(res.status_code, 204)

        req_id = make_request('common_user1', '123')

        res = c.delete('/api/request/{}/'.format(req_id), **http_auth('super_user', '123'))
        self.assertEqual(res.status_code, 204)

        make_request('common_user2', '123')
        make_request('common_user2', '123')
        make_request('common_user2', '123')

        res = c.get('/api/request/', **http_auth('common_user2', '123'))
        self.assertEqual(len(json.loads(res.content)), 3)

        res = c.get('/api/request/', **http_auth('common_user1', '123'))
        self.assertEqual(len(json.loads(res.content)), 0)

        res = c.get('/api/request/', **http_auth('bank_user', '123'))
        self.assertEqual(len(json.loads(res.content)), 3)

        res = c.get('/api/request/', **http_auth('super_user', '123'))

        reqs = json.loads(res.content)
        self.assertEqual(len(reqs), 3)

        for req in reqs:
            res = c.delete('/api/request/{}/'.format(req['id']), **http_auth('super_user', '123'))
            self.assertEqual(res.status_code, 204)

        res = c.get('/api/request/', **http_auth('super_user', '123'))
        reqs = json.loads(res.content)
        self.assertEqual(len(reqs), 0)
        self.assertEqual(len(list(Request.objects.all())), 0)

    def test_oauth2(self):
        c = Client()

        user = User.objects.get_by_natural_key('common_user1')

        client_id = user.application_set.first().client_id
        client_secret = user.application_set.first().client_secret

        res = c.post('/o/token/', urlencode({
            'grant_type': 'password',
            'username': 'common_user1',
            'password': '123',
            'client_id': client_id,
            'client_secret': client_secret,
            }), content_type='application/x-www-form-urlencoded;charset=UTF-8')

        res_obj = json.loads(res.content)
        self.assertIn('access_token', res_obj)

        access_token = res_obj['access_token']

        res = c.get('/api/request_type/', HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(json.loads(res.content)) > 0)

    def test_anonymous(self):
        c = Client()
        res = c.get('/api/request_type/')
        self.assertEqual(res.status_code, 401)
        res = c.get('/api/request/')
        self.assertEqual(res.status_code, 401)

