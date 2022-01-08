import psycopg2
from code_for_db.config import host, user, password, db_name

try:
    # config for connect
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # db version for ping
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server ver.:{cursor.fetchone()}")

    # create table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE users(
    #             id serial PRIMARY KEY,
    #             first_name varchar(50) NOT NULL,
    #             nick_name varchar(50) NOT NULL);"""
    #     )
    #     print("Create done!")

    # add in to db something
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO users (first_name,nick_name) VALUES
    #         ('oLeZkA','baba');"""
    #     )
    #     print("db inserted")

    # search in table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """SELECT nick_name FROM users WHERE first_name = 'oLeZkA';"""
    #     )
    #
    #     print(cursor.fetchone())

    # -table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """DROP TABLE users;"""
    #     )
    #
    #     print("gg -table")

except Exception as ex_:
    print(ex_)
finally:

    # check if its work close connection
    if connection:
        connection.close()
        print("db closed")
