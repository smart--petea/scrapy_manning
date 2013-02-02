Python script to scrape manning.com ebook catalog information

The script should support the following operations

$./manning_scrape.py list
>json file with a list of URLs for each book from http://www.manning.com/catalog/mobile

$./manning_scrape.py parse <bookurl>
>output JSON data for this one book

$./manning_scrape.py all
>output JSON data for all books

For each book I need the following information:

url
title
isbn
year
authors
image_url
ebook_price
