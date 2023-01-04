from stage import stage
from telegram import InlineKeyboardMarkup,InlineKeyboardButton

class Profile (stage):
    def __init__(self, id) -> None:
        self.chat_id = id
    

    def userProfile(self,update,context,query):
        self.set_user_data()
        if(update.message):

            self.DisplayProf(update,query)
            self.Inline_Keyboard = [[InlineKeyboardButton("✍️Edit",callback_data="Edit"),InlineKeyboardButton("👉More",callback_data="More")]
        ,[InlineKeyboardButton("🔚 Exit",callback_data="Exit")]]
            context.bot.send_message(chat_id = self.chat_id,
                        text=self.text,reply_markup =InlineKeyboardMarkup(self.Inline_Keyboard))

        else:

            self.DisplayProf(update,query)
            if(query.data == "More"):

                self.Inline_Keyboard = [[InlineKeyboardButton("✍️Edit",callback_data="Edit"),
                InlineKeyboardButton("🔙Back",callback_data="BackToProf")]]
                context.bot.edit_message_text(chat_id = self.chat_id,message_id =query.message.message_id,
                            text=self.text,reply_markup =InlineKeyboardMarkup(self.Inline_Keyboard))
            else:
                self.Inline_Keyboard = [[InlineKeyboardButton("✍️Edit",callback_data="Edit"),InlineKeyboardButton("👉More",callback_data="More")]
        ,[InlineKeyboardButton("🔚 Exit",callback_data="Exit")]]
                context.bot.edit_message_text(chat_id = self.chat_id,message_id =query.message.message_id,
                            text=self.text,reply_markup =InlineKeyboardMarkup(self.Inline_Keyboard)) 

        

    def set_user_data(self):
        return self.Search("Users","Active_ID",self.chat_id)

    def DisplayProf(self,update,query):
        if(query):
            self.ID = query.from_user['username']
        else:
            self.ID = update.message.from_user['username']

        self.text = f"""\n
=====> ⚙️ Your Profile ⚙️ <=====\n\n🪪Telegram ID: {self.ID} \n
👨‍💻Username : {self.set_user_data()[0]}\n
📧Email : {self.set_user_data()[2]}\n
"""
        if(query and query.data == "More"):
            self.text += f"""👨‍🎓Student_number : {self.set_user_data()[3]}\n
📱Phone_number : {self.set_user_data()[4]}\n
"""   

    @classmethod
    def Edit_Page(cls,query,context):
        context.bot.edit_message_text(text = "=====> ✍️ Edit ✍️ <===== \nwhich one you want to edit?",message_id = query.message.message_id,
            chat_id =query.message.chat_id,reply_markup = 
            InlineKeyboardMarkup([[InlineKeyboardButton("📧 Email",callback_data="Profile Email")],[InlineKeyboardButton("👨‍🎓 StudentNumber",callback_data="Profile StudentNumber")],
            [InlineKeyboardButton("📱 PhoneNumber",callback_data="Profile PhoneNumber")],[InlineKeyboardButton("🔙Back",callback_data="BackToProf")]]))
   
    @classmethod
    def Edit_Email(cls,update,context):
        cls.Mysql.Update("Users","Email",update.message.text,"Active_ID",update.message.chat.id)
        context.bot.send_message(chat_id = update.message.chat.id,
                    text="Your Email updated successfully",reply_to_message_id = update.message.message_id)
        cls.BackToProf(update,context)
    @classmethod
    def Edit_PhonNum(cls,update,context):
        cls.Mysql.Update("Users","Phone_Number",update.message.text,"Active_ID",update.message.chat.id)
        context.bot.send_message(chat_id = update.message.chat.id,
                    text="Your Phone Number updated successfully",reply_to_message_id = update.message.message_id)
        cls.BackToProf(update,context)
    
    @classmethod
    def Edit_StudentNum(cls,update,context):
        cls.Mysql.Update("Users","Student_Number",update.message.text,"Active_ID",update.message.chat.id)
        context.bot.send_message(chat_id = update.message.chat.id,
                    text="Your Student Number updated successfully",reply_to_message_id = update.message.message_id)
        cls.BackToProf(update,context)

    @classmethod
    def BackToProf(cls,update,context):
        context.bot.send_message(chat_id = update.message.chat.id,
                    text="=======>    Edit   <======= \nTo edit your profile\n select one of the items",reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📧Email",callback_data="Profile Email")],[InlineKeyboardButton("👨‍🎓StudentNumber",callback_data="Profile StudentNumber")],
            [InlineKeyboardButton("📱PhoneNumber",callback_data="Profile PhoneNumber")],[InlineKeyboardButton("🔙Back",callback_data="BackToProf")]]))
