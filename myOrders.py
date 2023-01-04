from DatabaseConnection import Database
from telegram import *
from telegram.ext import *
class myOrders (Database):

    Food_ID = ""
    def __init__(self) -> None:
        super().__init__()

    
    def display_results(cls,update,context):
        total_orders = cls.Mysql.Search("Sellers","Seller_ID",update.message.chat.id)
    
        if(total_orders):
            cls.total = len(total_orders)
            update.message.reply_text(text = cls.set_text(total_orders,1),reply_markup = 
            InlineKeyboardMarkup([[InlineKeyboardButton("⏮️ Previous",callback_data="Previous_{}".format(cls.page-1)),InlineKeyboardButton("Next ⏭️",callback_data="Next_{}".format(cls.page+1))]]))

        else:
            update.message.reply_text("Your order list is empty!")


    def set_text(self,total_orders,page):
        self.body =""
        self.page = page
        key = (page-1)*3
        last_record = 0
        for order in range(3):
            if(order+key<len(total_orders)):
                Food = self.Mysql.Search("Foods","Food_ID",total_orders[order+key][1])[0]
                self.body += "🟣 Record : {}\n🍱 Food : {}\n🔢 Quantity : {}\n💰 Price : {}\n📂 Description : {}\n📥 Get_record : \n{}\n{}\n".format(key+order+1,
                Food[1],Food[2],Food[3],Food[4],"{}".format(Food[0]),30*'=')
                last_record = key+order
            else:
                last_record=key+order-1
                break

        self.header = "🔴 Total Records : {}   From  {} To  {}\n{}\n".format(len(total_orders),key+1,last_record+1,'='*30)
        self.header +=self.body
        return self.header

    def Next(self,update,context:CallbackContext,next_page):
        next = int(next_page.split('_')[1])
        total_orders = self.Mysql.Search("Sellers","Seller_ID",update.callback_query.message.chat_id)
        if((next-1)*3<len(total_orders)):
            context.bot.editMessageText(chat_id = update.callback_query.message.chat_id,message_id = update.callback_query.message.message_id,text = self.set_text(total_orders,int(next)),reply_markup = 
                InlineKeyboardMarkup([[InlineKeyboardButton("Previous",callback_data="Previous_{}".format(self.page-1)),InlineKeyboardButton("Next",callback_data="Next_{}".format(self.page+1))]]))
        else:
            context.bot.answer_callback_query(callback_query_id = update['callback_query']['id'],text = "‼️You are in the last page‼️",show_alert = True)
       

    def Previous(self,update,context:CallbackContext,previous_page):

        if(int(previous_page.split('_')[1])>0):
            self.Next(update,context,previous_page)
        else:
            context.bot.answer_callback_query(callback_query_id = update['callback_query']['id'],text = "‼️You are in the first page‼️",show_alert = True)
    

    def editMyOrdersOption(self,update:Update,context:CallbackContext):
        myOrders.Food_ID = update.callback_query.data.split(" ")[1]
        context.bot.editMessageText(chat_id = update.callback_query.message.chat_id,message_id = update.callback_query.message.message_id,text = "you want to change your order details? select one :",reply_markup = 
                InlineKeyboardMarkup([[InlineKeyboardButton("🍱 Food Name",callback_data="change Food_Name"),InlineKeyboardButton("🔢 Quantity",callback_data="change Quantity")]
                ,[InlineKeyboardButton("💰 Price",callback_data="change Price"),InlineKeyboardButton("📂 Description",callback_data="change Description")],
                [InlineKeyboardButton("🧑🏻‍💻 Account Username",callback_data="change AccountUsername")],[InlineKeyboardButton("🔑 Account Password",callback_data="change AccountPassword")],[InlineKeyboardButton("🔚 Exit",callback_data="Exit")]]))


    def editMyOrders(self,update:Update,context:CallbackContext,query):
        editQuery = query.data.split(" ")[1]
        context.bot.send_message(text="Enter your new {}".format(editQuery),reply_markup=ForceReply(),chat_id = update.callback_query.from_user.id)

    
    def editOnMySQL(self,reply_text,update):
        self.Mysql.Update("Foods",reply_text.split(" ")[3],update.message.text,"Food_ID",myOrders.Food_ID)
        update.message.reply_text("Your {} updated successfully!".format(reply_text.split(" ")[3]),
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton("🔙Back")]],resize_keyboard=True))
