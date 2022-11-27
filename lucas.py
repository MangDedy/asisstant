#IMPORT EVAL
import telebot
import sys
import shutil
import traceback
import subprocess
import os
import time
import json
import requests
import jsonpickle
import re
from io import StringIO
from sys import version as pyver
from inspect import getfullargspec
from telebot import types
from html import escape




api = '5442053935:AAGLySF2qJFta00zW1-RLnkdCiO95ppTtV8'
bot = telebot.TeleBot(api)


def sudo(message):
    if message.from_user.id == 5039288972 :
        return True
    if message.from_user.id == 2003696861 :
        return True
    if message.from_user.id == 1928677026 :
        return True
    else:
        return False

def aexec(code, message):
    exec(
        "def __aexec(message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return locals()["__aexec"](message)


#EVAL
@bot.message_handler(regexp=("^\/anu"))
@bot.edited_message_handler(regexp=("^\/anu"))
def anu(message):
    if sudo(message):
        cmd = message.text.replace("/anu ","")
        if cmd == '/anu':
            return bot.reply_to(message,'*Masukan kode yang mau dianukan!!!*',parse_mode='Markdown')
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()
        stdout, stderr, exc = None, None, None
        try:
            aexec(cmd, message)
        except Exception:
            exc = traceback.format_exc()
        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = []
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation.append(stdout)
        else:
            evaluation = "SUCCESS"
        final_output = f"`OUTPUT:`\n\n`{evaluation.strip()}`"
        if len(final_output) > 4096:
            filename = "output.txt"
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(evaluation.strip()))
            bot.send_document(message.chat.id,
                  document=filename,
                  caption=f"`INPUT:`\n`{cmd[0:980]}`\n\n`OUTPUT:`\n`attached document`"
            ,parse_mode='Markdown')
            os.remove(filename)
        else:
            bot.reply_to(message,final_output,parse_mode='Markdown')
            #bot.edit_message_text(chat_id=message.chat.id, message_id=pr.message_id, text=final_output,parse_mode='Markdown')
    else:
        pass


@bot.message_handler(regexp=('^\/shell'))
@bot.edited_message_handler(regexp=("^\/shell"))
def pip(message):
    try:
        if sudo(message):
        #if message.from_user.id == 1928677026:
            cmd = message.text.replace("/shell ","")
            if cmd == "/shell" :
                return bot.reply_to(message,'*Kasi saya module untuk diinstall atau uninstall!!*',parse_mode='Markdown')
            prs = bot.reply_to(message,'`Dalam proses....!!`',parse_mode='Markdown')
            shell = subprocess.Popen(cmd, shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE).stdout.read()
            if len(shell) > 4096:
                with open('pypi_output.txt', 'w',encoding="utf8") as file:
                    file.write(str(shell))
                with open('pypi_output.txt', 'rb') as doc:
                    bot.send_document(message.chat.id,document=doc,caption=f'*Module:* `{cmd}`',parse_mode='Markdown')
                    bot.delete_message(message.chat.id,prs.message_id)
                    try:
                        os.remove('pypi_output.txt')
                    except:
                        pass
            elif len(shell) != 0:
                bot.edit_message_text(chat_id=message.chat.id, message_id=prs.message_id, text=shell)
            else:
                bot.edit_message_text(chat_id=message.chat.id, message_id=prs.message_id, text='Tidak tersedia!!')
    except Exception as e:
        bot.reply_to(message,e)

@bot.message_handler(regexp=('^\/remove'))
def remove(message):
    try:
        if sudo(message):
        #if message.from_user.id == 1928677026:
            cmd = message.text.replace("/remove ","")
            if cmd == "/remove" :
                return bot.reply_to(message,'*Kasi saya nama file untuk dihapus!!*',parse_mode='Markdown')
            a = os.remove(cmd)
            bot.reply_to(message,f'*Remove file :* `{cmd}`',parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message,e)

@bot.message_handler(regexp=('^\/save'))
def stop(message):
    try:
        if sudo(message):
        #if message.from_user.id == 1928677026:
            cmd = message.text.replace("/save ","")
            file = message.reply_to_message.document.file_id
            if cmd == "/save" :
                return bot.reply_to(message,'*Reply file dan kasi saya nama file baru untuk disave!!*',parse_mode='Markdown')
            newfile = bot.get_file(file)
            downloaded_file = bot.download_file(newfile.file_path)
            with open(cmd,'wb') as new_file:
                new_file.write(downloaded_file)
                new_file.close()
                bot.reply_to(message,f'*File di save*\n*Nama file :* {cmd}',parse_mode='Markdown')
            
    except Exception as e:
        bot.reply_to(message,e)



print('running')
while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        bot.send_message(1928677026,e)
        time.sleep(10)