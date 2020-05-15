import csv
from bson.objectid import ObjectId
from datetime import date
from db import Connection


current_date = date.today().strftime('%Y-%m-%d')
to_read_id = ObjectId("5eb6cbd0a6d5deed7094c000")
read_id = ObjectId("5eb6f968edb00ecbc5297660")
reading_id = ObjectId("5eb83bde88a3b005057598e0")
books = []

with open('/Users/abhishek/Downloads/goodreads_library_export.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		book = {}
		book['title'] = row['Title']
		book['author'] = row['Author']
		book['isbn'] = row['ISBN'].replace('=', '').replace('"', '')
		book['creation_date'] = current_date
		shelve = row['Exclusive Shelf']
		list_id = None
		if shelve == 'currently-reading':
			list_id = reading_id
		elif shelve == 'read':
			list_id = read_id
		elif shelve == 'to-read':
			list_id = to_read_id

		book['list_id'] = list_id

		books.append(book)


if len(books):
	con = Connection()
	con.insert_goodreads_books(books)
	con.close()

#print(books)

