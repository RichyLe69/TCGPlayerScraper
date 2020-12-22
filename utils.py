from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import prettytable
import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver



def get_seller_stats(text_only, match):
    rep_index = text_only.rfind('%', 0, match.end()) - 4
    rep_index2 = text_only.find(')', rep_index) + 1
    seller_stats = text_only[rep_index:rep_index2].lstrip(' ')
    return seller_stats


def get_price(text_only, match):
    index = text_only.find('$', match.end())
    card_price = text_only[index:index + 8].strip('')
    card_price = card_price.replace('+', '')
    card_price = card_price.replace(',', '')
    raw_value = float(card_price.strip('$').strip('"'))
    return raw_value  # Convert to dollars


# def get_price2(text_only, match): # used for sum of lowest listings available.
#     index = text_only.find('$', match.end())
#     card_price = text_only[index:index + 8].strip('')
#     card_price = card_price.replace('+', '')
#     card_price = card_price.replace(',', '')
#     raw_value = float(card_price.strip('$').strip('"'))
#     return raw_value  # Convert to dollars


def get_quantity(text_only, match):
    index = text_only.find('Add', match.end() + 10)
    quantity = text_only[index - 7:index].strip(' ')
    return int(quantity)


def extract_text_only(input_html):
    start = 'Viewing'  # First word before price table
    end = 'FIRST'  # Last word of price table (pages)
    text_only = input_html.get_text()
    text_only = text_only.strip('\n')
    text_only = text_only.strip('')
    text_only = text_only.replace('\n', ' ')
    text_only = text_only.replace('  ', ' ')
    market_price = get_market_price(text_only)
    text_only = text_only.split(start)[1].split(end)[0]
    return text_only, market_price


def get_market_price(input_html):
    index = input_html.find('Market Price', 0)
    market_price = input_html[index:index + 30]
    market_price = re.findall('\d+\.\d+', market_price)
    market_price = float(market_price[0])
    return market_price


def output_to_txt(card_name, table, market_price, card_quantity):
    current_date = str(datetime.date(datetime.now()))
    with open('full_listings/' + current_date + '.txt', 'a') as myfile:
        myfile.write('{0} [{1}] - Market Price: ${2}\n'.format(card_name, card_quantity, market_price))
        myfile.write(str(table) + '\n')


def scrape_website(collection_data_yaml):
    browser = webdriver.Chrome(executable_path=r'C:\Users\Richard Le\IdeaProjects\TCGPlayerScraper\chromedriver.exe')
    market_price_total = 0
    lowest_listed_price_total = 0
    first = True
    timer = 9
    for card in collection_data_yaml:
        url = collection_data_yaml[card]['url']
        condition_edition = collection_data_yaml[card]['edition']
        card_quantity = collection_data_yaml[card]['qty']

        browser.get(url)
        if first:
            time.sleep(timer)  # wait for page to finish loading (only for 1st time, to select settings)
            first = False

        viewing_present = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.CLASS_NAME, 'sort-toolbar__total-item-count')))
        # print(viewing_present)
        try:
            viewing_present = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.ID, 'priceTable')))
            # print('price table found')
            no_table = False
        except:
            print('no results for: {}'.format(card))
            no_table = True

        if no_table:
            continue  # increments to the next element in for loop.

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(['script', 'style']):
            script.extract()

        text_only = extract_text_only(soup)  # 0 = text_only Price Table data, 1 = market price float value

        my_table = prettytable.PrettyTable(['Seller', 'Condition', 'Price', 'Qty'])
        lowest_value_got = False
        for m in re.finditer(condition_edition, text_only[0]):
            if lowest_value_got is False:
                lowest_listed_price = get_price(text_only[0], m)  # saves lowest listed price
                lowest_value_got = True
            my_table.add_row([get_seller_stats(text_only[0], m),
                              condition_edition,
                              '${:,.2f}'.format(get_price(text_only[0], m)),  # convert raw value to string dollar
                              get_quantity(text_only[0], m)])

        output_to_txt(card, my_table, text_only[1], card_quantity)
        market_price_total += (text_only[1] * card_quantity)
        lowest_listed_price_total += lowest_listed_price * card_quantity
        timer = 7
        # making new yaml w/ market price for calculations
        market_price_yaml_generator(card, text_only[1])
    print('Sum of Market Prices: ${:,.2f}'.format(market_price_total))
    print('Sum of Lowest listings: ${:,.2f}'.format(lowest_listed_price_total))
    return 'Scrape End'


def market_price_yaml_generator(card_name, market_price):
    with open('market_prices.yaml', 'r') as stream:
        current_yaml = yaml.load(stream)
        current_yaml.update({card_name: market_price})

    with open('market_prices.yaml', 'w') as stream:
        yaml.safe_dump(current_yaml, stream)

    return 0


def sort_market_prices():
    with open('market_prices.yaml', 'r') as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            card_list = list()
            for cards in yaml_data:
                card_list.append(cards)
        except yaml.YAMLError as exc:
            print(exc)
    yaml_data = yaml_data
    card_list = card_list

    prices_sorted = {k: v for k, v in sorted(yaml_data.items(), key=lambda x: x[1], reverse=True)}

    my_table = prettytable.PrettyTable(['Card', 'Price'])

    for card in prices_sorted:
        my_table.add_row([card, prices_sorted[card]])

    with open('market_prices_sorted.txt', 'a') as myfile:
        current_date = str(datetime.date(datetime.now()))
        myfile.write(str(current_date) + '\n')
        myfile.write(str(my_table) + '\n')

    # delete contents of market_prices.yaml
    test_dict = {'test': 0}
    with open('market_prices.yaml', 'w') as stream:
        yaml.safe_dump(test_dict, stream)

    return 0
