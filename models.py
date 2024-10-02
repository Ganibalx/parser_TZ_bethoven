import csv
from bs4 import BeautifulSoup


class Result:
    city: str
    list = None
    thread = 1

    def __init__(self):
        self.city = input('Введите город для локализации:\n')
        self.thread = int(input('Укажите кол-во потоков:\n'))

    def set_shop_list(self, shop_list):
        print('Доступные магазины для выбранного города: \n')
        for i in range(len(shop_list)):
            print(f'{i + 1} : {shop_list[i].text}')
        tt = input('Введите нужные номера магазинов через запятую, либо 0 для всего списка\n')
        try:
            tt = tt.replace(' ', '').split(',')
            self.list = {shop_list[int(i)-1].text: [] for i in tt} if int(tt[0]) != 0 else {i.text: [] for i in shop_list}
        except Exception:
            raise Exception('что-то пошло не по инструкции')

    def save_info(self):
        i = 1
        for k, v in self.list.values():
            with open(f'file{i}.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['city', 'shop', 'category', 'code', 'name', 'price', 'sale_price', 'values', 'count'])
                writer.writeheader()
                writer.writerows(v)
            i += 1


class Category:
    value: str
    href: str
    children_category: list
    product_in_category: dict

    def __init__(self, value, href):
        self.value = value
        self.href = href
        self.product_in_category = dict()

    def category_pagen(self, session, header):
        page = session.get(self.href, headers=header)
        soup = BeautifulSoup(page.text, 'html.parser')
        self.page_scan(page)
        if soup.find('div', class_='nums'):
            end_page = int(soup.find('div', class_='nums').findAll('a')[-1].text)
            for i in range(2, end_page+1):
                page = session.get(self.href + f'/?PAGEN_1={i}', headers=header)
                self.page_scan(page)

    def page_scan(self, page):
        soup = BeautifulSoup(page.text, 'html.parser')
        product_list = soup.findAll('section', class_='bth-card-element')
        for j in product_list:
            id = j.get('data-product-id')
            self.product_in_category[id] = Product(id)

    def get_products_info(self, session, header):
        iter = list(self.product_in_category.keys())
        for i in range(0, len(iter), 20):
            url = ''.join([f'&id[]={j}' for j in iter[i: i+21]])
            page = session.get('https://www.bethowen.ru/api/local/v1/catalog/list?limit=20&offset=0&sort_type=popular'+url, headers=header)
            json = page.json()
            for product in json['products']:
                name = product['name']
                category = '->'.join(list(product['offers'][0]['categories_chain'].values()))
                children = [offer['id'] for offer in product['offers']]
                self.product_in_category[product['id']].update_info(name, category, children)

    def get_products_shop(self, session, header, result):
        for i in self.product_in_category.keys():
            for j in self.product_in_category[i].children:
                self._get_api_info(j, session, header, result, self.product_in_category[i].name, self.product_in_category[i].category,)

    def _get_api_info(self, product, session, header, result, name, category):
        page = session.get(f'https://www.bethowen.ru/api/local/v1/catalog/offers/{product.id}/details', headers=header)
        shops = list(result.list.keys())
        json = page.json()
        for i in json['availability_info']['offer_store_amount']:
            if i['address'] in shops:
                result.list[i['address']].append({
                    'city': result.city,
                    'shop': i['address'],
                    'category': category,
                    'code': json['vendor_code'],
                    'name': name,
                    'price': json['retail_price'],
                    'sale_price': json['discount_price'],
                    'values': json['size'],
                    'count': i['availability']['text']
                })


class Product:
    __slots__ = ('id', 'name', 'category', 'children')

    def __init__(self, id):
        self.category = None
        self.children = None
        self.name = None
        self.id = id

    def update_info(self, name, category, children):
        self.name = name
        self.children = children
        self.category = category




