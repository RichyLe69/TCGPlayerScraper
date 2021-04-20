from collection import Collection
from utils import scrape_website, sort_market_prices, append_console_to_txt
import time

# My List of Collections
yaml_name = {'decks/buylist.yaml', 'decks/collection.yaml'}
# temporary_list = {'decks/old_collection.yaml' }

split_buylists = {'decks/split_lists/buylist_lightsworn.yaml',
                  'decks/split_lists/buylist_teledad.yaml',
                  'decks/split_lists/buylist_plants.yaml',
                  'decks/split_lists/buylist_extras.yaml'}

split_collections = {'decks/split_lists/collection_deck_builder.yaml',
                     'decks/split_lists/collection_extra_deck.yaml',
                     'decks/split_lists/collection_old_school.yaml',
                     'decks/split_lists/collection_deck_core.yaml'}

starlight = {'decks/old_lists/9-starlight.yaml'} # only use this like once a month just to track starlights

if __name__ == "__main__":

    for card_list in starlight:
        my_collection = Collection(card_list)
        data = my_collection.get_yaml_data()
        name = my_collection.get_yaml_name()
        file_path = (scrape_website(data, name))
        sort_market_prices('market_prices.yaml')
        sort_market_prices('lowest_prices.yaml')
        append_console_to_txt(file_path)
        time.sleep(5)

# TODO
# More buylist yamls: return dad, 5ds staples, goat, mermail, swag singles, playset completion
# somehow get it synced to a mysql/db
# somehow get it to run on its own on cloud
