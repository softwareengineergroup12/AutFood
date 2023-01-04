
from telegram import *
from telegram.ext import *
class help :

    def __init__(self,update:Update,context) -> None:   
 
        self.url = "https://img.freepik.com/free-vector/website-faq-section-user-help-desk-customer-support-frequently-asked-questions-problem-solution-quiz-game-confused-man-cartoon-character_335657-1602.jpg?t=st=1672421511~exp=1672422111~hmac=868665f88799f2cb56d1fd251c9bc2234c68fd79302bf03b31c6064d55d0dfd6"
             
        update.message.reply_photo(photo=self.url,
            caption = "🤔 Do you need help ?",reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("📋 Menu",callback_data="Menu_Help"),InlineKeyboardButton("📋 Main Menu",callback_data="MainMenu_Help")],
                [InlineKeyboardButton("🔎 Search",callback_data="Search_Help"),InlineKeyboardButton("🛍️ MyOrders",callback_data="MyOrders_Help")],
                [InlineKeyboardButton("🧑🏻‍💻 Food Form",callback_data="FoodForm_Help"),InlineKeyboardButton("📇 Account Form",callback_data="AccountForm_Help")],
                [InlineKeyboardButton("🤔 Forget Password",callback_data="ForgetPassword_Help")],[InlineKeyboardButton("❌ Close",callback_data="Exit")]]))