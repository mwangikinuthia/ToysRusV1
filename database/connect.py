"""
This utility is for connecting to a database (toys) with MySQL.
"""
from pymysql import connect,err,sys, cursors


def create_tables(conn):
    try:
        cursor = conn.cursor()
        print("Creating table 'categories")

        cursor.execute("""CREATE TABLE IF NOT EXISTS categories(
  ID int(11) NOT NULL AUTO_INCREMENT,
  category_name varchar(255) DEFAULT NULL,
  category_url varchar(255) DEFAULT NULL,
  PRIMARY KEY (ID)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;""")
        print("creating table products")
        cursor.execute("""CREATE TABLE IF NOT EXISTS products(
  ID int(11) NOT NULL AUTO_INCREMENT,
  title varchar(255) DEFAULT NULL,
  productId int(11) DEFAULT NULL,
  categoryPath varchar(255) DEFAULT NULL,
  category_node longtext,
  rating varchar(20) DEFAULT NULL,
  reviews varchar(20) DEFAULT NULL,
  brand varchar(255) DEFAULT NULL,
  in_stock varchar(5) DEFAULT NULL,
  ship_to_home varchar(5) DEFAULT NULL,
  free_store_pick_up varchar(5) DEFAULT NULL,
  mg_url varchar(255) DEFAULT NULL,
  gift_wrap varchar(5) DEFAULT NULL,
  description longtext,
  features longtext,
  price varchar(10) DEFAULT NULL,
  product_url longtext,
  PRIMARY KEY (ID)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=latin1;""")
    except Exception as e:
        print ("Found Error {}".format(e))


def connect_db():
    # Replace with real credentials
    conn  =connect(host='******',user='*****',password='root',db='toys',autocommit=True)
    return conn





