from urllib.parse import urljoin

import requests


class BadCredentials(Exception):
    pass


class Timeout(Exception):
    pass


class BadRequest(Exception):
    pass


class BadResponse(Exception):
    pass

# Разрешенные параметры для фильрации списка товаров
allowed_params_get_products = [
    'market_hash_name',
    'market_hash_name__icontains',
    'categories',
    'name__ru',
    'name__ru__icontains',
    'game__id',
    'name__en',
    'name__en__icontains',
    'name__ru__exact',
    'name__en__exact',
    'market_hash_name__exact',
]


class Api(object):
    base_url = None
    token = None

    def __init__(self, url, token, timeout=None):
        self.base_url = url + '/' if not url.endswith('/') else url
        self.timeout = timeout
        self.headers = {'Authorization': 'Token %s' % token}

    def get_locales(self) -> dict:
        """
        Список поддерживаемых языков и валют
        :return:
        """
        url = urljoin(self.base_url, 'locales')

        r = requests.get(url, headers=self.headers, timeout=self.timeout)
        if r.status_code == requests.codes.ok:
            try:
                response = r.json()
            except:
                raise BadResponse('Cannot deserialize server response')
            else:
                return response

        if r.status_code == 401:
            raise BadCredentials()

        if r.status_code == 400:
            raise BadRequest()

        raise BadResponse('Unknown error')

    def get_products(self, page=1, per_page=None, fields=None, currency=None,
                     lang=None, **kwargs) -> dict:
        """
        Список продуктов в системе
        :param per_page: кол-во продуктов на странице
        :param page: номер страницы
        :param fields: список полей, требуемых от системы
        :param currency: список валют, в которых необхоимо отдавать цены
        :param lang: список языков, в которых необходимо передавать названия
                     товаров
        :param kwargs: фильтры по разрешенным полям
        :return:
        """
        assert page > 0
        assert per_page is None or per_page > 0
        assert fields is None or isinstance(fields, list)
        assert currency is None or isinstance(currency, list)
        assert lang is None or isinstance(lang, list)
        assert all(map(lambda k: k in allowed_params_get_products, kwargs.keys()))

        url = urljoin(self.base_url, 'products/')

        params = {'page': page}
        params.update(kwargs)

        if per_page:
            params['per_page'] = per_page

        if fields:
            params['fields'] = fields

        if currency:
            params['_currency'] = currency

        if lang:
            params['_lang'] = lang

        r = requests.get(url, params=params, headers=self.headers,
                         timeout=self.timeout)
        if r.status_code == requests.codes.ok:
            try:
                response = r.json()
            except:
                raise BadResponse('Cannot deserialize server response')
            else:
                return response

        if r.status_code == 401:
            raise BadCredentials()

        if r.status_code == 400:
            raise BadRequest()

        raise BadResponse('Unknown error')


# TODO: получение конкретного товара по его идентфиикатору
# TODO: получение списка категорий
# TODO: получение списка игр
