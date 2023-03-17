import psycopg2
import enum
import datetime


class RequestCodes(enum.Enum):
    POST = 0
    GET = 1


class DataBaseHandler:

    def __init__(self, database, host, user, password, port):
        self.conn = psycopg2.connect(database=database,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port)

    def handle_request(self, request, values, request_code):
        cursor = self.conn.cursor()
        cursor.execute(request, values)
        if request_code == RequestCodes.POST:
            self.conn.commit()
        if request_code == RequestCodes.GET:
            return cursor.fetchall()


class AbstractManager:
    def __init__(self, database, host, user, password, port):
        self.dbh = DataBaseHandler(database, host, user, password, port)


class UserManager(AbstractManager):

    # CRUD users

    def create_user(self, name, email, phone):
        sql = "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)"
        values = (name, email, phone)
        self.dbh.handle_request(sql, values, RequestCodes.POST)

    def read_users(self):
        sql = "SELECT * FROM users "
        values = ()
        return self.dbh.handle_request(sql, values, RequestCodes.GET)

    def read_user(self, user_id):
        sql = "SELECT * FROM users WHERE id = %s"
        return self.dbh.handle_request(sql, (user_id,), RequestCodes.GET)

    def update_user(self, user_id, name=None, email=None, phone=None):
        sql = "UPDATE users SET "
        values = []
        if name is not None:
            sql += "name = %s, "
            values.append(name)
        if email is not None:
            sql += "email = %s, "
            values.append(email)
        if phone is not None:
            sql += "phone = %s, "
            values.append(phone)
        if not values:
            return
        sql = sql[:-2] + " WHERE id = %s"
        values.append(user_id)
        self.dbh.handle_request(sql, values, RequestCodes.POST)

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = %s"
        self.dbh.handle_request(sql, (user_id,), RequestCodes.POST)


class BookManager(AbstractManager):

    # CRUD books

    def create_book(self, title, author, year, count):
        sql = "INSERT INTO books (title, author, year,count) VALUES (%s, %s, %s, %s)"
        values = (title, author, year, count)
        self.dbh.handle_request(sql, values, RequestCodes.POST)

    def read_books(self):
        sql = "SELECT * FROM books "
        values = ()
        return self.dbh.handle_request(sql, values, RequestCodes.GET)

    def read_book(self, book_id):
        sql = "SELECT * FROM books WHERE id = %s"
        return self.dbh.handle_request(sql, (book_id,), RequestCodes.GET)

    def update_book(self, book_id, title=None, author=None, year=None, count=None):
        sql = "UPDATE books SET "
        values = []
        if title is not None:
            sql += "title = %s, "
            values.append(title)
        if author is not None:
            sql += "author = %s, "
            values.append(author)
        if year is not None:
            sql += "year = %s, "
            values.append(year)
        if count is not None:
            sql += "count = %s, "
            values.append(count)
        if not values:
            return
        sql = sql[:-2] + " WHERE id = %s"
        values.append(book_id)
        self.dbh.handle_request(sql, values, RequestCodes.POST)

    def delete_book(self, book_id):
        sql = "DELETE FROM books WHERE id = %s"
        self.dbh.handle_request(sql, (book_id,), RequestCodes.POST)

    def take_book(self, user_id, book_id, time_taken):
        sql = "INSERT INTO user_book (user_id, book_id, time_taken) VALUES (%s, %s, %s)"
        values = (user_id, book_id, time_taken)
        self.dbh.handle_request(sql, values, RequestCodes.POST)


# um = UserManager("library", "localhost", "postgres", "password", "5432")
# user = um.read_user(1)
# print(*user)
# user = um.update_user(1,'anoxin','HUILA.com','228_228_228')
# um.delete_user(2)
# um.create_user('Samat', 'ssi.com', 123456789)
# bk = BookManager("library", "localhost", "postgres", "password", "5432")
# bk.create_book('Маша и Медведь', 'Пшкин', 1920, 3)
# bk.take_book(3, 5, datetime.datetime.now())
