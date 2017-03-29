from utility.utilities import open_url,get_id,cleaner


def get_prod_info(url):
    soup = open_url(url)
    print('product url {}'.format(url))

    data = {
        'price': '',
        'productId': get_id(url, 'productId='),
        'categoryPath': '',
        'categoryNode': '',
        'title': '',
        'rating': 'N/A',
        'numOfReviews': '0',
        'brand': '',
        'inStock': 'No',
        'shipToHome': 'No',
        'freeStorePickup': 'No',
        'imgUrl': '',
        'giftWrap': 'Yes',
        'description': '',
        'features': 'Check description',
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
            data['title'] = t.text

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
            data['inStock'] = 'Yes'
        if data['inStock'] == 'Yes':
            data['shipToHome'] = 'Yes'
        p = elegibility.find('li', {'class': 'ispu-eligible avail in-stock prd'})
        y = elegibility.find('li', {'class': 'sts-eligible avail in-stock prd'})
        if p or y:
            data['freeStorePickup'] = 'Yes'

        image = soup.find(id='productView')
        img_src = image.find('a')
        src = img_src.find('img')
        if src:
            base_url = 'www.toysrus.com'
            img_url = src['src']
            data['imgUrl'] = base_url + img_url
        s = soup.find('p', {'class': 'lineHt'})
        if s.text == 'Gift wrap is not available for this item.':
            data['giftWrap'] = 'No'
        short_desc = soup.find(id='Description')
        desc = short_desc.find('p')
        if desc:
            data['description'] = desc.text
        fr = soup.find(id='Features')
        if fr:
            features = []
            f = fr.find_all('li')
            for j in f:
                features.append(j.text)
            data['features'] = features
    except Exception as e:
        print(e)
        pass
    print(data)
    return data
