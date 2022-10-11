from cgitb import text
from email import message
from telegram.ext import *
from telegram import KeyboardButton, MenuButtonCommands, ReplyKeyboardMarkup, ReplyMarkup
from dotenv import load_dotenv
import csv
import os

import scrap


# checking changes and sending message
def send_changes():
    scrap.check_new_notice()
    scrap.changelog()
    scrap.changes.reverse()


class TelegramBot:

    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("TOKEN")

# start command event
    def start_command(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Welcome to cgu notice bot\n\ncommands:-\n/refresh -check for new notice\n/recent -show recent notice\n\nfor any query and suggestion contact @Walle_since2000\n\n[wall-e]",
        )

# refresh command event
    def refresh_command(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="fetching the latest updates..."
        )
        send_changes()
        if len(scrap.changes) != 0:
            for row in scrap.changes:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"{row[1]}\n\nLink:-\n{row[3]}"
                )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="No new update/notice found"
            )

# recent command event
    def recent_command(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="getting recent update..."
        )
        try:
            with open(scrap.filename, 'r+') as file:
                csvreader = csv.reader(file)
                i = 0
                for row in csvreader:
                    if i >= 1:
                        context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"{row[1]}\n\nLink:-\n{row[3]}"
                        )
                        break
                    i = i+1
        except:
            print("file reading error")
        file.close()

# handling error dubuging
    def error(self, update, context):
        print(f"Update {update} caused error {context.error}")

    def start_bot(self):
        updater = Updater(self.TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start_command))
        dp.add_handler(CommandHandler("refresh", self.refresh_command))
        dp.add_handler(CommandHandler("recent", self.recent_command))
        dp.add_error_handler(self.error)
        updater.start_polling()
        print("[+] BOT has started")
        updater.idle()
