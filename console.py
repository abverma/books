from datetime import date
from pymongo import MongoClient
from db import Connection
import searchBooks
from subprocess import call

current_date = date.today().strftime('%Y-%m-%d')
meta_map = [{
	'key': 'title',
	'required': True,
	'default': None,
	'prompt': 'Enter book tile: '
}, {
	'key': 'read_date',
	'required': True,
	'default': current_date,
	'prompt': 'Enter book date: '
}, {
	'key': 'author',
	'required': False,
	'default': None,
	'prompt': 'Enter book author: '
}, {
	'key': 'isbn',
	'required': False,
	'default': None,
	'prompt': 'Enter ISBN: '
}]
lists = []

def clear():
	call(["clear"])

def prompt(book):
	for meta in meta_map:
		value = None
		if not meta['key'] in book.keys():
			value = input(meta['prompt'])

			if meta['required']:
				if not value and not meta['default']:
					print(meta['key'], 'is required')
					return prompt()
				elif not value and meta['default']:
					value = meta['default']

			book[meta['key']] = value

	book['creation_date'] = current_date
	return book

def prompt_for_list():
	promptstr = 'Choose a list to add the book to:\n'
	if len(lists):
		for i in range(len(lists)):
			promptstr += str(i + 1) + '. ' + lists[i]['name'] +': '

	choice = input(promptstr)

	if (choice):
		book['list_id'] = lists[int(choice) - 1]['_id']

	return book



def save_book(book, con):
	con.insert_book(book)

def save_list(list, con):
	con.insert_list(list)

def create_list(con):
	choice = input('Enter new list name: ')
	if choice:
		save_list({
			'name': choice
		}, con)

def print_result(result):
	result_str = ''
	idx = 0
	
	for rec in result:
		idx += 1
		result_str += str(idx) + '. '

		for key in rec.keys():
			if key == 'lists':
				result_str  += key.title().replace('_', ' ') + ': ' + rec['lists'][0]['name'] + '\n'
			elif key != '_id' and key != 'list_id':
				result_str += key.title().replace('_', ' ') + ': ' + rec[key] + '\n'

		result_str +=  '\n'

	if not len(result_str):
		result_str = 'No records found'			
		
	print('\n')
	print('-'*20)
	print('Result')
	print('-'*20)
	print(result_str)

def search_books(book, con):
	result = con.find_books(book)
	print_result(result)


def search_prompt():
	query = None
	choice = input('Enter book title/author/ISBN to search: ')
	if choice:
		query = { '$text': { '$search': '\"'+choice+'\"' } }
	
	return query
	
def get_lists(con):
	return con.find_lists({})


clear()
con = Connection()
print('Fetching reading lists...')
lists_cusror = get_lists(con)

for list in lists_cusror:
	lists.append(list)

if len(lists):
	print('Fetched reading lists')
	choice = input('Choose one of the following options\n1. Enter new book\n2. Enter new list\n3. Search book\n4. List last 10 books\n5. Seach book online.\n')

else:
	print('No list found')
	create_list(con)
	choice = input('Choose one of the following options\n1. Enter new book\n2. Enter new list\n3. Search book\n4. List last 10 books\n5. Seach book online.\n')


if choice == '1':
	book = prompt({})	
	book = prompt_for_list()
	clear()
	save_book(book, con)
elif choice == '2':
	clear()
	create_list(con)
elif choice == '3':
	clear()
	query = search_prompt()
	if query:
		search_books(query, con)
elif choice == '4':
	clear()
	search_books({}, con)
elif choice == '5':
	clear()
	criteria = input('Enter book title/author/ISBN to search: ')
	books = searchBooks.search(criteria)
	print_result(books)
	idx = input('Enter book# to save: ')
	if idx:
		book = prompt(books[int(idx) - 1])	
		book = prompt_for_list()
		print(book)
		save_book(book, con)
else:
	print('Invalid choice')

con.close()

