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

#NOTE: This is just for testing and devleopment purposes right now...

if __name__ == '__main__':
    c = OpenSeaCollection()
    c.get_asset(asset_contract_address="0xeE8C0131aa6B66A2CE3cad6D2A039c1473a79a6d",limit='1')
    for asset in c.assets:
        print(f'{asset.id}')
    
    #source: typing.List[OpenSeaCollection] = []
    #for n, c in enumerate(c_list):
    #    os_collection = OpenSeaCollection(c)
    #    os_collection.get_assets()
    #    os_collection.calculate_rarity()
    #    source.append(os_collection)
    #    time.sleep(1) #delay between each request 
    #
    #for c in source:
    #    for asset in c.assets:
    #        print(f'{asset.id} : Rarity score: {asset.rarity_score}')
