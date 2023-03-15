import psycopg2


class Library:

    def __init__(self, database, host, user, password, port):
        self.conn = psycopg2.connect(database=database,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port)
        self.cursor = self.conn.cursor()

#CRUD books

    def create_book(self, title, author, year, is_available):
        sql = "INSERT INTO books (title, author, year,is_available) VALUES (%s, %s, %s, %s)"
        values = (title, author, year, is_available)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def read_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def read_book(self, book_id):
        sql = "SELECT * FROM books WHERE id = %s"
        self.cursor.execute(sql, (book_id,))
        return self.cursor.fetchone()

    def update_book(self, book_id, title=None, author=None, year=None):
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
        if not values:
            return
        sql = sql[:-2] + " WHERE id = %s"
        values.append(book_id)
        self.cursor.execute(sql, tuple(values))
        self.conn.commit()

    def delete_book(self, book_id):
        sql = "DELETE FROM books WHERE id = %s"
        self.cursor.execute(sql, (book_id,))
        self.conn.commit()

#CRUD users

    def create_user(self, name, email):
        sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
        values = (name, email)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def read_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def read_user(self, user_id):
        sql = "SELECT * FROM users WHERE id = %s"
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def update_user(self, user_id, name=None, email=None):
        sql = "UPDATE users SET "
        values = []
        if name is not None:
            sql += "name = %s, "
            values.append(name)
        if email is not None:
            sql += "email = %s, "
            values.append(email)
        if not values:
            return
        sql = sql[:-2] + " WHERE id = %s"
        values.append(user_id)
        self.cursor.execute(sql, tuple(values))
        self.conn.commit()

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = %s"
        self.cursor.execute(sql, (user_id,))
        self.conn.commit()




library = Library("library", "localhost", "postgres", "letu4i_1wsv9_tsv9", "5432")

# Create a book
library.create_book("буратино", "амир", 2003, True)

# Read all books
books = library.read_books()
for book in books:
    print(book)

# Read a specific book
book = library.read_book(1)
print(book)

# Update a book
library.update_book(1, "The Great Gatsby", "F. Scott Fitzgerald")

# Delete a book
library.delete_book(1)


# Update user
library.update_user(1, "samat", "sami4@gmail.com")
