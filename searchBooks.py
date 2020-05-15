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

	for book_node in root.iter('best_book'):
		book = {}
		title_node = book_node.find('title')
		book['title'] = title_node.text

		author_node = book_node.find('author')

		if author_node:
			book['author'] = author_node.find('name').text

		books.append(book)

	return books

