#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "sammy"
__date__ = "$Jan 18, 2017 7:10:03 PM$"

import requests
from bs4 import BeautifulSoup
from utility.utilities import get_id,open_url,cleaner,remove_
from database.connect import connect_db


base_url = "http://www.toysrus.com"



def get_all_products_urls(link):
    teaser_page = open_url(link)
    guiding_text = teaser_page.find('div', {'class': 'showingText'}).text
    numbers = [int(s) for s in guiding_text.split() if s.isdigit()]
    items_in_cat = numbers[2]
    print(items_in_cat)
    if items_in_cat:
        complete_page = link + '&ppg={}'.format(items_in_cat)
        print('[****]getting link {}'.format(complete_page))
        urls = prods(complete_page)
        print(len(urls),urls)
    return urls

def prods(page):
    prod_urls = []
    page = open_url(page)

    products = page.find_all('div', {'class': 'prodloop_float'})
    for prod in products:
        name = prod.find('div', {'class':'prodloop-thumbnail'})
        name_ = name.find('a')
        prod_href = base_url+ name_['href']
        prod_urls.append(prod_href)
    return prod_urls


def get_prod_info(url):
    product = requests.get(url)
    soup = BeautifulSoup(product.text, 'html.parser')
    print('         Getting product {}'.format(url))

    data = {
        'price': '',
        'productId': str(get_id(url, 'productId=')),
        'categoryPath': '',
        'categoryNode': '',
        'title': '',
        'rating': 'N/A',
        'numOfReviews': '0',
        'brand': '',

    }
    data2 = {
        'inStock': 'No',
        'shipToHome': 'No',
        'freeStorePickup': 'No',
        'imgUrl': '',
        'giftWrap': 'Yes',
        'description': '',
        'features': 'Check description',
        'productUrl': url
    }

    try:
        p = soup.find('li', {'class': 'first'})
        txt = p.find('label')
        data['brand'] = txt.text

        text_ = soup.find(id='AddnInfo')

        t = [str.strip(x) for x in text_.strings if str.strip(x) != '']
        ut = [str.strip(x.text) for x in text_.find_all()]
        y = set(t).difference(ut)
        t = t[1:13]
        d = dict(zip(t[::2], t[1::2]))
        for key, value in d.items():
            d[key] = value.replace("\xa0", ' ')
        data.update(d)

        breadcrumbs = soup.find(id='breadCrumbs')
        links = breadcrumbs.find_all('a')
        pp = []
        for i in links:
            pp.append(i.text)
        categoryPath = '|'.join(pp)
        categoryPath = categoryPath.replace("'","")
        data['categoryPath'] = categoryPath
        ll = []
        for i in links:
            ll.append(i['href'])
        g = ll[len(ll) - 1]
        category_id = get_id(g, 'categoryId=')
        data['categoryNode'] = category_id
        title = soup.find(id='lTitle')
        if title:
            t = title.find('h1')
            t = cleaner(t.text)
            data['title'] = t

        rating = soup.find('span', {'class': 'pr-rating pr-rounded average'})
        if rating is not None:
            data['rating'] = rating.text

        price = soup.find('li', {'class': 'retail fl '})
        if price is not None:
            pr = price.find('span')
            data['price'] = pr.text
        else:
            price = soup.find('li', {'class': 'retail fl withLP'})
            pr = price.find('span')
            data['price'] = pr.text
        Review = soup.find('span', {'class': "count"})
        if Review is not None:
            data['numOfReviews'] = Review.text
        elegibility = soup.find(id='eligibility')
        if elegibility.find('li', {'class': 'stock avail'}):
            data2['inStock'] = 'Yes'
        if data2['inStock'] == 'Yes':
            data2['shipToHome'] = 'Yes'
        p = elegibility.find('li', {'class': 'ispu-eligible avail in-stock prd'})
        y = elegibility.find('li', {'class': 'sts-eligible avail in-stock prd'})
        if p or y:
            data2['freeStorePickup'] = 'Yes'

        image = soup.find(id='productView')
        img_src = image.find('a')
        src = img_src.find('img')
        if src:
            base_url = 'www.toysrus.com'
            img_url = src['src']
            data2['imgUrl'] = base_url + img_url
        s = soup.find('p', {'class': 'lineHt'})
        if s.text == 'Gift wrap is not available for this item.':
            data2['giftWrap'] = 'No'
        short_desc = soup.find(id='Description')
        desc = short_desc.find('p')
        if desc:
            des = desc.text
            de = des.strip()
            de = remove_(de)
            data2['description'] = de
        fr = soup.find(id='Features')
        if fr:
            features = []
            f = fr.find_all('li')
            for j in f:
                features.append(j.text)

            p_ = "\n".join(features)
            p = remove_(p_)

            data2['features'] = p
        db = connect_db()
        cursor = db.cursor()
        try:

            cursor.execute(
                """INSERT INTO products(price,in_stock,title,productId,categoryPath,category_node,rating,reviews,brand,ship_to_home,img_url,free_store_pick_up,gift_wrap,features,description)VALUES ('%s','%s','%s','%s','%s','%s','%s', '%s','%s', '%s','%s','%s','%s','%s','%s')"""
                % (data['price'], data2['inStock'], data['title'], data['productId'], data['categoryPath'],
                   data['categoryNode'], data['rating'], data['numOfReviews'], data['brand'], data2['shipToHome'],
                   data2['imgUrl'], data2['freeStorePickup'], data2['giftWrap'], data2['features'],data2['description']))
            print("             *[***Committed {} details to database***]".format(data['title']))
        except Exception as e:
            print('         '+e)
            print('---------->Could not get {}'.format(url))

    except Exception as e:
        print(e)
        pass
    return data
