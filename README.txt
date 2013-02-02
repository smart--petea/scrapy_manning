Ptyon script to scrape manning.com ebook catalog information

The script should support the following operations

$./manning_scrape.py list
>output a list of URLs for each book http://www.manning.com/catalog/mobile/

$./manning_scrape.py <bookurl>
>output JSON data for this one book

$./manning_scrape.py all
>output a JSON list of data for all books

For each book It need the following information:

url
title
isbn
year
authors
image_url
ebook_price
