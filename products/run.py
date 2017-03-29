from categories.categories import find_if_subcategory,find_main_categories
from products.products import get_prod_info


def rec_run(link):
    p = find_if_subcategory(link)
    if p:
        for i in p:
            z = find_if_subcategory(i)
            if z:
                rec_run(i)
    else:
        y = get_prod_info(link)
        for p in y:
            get_prod_info(p)


def run():
    sub_cat_list = find_main_categories()

    for link in sub_cat_list:
        rec_run(link)