import csv
from bson.objectid import ObjectId
from datetime import date
from db import Connection

def find(arr, key, value):

	for item in arr:
		if item[key] == value:
			return item

lists = []
con = Connection()
lists_cusror = con.find_lists({})

for list in lists_cusror:
	lists.append(list)

current_date = date.today().strftime('%Y-%m-%d')
to_read = find(lists, 'name', 'To Read')['name']
read = find(lists, 'name', 'Read')['name']
reading = find(lists, 'name', 'Currently Reading')['name']
books = []

print(to_read_id)
print(read_id)
print(reading_id)

with open('/Users/abhishek/Downloads/goodreads_library_export.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		book = {}
		book['title'] = row['Title']
		book['author'] = row['Author']
		book['isbn'] = row['ISBN'].replace('=', '').replace('"', '')
		book['creation_date'] = current_date
		book['goodread_id'] = row['Book Id']
		book['average_rating'] = row['Average Rating']
		shelve = row['Exclusive Shelf']
		list_id = None
		if shelve == 'currently-reading':
			book['list'] = reading
		elif shelve == 'read':
			book['list'] = read_id
		elif shelve == 'to-read':
			book['list'] = to_read


		books.append(book)


if len(books):
	con = Connection()
	con.insert_goodreads_books(books)
	con.close()

#print(books)

