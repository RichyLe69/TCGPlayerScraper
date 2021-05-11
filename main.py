from collection import Collection
from utils import scrape_website, sort_market_prices, append_console_to_txt, get_yaml_lists
import time
from selenium import webdriver

timer = 3
setup = True
url = 'https://shop.tcgplayer.com/yugioh/turbo-pack-booster-one-pack/judgment-dragon'

if __name__ == "__main__":
    browser = webdriver.Chrome(executable_path=r'C:\Users\Richard Le\IdeaProjects\TCGPlayerScraper\chromedriver.exe')
    browser.get(url)
    if setup:
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
        setup = False

    yaml_lists = (get_yaml_lists('lists.yaml'))
    for card_list in yaml_lists:
        my_collection = Collection(yaml_lists[card_list]['path'])
        data = my_collection.get_yaml_data()
        name = my_collection.get_yaml_name()
        file_path = (scrape_website(data, name, browser))
        sort_market_prices('sorted_pricing/market_prices.yaml')
        sort_market_prices('sorted_pricing/lowest_prices.yaml')
        append_console_to_txt(file_path)
        time.sleep(5)
    browser.quit()

# TODO
# More buylist yamls: return dad, 5ds staples, swag singles, playset completion
# tabular columns, pricing continuing horizontally, compare prices to last check.

# day               123 125
# name_list         123 125
# sum of market:    123 125
# sum of lowest:    123 125 >

# somehow get it synced to a mysql/db
# somehow get it to run on its own on cloud
