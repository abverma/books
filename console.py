from datetime import date
from datetime import datetime
from pymongo import MongoClient
from db import Connection
from subprocess import call
import searchBooks
import sys


current_date = datetime.utcnow()
current_date_str = current_date.strftime('%Y-%m-%d')
meta_map = [{
	'key': 'title',
	'required': True,
	'default': None,
	'prompt': 'Enter book tile: '
}, {
	'key': 'list_update_date',
	'required': True,
	'default': current_date,
	'prompt': 'Enter list date: '
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
main_menu = 'Choose one of the following options\n1. Enter new book\n2. Enter new list\n3. Search book\n4. List last 5 books\n5. Seach book online.\n6. Exit\n'
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
	book['list_update_date'] = current_date
	return book

def prompt_for_list(book):
	promptstr = 'Choose a list to add the book to:\n'
	if len(lists):
		for i in range(len(lists)):
			promptstr += str(i + 1) + '. ' + lists[i]['name'] +': '

	choice = input(promptstr)

	if (choice):
		book['list'] = lists[int(choice) - 1]['name']

	return book



def save_book(book, con):
	con.insert_book(book)

def update_book(search, book, con):
	con.update_book(search, book)

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
	book_list = []
	for rec in result:
		book_list.insert(idx, rec)
		idx += 1
		result_str += str(idx) + '. '


		for key in rec.keys():
			if key not in ['_id','list_id', 'creation_date', 'last_update_date']:
				if key == 'lists':
					result_str  += key.title().replace('_', ' ') + ': ' + rec['lists'][0]['name'] + '\n'
				elif type(rec[key]) is datetime:
					result_str += key.title().replace('_', ' ') + ': ' + rec[key].strftime('%a %-d %b,  %Y') + '\n'
				elif 'date' in key and type(rec[key]) is str :
					result_str += key.title().replace('_', ' ') + ': ' + datetime.strptime(rec[key], '%Y-%m-%d').strftime('%a %-d %b,  %Y') + '\n'
				else:
					result_str += key.title().replace('_', ' ') + ': ' + rec[key] + '\n'

		result_str +=  '\n'

	if not len(result_str):
		result_str = 'No books found'			
		
	print('\n')
	print('-'*20)
	print('Result')
	print('-'*20)
	print(result_str)

	return book_list

def search_books(search, con, start = 0):
	result = con.find_books(search, start)
	books = print_result(result)

	if len(books):
		nxt = input('Press n to list next 5 books: ')

		if nxt == 'n':
			search_books(search, con, start + 5)
		else: 
			idx = input('Enter book# to take an action: ')
			if idx:
				try: 
					book = books[int(idx) - 1]
					updated_book = None
					choice = input('Choose one of the following options\n1. Edit list\n2. Add list date\n')

					if choice == '1':
						updated_book = prompt_for_list({})
						updated_book['last_update_date'] = current_date
						updated_book['list_update_date'] = current_date

						
					elif choice == '2':
						input_date = input('Enter date (yyyy-mm-dd): ')
						if input_date:
							update_date = datetime.strptime(input_date, '%Y-%m-%d')
							updated_book = {
								'last_update_date': update_date,
								'list_update_date': update_date
							}

					if updated_book:		
						update_book({
							'_id': book['_id']
						}, 
						updated_book, 
						con)
						print('Book updated')
				except Exception as e:
					print('Invalid choice')
	else: 
		input('Press any key to continue: ')

def search_prompt():
	query = None
	choice = input('Enter book title/author/ISBN to search: ')
	if choice:
		query = { '$text': { '$search': '\"'+choice+'\"' } }
	
	return query
	
def get_lists(con):
	return con.find_lists({})

def handle_choice(choice):

	if choice == '1':
		book = prompt({})	
		book = prompt_for_list(book)
		clear()
		save_book(book, con)
		input('Press any key to continue: ')
	elif choice == '2':
		clear()
		create_list(con)
		input('Press any key to continue: ')
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
			try:
				book = prompt(books[int(idx) - 1])	
				book = prompt_for_list(book)
				print_result([book])
				save_book(book, con)
				input('Press any key to continue: ')
			except Exception as e:
				print(e)
				print('Invalid Choice')
				input('Press any key to continue: ')

	elif choice == '6':
		print('Bye!')
		con.close()
		sys.exit()
	else:
		print('Invalid choice')
		input('Press any key to continue: ')

	clear()
	choice = input(main_menu)
	handle_choice(choice)

clear()
con = Connection()
print('#'*40)
print('#' + ' '*15 +'LIBRARY' + ' '*16 + '#')
print('#'*40)
print('Fetching reading lists...')
lists_cusror = get_lists(con)

for list in lists_cusror:
	lists.append(list)

if len(lists):
	print('Fetched reading lists')
	choice = input(main_menu)
else:
	print('No list found')
	create_list(con)
	choice = input(main_menu)

handle_choice(choice)



