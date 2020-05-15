import requests as req
import xml.etree.ElementTree as ET
import config

def search(name):

	KEY = config.KEY
	URL = 'https://www.goodreads.com/search/index.xml?key=' + KEY + '&q=' + name

	print(URL)
	print('Searching...')
	r = req.get(URL)
	root = ET.fromstring(r.text)

	books = []

	for book_node in root.iter('work'):
		book = {}

		book['ratings_count'] = book_node.find('ratings_count').text
		book['average_rating'] = book_node.find('average_rating').text
		best_book_node = book_node.find('best_book')
		title_node = best_book_node.find('title')
		book['goodread_id'] = best_book_node.find('id').text
		book['title'] = title_node.text

		author_node = best_book_node.find('author')

		if author_node:
			book['author'] = author_node.find('name').text

		books.append(book)

	return books