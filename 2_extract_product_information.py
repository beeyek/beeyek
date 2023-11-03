from lxml import html
import csv
from pathlib import Path
import json

keyword = 'blender bottle'

current_directory = Path().absolute()
data_1_directory  = current_directory.joinpath("product-url_img_title_rate")
data_2_directory  = current_directory.joinpath("request-to-product-url")
result_directory = current_directory.joinpath("excavating_information")

with open(result_directory.joinpath(f'result_product({keyword}).csv'), mode='w', encoding='utf-8', newline='') as product_file:
    employee_writer = csv.writer(product_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow(['product_id', 'marketplace_id', 'product_title', 'product_price', 'list_price', 'manufacturer', 'upc', 'model_name', 'product_dimensions', 'product_weight', 'customer_ratings', 'average_rating', 'listing_url', 'image_url', 'seller_info_url'])

with open(data_1_directory.joinpath(f'product_url({keyword}).json'), 'r', encoding='utf-8') as file:
    data_1 = json.load(file)

for i in range(len(data_1["product_data"])):
    print(i,'/',len(data_1["product_data"]))
    product_image_url = data_1["product_data"][i][1]
    product_title = data_1["product_data"][i][2]
    product_rate = data_1["product_data"][i][3]
    with open(data_2_directory.joinpath(f'{i}_product_html({keyword}).html'), 'r', encoding='utf-8') as file:
        html_content = file.read()
    tree = html.fromstring(html_content)

    product_id_1 = tree.xpath('//th[contains(text(),"ASIN")]/../td/text()')
    if product_id_1:
        product_id = product_id_1[0]
    else:
        product_id_2 = tree.xpath('(//span[contains(text(),"ASIN")]/../span)[last()]/text()')
        if product_id_2:
            product_id = product_id_2[0]
        else:
            product_id = '-'

    product_seller_1 = tree.xpath('(//div[@id="merchantInfoFeature_feature_div"]//div[@offer-display-feature-name="desktop-merchant-info"])[last()]//text()')
    if product_seller_1:
        product_seller = product_seller_1[2]
        if product_seller == 'Amazon.com':
            marketplace_id = 1
        else:
            marketplace_id = 2
    else:
        marketplace_id = '-'

    product_price_1 = tree.xpath('//div[@id="corePrice_feature_div"]//text()')
    if product_price_1:
        product_price = product_price_1[3]
    else:
        product_price_2 = tree.xpath('//span[@id="price_inside_buybox"]/text()')
        if product_price_2:
            product_price = product_price_2[0]
        else:
            product_price = '-'

    product_list_price_1 = tree.xpath('((//span[contains(text(),"List Price")])[1]/..)//text()')
    if product_list_price_1:
        product_list_price = product_list_price_1[2]
    else:
        product_list_price = product_price

    product_brand_manufacturer_1 = tree.xpath('//th[contains(text(),"Brand")]/../td/text()')
    if product_brand_manufacturer_1:
        product_brand_manufacturer = product_brand_manufacturer_1[0].strip()
    else:
        product_brand_manufacturer_2 = tree.xpath('(//span[contains(text(),"Manufacturer")]/../span)[last()]/text()')
        if product_brand_manufacturer_2:
            product_brand_manufacturer = product_brand_manufacturer_2[0]
        else:
            product_brand_manufacturer = '-'
    
    product_upc_1 = tree.xpath('//th[contains(text(),"Part Number")]/../td/text()')
    if product_upc_1:
        product_upc = product_upc_1[0].strip()
    else:
        product_upc_2 = tree.xpath('(//span[contains(text(),"Item model number")]/../span)[last()]/text()')
        if product_upc_2:
            product_upc = product_upc_2[0]
        else:
            product_upc = '-'

    product_model_name_1 = tree.xpath('//th[contains(text(),"Model Name")]/../td/text()')
    if product_model_name_1:
        product_model_name = product_model_name_1[0].strip()
    else:
        product_model_name = '-'

    product_dimensions_1 = tree.xpath('//th[contains(text(),"Product Dimensions")]/../td/text()')
    if product_dimensions_1:
        product_dimensions = product_dimensions_1[0].strip()
    else:
        product_dimensions_2 = tree.xpath('(//span[contains(text(),"Dimensions")]/../span)[last()]/text()')
        if product_dimensions_2:
            product_dimensions = product_dimensions_2[0].split(';')[0]
        else:
            product_dimensions = '-'

    product_weight_1 = tree.xpath('//th[contains(text(),"Item Weight")]/../td/text()')
    if product_weight_1:
        product_weight = product_weight_1[0].strip()
    else:
        product_weight_2 = tree.xpath('(//span[contains(text(),"Dimensions")]/../span)[last()]/text()')
        if product_weight_2:
            try:
                product_weight = product_weight_2[0].split(';')[1]
            except:
                product_weight = '-'
        else:
            product_weight = '-'
            
    product_customer_ratings_1 = tree.xpath('(//span[@id="acrCustomerReviewText"])[1]/text()')
    if product_customer_ratings_1:
        product_customer_ratings = product_customer_ratings_1[0]
    else:
        product_customer_ratings = '-'

    listing_url = product_img_url = data_1["product_data"][i][0]

    if marketplace_id == 2:
        seller_info_url_1 = tree.xpath('(//div[@id="merchantInfoFeature_feature_div"]//div[@offer-display-feature-name="desktop-merchant-info"])[last()]//a')
        if seller_info_url_1:
            seller_info_url = 'https://www.amazon.com' + seller_info_url_1[0].get('href')
        else:
            seller_info_url = '-'
    else:
        seller_info_url = '-'

    with open(result_directory.joinpath(f'result_product({keyword}).csv'), mode='a', encoding='utf-8', newline='') as product_file:
        employee_writer = csv.writer(product_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow([product_id, marketplace_id, product_title, product_price, product_list_price, product_brand_manufacturer, product_upc, product_model_name, product_dimensions, product_weight, product_customer_ratings, product_rate, listing_url, product_image_url, seller_info_url])
        
