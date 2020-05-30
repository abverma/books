from pymongo import MongoClient
import logging
import sys
import config
import emoji


HOST = config.HOST
PORT = config.PORT
DB_NAME = config.DB_NAME
USER = config.USER
PWD = config.PWD


class Connection():

	def __init__(self, host=HOST, port=PORT):
		try:
			logging.basicConfig(stream=sys.stderr, level=logging.INFO)

			self.client = MongoClient(host=HOST, port=PORT, username=USER, password=PWD, retryWrites=False, authSource=DB_NAME)

			logging.debug(emoji.emojize('Connection successful! :thumbs_up:'))
		except Exception as e:
			logging.debug(emoji.emojize('Error in connection :stop sign:'))
			logging.debug(e)
			return None
	def insert_book(self, books):
		try:
			db = self.client[DB_NAME]
			db.books.insert_one(books)
			logging.debug(emoji.emojize('Books inserted! :thumbs_up:'))	
		except Exception as e:
			logging.debug(emoji.emojize('Error in inserting books :stop_sign:'))
			logging.debug(e)

	def update_book(self, search, update):
		try:
			db = self.client[DB_NAME]
			db.books.update_one(search, {
				'$set': update
			})
			logging.debug(emoji.emojize('Books inserted! :thumbs_up:'))		
		except Exception as e:
			logging.debug(emoji.emojize('Error in inserting books :stop_sign:'))
			logging.debug(e)

	def insert_goodreads_books(self, books):
		try:
			db = self.client[DB_NAME]
			result = db.books.insert_many(books)
			logging.debug(emoji.emojize('%s books inserted! :thumbs_up:', len(result.inserted_ids)))
		except Exception as e:
			logging.debug(emoji.emojize('Error in inserting books :stop_sign:'))
			logging.debug(e)

	def insert_list(self, list):
		try:
			db = self.client[DB_NAME]
			db.lists.insert_one(list)
			logging.debug(emoji.emojize('List inserted! :thumbs_up:'))	
		except Exception as e:
			logging.debug(emoji.emojize('Error in inserting list :stop_sign:'))
			logging.debug(e)		

	def find_books(self, books, start = 0):
		try:
			logging.debug(books)
			db = self.client[DB_NAME]
			pipelines = [{
				'$match': books
			},
			{
				'$sort': {
					'last_update_date': -1,
					'creation_date': -1
				}
			}, 
			{	
				'$skip': start
			},
			
			{
				'$limit': 5
			}]
			result = db.books.aggregate(pipelines)
			return result
		except Exception as e:
			logging.debug(emoji.emojize('Error in searching books :stop_sign:'))
			logging.debug(e)
			return None

	def find_lists(self, books):
		try:
			logging.debug(books)
			db = self.client[DB_NAME]
			result = db.lists.find(books, limit = 10)
			return result
		except Exception as e:
			logging.debug(emoji.emojize('Error in searching lists :stop_sign:'))
			logging.debug(e)
			return None

	def close(self):
		try:
			self.client.close()
			logging.debug(emoji.emojize('Connection closed :thumbs_up:'))	
		except Exception as e:
			logging.debug(emoji.emojize('Error in closing connection :stop_sign:'))
			logging.debug(e)

# client = connect_mongo()

# db = client[DB_NAME]

# insert_books(workout)



