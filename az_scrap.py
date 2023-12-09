from requests_html import HTMLSession
import csv
import datetime
import sqlite3

#connect to/create database
conn = sqlite3.connect('amztracker.db')
c = conn.cursor()
# c.execute('''CREATE TABLE prices(date DATE, asin TEXT, price FLOAT, title TEXT)''')

# Start session and create lists
s = HTMLSession()
asins = []

# Read CSV to list
with open('asins.csv', 'r') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        asins.append(row[0])

# Scrap data
for asin in asins:
    r = s.get(f'https://www.amazon.com/dp/{asin}')
    r.html.render(sleep=1)
    try:
        price_elements = r.html.find('#price_inside_buybox')
        if price_elements:
            price = price_elements[0].text.replace('$','').replace(',','').strip()
        else:
            raise IndexError 
    except IndexError:
        try:
            price_elements = r.html.find('.a-price-whole')
            if price_elements:
                price = price_elements[0].text.replace('$','').replace(',','').strip()
            else:
                raise IndexError  
        except IndexError:
            price = 'Price not found'
    try:
        # Try to get the title using the first selector
        title_elements = r.html.find("#productTitle")
        if title_elements:
            title = title_elements[0].text.strip()
        else:
            raise IndexError  # Trigger IndexError to move to the except block
    except IndexError:
        title = 'Title not found'
    date = datetime.datetime.today()
    c.execute('''INSERT INTO prices VALUES(?,?,?,?)''', (date, asin, price, title))
    print(f'Added data for {asin}, {price}')

conn.commit()
print('Committed new entries to database')





