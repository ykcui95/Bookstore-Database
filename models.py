from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
DB_NAME = "database.db"

class Customer(db.Model, UserMixin):
    loginName = db.column(db.VARCHAR(25),
                          db.ForeignKey('address.loginName', ondelete="CASCADE"),
                          db.ForeignKey('payment.loginName', ondelete="CASCADE"),
                          db.ForeignKey('comment.loginName', ondelete="CASCADE"),
                          db.ForeignKey('commentrate.ratingUser', ondelete="CASCADE"),
                          db.ForeignKey('trust.loginName', ondelete="CASCADE"),
                          db.ForeignKey('trust.declareName', ondelete="CASCADE"),
                          primary_key=True)
    password = db.column(db.VARCHAR(30))
    firstName = db.column(db.VARCHAR(25))
    lastName = db.column(db.VARCHAR(25))
    manager = db.column(db.BINARY, default=0)

class Address(db.Model):
    loginName = db.column(db.VARCHAR(25), primary_key=True)
    addID = db.column(db.INTEGER,
                      db.ForeignKey('address.loginName', ondelete="CASCADE"),
                      primary_key=True)
    street = db.column(db.VARCHAR(30))
    city = db.column(db.VARCHAR(25))
    state = db.column(db.VARCHAR(25))
    phone = db.column(db.VARCHAR(15))
    postalCode = db.column(db.INTEGER)

class Payment(db.Model):
    loginName = db.column(db.VARCHAR(25), primary_key=True)
    cardNumber = db.column(db.INTEGER, primary_key=True)
    expireDate = db.column(db.DateTime)

class Orders(db.Model):
    orderNumber = db.column(db.VARCHAR(25), primary_key=True)
    loginName = db.column(db.VARCHAR(25),
                          db.ForeignKey('customer.loginName'))
    ISBN = db.column(db.CHAR(13),
                     db.ForeignKey('book.ISBN'))
    addID = db.column(db.Integer,
                      db.ForeignKey('address.addID'))
    cardNumber = db.column(db.Integer,
                           db.ForeignKey('payment.cardNumber'))
    amount = db.column(db.INTEGER)

class Comment(db.Model):
    loginName = db.column(db.VARCHAR(25),
                          db.ForeignKey('commentrate.loginName', ondelete="CASCADE"),
                          primary_key=True)
    ISBN = db.column(db.CHAR(13),
                     db.ForeignKey('commentrate.ISBN', ondelete="CASCADE"),
                     primary_key=True)
    content = db.column(db.VARCHAR(255))
    score = db.column(db.INTEGER)

class Commentrate(db.Model):
    loginName = db.column(db.VARCHAR(25), primary_key=True)
    ISBN = db.column(db.CHAR(13), primary_key=True)
    ratingUser = db.column(db.VARCHAR(25), primary_key=True)
    rating = db.column(db.INTEGER)

class Trust(db.Model):
    loginName = db.column(db.VARCHAR(25), primary_key=True)
    declareName = db.column(db.VARCHAR(25), primary_key=True)
    trustornot = db.column(db.BINARY)

class Book(db.Model):
    ISBN = db.column(db.CHAR(13),
                     db.ForeignKey('write.ISBN', ondelete="CASCADE"),
                     db.ForeignKey('comment.ISBN', ondelete="CASCADE"),
                     db.ForeignKey('key.ISBN', ondelete="CASCADE"),
                     primary_key=True)
    title = db.column(db.VARCHAR(25))
    publisher = db.column(db.VARCHAR(255))
    language = db.column(db.VARCHAR(20))
    publishDate = db.column(db.DateTime)
    stockLevel = db.column(db.Integer)
    price = db.column(db.DECIMAL(12, 2))
    subject = db.column(db.VARCHAR(20))

class Write(db.Model):
    ISBN = db.column(db.CHAR(13), primary_key=True)
    firstName = db.column(db.VARCHAR(25), primary_key=True)
    lastName = db.column(db.VARCHAR(25), primary_key=True)

class Author(db.Model):
    firstName = db.column(db.VARCHAR(25),
                          db.ForeignKey('write.firstName', ondelete="CASCADE"),
                          primary_key=True)
    lastName = db.column(db.VARCHAR(25),
                         db.ForeignKey('write.lastName', ondelete="CASCADE"),
                         primary_key=True)

class Key(db.Model):
    keywordType = db.column(db.CHAR(25), primary_key=True)
    ISBN = db.column(db.CHAR(13), primary_key=True)

class Keyword(db.Model):
    keywordType = db.column(db.CHAR(25),
                            db.ForeignKey('key.keywordType', ondelete="CASCADE"),
                            primary_key=True)