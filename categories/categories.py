from utility.utilities import open_url,get_id
from products.products import get_prod_info,prods
from database.connect import connect_db

departments = ['Action Figures & Hero Play, NERF Blasters','Arts & Crafts, Educational Toys, Books',
               'Baby, Toddler & Preschool Learning Toys','Bikes, Scooters & Ride-Ons','Building Blocks, LEGO Toys',
               'Cooking for Kids, Play Kitchen Sets','Dolls, Dress Up, Stuffed Animals, Tween',
               'Electronics, Tech Toys, Movies, Music','Games, Puzzles, Boutique Toys','Outdoor Play, Kids Sports, Swimming Pools',
               'Party Supplies & Candy Shop','Vehicles, Trains, RC','Video Games','Holiday Shops',"Kids' Clothes",'Kids Furniture']

base_url = "http://www.toysrus.com"


def find_main_categories():
    """Returns a dict object of sub category urls from the main page"""
    categories = []
    cat = 'http://www.toysrus.com/category/index.jsp?categoryId=2273442&ab=TRU_Header:Utility3:See-All-Categories:Home-Page'
    soup = open_url(cat)
    categories_parent = soup.find_all('div', {'class': 'subCatBlockTRU'})

    for j in categories_parent:
        category_title = j.find('h2').text
        cat= category_title.strip()
        if cat in departments:
            # print('Category {}'.format(category_title))
            sub_categories = j.find_all('li')
            for n in sub_categories:
                name = n.text
                p = n.find('a')
                u=(base_url+p['href'])
                categories.append(u)
        else:
           pass
    return categories

def find_main_categories():
    """Returns a dict object of sub category urls from the main page"""
    categories = []
    cat = 'http://www.toysrus.com/category/index.jsp?categoryId=2273442&ab=TRU_Header:Utility3:See-All-Categories:Home-Page'
    soup = open_url(cat)
    categories_parent = soup.find_all('div', {'class': 'subCatBlockTRU'})

    for j in categories_parent:
        category_title = j.find('h2').text
        cat= category_title.strip()
        if cat in departments:
            # print('Category {}'.format(category_title))
            sub_categories = j.find_all('li')
            for n in sub_categories:
                name = n.text
                p = n.find('a')
                u=(base_url+p['href'])
                categories.append(u)
        else:
           pass
    return categories

def find_if_subcategory(link):

    """For categories with sub categories"""
    db = connect_db()
    cursor = db.cursor()
    print('opening link {}'.format(link))
    category_id = int(get_id(link, 'categoryId='))
    soup = open_url(link)
    nullify_search = soup.find('form', id ='results-form')
    sub_cat = soup.find(id = 'TRUFamilyBrandTitle').text
    if category_id:
        sql = """INSERT INTO categories(category_url, category_name) VALUES (%s,%s)"""

        cursor.execute(sql,(link, sub_cat))
    if nullify_search:
        p = prods(link)
        print('[**]Found {} products in {}'.format(len(p),sub_cat))
        for product in p:

            get_prod_info(product)
        return p
    p = soup.find('div', {'class':'sliderWrapper'})
    d = []
    if p:
        ps = p.find_all('p')
        for links in ps:
            urls = links.find('a')
            url = urls['href']
            name = urls.text
            if 'ALL' not in name:
                sample =url
                if base_url in sample:
                    d.append(sample)
                else:
                    d.append(base_url+sample)
    if d:
        for elem in d:
            print('[******Category {}*******'.format(sub_cat))
            find_if_subcategory(elem)
    db.close()
    return
