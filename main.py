from telegram.ext import *
from telegram import *
from stage import stage 
from APIKEY import API

class telegrambot :


    def start(self,update:Updater,context:CallbackContext):
        chat_id =  update.message.chat.id
        if(stage.getIsLogin(stage,str(chat_id)) == "1"):
             update.message.reply_text("Welcome back!")
             keyboard = [[KeyboardButton("Sell Food"),KeyboardButton("Buy Food")],
                [KeyboardButton("Profile"),KeyboardButton("Wallet")],[KeyboardButton("Exit")]]

             context.bot.send_message(chat_id = chat_id,text = "select one of the items of MainMenu"
            ,reply_markup=ReplyKeyboardMarkup(keyboard = keyboard,resize_keyboard=True))

        else:
            keyboard = [[KeyboardButton("Login"),KeyboardButton("SignUp")],[KeyboardButton("ForgetPassword")]]
            context.bot.send_message(chat_id = update.message.chat.id,text = "🤖 Choose your option please !"
                    ,reply_markup=ReplyKeyboardMarkup(keyboard = keyboard,resize_keyboard=True))
        
    def Reply_Handler(self,update:Updater,context:CallbackContext)->None:
        message_text = update.message.text
        chat_id = update.message.chat.id

        if("Login" in update.message.reply_to_message.text):
            self.Login(update,context)

        elif("SignUp" in update.message.reply_to_message.text):
            self.SignUp(update,context)  
        

    def Login(self,update,context) -> None:
        chat_id = update.message.chat.id
        messsage_text = update.message.text

        if(update.message.reply_to_message):
            reply_text = update.message.reply_to_message.text
            user = stage(chat_id)

            if("Login's username" in reply_text):
                user.setUsername(messsage_text,chat_id)
                context.bot.send_message(chat_id = chat_id ,
                    text="Login's password :",reply_markup = ForceReply())
            else:
                user.setPassword(messsage_text,chat_id)
                user.auth(chat_id,context)
    
        else :
            context.bot.send_message(chat_id = chat_id ,
                text="Login's username :",reply_markup = ForceReply())


    def SignUp(self,update,context : CallbackContext) -> None:

        chat_id = update.message.chat.id
        messsage_text = update.message.text

        if(not stage.Search(stage,"Users","ID",chat_id)):

            user = stage(update.message.chat.id)

            if(update.message.reply_to_message):
                reply_text = update.message.reply_to_message.text
        
                # Adding Password to stage
                if("SignUp's password" in reply_text): 
                    user.setPassword(messsage_text,chat_id)

                    context.bot.send_message(chat_id = chat_id ,
                    text="Click to Submit",
                    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Submit Now")]],resize_keyboard=True))
                #Adding Username to stage
                else:
                    user.setUsername(messsage_text,chat_id)
                    context.bot.send_message(chat_id = chat_id ,
                    text="SignUp's password :",reply_markup = ForceReply())
            else :
                # Submit request to MySql
                if("Submit" in messsage_text):
                    user.add_to_mysql(chat_id,context)
                else:
                    context.bot.send_message(chat_id = chat_id ,
                        text="SignUp's username :",reply_markup = ForceReply())
        else:
            context.bot.send_message(chat_id = chat_id,
                    text="You've already registered before!",
                    reply_markup= ReplyKeyboardMarkup([[KeyboardButton("Back")]],resize_keyboard=True))
        
    def ForgetPass(self,update,context):
            pass

    def Exit (self,update,context):
        chat_id = update.message.chat.id
        stage.setIsLogin(stage,"is_Login","0","ID",str(chat_id))
        self.start(update,context)


if __name__ == "__main__" :

    try :
        updater =  Updater(token=API.key,use_context=True)
        dp = updater.dispatcher
        telebot =  telegrambot()

        dp.add_handler(CommandHandler('start',telebot.start,run_async=True))
        dp.add_handler(MessageHandler(Filters.reply,telebot.Reply_Handler))
        dp.add_handler(MessageHandler(Filters.regex("^Login$") ,telebot.Login,run_async=True))
        dp.add_handler(MessageHandler(Filters.regex("^SignUp$") ,telebot.SignUp,run_async=True))
        dp.add_handler(MessageHandler(Filters.regex("^ForgetPassword$") ,telebot.ForgetPass))
        dp.add_handler(MessageHandler(Filters.regex("^Back$") ,telebot.start))
        dp.add_handler(MessageHandler(Filters.regex("^Submit Now$") ,telebot.SignUp,run_async=True))
        dp.add_handler(MessageHandler(Filters.regex("^Exit$") ,telebot.Exit,run_async=True))

        updater.start_polling(0.2)
        updater.idle()  
    except:
        print("Cannot connect to telegram server!")
    
