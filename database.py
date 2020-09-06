import sqlite3
import os
import subprocess
from config import readConfig

def dbConnection():
    connection = sqlite3.connect('imageRepo.db')
    return connection, connection.cursor()


def initDB():
    connection, cursor = dbConnection()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS images (
         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         name TEXT,
         fileType TEXT,
         amount INTEGER,
         price FLOAT,
         discount FLOAT,
         data BLOB)"""
    )
    connection.commit()
    connection.close()

def updateDB(obj):
    connection, cursor = dbConnection()
    query = """UPDATE images SET name = ?, amount = ?, price = ?, discount = ? WHERE ID = ?"""
    cursor.execute(query, (obj[1], obj[2], obj[3], obj[4], obj[0]))
    connection.commit()
    connection.close()

def insertImage(personalInfo):
    connection, cursor = dbConnection()
    file = input("Input the name of the file: ")
    amount = input("Input the amount in inventory: ")
    price = input("Input the price: ")
    discount = input("Input the discount: ")
    name, extension = os.path.splitext(file)
    extension = extension.replace('.', '')
    print(name, extension)
    with open(file, 'rb') as file:
        try:
            data = file.read()
        except FileNotFoundError:
            print("File not found.")
            file = input("Input the name of the file: ")
    query = """INSERT INTO images (name, fileType, amount, price, discount, data) VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (name, extension, amount, price, discount, data))
    connection.commit()
    connection.close()


def editName(target):
    newName = input("Enter new name: ")
    target[1] = newName

def editInventory(target):
    newInventory = input("Enter new inventory: ")
    target[2] = int(newInventory)

def editPrice(target):
    newPrice = input("Enter new price: ")
    target[3] = float(newPrice)

def editDiscount(target):
    newDiscount = float(input("Enter new discount: "))
    newDiscount /= 100
    target[4] = float(newDiscount)


def editOptions(target):
    options = {
        0 : editName,
        1 : editInventory,
        2 : editPrice,
        3 : editDiscount
    }
    while(True):
        print("0. Edit name")
        print("1. Edit inventory")
        print("2. Edit price")
        print("3. Edit discount")
        print("4. Return")
        while(True):
            try:
                selection = int(input("Selection: "))
                if (selection < 0 or selection > 4):
                    raise ValueError
                if (selection == 4):
                    updateDB(target)
                    return 0
                    break
                else:
                    options[selection](target)
                    break
            except ValueError:
                print("Invalid input: {}".format(ValueError))
                print("0. Edit name")
                print("1. Edit inventory")
                print("2. Edit price")
                print("3. Edit discount")
                print("4. Return")

def editImage(personalInfo):
    connection, cursor = dbConnection()
    name = input("Enter the name of the file: ")
    query = """SELECT * FROM images WHERE name = ?"""
    cursor.execute(query, (name,))
    info = cursor.fetchall()
    # ID, name, inventory, price, discount
    editList = [info[0][0], info[0][1], info[0][3], info[0][4], info[0][5]]
    editOptions(editList)
    connection.close()


def deleteImage(personalInfo):
    connection, cursor = dbConnection()
    name = input("Enter the name of the file: ")
    query = """DELETE FROM images WHERE name = ?"""
    cursor.execute(query, (name,))
    connection.commit()
    connection.close()


def listImages(personalInfo):
    connection, cursor = dbConnection()
    query = """SELECT * FROM images"""
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        print("Image Name: {}, Amount: {}, Price: {}, Discount: {}".format(result[i][1], result[i][3], result[i][4], result[i][5]))
    connection.close()


def buyImage(personalInfo):
    connection, cursor = dbConnection()
    name = input("Enter the name of the image: ")
    query = """SELECT * FROM images WHERE name = ?"""
    updateQuery = """UPDATE images SET amount = ? WHERE name = ?"""
    cursor.execute(query, (name,))
    obj = cursor.fetchall()
    amount = obj[0][3]
    price = obj[0][4]
    discount = obj[0][5]
    if (amount > 0):
        if (personalInfo["balance"] > price):
            total = price - (price * discount)
            print("Image: {} purchased for {}".format(name, total))
            if (discount > 0):
                print("You saved {}".format(price * discount))
            personalInfo["balance"] -= total
            amount -= 1
            cursor.execute(updateQuery, (amount, name,))
            connection.commit()
        else:
            print("Current balance insufficient")
    else:
        print("No stock left")


