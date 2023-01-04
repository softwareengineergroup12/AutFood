from telegram.ext import *
from telegram import *
from stage import stage 
from APIKEY import API
from Profile import Profile
from wallet import wallet 
from Buy import buy
import json
from Foods import Foods
from Sellers import Seller
from myOrders import myOrders
from EditMessageHandler import EditMessageHandler
from help import help
from resetPassword import resetPass

class telegrambot :


    def start(self,update:Update,context):

        self.chat_id =  update.message.chat.id

        if(self.check_Login(self.chat_id)):
            self.keyboard = [[KeyboardButton("🔖Help")],[KeyboardButton("🍟Sell Food",
            web_app=WebAppInfo(url="https://shervin-ghaffari.github.io/")),KeyboardButton("🍔Buy Food")],
                [KeyboardButton("📇MyOrders"),KeyboardButton("⚙️MyProfile")],[KeyboardButton("💳Wallet"),KeyboardButton("👨‍💻AboutUs")],[KeyboardButton("🔐Logout")]]
            update.message.reply_text("😉 Welcome back {}!".format(update.message.from_user.first_name),reply_markup=ReplyKeyboardMarkup(self.keyboard,resize_keyboard=True))

        else:
            self.keyboard = [[KeyboardButton("🔖Help")],[KeyboardButton("🧾Login",web_app=WebAppInfo(url="https://shervinghaffari23.github.io")),
            KeyboardButton("🗂️SignUp",web_app=WebAppInfo(url="https://shervingh2000.github.io/"))],
            [KeyboardButton("🤔ForgetPassword")]]
            context.bot.send_message(chat_id = self.chat_id,text = "Choose your option please :"
                    ,reply_markup=ReplyKeyboardMarkup(keyboard = self.keyboard,resize_keyboard=True))
        
    def Reply_Handler(self,update,context)->None:
        reply_text = update.message.reply_to_message.text
        if("username" in reply_text):
            self.resetPass_Handler(update,context)
        elif("verification code" in reply_text):
            resetPass(update.message.chat.id).verifyCode(update,context)
        elif("new password" in reply_text):
            resetPass(update.message.chat.id).UpdatePass(update,context)
        elif("new Email" in reply_text):
            Profile.Edit_Email(update,context)
        elif("new StudentNumber" in reply_text):
            Profile.Edit_StudentNum(update,context)
        elif("new PhoneNumber" in reply_text):
            Profile.Edit_PhonNum(update,context)
        elif("credit amount" in reply_text):
            wallet().add_Optional(update)
        else:
            myOrders().editOnMySQL(reply_text,update)

    def CallBack_Handler(self,update :Update,context:CallbackContext):
        query = update.callback_query
        self.chat_id = query.message.chat_id
        self.message_id = query.message.message_id

        if(query.data == "Exit"):
            context.bot.delete_message(message_id = self.message_id ,chat_id = query.from_user.id)
        elif(query.data == "More" or query.data =="BackToProf"):
            Profile(self.chat_id).userProfile(update,context,query)
        elif("Buy" in query.data):
            context.bot.edit_message_text(message_id = self.message_id ,chat_id =self.chat_id,text = "💰Choose your payment option:",
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("💳Direct Pay",callback_data="DirectPay")],
            [InlineKeyboardButton("💰PayByCredit",callback_data="PayByCredit {}".format(query.data.split(" ")[1]))],[InlineKeyboardButton("🔚 Exit",callback_data="Exit")]]))
        elif("rm/" in query.data):
            buy.removeOrder(update,context,"remove")
        elif("Next" in query.data):
            myOrders().Next(update,context,query.data)
        elif("Previous" in query.data):
            myOrders().Previous(update,context,query.data)
        elif("addBalance" == query.data):
            wallet().add_Balance(update,context)
        elif("add/" in query.data):
            wallet().add(update,context)
        elif("PayByCredit " in query.data):
            context.bot.edit_message_text(text = "Are you sure ?",chat_id = self.chat_id,message_id = self.message_id,reply_markup = 
            InlineKeyboardMarkup([[InlineKeyboardButton("👍",
            callback_data="YES {}".format(query.data.split(" ")[1])),InlineKeyboardButton("👎",callback_data="NO")]]))
        elif("YES " in query.data or query.data == "NO"):
            wallet().PayByCredit(update,context)
        else:
            EditMessageHandler(query,update,context)

    def WebApp_Handler(self,update:Update,context:CallbackContext):
        chat_ID = update.message.chat.id
        method = json.loads(update.message.web_app_data.data).get("method")
        data = json.loads(update.message.web_app_data.data)
        if(method == "login"):
            self.Login_Auth(data,update)
        elif(method == 'signup'):
            self.SignUpSubmit(data,update)
        else:
            load = json.loads(update.message.web_app_data.data)
            Foods(load)
            Seller(chat_ID,load)
            update.message.reply_text("Your data was added successfully")

    def InlineQuery_Handler(self,update:Update,context:CallbackContext):
        buy(update.inline_query,update.inline_query.from_user.id,context)

    def Login_Auth(self,data:dict,update):
        user = stage()
        user.auth(data,update)

    def check_Login(self,chat_id):
        user = stage()
        return user.get_Active_ID(chat_id)

    def SignUpSubmit(self,data,update):
        user = stage()
        user.add_to_mysql(data,update)

    def resetPass(self,update,context):
    
        context.bot.send_message(chat_id = update.message.chat.id,
            text="to reset your password enter your username :",
            reply_markup = ForceReply())

    def resetPass_Handler(self,update,context):
        reset = resetPass(update.message.chat.id)
        reset.resetPass(update.message.text,update,context)
        
    def Profile(self,update,context):
        profile = Profile(update.message.chat.id)
        profile.userProfile(update,context,None)

    def AboutUs(self,update:Update,context):
        update.message.reply_text("👨‍💻 this bot has developed by 👨‍💻\n🟠Shervin\n🟠Khashayar\n🟠Arshya\n🟠Amir",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔚 Exit",callback_data="Exit")]]))

    def Wallet(self,update:Update,context:CallbackContext):
        wallet().showBlance(update,context)

    def myOrders(self,update,context):
       myOrders().display_results(update,context)

    def help(self,update:Update,context):
        help(update,context)

    def BuyFood(self,update,context):
        update.message.reply_text("Select one of the items below:" ,reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Search",switch_inline_query_current_chat="")],
        [InlineKeyboardButton('🔚 Exit',callback_data='Exit')]]))

    def Logout (self,update,context):
        chat_id = update.message.chat.id
        username = stage.Search(stage,"Users","Active_ID",chat_id)[0]
        stage.set_Active_ID(stage,"",username)
        self.start(update,context)
    
    def Message_Hanlder(self,update,context:CallbackContext):
        buy.show_selected_item(update,context)

if __name__ == "__main__" :

    try :
        updater =  Updater(token=API.key,use_context=True)
        dp = updater.dispatcher
        telebot =  telegrambot()

        dp.add_handler(CommandHandler('start',telebot.start))
        dp.add_handler(CommandHandler('help',telebot.help))
        dp.add_handler(MessageHandler(Filters.regex("^🔖Help$"),telebot.help))
        dp.add_handler(MessageHandler(Filters.regex("^/fd_"),telebot.Message_Hanlder))
        dp.add_handler(MessageHandler(Filters.reply,telebot.Reply_Handler))
        dp.add_handler(MessageHandler(Filters.regex("^🤔ForgetPassword$") ,telebot.resetPass,run_async = True))
        dp.add_handler(MessageHandler(Filters.regex("^🔙Back$") ,telebot.start))
        dp.add_handler(MessageHandler(Filters.regex("^🔐Logout$") ,telebot.Logout))
        dp.add_handler(MessageHandler(Filters.regex("^⚙️MyProfile$") ,telebot.Profile,run_async = True))
        dp.add_handler(MessageHandler(Filters.regex("^👨‍💻AboutUs$"),telebot.AboutUs))
        dp.add_handler(MessageHandler(Filters.regex("^📇MyOrders$"),telebot.myOrders))
        dp.add_handler(MessageHandler(Filters.regex("^🍔Buy Food$") ,telebot.BuyFood))
        dp.add_handler(InlineQueryHandler(telebot.InlineQuery_Handler))
        dp.add_handler(MessageHandler(Filters.regex("^💳Wallet$") ,telebot.Wallet,run_async = True))
        dp.add_handler(MessageHandler(Filters._StatusUpdate.web_app_data,telebot.WebApp_Handler))
        dp.add_handler(CallbackQueryHandler(telebot.CallBack_Handler))
       
        updater.start_polling()
        updater.idle()  


    except:
        print("Cannot connect to telegram server!")
    
