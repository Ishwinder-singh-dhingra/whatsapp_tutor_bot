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
        "\n\n*Type*\n\n 1️⃣ *Tutor Search*\n 2️⃣ *Doubts*\n 3️⃣ *Help* ")
        users.insert_one({'number':number,'status':'main','messages':[]})
    elif user['status'] == 'main':
        try:
            option = int(text)
        except:
            res.message("Hi Welcome back to *The Mathly*\n\n You can choose from the following options below:"
            "\n\n*Type*\n\n 1️⃣ *Tutor Search*\n 2️⃣ *Doubts*\n 3️⃣ *Help* ")
            return str(res)
        if option == 1:
            users.update_one({'number':number},{"$set":{"status":"tutor_search"}})
            res.message("*You have entered Tutor search mode*\n \nYou can choose from the following options below:"
            "\n\n*Type*\n\n 1️⃣ *Home Tutor*\n 2️⃣ *Online Class*\n 3️⃣ *Coaching Centre*\n 0️⃣ *Go Back to Main Menu*")

        elif option == 2:
            res.message("*Thanks for asking doubts this feature will be live soon*\n\n. To go Back to Main Menu Type 0️⃣")

        elif option == 3:
            res.message("You can contact us through Phone number or email.\n\n *Phone: +918076114137* \n *Email:contact@themathly.com*\n\n.To go Back to Main Menu Type 0️⃣")

        else:
            res.message("*Hi Welcome Back to The Mathly*\n\n You can choose from the following options below:"
            "\n\n*Type*\n\n 1️⃣ *Tutor Search*\n 2️⃣ *Doubts*\n 3️⃣ *Help*")
            return str(res)
    elif user['status'] == 'tutor_search':
        try:
            option = int(text)
        except:
            res.message("Please respond with valid option\n. *To go back to main menu Type* 0️⃣")
            return str(res)
        if option == 0:
            users.update_one({'number':number},{"$set":{"status":"main"}})
            res.message("Hi Welcome back to *The Mathly*.\n You can choose from the following options below:"
            "\n\n*Type*\n\n 1️⃣ *Tutor Search*\n 2️⃣ *Doubts*\n 3️⃣ *Help* ")
        elif 1<=option<=3:
            tutoring_options = ['Home Tutor','Online Class','Coaching Centre']

            selected = tutoring_options[option-1]
            res.message("Excellent Choice 😎")
            #users.update_one({'number':number},{"$set":{"status":"Home Tutor"},{"item":selected}})
            users.update_one({'number':number},{"$set":{"status":"Home Tutor"}})
            users.update_one({'number':number},{"$set":{"item":selected}})
            res.message("*Please enter the Subject of Your Choice*\n 1️⃣ *Maths*\n 2️⃣ *Science*\n 3️⃣ *English*")
    elif user['status'] == 'Home Tutor':
        try:
            option = int(text)
        except:
            res.message("Please select from the following options:\n\n.1️⃣ *Maths*\n 2️⃣ *Science*\n 3️⃣ *English*")
            return str(res)

        if option == 1:
            users.update_one({'number':number},{"$set":{"Subject":"Maths"}})
            res.message("Great You have selected *Maths* as subject")
            users.update_one({'number':number},{"$set":{"status":"Grade"}})
        elif option == 2:
            users.update_one({'number':number},{"$set":{"Subject":"Science"}})
            res.message("Great You have selected *Science* as subject")
            users.update_one({'number':number},{"$set":{"status":"Grade"}})
        elif option == 3:
            users.update_one({'number':number},{"$set":{"Subject":"English"}})
            res.message("Great You have selected *English* as subject")
            users.update_one({'number':number},{"$set":{"status":"Grade"}})

        else:
            res.message("Please enter valid response")
            return str(res)
        res.message("*Please Select the Grade level:\n\n 1️⃣ *Class 1st to 5th std*\n 2️⃣ *Class 6th to 8th std*\n 3️⃣ *Class 9th to 10th std*")
    elif user['status'] == 'Grade':
        try:
            option = int(text)
        except:
            res.message("Sorry not able to understand  \n\n1️⃣ *Class 1st to 5th std*\n 2️⃣ *Class 6th to 8th std*\n 3️⃣ *Class 9th to 10th std*")
            return str(res)
        if option == 1:
            users.update_one({'number':number},{"$set":{"Grade":"1st to 5th"}})
            res.message("Great You want tutor for *Class 1st to 5th std*")
            users.update_one({'number':number},{"$set":{"status":"pin code"}})
        elif option == 2:
            users.update_one({'number':number},{"$set":{"Grade":"6th to 8th"}})
            res.message("Great You want tutor for *Class 1st to 5th std*")
            users.update_one({'number':number},{"$set":{"status":"pin code"}})
        elif option == 3:
            users.update_one({'number':number},{"$set":{"Grade":"9th to 10th"}})
            res.message("Great You want tutor for *Class 1st to 5th std*")
            users.update_one({'number':number},{"$set":{"status":"pin code"}})
        else:
            res.message("Please enter valid response")
            return str(res)
        res.message("*Please enter the area pin code:*")
    elif user['status'] == 'pin code':


        try:
            pin_code = int(text)
        except:
            res.message("Please enter the valid area pin code")
            return str(res)
        Subject = user['Subject']
        Grade = user['Grade']
        users.update_one({'number':number},{"$set":{"pin_code":pin_code}})
        res.message(f"Here we go Neha Mam is great *{Subject}* teacher for *{Grade}* in your area \n\n. She has taught students from DPS Delhi and various other prestigious schools in India , she has also worked with many Edtech companies like Byjus, Meritnation and taken classes for students accross the Globe\n\n. To connect with her you can call or send whatsapp message: +919958508031")
        users.update_one({'number':number},{"$set":{"status":"main"}})
        res.message("*Thanks for Using The Mathly as your Tutoring Service See You soon*\n. Happy Learning")



    users.update_one({"number":number},{'$push':{"messages":{"text":text,"date":datetime.now()}}})
    return str(res)


if __name__ == '__main__':
    app.run()
