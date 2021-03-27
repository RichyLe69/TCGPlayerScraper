from collection import Collection
from utils import scrape_website, sort_market_prices

if __name__ == "__main__":
    my_collection = Collection()
    data = my_collection.get_yaml_data()
    print(scrape_website(data))
    sort_market_prices('market_prices.yaml')
    sort_market_prices('lowest_prices.yaml')


# TODO
# Make new list for lowest listed prices sorted (not market prices sorted)
# when it takes the lowest price, transfer it over to a new "lowest_prices.yaml". maybe put market in there too?
# Example Card:
#   lowest_listed_price: 100
#   market_price: 75
# then sort the values in "lowest_prices.yaml"

# get extra info on condition? search after ')' and up to 'Near Mint' index. only good for foreign w/ pics
# split card_list.yaml into their respective decks, put all
# Update buylist with new stuff
