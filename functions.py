from .models import db

#1
def  CustomerRegistration(loginName, password, firstName, lastName):
    if len(loginName)>25:
        print("Username is too long")
        return
    elif len(password)>30:
        print("Password is too long")
        return
    elif len(firstName)>25:
        print("Firstname is too long")
        return
    elif len(lastName)>30:
        print("Lastname is too long")
        return
    lognumber = db.session.execute(
        'SELECT *'
        'FROM customer'
        'WHERE loginName = :loginName', {'loginName': loginName}
    )
    #elif 0 != not(lognumber):
    #    print("Username is taken")
    #    return

    db.session.execute(
        'INSERT INTO customer(:loginName, :password, :firstName, :lastName)'
        , {'loginName': loginName, 'password': password, 'firstName': firstName, 'lastName': lastName}
    )
    db.session.commit()

#2
def ManagerRegistration(loginName):
    db.session.execute(
        'UPDATE customer'
        'SET customer.manager=1'
        'WHERE loginName = :loginName', {'loginName': loginName}
    )
    db.session.commit()

#3
def Ordering(loginName, ISBN, amount, addID, cardNumber):
    db.session.execute(
        'INSERT INTO orders(:loginName, :ISBN, :amount, :addID, :cardNumber)',
        {'loginName': loginName, 'ISBN': ISBN, 'amount': amount,
         'addID': addID, 'cardNumber': cardNumber}
    )
    db.session.commit()
    db.session.execute(
        'UPDATE book'
        'SET book.stockLevel= book.stockLevel- :amount'
        'WHERE ISBN = :ISBN', {'amount': amount, 'ISBN': ISBN}
    )
    db.session.commit()

#4
def NewBook(ISBN, title, publisher, language, publishDate, pageNumber, amount, authorlist, price, keywordlist, subject):
    booknumber = db.session.excute(
        'SELECT COUNT(ISBN)'
        'FROM book'
        'WHERE ISBN=:ISBN1',
        {'ISBN1': ISBN}
    )
    #if booknumber!=0:
        #NewCopy(ISBN, amount)
        #return
    #else:
    db.session.execute(
        'INSERT INTO book(:ISBN, :title, :publisher, :language, :publishDate, :pageNumber, :amount, :price)',
        {'ISBN': ISBN, 'title': title, 'publisher':publisher, 'language': language, 'publishDate': publishDate, 'pageNumber': pageNumber, 'amount': amount, 'amount': price}
    )
    db.session.commit()
    for element in authorlist:
        NewAuthor(element[0-24], element[25-49])
        db.session.execute(
            'INSERT INTO write(:ISBN, :firstName, :lastName)',
            {'ISBN': ISBN, 'firstName1': element[0-24], 'lastName1': element[25-49]}
        )
        db.session.commit()
    for element in keywordlist:
        NewKeyword(element)
        db.session.execute(
            'INSERT INTO key(:ISBN, :keywordType)',
            {'ISBN': ISBN, 'keywordType': element}
        )
        db.session.commit()

def NewAuthor(firstName, lastName):
    atuhornumber=db.session.excute(
        'SELECT COUNT(firstName, lastNme)'
        'FROM author'
        'WHERE firstName=:firstName1 AND lastName=:lastName1',
        {'firstName1': firstName, 'lastName1': lastName}
    )
    #if authornumber!=0:
        #return
    db.session.execute(
        'INSERT INTO author(:firstName, :lastName)',
        {'firstName': firstName, 'lastName': lastName}
        )
    db.session.commit()

def NewKeyword(keywordType):
    keynumber=db.session.excute(
        'SELECT COUNT(keywordType)'
        'FROM keyword'
        'WHERE keywordType=:keywordType1',
        {'keywordType1': keywordType}
    )
    #if keynumber!=0:
        #return
    db.session.execute(
        'INSERT INTO keyword(:keywordType)',
        {'keywordType': keywordType}
        )
    db.session.commit()

#5
def NewCopy(ISBN, amount):
    db.session.execute(
        'UPDATE book'
        'SET book.stockLevel= book.stockLevel+ :amount'
        'WHERE ISBN = :ISBN', {'amount': amount, 'ISBN': ISBN}
    )
    db.session.commit()

#6
def AddComment(loginName, ISBN, content, score):
    db.session.execute(
        'INSERT INTO comment(:loginName, :ISBN, :content, :score)',
        {'loginName': loginName, 'ISBN': ISBN, 'content': content,
         'score': score}
    )
    db.session.commit()

#7
def CommentRating(loginName, ISBN, ratingUser, rating):
    db.session.execute(
        'INSERT INTO commentrate(:loginName, :ISBN, :ratingUser, :rating)',
        {'loginName': loginName, 'ISBN': ISBN, 'ratingUser': ratingUser,
         'rating': rating}
    )
    db.session.commit()

#8
def TrustRecording(loginName, ISBN, declareName, trustornot):
    db.session.execute(
        'INSERT INTO trust(:loginName, :ISBN, :declareName, :trustornot)',
        {'loginName': loginName, 'ISBN': ISBN, 'declareName': declareName,
         'trustornot': trustornot}
    )
    db.session.commit()

#9
def BookBrowsing(ifauthor, author, ifpublisher, publisher, iftitle, title, iflanguage, language, ifdate, ifscore, iftrust):
    if ifauthor:
        booklist = db.session.execute(
            'SELECT *'
            'FROM book JOIN write'
            'WHERE write.firstName=:firstName1 AND write.lastName=:lastName1',
            {'firstName1': author[0:24], 'lastName1': author[25:49]}
        )
        return booklist
    if ifpublisher:
        booklist = db.session.execute(
            'SELECT *'
            'FROM book '
            'WHERE publisher=:publisher1',
            {'publisher1': publisher}
        )
        return booklist
    if iftitle:
        booklist = db.session.execute(
            'SELECT *'
            'FROM book '
            'WHERE title=:title1',
            {'title1': title}
        )
        return booklist
    if iflanguage:
        booklist = db.session.execute(
            'SELECT *'
            'FROM book '
            'WHERE language=:language1',
            {'language1': language}
        )
        return booklist
    if ifdate:
        booklist = db.session.execute(
            'SELECT *'
            'FROM book '
            'ORDER BY publishDate DESC'
        )
        return booklist
    if ifscore:
        booklist = db.session.execute(
            'SELECT *'
            'FROM book JOIN comment'
            'GROUP BY book.ISBN, comment.score'
            'ORDER BY AVERAGE(comment.score) DESC'
        )
        return booklist
    if iftrust:
        booklist = db.session.execute(
            'SELECT *'
            'FROM book JOIN comment JOIN customer JOIN trust on customer.loginNaem = trust.loginName'
            'WHERE trust.trustornot=1'
            'GROUP BY book.ISBN, comment.score'
            'ORDER BY AVERAGE(comment.score) DESC'
        )
        return booklist

#10
def UsefulComment(ISBN, n):
    useful = db.session.execute(
        'SELECT C.loginName, C.ISBN, C.content, C.score, avgRating'
        'FROM comment AS C JOIN commentrate AS Cr'
        'WHERE C.ISBN = :ISBN1'
        'GROUP BY C.loginName, C.ISBN, C.content, C.score'
        'ORDER BY AVERAGE(Cr.rating) AS avgRating DESC'
        'LIMIT :num', {'ISBN1': ISBN, 'num': n}
    )
    return useful

#11
def BuyingSuggestion(ISBN):
    suggest = db.session.execute(
        'SELECT O2.ISBN'
        'FROM customer AS C JOIN order AS O1, order AS O2'
        'WHERE O1.ISBN = :ISBN1'
        'AND O2.loginName = C.loginName AND O2.ISBN <> O1.ISBN'
        'LIMIT :num', {'ISBN1': ISBN}
    )
    return suggest

#12
def Degree(author, degree):
    if(degree==1):
        degreeauthor = db.session.execute(
            'SELECT A2.firstName, A2.firstName'
            'FROM author AS A1 JOIN write AS W, author AS A2'
            'WHERE A1.firstName = :firstName AND A1.lastName = :lastName'
            'AND A1.ISBN = A2.ISBN'
            'AND A1.firstName <> A2.firstName AND A1.lastName <> A2.lastName',
            {'firstName': author[0:24], 'lastName': author[25:49]}
        )
    elif (degree == 2):
        degreeauthor = db.session.execute(
            'SELECT A3.firstName, A3.firstName'
            'FROM author AS A1 JOIN write AS W, author AS A2, author AS A3'
            'WHERE A1.firstName = :firstName AND A1.lastName = :lastName'
            'AND A1.ISBN = A2.ISBN AND A2.ISBN = A3.ISBN'
            'AND A1.firstName <> A2.firstName AND A1.lastName <> A2.lastName'
            'AND A1.firstName <> A3.firstName AND A1.lastName <> A3.lastName'
            'AND A3.firstName <> A2.firstName AND A3.lastName <> A2.lastName'
            'AND A2.ISBN <> A1.ISBN',
            {'firstName': author[0:24], 'lastName': author[25:49]}
        )
    return degreeauthor

#13
def BookeStatistics(m):
    popularbook = db.session.execute(
        'SELECT B.title'
        'FROM book AS B JOIN order AS O'
        'GROUP BY B.ISBN, O.amount'
        'ORDER BY SUN(O.amount) AS sumSell'
        'LIMIT :num',
        {'num': m}
    )
    popularauthor = db.session.execute(
        'SELECT W.firstName, W.lastName'
        'FROM order AS O JOIN book AS B JOIN write AS W'
        'GROUP BY O.amount, B.W.ISBN, W.firstName, W.lastName'
        'ORDER BY SUN(O.amount) AS sumSell'
        'LIMIT :num',
        {'num': m}
    )
    popularpublisher = db.session.execute(
        'SELECT B.publisher'
        'FROM book AS B JOIN order AS O'
        'GROUP BY B.ISBN, O.amount'
        'ORDER BY SUN(O.amount) AS sumSell'
        'LIMIT :num',
        {'num': m}
    )
    return popularbook, popularauthor, popularpublisher

#14
def UserAwards(m):
    trustuser = db.session.execute(
        'SELECT C1.loginName'
        'FROM customer AS C1 JOIN trust AS T1 on C1.loginName = T1.loginName '
        'JOIN customer AS C2 on C2.loginName = T1.declareName'
        'WHERE T1.trustornot=1'
        'GROUP BY C1.loginName, T1.trustornot'
        'ORDER BY COUNT(C2.loginName)-('
            'SELECT COUNT(C4.loginName)'
            'FROM customer AS C3 JOIN trust AS T2 on C3.loginName = T2.loginName '
            'JOIN customer AS C4 on C4.loginName = T2.declareName'
            'WHERE T2.trustornot=0'
            'GROUP BY C3.loginName, T2.trustornot'
        ')'
        'LIMIT :num',
        {'num': m}
    )
    usefuluser = db.session.execute(
        'SELECT C1.loginName'
        'FROM customer AS C1 JOIN comment AS CM on C1.loginName = CM.loginName '
        'JOIN customer AS C2 on C2.loginName = CM.ratingUser'
        'GROUP BY C.loginName, CM.rating'
        'ORDER BY AVERAGE(CM.rating)'
        'LIMIT :num',
        {'num': m}
    )
    return trustuser, usefuluser

#15
def NewAddress(loginName, street, city, state, phone, postalCode):
    db.session.execute(
        'INSERT INTO address(:loginName, :street, :city, :state, :phone, :postalCode)',
        {'loginName': loginName, 'street': street, 'city': city,
         'state': state, 'phone': phone, 'postalCode': postalCode}
    )
    db.session.commit()

#16
def PaymentMethod(loginName, cardNumber, expireDate):
    db.session.execute(
        'INSERT INTO payment(:loginName, :cardNumber, :expireDate)',
        {'loginName': loginName, 'cardNumber': cardNumber,
         'expireDate': expireDate}
    )
    db.session.commit()

#17
def deleteComment(loginName, ISBN):
    db.session.execute(
        'DELETE'
        'FROM comment AS C'
        'WHERE C.loginName = :loginName1 AND C.ISBN = :ISBN1',
        {'loginName1': loginName, 'ISBN1': ISBN}
    )
    db.session.commit()

#18
def deleteAddress(loginName, addID):
    db.session.execute(
        'DELETE'
        'FROM address AS A'
        'WHERE A.loginName = :loginName1 AND A.addID = :addID1',
        {'loginName1': loginName, 'addID1': addID}
    )
    db.session.commit()

#19
def deletePaymentMethod(loginName, cardNumber):
    db.session.execute(
        'DELETE'
        'FROM payment AS P'
        'WHERE P.loginName = :loginName1 AND P.cardNumber = :cardNumber1',
        {'loginName1': loginName, 'cardNumber1': cardNumber}
    )
    db.session.commit()

#20
def CancelOrder(orderNumber):
    db.session.execute(
        'DELETE'
        'FROM Order AS O'
        'WHERE O.orderNumber = oderNumber1',
        {'orderNumber1': orderNumber}
    )
    db.session.commit()