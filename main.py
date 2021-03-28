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
# reorganize cardlists by my current binder placements
# Update buylist with new stuff
