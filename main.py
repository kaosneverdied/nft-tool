import urllib.request
import requests
import logging
import json
import time

from opensea import *

logger = logging.getLogger()
logger.setLevel(logging.INFO) #minimum logging level

#config logging
stream_handler = logging.StreamHandler() 
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO) 
file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG) 
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


#NOTE: Collections are ethermerals, KitPics, etherphrocks
c_list = ["0xeE8C0131aa6B66A2CE3cad6D2A039c1473a79a6d", "0xB1bb22c3101E7653d0d969F42F831BD9aCCc38a5", "0x23FC142A6bA57a37855D9D52702fDA2EC4B4Fd53"]

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 2500)
pd.set_option("max_colwidth", 100)

if __name__ == '__main__':
    source: typing.List[OpenSeaCollection] = []
    for n, c in enumerate(c_list):
        os_collection = OpenSeaCollection(c)
        os_collection.get_assets()
        print(f'Number of assets: {len(os_collection.assets)}')
        for a in os_collection.assets:
            print(f'THE ASSET: {a}')
        source.append(os_collection)
        time.sleep(1) #delate between each request 
    
    for n, os_collection in enumerate(source):
        print(f'COLLECTION {n} : {os_collection.collection_string}')
        for n, asset in enumerate(os_collection.assets):
            print(f'\tASSET {n} : {asset.id}')
            for n, trait in enumerate(asset.traits_list):
                print(f'\t\tTRAIT: {trait.trait_type}')

                




    