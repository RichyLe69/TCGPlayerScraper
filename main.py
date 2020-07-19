from collection import Collection
from utils import scrape_website, sort_market_prices

if __name__ == "__main__":
    my_collection = Collection()
    data = my_collection.get_yaml_data()
    print(scrape_website(data))
    sort_market_prices()


# TODO
# get extra info on condition? search after ')' and up to 'Near Mint' index. only good for foreign w/ pics
# split card_list.yaml into their respective decks, put all
