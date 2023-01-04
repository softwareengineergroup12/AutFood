from Profile import Profile
from myOrders import myOrders
from telegram import *
from telegram.ext import *
import os

class EditMessageHandler:
    
    def __init__(self,query,update,context) -> None:
        
        self.chat_id =query.message.chat_id
        self.Handler(query,update,context)

    def Handler(self,query,update,context):
        if(query.data == "Edit"):
            Profile.Edit_Page(query,context)
        elif("Profile" in query.data):
            context.bot.send_message(chat_id = self.chat_id,text =
              "Enter your new {} :".format(query.data.split(" ")[1]),reply_markup = ForceReply())

        elif("EditMyOrders" in query.data):
            myOrders().editMyOrdersOption(update,context)
        elif("Menu_Help" == query.data):
            self.Menu_Help(update,context)
        elif("MainMenu_Help" == query.data):
            self.Main_Menu_Help(update,context)
        elif("Search_Help" == query.data):
            self.Search_Help(update,context)
        elif("FoodForm_Help" == query.data):
            self.FoodForm_Help(update,context)
        elif("AccountForm_Help" == query.data):
            self.Account_Help(update,context)
        elif("MyOrders_Help" == query.data):
            self.MyOrders_Help(update,context)
        elif("ForgetPassword_Help" == query.data):
            self.ForgetPasswordHelp(update,context)
        elif("change" in query.data):
            myOrders().editMyOrders(update,context,query)

    def Menu_Help(self,update:Update,context:CallbackContext):
        context.bot.send_photo(caption="1️⃣ if your not sure how to use the bot, just click Help button\n\n2️⃣ after you signed up ,you have to click login button to get access to the bot\
            \n\n3️⃣ first of all you have to SignUp, then your data will be store in our database \n\n4️⃣ if your not sure what was your password,just click 'ForgetPassword' button", chat_id = update.callback_query.from_user.id,photo=open("Img/menu.png","rb").read(),reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close",callback_data="Exit")]]))

    def Main_Menu_Help(self,update:Update,context:CallbackContext):
        context.bot.send_photo(caption="1️⃣ if your not sure how to use the bot, just click Help button\n\n2️⃣ You want to sell your food ? use this button\
            \n\n3️⃣ Are you looking for food to buy, try to use 'Buy Food' \n\n4️⃣ You can view or edit the data which was added\n\n5️⃣ Before you buy anything ,be sure that there's enough balance in your wallet \n\n6️⃣ if you want to know who has developed this bot click this button\
            \n\n7️⃣for more security we suggest you to Logout from your account" ,chat_id = update.callback_query.from_user.id,photo=open("Img/mainMenu.jpg","rb").read(),reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close",callback_data="Exit")]]))
        
    def Search_Help(self,update,context):
        context.bot.send_photo(caption="1️⃣ This is the name of food which you're looking for \n\n2️⃣ the price which you have to pay\
            \n\n3️⃣ more details about seller or something else \n\n4️⃣ Just try to use the name of food which you are looking for, then the results will be shown",chat_id = update.callback_query.from_user.id,photo=open("Img/search.jpg","rb").read(),reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close",callback_data="Exit")]]))
        
    def Account_Help(self,update,context):
        context.bot.send_photo(caption="1️⃣ Becareful to enter your account's username correctly \n\n2️⃣ enter your account's password\n\n3️⃣ Dont forget to click send ,otherwise your data will not be added to our database",chat_id = update.callback_query.from_user.id,photo=open("Img/Account.jpg","rb").read(),reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close",callback_data="Exit")]]))
    
    def FoodForm_Help(self,update,context):
        context.bot.send_photo(caption="1️⃣ Your Food name\n\n2️⃣ Number of orders you want to sell\
            \n\n3️⃣ the price you want to add for this food \n\n4️⃣ for more information about you or your food try to use this section",chat_id = update.callback_query.from_user.id,photo=open("Img/FoodForm.jpg","rb").read(),reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close",callback_data="Exit")]]))
    
    def MyOrders_Help(self,update,context):
        context.bot.send_photo(caption="1️⃣ this is the total orders, you've' added to sell\n\n2️⃣ first and last record that exist at every page you're on\
            \n\n3️⃣this the id of your food ,so you can click that to make any changes you want",chat_id = update.callback_query.from_user.id,photo=open("Img/MyOrders.jpg","rb").read(),reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close",callback_data="Exit")]]))
    
    def ForgetPasswordHelp(self,update,context):
        context.bot.send_photo(caption="🔴 if you want to reset your password you have to enter the random code which has sent to the email address you were added, if the entered code be correct, you were asked to write the new one",chat_id = update.callback_query.from_user.id,photo=open("Img/resetpassword.jpg","rb").read()
        ,reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close",callback_data="Exit")]]))