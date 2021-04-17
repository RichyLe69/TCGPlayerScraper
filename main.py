from collection import Collection
from utils import scrape_website, sort_market_prices, append_console_to_txt
import time

# My List of Collections
yaml_name = {'decks/new-collection-wip.yaml'}
# yaml_name =  'decks/buylist.yaml',  'decks/collection.yaml'


split_lists = {'decks/buylist_lightsworn.yaml',
               'decks/buylist_teledad.yaml',
               'decks/buylist_plants.yaml',
               'decks/buylist_extras.yaml'}

if __name__ == "__main__":

    for card_list in yaml_name:
        my_collection = Collection(card_list)
        data = my_collection.get_yaml_data()
        name = my_collection.get_yaml_name()
        file_path = (scrape_website(data, name))
        sort_market_prices('market_prices.yaml')
        sort_market_prices('lowest_prices.yaml')
        append_console_to_txt(file_path)
        time.sleep(5)

# TODO
# then make yaml file of just deck nodes.
# 1 total buylist
#       split buylist: retro format staples, high rarity singles
# 1 total collection
#       split collection: ultimate deck binder, extra deck binder, old school binder, deck core binder


# somehow get it synced to a mysql/db
# somehow get it to run on its own on cloud
