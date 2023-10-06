from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# URL of the website to scrape
website = 'https://www.cars.com/shopping/results/?stock_type=cpo&makes%5B%5D=mercedes_benz&models%5B%5D=&list_price_max=&maximum_distance=20&zip='

# Send a GET request to the website
response = requests.get(website)
response.status_code

# Soup object
soup = BeautifulSoup(response.content, 'html.parser')

# Results
results = soup.find_all('div', {'class': 'vehicle-card'})
len(results)

# Target necessary data
# Name
results[0].find('h2').get_text()

# Mileage
results[0].find('div', {'class': 'mileage'}).get_text()

# Dealer Name
results[0].find('div', {'class': 'dealer-name'}).get_text().strip()

# Rating
# results[0].find('span', {'class': 'sds-rating__count'}).get_text().strip()
try:
    rating_count = results[0].find(
        'span', {'class': 'sds-rating__count'}).get_text().strip()
except AttributeError:
    rating_count = "Not available"


# Rating Count
try:
    rating_link = results[0].find(
        'span', {'class': 'sds-rating__link'}).get_text()
except AttributeError:
    rating_link = "Not available"

# Price
results[0].find('span', {'class': 'primary-price'}).get_text()


# Put everything together inside a For-Loop
name = []
mileage = []
dealer_name = []
rating = []
review_count = []
price = []

for result in results:

    # name
    try:
        name.append(result.find('h2').get_text())
    except:
        name.append('n/a')

    # mileage
    try:
        mileage.append(result.find('div', {'class': 'mileage'}).get_text())
    except:
        mileage.append('n/a')

    # dealer_name
    try:
        dealer_name.append(result.find(
            'div', {'class': 'dealer-name'}).get_text().strip())
    except:
        dealer_name.append('n/a')

    # rating
    try:
        rating.append(result.find(
            'span', {'class': 'sds-rating__count'}).get_text())
    except:
        rating.append('n/a')

    # review_count
    try:
        review_count.append(result.find(
            'span', {'class': 'sds-rating__link'}).get_text())
    except:
        review_count.append('n/a')

    # price
    try:
        price.append(result.find(
            'span', {'class': 'primary-price'}).get_text())
    except:
        price.append('n/a')


# Create Pandas Dataframe
# dictionary
car_dealer = pd.DataFrame({'Name': name, 'Mileage': mileage, 'Dealer Name': dealer_name,
                          'Rating': rating, 'Review Count': review_count, 'Price': price})

# Data Cleaning
car_dealer['Review Count'] = car_dealer['Review Count'].apply(
    lambda x: x.strip('reviews)').strip('('))


# Output in Excel
car_dealer.to_excel('car_dealer_single_page.xlsx', index=False)


# Part 2 - Pagination
name = []
mileage = []
dealer_name = []
rating = []
review_count = []
price = []

for i in range(1, 11):

    # website in variable
    website = 'https://www.cars.com/shopping/results/?page=' + \
        str(i) + '&page_size=20&dealer_id=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=20&mileage_max=&sort=best_match_desc&stock_type=cpo&year_max=&year_min=&zip='

    # request to website
    response = requests.get(website, headers=headers)

    # soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # results
    results = soup.find_all('div', {'class': 'vehicle-card'})

    # loop through results
    for result in results:

        # name
        try:
            name.append(result.find('h2').get_text())
        except:
            name.append('n/a')

        # mileage
        try:
            mileage.append(result.find('div', {'class': 'mileage'}).get_text())
        except:
            mileage.append('n/a')

        # dealer_name
        try:
            dealer_name.append(result.find(
                'div', {'class': 'dealer-name'}).get_text().strip())
        except:
            dealer_name.append('n/a')

        # rating
        try:
            rating.append(result.find(
                'span', {'class': 'sds-rating__count'}).get_text())
        except:
            rating.append('n/a')

        # review_count
        try:
            review_count.append(result.find(
                'span', {'class': 'sds-rating__link'}).get_text())
        except:
            review_count.append('n/a')

        # price
        try:
            price.append(result.find(
                'span', {'class': 'primary-price'}).get_text())
        except:
            price.append('n/a')

        time.sleep(2)

# dictionary
car_dealer = pd.DataFrame({'Name': name, 'Mileage': mileage, 'Dealer Name': dealer_name,
                          'Rating': rating, 'Review Count': review_count, 'Price': price})

car_dealer['Review Count'] = car_dealer['Review Count'].apply(
    lambda x: x.strip('reviews)').strip('('))
