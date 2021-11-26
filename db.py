import mysql.connector

def connection_BDD():
    mydb = mysql.connector.connect(
        host="idelont.fr",
        port="59435",
        user="rvoiture",
        password="!NtM$nQ52zT3",
        database="projet_irve",
        auth_plugin="mysql_native_password"
    )
    return mydb

def get_voiture():
    mydb = connection_BDD()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * From Voiture;")
    myresult = mycursor.fetchall()
    
    list_car = []
    for x in myresult:
        list_car.append(x)
    return list_car

def get_autonomie(id):
    mydb = connection_BDD()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT autonomie From Voiture where id = "+str(id)+";")
    myresult = mycursor.fetchone()
    return(myresult[0])

def get_tempsRecharge(id):
    mydb = connection_BDD()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT loadTime From Voiture where id = "+str(id)+";")
    myresult = mycursor.fetchone()
    return(myresult[0])