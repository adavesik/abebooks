from re import sub
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
import csv

# here we should store generated links for abebooks
links = []

# here we should store grabbed prices
prices = []


def abebook_request(links):
    for link in links[0:1000]:
        tmp_prices = []
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        price_list = soup.find_all('div', {'class': ['srp-item-price']})
        for price in price_list:
            pr = Decimal(sub(r'[^\d.]', '', price.text[4:]))
            tmp_prices.append(pr)
        prices.append(tmp_prices)

    return prices


def build_link(csv_file):
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Book Title']:
                links.append("https://www.abebooks.com/servlet/SearchResults?an="+row['Last Name'].strip()+" "+row['First Name'].strip()+"&bi=0&bx=off&cm_sp=SearchF-_-Advtab1-_-Results&ds=30&recentlyadded=all&sortby=20&sts=t&tn="+ row['Book Title']+"")
            else:
                links.append("https://www.abebooks.com/servlet/SearchResults?an="+row['Last Name'].strip()+" "+row['First Name'].strip()+"&bi=0&bx=off&cm_sp=SearchF-_-Advtab1-_-Results&ds=30&recentlyadded=all&sortby=20&sts=t&tn=" + row['Series Title/Book Title'] + "")

    return links


def generate_csv():
    with open('albert.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        with open('albert_cp.csv', 'a', newline='') as csvfinal:
            fieldnames = ['Box', 'Last Name', 'First Name', 'Series Title/Book Title', 'Series #', 'Book Title', 'Price 1', 'Price 2', 'Avg Price', 'Search Result']
            writer = csv.DictWriter(csvfinal, fieldnames=fieldnames)
            writer.writeheader()
            for row, value in zip(reader, prices):
                if not value:
                    writer.writerow({'Box': row['Box'],
                                     'Last Name': row['Last Name'],
                                     'First Name': row['First Name'],
                                     'Series Title/Book Title': row['Series Title/Book Title'],
                                     'Series #': row['Series #'],
                                     'Book Title': row['Book Title'],
                                     'Price 1': '',
                                     'Price 2': '',
                                     'Avg Price': '',
                                     'Search Result': 'No Result'})
                    print("Wrote: "+row['Last Name']+" book "+ row['Book Title'])

                elif len(value) >= 2:
                    price1 = value[0]
                    price2 = value[1]
                    writer.writerow({'Box': row['Box'],
                                     'Last Name': row['Last Name'],
                                     'First Name': row['First Name'],
                                     'Series Title/Book Title': row['Series Title/Book Title'],
                                     'Series #': row['Series #'],
                                     'Book Title': row['Book Title'],
                                     'Price 1': price1,
                                     'Price 2': price2,
                                     'Avg Price': price_average(value)})
                    print("Wrote: " + row['Last Name'] + " book " + row['Book Title'])
                else:
                    price1 = value[0]
                    price2 = ''
                    writer.writerow({'Box': row['Box'],
                                     'Last Name': row['Last Name'],
                                     'First Name': row['First Name'],
                                     'Series Title/Book Title': row['Series Title/Book Title'],
                                     'Series #': row['Series #'],
                                     'Book Title': row['Book Title'],
                                     'Price 1': price1,
                                     'Price 2': price2,
                                     'Avg Price': price_average(value)})
                    print("Wrote: " + row['Last Name'] + " book " + row['Book Title'])

    print("Writing complete")


def price_average(lst):
    """
Returns the average price of the given book
    :param lst:
    :return:
    """

    return sum(lst) / len(lst)

build_link("albert.csv")
abebook_request(links)
generate_csv()


# for link in links[0:500]:
#     print(link)

#print(prices)

