import telebot
from telebot import types

import vk_api
import os
import re
import sqlite3
import urllib.request

import time

import sys
sys.path.insert(0, r'C:\Users')#path where config.py file stores
import config

from retriever import exfunction

conn = sqlite3.connect('files/dict.sqlite',check_same_thread=False)
cur = conn.cursor()

bot = telebot.TeleBot(config.TOKEN)

def generatewords(message,title):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("1")
	item2 = types.KeyboardButton("5")
	item3 = types.KeyboardButton("10")
	item4 = types.KeyboardButton("20")
	markup.add(item1, item2, item3, item4)
	bot.send_message(message.chat.id, title.format(message.from_user),
		parse_mode='html', reply_markup=markup)



def deletefunc(message,title):
	sqlstr = '''
	DELETE FROM Dictionary WHERE word = ?
	'''
	results = cur.execute(sqlstr,(word,))
	conn.commit()
	try:
		os.remove(path)
	except PermissionError:
		print("[x]PermissionError due to current usage of the file")
		time.sleep(2)
		os.remove(path)
		print("[x]File was successefully deleted")
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Generate words")
	item2 = types.KeyboardButton("Review words")

	markup.add(item1, item2)
	bot.send_message(message.chat.id, title.format(message.from_user),
		parse_mode='html', reply_markup=markup)



@bot.message_handler(commands=['start'])
def welcome(message):

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Generate words")
	item2 = types.KeyboardButton("Review words")

	markup.add(item1, item2)
	bot.send_message(message.chat.id, "Welcome, {0.first_name}, What do you want?".format(message.from_user),
		parse_mode='html', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':

		if message.text == 'Generate words':
			title = 'How much words do you want to create?'
			generatewords(message,title)

		elif message.text == 'Review words':

			sqlstr = '''
			SELECT word, path, one, two, three
			FROM Dictionary
			'''
			cur.execute(sqlstr)
			rows = cur.fetchall()
			#print(len(rows))
			if len(rows) < 1:
				title = 'There is no words left\nYou need to create new ones\nHow much words you want to create'
				generatewords(message, title)
			else:
				for row in rows:
					global word, path, one, two, three
					word, path, one, two, three = row
					if one is None:
						one = 'None'
					if two is None:
						two = 'None'
					if three is None:
						three = 'None'
					mess = 'word: ' + word + '\n' + 'definitions' + '\n' + one + '\n' + two + '\n' + three
					bot.send_message(message.chat.id, mess)
					try:
						bot.send_photo(message.chat.id, photo=open(path, 'rb'))
					except:
						bot.send_message(message.chat.id, "photo for that word was broken")

					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					item1 = types.KeyboardButton("Publish")
					item2 = types.KeyboardButton("Delete")
					markup.add(item1, item2)
					bot.send_message(message.chat.id, "What do you want?".format(message.from_user),
					parse_mode='html', reply_markup=markup)
					break

		elif message.text == 'Publish':
			bot.send_message(message.chat.id, "...loading")
			vk_session = vk_api.VkApi(config.LOGIN, config.PASSWORD)
			try:
				vk_session.auth(token_only=True)
			except vk_api.AuthError as error_msg:
				mess = 'Problem with connection, Error #' + str(error_msg)
				bot.send_message(message.chat.id, mess)
				return
		    #UPLOAD PHOTO
			upload = vk_api.VkUpload(vk_session)
			photo = upload.photo(
				path,
				album_id=279409061,
				group_id=''
			)
			vk_photo_url = 'https://vk.com/photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])
			photourl = 'photo' + str(photo[0]['owner_id']) + '_' + str(photo[0]['id'])
			vk = vk_session.get_api()

			if one == 'None':
				mess = word
			elif two == 'None':
				mess = '* '+ word + '\n\n' + 'definition:' + '\n[1]' + one
			elif three == 'None':
				mess = '* '+ word + '\n\n' + 'definitions:' + '\n[1]' + one + '\n[2]' + two
			else:
				mess = '* '+ word + '\n\n' + 'definitions:' + '\n[1]' + one + '\n[2]' + two + '\n[3]' + three
			a = dict()
			a = vk.wall.post(owner_id=-31160174,attachments = photourl,message=mess)
			print(a['post_id'],'post was sucessefully publicated to vk group')
			title = 'post with id ' + str(a['post_id']) + " was successfully \npublicated to VK. What next?"
			deletefunc(message,title)

		elif message.text == 'Delete':
			title = "Word has been deleted, what next?"
			deletefunc(message,title)

		elif message.text == '1' or	message.text == '5' or message.text == '10' or message.text == '20':
			bot.send_message(message.chat.id, "...loading(please wait)")
			count = int(message.text)
			exfunction(count)
			text = str(count) + ' new words has been added to the database\nWhat do you want now?'

			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton("Review words")
			item2 = types.KeyboardButton("Generate words")
			markup.add(item1, item2)
			bot.send_message(message.chat.id, text.format(message.from_user),
			parse_mode='html', reply_markup=markup)
		else:
			bot.send_message(message.chat.id, "I don't know what to answer ")

# RUN
bot.polling(none_stop=True)
