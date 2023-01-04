from DatabaseConnection import Database
from telegram import *
from random import randint
from sendEmail import sendMail
from wallet import wallet

class stage :   
    Mysql = Database.Mysql
    Atrribute = "(Username,Password,Email,Student_Number,Phone_Number,Active_ID)"

    def set_Active_ID(self,ID,username):
        self.Mysql.Update("Users","Active_ID",ID,"Username",username)

    def get_Active_ID(self,ID):
        Resault = self.Search("Users","Active_ID",ID)
        if(Resault):
            return True
        return False

    def setValue(self,data,update):
        keys = ['username','password','email','studentNumber','phoneNumber']
        temp = []
        for key in keys :
            temp.append(f'{data.get(key)}')
        temp.append("")
        return tuple(temp)

    def add_to_mysql (self,data,update):
        
        userExist = self.Search("Users","Username",data.get("username"))
        if(not userExist):
            self.Mysql.Insert("Users",self.Atrribute,str(self.setValue(data,update)))
            update.message.reply_text("You'have successfully registered!")
            update.message.reply_text("Get back to Login",reply_markup = 
            ReplyKeyboardMarkup([[KeyboardButton("🔙Back")]],resize_keyboard=True))
            wallet().setValue(data.get("username"),update)
        else:
            update.message.reply_text("Your username has been used before!")

    def auth(self,data,update) :

        self.keyboard = [[KeyboardButton("🔖Help")],[KeyboardButton("🍟Sell Food",
            web_app=WebAppInfo(url="https://shervin-ghaffari.github.io/")),KeyboardButton("🍔Buy Food")],
                [KeyboardButton("📇MyOrders"),KeyboardButton("⚙️MyProfile")],
                [KeyboardButton("💳Wallet"),KeyboardButton("👨‍💻AboutUs")],[KeyboardButton("🔐Logout")]]

        Resault = self.Search("Users","Username",data.get("username"))

        if(not Resault or Resault[1] != data.get("password")):
            update.message.reply_text("Your username or password is wrong!")
        elif(Resault[5]!=""):
            update.message.reply_text("Your account is active on other devices; try to logout first")
        else:
            update.message.reply_text("You'have successfully logged in",reply_markup = 
            ReplyKeyboardMarkup(self.keyboard,resize_keyboard=True))
            self.set_Active_ID(update.message.chat.id,data.get("username"))
    
    def Search(self,table,attr,value):
        results =self.Mysql.Search(table,attr,value)
        if(results):
            return self.Mysql.Search(table,attr,value)[0]
        else:
            return 0