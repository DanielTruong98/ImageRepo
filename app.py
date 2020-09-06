import database

def optionInput(personalInfo):
    switch = {
        0 : database.insertImage,
        1 : database.editImage,
        2 : database.deleteImage,
        3 : database.listImages,
        4 : database.buyImage,
        5 : exit
    }
    while(True):
        print("0. Add image")
        print("1. Edit image")
        print("2. Delete image")
        print("3. List images")
        print("4. Buy image")
        print("5. Exit program")
        while(True):
            try:
                selection = int(input("Selection: "))
                if (selection < 0 or selection > len(switch)):
                    raise ValueError
                else:
                    break
            except:
                print("Invalid input")
                print("0. Add image")
                print("1. Edit image")
                print("2. Delete image")
                print("3. List images")
                print("4. Buy image")
                print("5. Exit program")
        
        switch[selection](personalInfo)

if __name__ =="__main__":
    database.initDB()
    personalInfo = {
        "balance" : 1000.00
    }
    optionInput(personalInfo)
