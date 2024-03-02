import csv
import mysql.connector
from pymongo import MongoClient
from datetime import datetime
from db_config import database_host,database_user, database_password, database_name, mongodb_connection, mongo_name

client = MongoClient (mongodb_connection)

def create_database():
    connection = mysql.connector.connect(
        host=database_host,
        user=database_user,
        password=database_password,
    )
    cursor = connection.cursor()
    create_table_query ="""
    CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    address TEXT,
    telefon_number INT
    );
    CREATE TABLE IF NOT EXISTS login_history (
    username VARCHAR(255) NOT NULL,
    time DATETIME NOT NULL
    );
    """

    try:    
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.execute(f"USE {database_name}")
        cursor.execute(create_table_query, multi=True)
    except mysql.connector.Error as e:
        print("Error:", e)


def create_user():
    print("Welcome to User creation.")
    while True:
        create_username = input("Please input username: ")
        while create_username.strip() == "":
            print("Username cant be empty")
            create_username = input("Please input username: ")   
        cursor.execute("SELECT * FROM users WHERE username=%s", (create_username,))
        existing = cursor.fetchone()
        if existing is not None:
            print("Error, Username already in use, please try again")
        else:
            break
    
    create_password = input("Enter password: ")
    while create_password.strip() == "":
        print("Password cant be empty")
        create_password = input("Enter password: ")
    create_first_name = input("Enter firstname: ")
    while create_first_name.strip() == "":
        print("First name cant be empty")
        create_first_name = input("Enter firstname: ") 
    create_last_name = input("Enter lastname: ")
    while create_last_name.strip() == "":
        print("Last name cant be empty")
        create_last_name = input("Enter lastname: ")
    create_address = input("Enter address (Optional): ")
    create_telefon = input("Input telefon number (Optional): ")
    if create_telefon.isdigit():
        create_telefon = int(create_telefon)
    else:
        create_telefon = None

    cursor.execute("""INSERT INTO users(
                   username, password, first_name, last_name, address, telefon_number)
                   VALUES(%s, %s, %s, %s, %s, %s)""",
                   (create_username, create_password, create_first_name, create_last_name, create_address, create_telefon)
               )
    connection.commit()
    print("User created successfully")

def login():
    login_success = False
    login_username = None
    print ("Please enter username")
    login_username = input("Username: ")
    
    cursor.execute(f"SELECT * FROM users WHERE username=%s",(login_username,))
    fetch_user = cursor.fetchone()
    if fetch_user:
        fetch_username = fetch_user[0]
        if fetch_username == login_username:
            login_password = input("Password: ")
            fetch_password = fetch_user[1]
            if fetch_password == login_password:
                print("login Succesful")
                login_success = True
                
            else:
                print("Password is incorrect.")
        else:
            print ("User not found")
    else:
        print("User not found")
    return login_success, login_username

def log_login(username):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("user_login.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, timestamp])

def logged_in_user_action(username):
    print("1.Change firstname")
    print("2.Change lastname")
    print("3.Change password")
    print("4.Change address")
    print("5.Change telefonnumber")
    print("9.Exit update function")
    user_action = input("")
    if user_action != "9":
        print("What do you want to change it to?")
        new_value = input("")
    update_query = None
    if user_action == "1":
        update_query = "UPDATE users SET firstname =%s WHERE username = %s"
    elif user_action == "2":
        update_query = "UPDATE users SET lastname =%s WHERE username = %s"
    elif user_action == "3":
        update_query = "UPDATE users SET password =%s WHERE username = %s"
    elif user_action == "4":
        update_query = "UPDATE users SET address =%s WHERE username = %s"
    elif user_action == "5":
        update_query = "UPDATE users SET telefon_number =%s WHERE username = %s"
        if new_value.isdigit():
            new_value = int(new_value)
        else:
            print("Error: Can only include numbers")
            return
    elif user_action == "9":
        return False
        
    else:
        print("Unrecognized input")

    if update_query:
        cursor.execute(update_query,(new_value,username))
        print("Information updated")
    return True

def post_to_wall(username,mongo_name):
    db = client[mongo_name]
    collection = db.wall
    post = None
    print("1.Post message")
    print("2.Post picture")
    print("3.Post Video")
    print("9.Exit posting")
    user_action = input("")
    if user_action == "1":
        post_title = input("Title: ")
        while post_title.strip() == "":
            print("Title can't be empty")
            post_title = input("Title: ")
        post_message = input("Message: ")
        while post_message.strip() == "":
            print("Message can't be empty")
            post_message = input("Message: ")
        time = datetime.now()
        post = {"title":post_title,
                "message":post_message,
                "poster":username,
                "time":time}

    
    elif user_action == "2":
        post_title = input("Title: ")
        while post_title.strip() == "":
            print("Title can't be empty")
            post_title = input("Title: ")
        post_picture = input("Insert picture(Simulated): ")
        while post_picture.strip() == "":
            print("Picture can't be empty")
            post_picture = input("picture: ")
        time = datetime.now()
        post = {"title":post_title,
                "picture":post_picture,
                "poster":username,
                "time":time}
    
    elif user_action == "3":
        post_title = input("Title: ")
        while post_title.strip() == "":
            print("Title can't be empty")
            post_title = input("Title: ")
        post_video = input("Insert video(Simulated): ")
        while post_video.strip() == "":
            print("Video can't be empty")
            post_video = input("Video: ")
        time = datetime.now()
        post = {"title":post_title,
                "video":post_video,
                "poster":username,
                "time":time}
    
    elif user_action == "9":
        return False
    else:
        print("Unrecognized input")
    
    if post:
        collection.insert_one(post)
        print("Post on the wall")

    return True
        
def read_from_wall():
    db = client[mongo_name]
    collection = db.wall
    print("1.Search for title")
    print("2.Search for user")
    print("9.Exit reading function")
    user_action = input("")
    if user_action == "1":
        search_title = input("Title to search for: ")
        search_criteria = {"title":search_title}
        search_result = collection.find(search_criteria)
        for document in search_result:
            print("Post made by:", document["poster"])
            if "message" in document:
                print("Message: ", document["message"])
            elif "picture" in document:
                print("Picture:", document["picture"])
            elif "video" in document:
                print("Video:", document["video"])
            else:
                print("Unknown Post type")
        if search_result == None:
            print ("No posts with that title found")

    elif user_action == "2":
        post_count = 0
        result_titles = []
        search_username = input("Username to search for: ")
        search_criteria = {"poster":search_username}
        search_result = collection.find(search_criteria)
        for document in search_result:
            result_titles.append(document["title"])
            post_count +=1
        if result_titles:
            print(f"User {search_username} has created posts:{post_count}")
            print("Titles of posts:")
            for title in result_titles:
                print(title)
        else:
            print(f"No titles found under user {search_username}")    
    elif user_action == "9":
        return False
    else:
        print("Unrecognized input")
    return True




    
if __name__ == "__main__":
    create_database()
    connection = mysql.connector.connect(
        host=database_host,
        user=database_user,
        password=database_password,
        database=database_name
    )
    cursor = connection.cursor()

    while True:
        print("1.Create user")
        print("2.Login")
        print("9.Quit Program")
        user_action = input ("")
        if user_action == "1":
            create_user()
        elif user_action == "2":
            login_success, login_username = login()
            if login_success:
                log_login(login_username)
                while True:
                    print("1.Post Message to the wall")
                    print("2.Read from the wall")
                    print("3.Update user information")
                    print("9.Logg out")
                    
                    user_action = input("")
                    if user_action == "1":
                        while True:
                            if not post_to_wall(login_username,mongo_name):
                                break
                    elif user_action == "2":
                        while True:
                            if not read_from_wall():
                                break
                    elif user_action == "3":
                        while True:
                            if not logged_in_user_action(login_username):
                                break
                    elif user_action == "9":
                        break
                    else:
                        print("Unrecognized input")
            else:
                print("Login unsuccessful, try again.")
        elif user_action == "9":
            print("Exiting program")
            break
        else:
            print("Unrecognized input")


    #End of main
    connection.close()
    client.close()