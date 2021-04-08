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
import os

current_date = str(datetime.date(datetime.now()))
current_year_full = datetime.now().strftime('%Y')  # 2018
current_month = datetime.now().strftime('%m')  # 02 //This is 0 padded
current_month_text = datetime.now().strftime('%h')  # Feb


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
    try:
        market_price = float(market_price[0])
    except IndexError:
        market_price = 0
    return market_price


def output_to_txt(card_name, table, market_price, card_quantity, name):
    yaml_name = name + '-' + current_date + '.txt'
    directory = 'full_listings/{0}/{1}-{2}'.format(current_year_full, current_month, current_month_text)
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass  # directory already exists

    file_path = 'full_listings/{0}/{1}-{2}/{3}'.format(current_year_full, current_month, current_month_text, yaml_name)
    with open(file_path, 'a') as my_file:
        my_file.write('{0} [{1}] - Market Price: ${2}\n'.format(card_name, card_quantity, market_price))
        my_file.write(str(table) + '\n')
        return file_path


def output_to_txt_console(string):
    txt_console = 'console.txt'
    with open(txt_console, 'a') as my_file:
        my_file.write(string + '\n')


def scrape_website(collection_data_yaml, name):
    delete_console_txt()
    start = time.time()
    browser = webdriver.Chrome(executable_path=r'C:\Users\Richard Le\IdeaProjects\TCGPlayerScraper\chromedriver.exe')
    market_price_total = 0
    lowest_listed_price_total = 0
    lowest_listed_price = 0
    first = True
    timer = 5
    for card in collection_data_yaml:
        url = collection_data_yaml[card]['url']
        condition_edition = collection_data_yaml[card]['edition']
        card_quantity = collection_data_yaml[card]['qty']

        browser.get(url)
        if first:
            time.sleep(timer)  # wait for page to finish loading (only for 1st time, to select settings)
            browser.find_element_by_xpath(
                "(//ancestor::a[@class='filter-facet__link'])[position()=6]").click()  # Hard coded click on "Listings Without Photos" - 6th Box down
            time.sleep(timer)
            browser.find_element_by_xpath(
                "(//ancestor::a[@class='filter-facet__link'])[position()=7]").click()  # Hard coded click on "Near Mint" - 7th Box down
            time.sleep(timer)
            browser.find_element_by_xpath("(//ancestor::select[@class='sort-toolbar__select form-control'])[2]").click()
            time.sleep(timer)
            browser.find_element_by_xpath("//ancestor::option[@value='50']").click()
            time.sleep(timer)  # wait for page to finish loading (only for 1st time, to select settings)
            first = False
        timer = 7
        viewing_present = WebDriverWait(browser, timer).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sort-toolbar__total-item-count')))
        # print(viewing_present)
        try:
            viewing_present = WebDriverWait(browser, timer).until(EC.presence_of_element_located((By.ID, 'priceTable')))
            # print('price table found')
            no_table = False
        except:
            print('No Results for: {}'.format(card))
            output_to_txt_console('No Results for: {}'.format(card))
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

        file_path = output_to_txt(card, my_table, text_only[1], card_quantity, name)
        market_price_total += (text_only[1] * card_quantity)
        lowest_listed_price_total += lowest_listed_price * card_quantity

        # making new yaml w/ market & lowest price for calculations and sorting
        price_yaml_generator(card, lowest_listed_price, 'lowest_prices.yaml')
        price_yaml_generator(card, text_only[1], 'market_prices.yaml')
    print('Sum of Market Prices: ${:,.2f}'.format(market_price_total))
    print('Sum of Lowest listings: ${:,.2f}'.format(lowest_listed_price_total))
    output_to_txt_console('Sum of Market Prices: ${:,.2f}'.format(market_price_total))
    output_to_txt_console('Sum of Lowest listings: ${:,.2f}'.format(lowest_listed_price_total))
    done = time.time()
    print(done - start)
    return file_path


def price_yaml_generator(card_name, market_price, yaml_name):
    with open(yaml_name, 'r') as stream:
        current_yaml = yaml.load(stream)
        current_yaml.update({card_name: market_price})

    with open(yaml_name, 'w') as stream:
        yaml.safe_dump(current_yaml, stream)

    return 0


def sort_market_prices(yaml_name):
    with open(yaml_name, 'r') as stream:
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

    sorted_yaml = yaml_name.replace('.yaml', '') + '_sorted.txt'
    with open(sorted_yaml, 'a') as my_file:
        current_date = str(datetime.date(datetime.now()))
        my_file.write(str(current_date) + '\n')
        my_file.write(str(my_table) + '\n')

    # delete contents of market_prices.yaml
    delete_yaml_contents(yaml_name)
    return 0


def delete_yaml_contents(yaml_name):
    test_dict = {'test': 0}
    with open(yaml_name, 'w') as stream:
        yaml.safe_dump(test_dict, stream)


def append_console_to_txt(path):
    console = 'console.txt'
    with open(console, 'r') as console:
        console_data = console.read()
    with open(path, 'r') as original:
        data = original.read()
    with open(path, 'w') as modified:
        modified.write(console_data + "\n" + data)
    delete_console_txt()


def delete_console_txt():
    console = 'console.txt'
    with open(console, 'w') as f:
        f.write('')
