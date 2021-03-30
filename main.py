from collection import Collection
from utils import scrape_website, sort_market_prices

if __name__ == "__main__":
    my_collection = Collection()
    data = my_collection.get_yaml_data()
    name = my_collection.get_yaml_name()
    print(scrape_website(data, name))
    sort_market_prices('market_prices.yaml')
    sort_market_prices('lowest_prices.yaml')

# TODO
# somehow get it synced to a mysql/db
# somehow get it to run on its own on cloud
# reorganize cardlists by my current binder placements
# Update buylist with new stuff
