import csv
from lxml import html
from pathlib import Path

keyword = 'blender bottle'

current_directory = Path().absolute()
result_directory = current_directory.joinpath("excavating_information")
data_seller_directory = current_directory.joinpath("request-to-seller_info_url")


seller_info_urls = []

with open(result_directory.joinpath(f'result_product({keyword}).csv'), mode='r', encoding='utf-8', newline='') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        seller_info_url = row[-1]  
        seller_info_urls.append(seller_info_url)


columns = ['seller_name','business_name','business_address','zip_code','country']

with open(result_directory.joinpath(f'result_product({keyword}).csv'), mode='r', encoding='utf-8', newline='') as file:
    rows = list(csv.reader(file))
    rows[0].extend(columns)

    for index in range(len(rows[1:])):
        if rows[1:][index][-1] != '-':
            print(rows[1:][index][-1])
            print(index)
            with open(data_seller_directory.joinpath(f'{index}_seller_html({keyword}).html'), 'r', encoding='utf-8') as file:
                html_content = file.read()
            tree = html.fromstring(html_content)

            seller_name_1 = tree.xpath('//h1[@id="seller-name"]/text()')
            seller_name = seller_name_1[0]

            business_name_1 = tree.xpath('(//span[contains(text(),"Business Name")]/..)//text()')
            business_name = business_name_1[1]

            business_address_1 = tree.xpath('(//span[contains(text(),"Business Address")]/../..)//div[contains(@class,"indent-left")]//text()')
            business_address = ''
            for address_index in range(len(business_address_1) - 2):
                if address_index == range(len(business_address_1) - 2)[-1]:
                    business_address += business_address_1[address_index]
                else:    
                    business_address += business_address_1[address_index] + ' - '
            zip_code = business_address_1[-2]
            country = business_address_1[-1]

            rows[1:][index].extend([seller_name,business_name,business_address,zip_code,country])
        else:
            rows[1:][index].extend(['-','-','-','-','-'])

with open(result_directory.joinpath(f'result_product({keyword}).csv'), mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

