from re import sub
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
import csv

# here we should store generated links for abebooks
links = []

# here we should store grabbed prices
prices = []


def wonderbook_request(links):
    for link in links[0:10]:
        tmp_prices = []
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        price_list = soup.find_all('p', {'class': ['pcShowProductPrice']})
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
                links.append("http://www.wonderbk.com/productcart/pc/showsearchresults.asp?idcategory_type=0&idcategory=0&Title="+ row['Book Title']+"&Author="+row['Last Name'].strip()+"%2C+"+row['First Name'].strip()+"&ISBN=&Publisher=&pubDateFrom=yyyy&pubDateTo=yyyy&idbinding=0&priceFrom=0&priceUntil=999999999&withstock=-1&sku=&includeSKU=&resultCnt=15&order=1&Submit.x=85&Submit.y=15")
            else:
                links.append("http://www.wonderbk.com/productcart/pc/showsearchresults.asp?idcategory_type=0&idcategory=0&Title="+ row['Series Title/Book Title']+"&Author="+row['Last Name'].strip()+"%2C+"+row['First Name'].strip()+"&ISBN=&Publisher=&pubDateFrom=yyyy&pubDateTo=yyyy&idbinding=0&priceFrom=0&priceUntil=999999999&withstock=-1&sku=&includeSKU=&resultCnt=15&order=1&Submit.x=85&Submit.y=15")

    return links


# 'albert.csv' - input file
# 'albert_final.csv'  - genreted file
def generate_csv():
    with open('albert.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        with open('albert_wonder.csv', 'a', newline='') as csvfinal:
            fieldnames = ['Box', 'Last Name', 'First Name', 'Series Title/Book Title', 'Series #', 'Book Title', 'Minimum Price', 'Maximum Price', 'Avg Price', 'Search Result']
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
                                     'Minimum Price': '',
                                     'Maximum Price': '',
                                     'Avg Price': '',
                                     'Search Result': 'No Result'})
                    print("Wrote: "+row['Last Name']+" book "+ row['Book Title'])

                elif len(value) >= 2:
                    price1 = min(value)
                    price2 = max(value)
                    writer.writerow({'Box': row['Box'],
                                     'Last Name': row['Last Name'],
                                     'First Name': row['First Name'],
                                     'Series Title/Book Title': row['Series Title/Book Title'],
                                     'Series #': row['Series #'],
                                     'Book Title': row['Book Title'],
                                     'Minimum Price': price1,
                                     'Maximum Price': price2,
                                     'Avg Price': price_average(value)})
                    print("Wrote: " + row['Last Name'] + " book " + row['Book Title'])
                else:
                    price1 = min(value)
                    price2 = max(value)
                    writer.writerow({'Box': row['Box'],
                                     'Last Name': row['Last Name'],
                                     'First Name': row['First Name'],
                                     'Series Title/Book Title': row['Series Title/Book Title'],
                                     'Series #': row['Series #'],
                                     'Book Title': row['Book Title'],
                                     'Minimum Price': price1,
                                     'Maximum Price': price2,
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

build_link("albert.csv") # input CVS file
wonderbook_request(links)
generate_csv()


# for link in links[0:500]:
#     print(link)

#print(prices)
