from products.run import run
from contextlib import redirect_stdout
from database.connect import create_tables,connect_db


if __name__ == '__main__':
    print("Ensure you have a database named toys in your mysql db")
    create_tables(connect_db())
    def logger():
        with open('help.txt', 'a') as f:
            with redirect_stdout(f):
                print("CHECK THIS FILE FOR PROGRESS AND ERRORS")
                run()
    logger()