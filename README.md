# TCGPlayerScraper

![Alpha status](https://img.shields.io/badge/Project%20status-Alpha-red.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI pyversions](https://camo.githubusercontent.com/fd8c489427511a31795637b3168c0d06532f4483/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f77696b6970656469612d6170692e7376673f7374796c653d666c6174)](https://pypi.python.org/pypi/ansicolortags/)

NOTICE: Development on this program has stopped. New version PortalSellerDatabase is now the main prorgam for web scraping card prices.

UPDATE: June 2021 - Tcgplayer has updated their user interface. If you want to use this version, it needs to be updated for the new HTML format. Use sellerportal database instead because it is just better.

Automated WebScraper using Selenium Webdriver and data parsers to automatically retrieve any amount and any specified card based on the configs.

The WebDriver handles all the operations and saves the data in plain text tables for ease of analysis.

This program is incredibly useful for auditing any sort of card collection as long as the TCGPlayer database and live listings are accurate.

The configurations can be found in the .yaml files which contain all the data needed for the data collection process.

Simply use the following config structure and add in as many items as needed:

```
Card Name:
  url: '' # Url 
  edition: 'Near Mint' # card condition
  qty: 1 # Number of cards 
```

# A Typical output for a single entry:
```
Judgment Dragon Ultimate [3] - Market Price: $148.83
+-----------------------+---------------------+---------+-----+
|         Seller        |      Condition      |  Price  | Qty |
+-----------------------+---------------------+---------+-----+
|   97.3% (173 Sales)   | Near Mint Unlimited | $274.99 |  1  |
|    100% (616 Sales)   | Near Mint Unlimited | $275.00 |  1  |
|     100% (1 Sales)    | Near Mint Unlimited | $289.00 |  2  |
|    100% (88 Sales)    | Near Mint Unlimited | $320.00 |  3  |
|    100% (64 Sales)    | Near Mint Unlimited | $348.75 |  3  |
| 98.8% (25,000+ Sales) | Near Mint Unlimited | $399.95 |  3  |
| 99.9% (50,000+ Sales) | Near Mint Unlimited | $799.90 |  1  |
+-----------------------+---------------------+---------+-----+
```

Card name and quantity on top with current market price.
Full up-to-date active listings show Seller and their reputation, condition and edition, price, and quantity available.
Intended to keep track of my personal collection.