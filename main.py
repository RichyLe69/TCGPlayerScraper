from collection import Collection
from utils import scrape_website, sort_market_prices, append_console_to_txt, get_yaml_lists
import time


if __name__ == "__main__":

    yaml_lists = (get_yaml_lists('lists.yaml'))
    for card_list in yaml_lists:
        my_collection = Collection(yaml_lists[card_list]['path'])
        data = my_collection.get_yaml_data()
        name = my_collection.get_yaml_name()
        file_path = (scrape_website(data, name))
        sort_market_prices('sorted_pricing/market_prices.yaml')
        sort_market_prices('sorted_pricing/lowest_prices.yaml')
        append_console_to_txt(file_path)
        time.sleep(5)

# TODO
# More buylist yamls: return dad, 5ds staples, swag singles, playset completion

# somehow get it synced to a mysql/db
# somehow get it to run on its own on cloud
