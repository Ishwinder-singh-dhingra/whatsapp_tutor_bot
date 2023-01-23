from flask import Flask,request, redirect,url_for,render_template
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://ishwinder:singh@cluster0.4bdgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["tutor"]
users = db["users"]
profile = db["profile"]
search = db["search"]

app = Flask(__name__) # creating a variable app which takes modue name as input

@app.route("/", methods =['get','post'])  # route is like which redirects a website to another page , get message is get and read
# post is to send Messages

# now lets define the main reply function

def reply():
    text = request.form.get("Body") # To get the body of text message sent by user
    #print(text)
    number = request.form.get("From") # To get the whatsapp number
    #print(number)
    number =number.replace("whatsapp:","")
    res = MessagingResponse()
    user = users.find_one({'number':number}) # command to find user
    tutor = profile.find_one({'number':number})

    if bool(user) == False and bool(tutor) == False:
        try:
            type = int(text)
        except:
            res.message("Hi 🙋‍♀️ Welcome to *The Mathly* 🕺🙏.\n You can choose from the following options below:"
            "\n\n*Type*\n\n 1️⃣ *Are you Looking For Tutor ??*\n 2️⃣ *You Want to Become Tutor ??*")
            return str(res)

        if type == 1:
            users.insert_one({'number':number,'status':'main','messages':[]})
            res.message("Hi 🙋‍♀️ welcome to The Mathly* 🕺🙏\n\n You can choose from the following options below: 👍"
            "\n\n*Type*\n\n 1️⃣ *Tutor Search*\n 2️⃣ *Doubts*\n 3️⃣ *Help* ")
        elif type == 2:
            profile.insert_one({'number':number,'status':'tutor_main','messages':[]})
            res.message("Hi 🙋‍♀️ Welcome to *The Mathly* 🕺🙏.\n For Tutor Registration please enter the following details as Listed"
            "\n\n*Information Required*\n\n ✅ *Name*\n ✅ *Email Id*\n ✅ *Qualification and Work experience*\n ✅ *Area pin Code*\n ✅ *Subject*\n ✅ *Grade*\n\n 📔*So Lets Start the Process*\n\n ✔*Please Enter Your Full Name*")



    elif bool(user)==True:
        if user['status'] == 'main':
            try:
                option = int(text)
            except:
                res.message("Hi Welcome back to *The Mathly* 🕺🙏\n\n ✔ You can choose from the following options below:"
                "\n\n*Type*\n\n 1️⃣ *Tutor Search*\n 2️⃣ *Doubts*\n 3️⃣ *Help* ")
                return str(res)
            if option == 1:
                users.update_one({'number':number},{"$set":{"status":"tutor_search"}})
                res.message("*Awesome Let's Search the Tutor 😎😎*\n \nYou can choose from the following options below:"
                "\n\n*Type*\n\n 1️⃣ *Home Tutor*\n 2️⃣ *Online Class*\n 3️⃣ *Coaching Centre*\n 0️⃣ *Go Back to Main Menu*")

            elif option == 2:
                res.message("*Thanks 🙏🙏🙏 for asking doubts this feature will be live soon* \n\n. ✔To go Back to Main Menu Type 0️⃣")

            elif option == 3:
                res.message("You can contact us through Phone number or email.\n\n ✅ *Phone: +918076114137* \n ✅ *Email:contact@themathly.com*\n\n.✔To go Back to Main Menu Type 0️⃣")
            else:
                res.message("Hi Welcome back to *The Mathly* 🕺🙏\n\n ✔ You can choose from the following options below:"
                "\n\n*Type*\n\n 1️⃣ *Tutor Search*\n 2️⃣ *Doubts*\n 3️⃣ *Help* ")
                return str(res)
        elif user['status'] == 'tutor_search':
             try:
                 option = int(text)
             except:
                 res.message("Please respond 🤷‍♀️ with valid option\n\n. ✔*To go back to main menu Type* 0️⃣")
                 return str(res)
             if option == 0:
                 users.update_one({'number':number},{"$set":{"status":"main"}})
                 res.message("Hi Welcome back to *The Mathly* 🕺🙏\n\n ✔ You can choose from the following options below:"
                 "\n\n*Type*\n\n 1️⃣ *Tutor Search*\n 2️⃣ *Doubts*\n 3️⃣ *Help* ")
                 return str(res)
             elif 1<=option<=3:
                 tutoring_options = ['Home Tutor','Online Class','Coaching Centre']
                 selected = tutoring_options[option-1]
                 users.update_one({'number':number},{"$set":{"status":"Home Tutor"}})
                 users.update_one({'number':number},{"$set":{"item":selected}})
                 res.message("*Excellent Choice 😎*\n\n*Please enter the Subject of Your Choice*\n 1️⃣ *Maths*\n 2️⃣ *Science*\n 3️⃣ *English*")
        elif user['status'] == 'Home Tutor':
             try:
                 option = int(text)
             except:
                 res.message("Please select the valid 🤷 option:\n\n.1️⃣ *Maths*\n 2️⃣ *Science*\n 3️⃣ *English*")
                 return str(res)

             if option == 1:
                 users.update_one({'number':number},{"$set":{"Subject":"Maths"}})
                 #res.message("Great You have selected *Maths* as subject")
                 users.update_one({'number':number},{"$set":{"status":"Grade"}})
             elif option == 2:
                 users.update_one({'number':number},{"$set":{"Subject":"Science"}})
                 #res.message("Great You have selected *Science* as subject")
                 users.update_one({'number':number},{"$set":{"status":"Grade"}})
             elif option == 3:
                 users.update_one({'number':number},{"$set":{"Subject":"English"}})
                 #res.message("Great You have selected *English* as subject")
                 users.update_one({'number':number},{"$set":{"status":"Grade"}})

             else:
                 res.message("Please select the valid 🤷 option:\n\n.1️⃣ *Maths*\n 2️⃣ *Science*\n 3️⃣ *English*")
                 return str(res)
             res.message("*Awesome Choice* 😎😎 \n\n ✔✔✔Please Select the Grade level:\n\n 1️⃣ *Class 1st to 5th std*\n 2️⃣ *Class 6th to 8th std*\n 3️⃣ *Class 9th to 10th std*")
        elif user['status'] == 'Grade':
             try:
                 option = int(text)
             except:
                 res.message("Sorry not able to understand 🙂☹  \n\n1️⃣ *Class 1st to 5th std*\n 2️⃣ *Class 6th to 8th std*\n 3️⃣ *Class 9th to 10th std*")
                 return str(res)
             if option == 1:
                 users.update_one({'number':number},{"$set":{"Grade":"1st to 5th"}})
                 #res.message("Great You want tutor for *Class 1st to 5th std*")
                 users.update_one({'number':number},{"$set":{"status":"pin code"}})
             elif option == 2:
                 users.update_one({'number':number},{"$set":{"Grade":"6th to 8th"}})
                 #res.message("Great You want tutor for *Class 6th to 8th std*")
                 users.update_one({'number':number},{"$set":{"status":"pin code"}})
             elif option == 3:
                 users.update_one({'number':number},{"$set":{"Grade":"9th to 10th"}})
                 #res.message("Great You want tutor for *Class 9th to 10th std*")
                 users.update_one({'number':number},{"$set":{"status":"pin code"}})
             else:
                 res.message("Sorry not able to understand 🙂☹  \n\n1️⃣ *Class 1st to 5th std*\n 2️⃣ *Class 6th to 8th std*\n 3️⃣ *Class 9th to 10th std*")
                 return str(res)
             res.message("*Bingo 😎😎*\n\n*Please enter the area pin code 🏡:*")
        elif user['status'] == 'pin code':
             try:
                 code = int(text)
             except:
                 res.message("*Please enter the valid 🤷‍♀️ area pin code 🏡:*")
                 return str(res)
             users.update_one({'number':number},{"$set":{"pin_code":code}})
             Subject = user['Subject']
             Grade = user['Grade']
             item = user['item']
             selected_profile = ''
             lst = []
             i = 0


             for data in profile.find({"$and":[{'Subject':Subject,'Grade':Grade,'item':item,'pin_code':code}]}):
                 selected_profile = data
                 lst.append(selected_profile)
                 print(lst)
             #res.message(f"Here we go *{lst[i]['name']}* is great *{Subject}* teacher for *{Grade}* in your area \n\n. *{lst[i]['prof']}*\n\n. To connect with the tutor you can call:{lst[i]['number']}\n\n To connect on Whatsapp click on the link\n\n:{lst[i]['chat']}\n\n ✅*To see next profile type* 1️⃣")



             #users.update_one({'number':number},{"$set":{"status":"main"}})
             if selected_profile == '':
                 res.message("*Sorry 🙁☹☹ Right Now we dont have tutor in your area🏡* , will update as soon as possible*\n\n *Thanks 🙏🙏🙏 for Using The Mathly as your Tutoring Service See You soon*\n. Happy Learning 👍😊 \n\n ✅To start Chat again send *'Hi'*")
                 users.update_one({'number':number},{"$set":{"status":"main"}})

    elif bool(tutor) ==True:
        if tutor['status'] == 'tutor_main':
             try:
                 name_tutor = str(text)
             except:
                 res.message("*Please 🙏🙏 enter valid 🤷‍♂️ Name:*")
                 return str(res)
             profile.update_one({'number':number},{"$set":{'name':name_tutor}})
             profile.update_one({'number':number},{"$set":{'status':'name_done'}})
             res.message("*Excellent!!!* 😎👍 \n\n ✔*Please enter your email ID*")
        elif tutor['status'] == 'name_done':
            try:
                email_tutor = str(text)
            except:
                res.message("Sorry!!! ☹🙁 Please enter🤷‍♀️ Valid Email ID")
                return str(text)
            profile.update_one({'number':number},{"$set":{'email':email_tutor}})
            profile.update_one({'number':number},{"$set":{'status':'email_done'}})
            res.message("*Awesome Job !!!* 😎👍 \n\n ✔ *Please enter your Qualification 🤵 and work experience* 🏨")
        elif tutor['status'] == 'email_done':
            try:
                qual_tutor = str(text)
            except:
                res.message("Sorry!!! 🙁☹ \n\n Please enter valid 🤷‍♂️ information\n\n ✔ *Please enter your Qualification 🤵 and work experience* 🏨")
                return str(text)
            profile.update_one({'number':number},{"$set":{'prof':qual_tutor}})
            profile.update_one({'number':number},{"$set":{'status':'qual_done'}})
            res.message("Excellent !!! 😎😊🙏 Please enter your area 🏡 pin code For Tutoring:*")
        elif tutor['status'] == 'qual_done':
            try:
                code_tutor = int(text)
            except:
                res.message("Sorry!!! 🙁☹ \n\n Please enter valid 🤷‍♂️ information\n\n. 😎😊🙏 Please enter your area 🏡 pin code For Tutoring:*" )
                return str(res)
            profile.update_one({'number':number},{"$set":{'pin_code':code_tutor}})
            profile.update_one({'number':number},{"$set":{'status':'code_done'}})
            res.message("*Excellent Choice 😎*\n\n* ✔✔✔ Please enter the Subject of Your Choice*\n 1️⃣ *Maths*\n 2️⃣ *Science*\n 3️⃣ *English*")
        elif tutor['status'] == 'code_done':
            try:
                sub_tutor = int(text)
            except:
                res.message("Sorry!!! 🙁☹ \n\n Please enter valid 🤷‍♂️ information\n\n. 😎😊🙏 ✔✔✔ *Please enter the Subject of Your Choice*\n 1️⃣ *Maths*\n 2️⃣ *Science*\n 3️⃣ *English*" )
                return str(res)
            if sub_tutor == 1:
                profile.update_one({'number':number},{"$set":{"Subject":"Maths"}})
                #res.message("Great You have selected *Maths* as subject")
                profile.update_one({'number':number},{"$set":{"status":"sub_done"}})
            elif sub_tutor == 2:
                profile.update_one({'number':number},{"$set":{"Subject":"Science"}})
                #res.message("Great You have selected *Maths* as subject")
                profile.update_one({'number':number},{"$set":{"status":"sub_done"}})
            elif sub_tutor == 3:
                profile.update_one({'number':number},{"$set":{"Subject":"English"}})
                #res.message("Great You have selected *Maths* as subject")
                profile.update_one({'number':number},{"$set":{"status":"sub_done"}})
            res.message("*Awesome Choice* 😎😎 \n\n ✔✔✔Please Select the Grade level:\n\n 1️⃣ *Class 1st to 5th std*\n 2️⃣ *Class 6th to 8th std*\n 3️⃣ *Class 9th to 10th std*")
        elif tutor['status'] == 'sub_done':
            try:
                grade_tutor = int(text)
            except:
                res.message("*Sorry!!! 🙁☹ \n\n Please enter valid 🤷‍♂️ information*\n\n. 😎😊🙏 ✔✔✔ *Please Select the Grade level:\n\n 1️⃣ *Class 1st to 5th std*\n 2️⃣ *Class 6th to 8th std*\n 3️⃣ *Class 9th to 10th std*" )
                return str(text)
            if grade_tutor == 1:
                profile.update_one({'number':number},{"$set":{"Grade":"1st to 5th"}})
                #res.message("Great You want Classes for *Class 1st to 5th std*")
                profile.update_one({'number':number},{"$set":{"status":"grade_done"}})
            elif grade_tutor == 2:
                profile.update_one({'number':number},{"$set":{"Grade":"6th to 8th"}})
                #res.message("Great You want Classes for *Class 6th to 8th*")
                profile.update_one({'number':number},{"$set":{"status":"grade_done"}})
            elif grade_tutor == 3:
                profile.update_one({'number':number},{"$set":{"Grade":"9th to 10th"}})
                #res.message("Great You want tutor for *Class 9th to 10th*")
                profile.update_one({'number':number},{"$set":{"status":"grade_done"}})
            res.message("*Excellent !!!* 😎🙏👍\n\n *Please create whatsapp link using the following link and then enter the same \n\n https://create.wa.link/")

        elif tutor['status'] == 'grade_done':
            try:
                link_tutor = str(text)
            except:
                res.message("*Sorry!!! 🙁☹ \n\n Please enter valid 🤷‍♂️ information*\n\n. 😎😊🙏 ✔✔✔ *Please create whatsapp link using the following link and then enter the same \n\n https://create.wa.link/*" )
                return str(res)
            profile.update_one({'number':number},{"$set":{'chat':link_tutor}})
            profile.update_one({'number':number},{"$set":{'status':'link_done'}})
            res.message("*Excellent !!!* 😎😊✔ \n\n ✔✔✔*Please choose the mode of class from the following options below:*"
            "\n\n*Type*\n\n 1️⃣ *Home Tutor*\n 2️⃣ *Online Class*\n 3️⃣ *Coaching Centre*")
        elif tutor['status'] == 'link_done':
            try:
                mode_tutor = int(text)
            except:
                res.message("*Sorry!!! 🙁☹ \n\n Please enter valid 🤷‍♂️ information*\n\n. 😎😊🙏 ✔✔✔*Please choose the mode of class from the following options below:*"
                "\n\n*Type*\n\n 1️⃣ *Home Tutor*\n 2️⃣ *Online Class*\n 3️⃣ *Coaching Centre*" )
                return str(res)
            if 1<=mode_tutor<=3:
                tutoring_options = ['Home Tutor','Online Class','Coaching Centre']
                selected = tutoring_options[mode_tutor-1]
                profile.update_one({'number':number},{"$set":{"status":"final_check"}})
                profile.update_one({'number':number},{"$set":{"item":selected}})
                #res.message(f"Here we go *{profile['name']}* is great *{profile['Subject']}* teacher for *{profile['Grade']}* in your area \n\n. *{profile['prof']}*\n\n. To connect with the tutor you can call:{profile['number']}\n\n To connect on Whatsapp click on the link\n\n:{profile['chat']}\n\n*To register the profile Type 1️⃣*")
                res.message("*Do you want to register the given information* ❔❔❔\n\n ✅ *To register the profile type 1️⃣\n ✅ Else type 0️⃣ to start again* ")
        elif tutor['status'] == 'final_check':
            try:
                final = int(text)
            except:
                res.message("Please enter valid response")
            if final == 1:
                profile.update_one({'number':number},{"$set":{"status":"reg_success"}})
                res.message("Congratuations!!! 💃💃🙏 you have successfully regsitered your profile \n\n ✔✔✔ Anytime you need to update your profile say *'Hi'* from same registered number")
            if final == 0:
                profile.update_one({'number':number},{"$set":{"status":"tutor_main"}})
                res.message("Its okay !!! 😊👍\n\n ✔ *To start again follow the process* \n\n *Information Required*\n\n ✅ *Name*\n ✅ *Email Id*\n ✅ *Qualification and Work experience*\n ✅ *Area pin Code*\n ✅ *Subject*\n ✅ *Grade*\n\n 📔*So Lets Start the Process*\n\n ✔*Please Enter Your Full Name*")
        elif tutor['status'] == 'reg_success':

            try:
                update = int(text)
            except:
                res.message("You are already registered Tutor 😎🤵\n\n ✔ To Update your profile type 0️⃣ \n ✔ Press 1️⃣ to exit")
                return str(res)
            if update == 0:
                res.message("Its okay !!! 😊👍\n\n ✔ *To start again follow the process* \n\n *Information Required*\n\n ✅ *Name*\n ✅ *Email Id*\n ✅ *Qualification and Work experience*\n ✅ *Area pin Code*\n ✅ *Subject*\n ✅ *Grade*\n\n 📔*So Lets Start the Process*\n\n ✔*Please Enter Your Full Name*")
                profile.update_one({'number':number},{"$set":{"status":"tutor_main"}})
            elif update == 1:
                res.message("Thanks 🙏😎 for using The Mathly as your tutoring service")
                profile.update_one({'number':number},{"$set":{"status":"tutor_fresh"}})
        elif tutor['status'] == 'tutor_fresh':
            try:
                fresh = int(text)
            except:
                res.message("Hi welcome to The Mathly 😎🤵 Tutor \n\n ✔✔ To update your Profile Type 1️⃣\n ✔✔ To Exit Type 0️⃣")
                return str(res)
            if fresh == 1:
                res.message("Hi 🙋‍♀️ Welcome to *The Mathly* 🕺🙏.\n For Tutor Registration please enter the following details as Listed"
                "\n\n*Information Required*\n\n ✅ *Name*\n ✅ *Email Id*\n ✅ *Qualification and Work experience*\n ✅ *Area pin Code*\n ✅ *Subject*\n ✅ *Grade*\n\n 📔*So Lets Start the Process*\n\n ✔*Please Enter Your Full Name*")
                profile.update_one({'number':number},{"$set":{"status":"tutor_main"}})
            elif fresh == 0:
                res.message("Thanks 🙏😎 for using The Mathly as your tutoring service")
                profile.update_one({'number':number},{"$set":{"status":"tutor_fresh"}})

    users.update_one({"number":number},{'$push':{"messages":{"text":text,"date":datetime.now()}}})
    profile.update_one({"number":number},{'$push':{"messages":{"text":text,"date":datetime.now()}}})
    return str(res)


if __name__ == '__main__':
    app.run(port=5000)