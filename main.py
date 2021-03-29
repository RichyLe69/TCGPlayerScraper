from collection import Collection
from utils import scrape_website, sort_market_prices
import time

if __name__ == "__main__":
    start = time.time()
    my_collection = Collection()
    data = my_collection.get_yaml_data()
    print(scrape_website(data))
    sort_market_prices('market_prices.yaml')
    sort_market_prices('lowest_prices.yaml')
    done = time.time()
    print(done-start)


# TODO
# somehow click 50 quantity, near mint, listings without photos
# somehow incorporate 'collection-' and 'buylist-' into name of file
# somehow get it synced to a mysql/db
# somehow get it to run on its own
# reorganize cardlists by my current binder placements
# Update buylist with new stuff
