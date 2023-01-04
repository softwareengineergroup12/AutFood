from DatabaseConnection import Database
from random import randint
from sendEmail import sendMail
from telegram import *
from telegram.ext import *

class resetPass(Database):
    def __init__(self,Chat_ID) -> None:
        super().__init__()
        if(not self.Mysql.Search("ForgetPassword","User_ID",Chat_ID)):
            self.Mysql.Insert("ForgetPassword","(User_ID,Username,Auth_Code)","('{}',' ',' ')".format(Chat_ID))

    def resetPass(self,username,update,context):
        data = self.Mysql.Search("Users","Username",username)[0]
        
        if(data):
            code = randint(1000,9999)
            self.Mysql.Update("ForgetPassword","Auth_Code",code,"User_ID",update.message.chat.id)
            self.Mysql.Update("ForgetPassword","Username",data[0],"User_ID",update.message.chat.id)
            context.bot.send_message(chat_id = update.message.chat.id ,
            text="Enter the verification code has been sent to your email :",
            reply_markup = ForceReply())
            send=sendMail(code=code,reciver=data[2])
            send.sendEmail()
        else:
            context.bot.send_message(chat_id = update.message.chat.id ,text="Your username does not exist!",
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton("🔙Back")]],resize_keyboard=True))

    def verifyCode(self,update,context):
        data = self.Mysql.Search("ForgetPassword","User_ID",value = update.message.chat.id)[0]
        if(update.message.text == str(data[2])):
            context.bot.send_message(chat_id = update.message.chat.id ,text="Enter your new password :",
            reply_markup = ForceReply())
        else:
            update.message.reply_text("Your verfication code is wrong!")

    
    def UpdatePass(self,update,context):
        results= self.Mysql.Search("ForgetPassword","User_ID",update.message.chat.id)[0]
        self.Mysql.Update("Users","Password",update.message.text,"Username",results[1])
        context.bot.send_message(chat_id = update.message.chat.id ,text="Your password was changed successfully!",
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton("🔙Back")]],resize_keyboard=True))