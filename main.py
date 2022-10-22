import bs4
import requests
import csv
import unicodecsv

# with open('waatafak.html','r',encoding='utf-8') as file:
#     text_of_site = file.read()
#     file = bs4.BeautifulSoup(text_of_site,'lxml')
#     h1 = file.find_all('a')
#     for item in h1:
#         item_text = item.text
#         item_url = item.get('href')
#         print(item_url)
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"
}
req = requests.get('https://calorizator.ru/product', headers=headers)


# def pereb_item(item1):
#     a = 0
#     with open('one.csv', 'w', encoding="cp1251", newline='') as table:
#         for item in item1:
#
#             item_text = item.text
#             print(item_text.replace(' ', ''))
#             writer = csv.writer(table)
#             writer.writerow([item_text])
#             if item_text == 'Кал, ккал' and a == 0:
#                 break
#                 a = 1
#         table.close()
#

def heads(heads,count,item_text):
    product = heads[1].text
    protein = heads[2].text
    fats = heads[3].text
    carbohydrate = heads[4].text
    kkal = heads[5].text
    with open(f'Tables/{item_text}.csv', 'w', encoding="cp1251", newline='') as table:
        writer = csv.writer(table)
        writer.writerow(([product, protein, fats, carbohydrate, kkal]))


soup = bs4.BeautifulSoup(req.text, 'lxml')
tags = soup.find(class_='product').find_all('a')
count = 0
table = []
for item in tags:
    item_text = item.text
    item_url = item.get('href')
    req_next = requests.get(f'https://calorizator.ru/{item_url}')
    soup_next = bs4.BeautifulSoup(req_next.text, 'lxml')
    table = soup_next.find('table').find_all(class_='active')
    heads(table,count,item_text)

    #Данные продуктов

    table_value = soup_next.find('tbody').find_all('tr')
    x = 0
    for value in table_value:
        #print(x)
        product_name = value.find_all('td')
        name = product_name[1].find('a').text
        product = product_name[1].find('a').text
        protein = product_name[2].text
        fats = product_name[3].text
        carbohydrate = product_name[4].text
        kkal = product_name[5].text

        with open(f'Tables/{item_text}.csv', 'a', encoding="cp1251") as table:
            writer = csv.writer(table)
            writer.writerow(
                (
                    [
                        product,
                        protein,
                        fats,
                        carbohydrate,
                        kkal

                    ]
                )
            )

        #print(kkal)
        x+=1
    # print(f'{item_text}: https://calorizator.ru/{item_url}')
    count += 1
#print(table_value[2].text)