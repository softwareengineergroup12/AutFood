from DatabaseConnection import Database
from telegram.ext import *
from telegram import *

class buy(Database):
    
    index = 1000
    def __init__(self,Query,Chat_ID,context) -> None:
        self.Query = Query
        self.Chat_ID = Chat_ID
        self.url = "https://www.pngmart.com/files/15/Food-Plate-Top-View-Non-Veg-PNG.png"
        self.set_Results(context)
    
    
    def set_Results(self,context:CallbackContext):
        
        self.results = []
        if(self.Query.query or self.Query.query!=''):
            Query=self.Mysql.Search("Foods","Food_Name",self.Query.query)
            if(Query and len(Query)!=0):

                for result in Query:
                    self.index+=1
                    self.results.append(InlineQueryResultArticle(id=self.index,title=f'🍟 Food : {result[1]}',thumb_url=self.url,
                    input_message_content=InputTextMessageContent(message_text=result[0]),type ='article',
                    description=f"💰 Price :{result[3]}\n📂 Description : {result[4]}"))
                self.show_inline_query_results(context)
                     
    def show_inline_query_results(self,context:CallbackContext):
            context.bot.answer_inline_query(inline_query_id =self.Query['id'],results = self.results,cache_time=2) 
    @classmethod
    def show_selected_item(cls,update:Update,context:CallbackContext):
        cls.chat_id = update.message.chat_id
        cls.Food_ID = update.message.text
    
        result = cls.Mysql.Search("Foods","Food_ID",cls.Food_ID)
        data = cls.Mysql.Search("Sellers","Food_ID",cls.Food_ID)

        if(data):
            cls.seller_ID = data [0][0]
    
            if(int(cls.seller_ID) == cls.chat_id):
                update.message.reply_text(text="to remove or edit your order details select your option :",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✍️ Edit",callback_data="EditMyOrders {}".format(cls.Food_ID)),
                InlineKeyboardButton("❌ Remove",callback_data="rm/{}".format(cls.Food_ID))],
                    [InlineKeyboardButton("🔚 Exit",callback_data="Exit")]]))
            else:
                keys = ['🍔 Food Name : ','🔢 Quantity : ','💰 Price : ','📂 Description : ']
                cls.text = "==>🍟 Your Food Details 🍟<==\n"
                cls.index = 0
                if(result):
                    for item in result[0]:
                        if(not 'fd' in str(item)):
                            cls.text +="\n{}{}\n".format(keys[cls.index],item)
                            cls.index+=1
                    update.message.reply_text(text=cls.text,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Buy",callback_data="Buy {}".format(cls.Food_ID))],
                    [InlineKeyboardButton("🔚 Exit",callback_data="Exit")]]))
        else:
            update.message.reply_text("No order found",reply_to_message_id=update.message.message_id)
    
    @classmethod
    def removeOrder(cls,update:Update,context:CallbackContext,type):
        data = update.callback_query.data.split("/")[1]
        cls.Mysql.Delete("Foods","Food_ID",data)
        cls.Mysql.Delete("Sellers","Food_ID",data)
        if(type =="remove"):
            context.bot.send_message(chat_id = update.callback_query.message.chat_id,text = "Your order was removed!")