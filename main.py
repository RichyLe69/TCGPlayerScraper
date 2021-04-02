from collection import Collection
from utils import scrape_website, sort_market_prices, append_console_to_txt
import time

# My List of Collections
yaml_name = {'decks/collection.yaml', 'decks/buylist.yaml'}
# yaml_name = 'decks/new-collection-wip.yaml'

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
# somehow get it synced to a mysql/db
# somehow get it to run on its own on cloud
# reorganize cardlists by my current binder placements
# Update buylist with new stuff
