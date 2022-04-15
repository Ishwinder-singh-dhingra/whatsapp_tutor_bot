from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://ishwinder:singh@cluster0.4bdgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["tutor"]
users = db["users"]
profile = db['profile']
search = db['search']

app = Flask(__name__) # creating a variable app which takes modue name as input

@app.route("/", methods =['get','post'])  # route is like which redirects a website to another page , get message is get and read
# post is to send Messages

# now lets define the main reply function
def reply():

    text = request.form.get("Body") # To get the body of text message sent by user
    number = request.form.get("From") # To get the whatsapp number
    number =number.replace("whatsapp:","")
    res = MessagingResponse()
    user = users.find_one({'number':number}) # command to find user
    if bool(user) == False:
        res.message("Hi Welcome to *The Mathly*.\n You can choose from the following options below:"
        "\n\n*Type*\n\n 1️⃣ *Tutor Registration*\n 2️⃣ *Tutor Search*\n 3️⃣ *To Contact Us* ")
        users.insert_one({'number':number,'status':'main','messages':[]})
        #search.insert_one({'number':number,'status':'main','messages':[]})
    elif user['status'] == 'main':
        try:
            option = int(text)
        except:
            res.message("Sorry !!! not able to understand.Please respond with valid option\n You can choose from the following options below:"
            "\n\n*Type*\n\n 1️⃣ *Tutor Registration*\n 2️⃣ *Tutor Search*\n 3️⃣ *To Contact Us* ")
            return str(res)
        if option == 1:
            res.message("You have entered Tutor Registration Mode")
            users.update_one({'number':number},{"$set":{"status":"tutor_register"}})
            res.message("Here we go!!! please visit the link www.themathly.com and fill your details\n .Once you fill up your details it will take another 2-3 working days to verify and regsiter for the same")
        elif option == 2:
            users.update_one({'number':number},{"$set":{"status":"tutor_search"}})
            res.message("*You have entered Tutor search mode*\n \nYou can choose from the following options below:"
            "\n\n*Type*\n\n 1️⃣ *Home Tutor*\n 2️⃣ *Online Class*\n 3️⃣ *Coaching centre*")
        elif option == 3:
            res.message("You can contact us through Phone number or email.\n\n *Phone: +918076114137* \n *Email:contact@themathly.com*")
        else:
            res.message("Please respond with valid option")
            return str(res)
    elif user["status"] =='tutor_search':
        try:
            option = int(text)
        except:
            res.message("Please respond with valid option\n. *To go back to main menu Type* 0️⃣")
            return str(res)
        if option == 0:
            users.update_one({'number':number},{"$set":{"status":"main"}})
            res.message("Hi Welcome back to *The Mathly*.\n You can choose from the following options below:"
            "\n\n*Type*\n\n 1️⃣ *Tutor Registration*\n 2️⃣ *Tutor Search*\n 3️⃣ *To Contact Us* ")
        elif 1<= option <=3:
            tutoring_options =['Home Tutor','Online Class','Coaching Centre']

            selected =tutoring_options[option-1]
            users.update_one({'number':number},{"$set":{"status":"pin_code"}})
            users.update_one({'number':number},{"$set":{"item":selected}})
            res.message("Excellent Choice 😎")
            res.message("Please enter your Pin Code")
        else:
            res.message("Please enter valid response\n\n *You can choose from the following options below:*"
            "\n\n*Type*\n\n 1️⃣ *Home Tutor*\n 2️⃣ *Online Class*\n 3️⃣ *Coaching centre*")
    elif user["status"] == 'pin_code':
        selected = user['item']
        res.message("Thanks for using the mathly for tutoring needs")
        res.message(f" Let me search {selected} for you")
        res.message("here we go *Neha mam* is avaliable for classes today")
        #search.insert_one({'number':number},{'$push':{'messages':{'text':text,'date':datetime.now()}}})
        #search.insert_one({'number':number})
        search.insert_one({'number':number,'item':selected,'pin_code':text,'booking_time':datetime.now()})
        users.update_one({'number':number},{"$set":{"status":"searched"}})
    elif user['status'] == 'searched':
        res.message("Any more your are looking for \n\n *You can choose from the following options below:*"
        "\n\n*Type*\n\n 1️⃣ *Home Tutor*\n 2️⃣ *Online Class*\n 3️⃣ *Coaching centre*")
        users.update_one({'number':number},{"$set":{"status":"main"}})






    users.update_one({"number":number},{'$push':{"messages":{"text":text,"date":datetime.now()}}})
    return str(res)

if __name__ == "__main__":
    app.run()
