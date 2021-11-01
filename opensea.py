import itertools
from logging import exception
import requests
import logging
import typing
import pandas as pd
from itertools import combinations

logger = logging.getLogger()

class OpenSeaCollection:
    def __init__(self, collection_string : str) -> None:
        self._assets_api = "https://api.opensea.io/api/v1/assets?&asset_contract_address="
        self._events_api = "https://api.opensea.io/api/v1/events?asset_contract_address="        
        self.collection_string = collection_string
        self.assets: typing.List[Asset] = []

    def get_assets(self):
        url = self._assets_api+"&order_direction=desc&offset=0&limit=1"+self.collection_string+"&order_direction=desc&offset=0&limit=10"
        try:
            get_json = requests.get(url)
        except exception as e:
            logger.error(f'connectionmanager.get_asset(): {e}')
        else:
            results = get_json.json()
            for asset in results['assets']:
                a = Asset(asset)
                a.set_traits() 
                a.calculate_rarity()
                self.assets.append(a)

    #FIXME: this method needs some work done. 
    def calculate_rarity(self):
        for asset_a, asset_b in itertools.combinations(self.assets, 2):
            for trait_a in asset_a.traits_list:
                for trait_b in asset_b.traits_list:
                    if trait_a.trait_type == trait_b.trait_type:
                        trait_a.trait_type_r_score += 1
                    
                    if trait_a.value == trait_b.value:
                        trait_a.value_r_score += 1
                    
                    if trait_a.display_type == trait_b.display_type:
                        trait_a.display_type_r_score +=1
                    
                    if trait_a.max_value == trait_b.max_value:
                        trait_a.max_value_r_score +=1
                    
                    if trait_a.trait_count == trait_b.trait_count:
                        trait_a._trait_count_r_score += 1
                    
                    if trait_a.order == trait_b.order:
                        trait_a.order_r_score += 1
            
                asset_a.rarity_score += trait_a.trait_type_r_score + trait_a.value_r_score + trait_a.display_type_r_score + trait_a.max_value_r_score + trait_a._trait_count_r_score + trait_a.order_r_score


    #TODO: Write me
    def get_events(self, events):
        pass

class Asset:
    def __init__(self, data: dict):   
        self.id = data['id'] 
        self.token_id = data['token_id'] 
        self.num_sales = data['num_sales'] 
        self.background_color = data['background_color']
        self.image_url = data['image_url'] 
        self.image_preview_url = data['image_preview_url'] 
        self.image_thumbnail_url = data['image_thumbnail_url'] 
        self.image_original_url = data['image_original_url']
        self.animation_url = data['animation_url']
        self.animation_original_url = data['animation_original_url'] 
        self.name = data['name'] 
        self.description = data['description'] 
        self.external_link = data['external_link'] 
        self.asset_contract = data['asset_contract'] 
        self.permalink = data['permalink']
        self.collection = data['collection'] 
        self.decimals = data['decimals']
        self.token_metadata = data['token_metadata'] 
        self.owner = data['owner'] 
        self.sell_owners = data['sell_orders'] 
        self.creator = data['creator'] 
        self.traits = data['traits'] 
        self.traits_qty = len(data['traits'])
        self.traits_list: typing.List[AssetTraits] = []
        self.last_sale = data['last_sale'] 
        self.top_bid = data['top_bid'] 
        self.listing_date = data['listing_date'] 
        self.is_presale = data['is_presale'] 
        self.transfer_fee_payment_token = data['transfer_fee_payment_token'] 
        self.transfer_fee = data['transfer_fee']
        self.rarity_score = 0
    
    def set_traits(self):
        logger.info(f"Setting traits for {self.token_id} with {self.traits_qty} traits")
        for n, trait in enumerate(self.traits):
            self.traits_list.append(AssetTraits(trait))
    
    def calculate_rarity(self):
        #FIXME: I'm not sure how this is being calculated as my code is too different from the original. If it can be explained I'll impliment it. 
        for attributes in self.traits_list:
            properties = vars(attributes).keys()
            for var in properties:
                #print(properties)
                pass 


class AssetTraits:
    def __init__(self, data) -> None:
        self.trait_type = data['trait_type']
        self.value = data['value'] 
        self.display_type = data['display_type'] 
        self.max_value = data['max_value'] 
        self.trait_count = data['trait_count'] 
        self.order = data['order']
        
        #use these to hold the rarity value of each trait 
        self.trait_type_r_score = 0
        self.value_r_score = 0
        self.display_type_r_score = 0
        self.max_value_r_score: int = 0
        self._trait_count_r_score: int = 0 
        self.order_r_score: int = 0


    
    def __str__(self) -> str:
        return (f'trait_type: {self.trait_type}, value: {self.value}, display_type: {self.display_type}, max_value: {self.max_value}, trait_count: {self.trait_count}, order: {self.order}')

        

    
    
