import itertools
from logging import exception
import requests
import logging
import typing
import pandas as pd
from itertools import combinations

logger = logging.getLogger()

class OpenSeaCollection:
    def __init__(self) -> None:
        self.assets: typing.List[Asset] = []
        self._baseurl_assets = "https://api.opensea.io/api/v1/assets?"
        self._baseurl_events = "https://api.opensea.io/api/v1/events?"
    

    def _make_request(self, url):
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
    
    

    #REF: https://docs.opensea.io/reference/getting-assets
    def get_asset(self, owner: typing.Union[str, None] = None, token_ids: typing.Union[str, None] = None, 
    asset_contract_address: typing.Union[str, None] = None, asset_contract_addresses: typing.Union[typing.List, None] = None, 
    order_by: typing.Union[str, None] = None, order_direction: typing.Union[str, None] = None, offset: typing.Union[str, None] = None, 
    limit: typing.Union[str, None] = None, collection: typing.Union[str, None] = None):
        
        req_str = []        
        if owner is not None: 
            req_str.append(f"owner={owner}")
        if token_ids is not None:
            req_str.append(f"&token_ids={token_ids}") if len(req_str) >=0 else req_str.append(f"token_ids={token_ids}")
        if asset_contract_address is not None:
            req_str.append(f"&asset_contract_address={asset_contract_address}") if len(req_str) >=0 else req_str.append(f"asset_contract_address={asset_contract_address}")
        if asset_contract_addresses is not None:
            req_str.append(f"&asset_contract_addresses={asset_contract_addresses}") if len(req_str) >=0 else req_str.append(f"asset_contract_addresses={asset_contract_addresses}")
        if order_by is not None:
            req_str.append(f"&order_by={order_by}") if len(req_str) >=0 else req_str.append(f"order_by={order_by}")
        if order_direction is not None:
            req_str.append(f"&order_direction={order_direction}") if len(req_str) >=0 else req_str.append(f"order_direction={order_direction}")
        if offset is not None:
            req_str.append(f"&offset={offset}") if len(req_str) >=0 else req_str.append(f"offset={offset}")
        if limit is not None:
            req_str.append(f"&limit={limit}") if len(req_str) >=0 else req_str.append(f"limit={limit}")
        if collection is not None:
            req_str.append(f"&collection={collection}") if len(req_str) >=0 else req_str.append(f"collection={collection}")
        
        url_request_string = self._baseurl_assets + ''.join(req_str)
        self._make_request(url_request_string)
    


    #FIXME: Need error handling etc
    #REF: https://docs.opensea.io/reference/retrieving-asset-events
    def get_events(self, asset_contract_address: typing.Union[str, None] = None, collection_slug: typing.Union[str, None] = None, 
    token_id : typing.Union[str, None] = None, account_address : typing.Union[str, None] = None, event_type: typing.Union[str, None] = None, 
    only_opensea: typing.Union[str, None] = None, auction_type: typing.Union[str, None] = None, offset: typing.Union[str, None] = None, 
    limit: typing.Union[str, None] = None, occurred_before: typing.Union[str, None] = None, occurred_after: typing.Union[str, None] = None):
        
        req_str = []

        if asset_contract_address is not None:
            req_str.append(f"asset_contract_address={asset_contract_address}") 
        if collection_slug is not None:
            req_str.append(f"&collection_slug={collection_slug}") if len(req_str) >= 0 else req_str.append(f"collection_slug={collection_slug}")  
        if token_id is not None:
            req_str.append(f"&token_id={token_id}") if len(req_str) >= 0 else req_str.append(f"token_id={token_id}")  
        if account_address is not None:
            req_str.append(f"&account_address={account_address}") if len(req_str) >= 0 else req_str.append(f"account_address={account_address}")  
        if event_type is not None:
            req_str.append(f"&event_type={event_type}") if len(req_str) >= 0 else req_str.append(f"event_type={event_type}")  
        if only_opensea is not None:
            req_str.append(f"&only_opensea={only_opensea}") if len(req_str) >= 0 else req_str.append(f"only_opensea={only_opensea}")  
        if auction_type is not None:
            req_str.append(f"&auction_type={auction_type}") if len(req_str) >= 0 else req_str.append(f"auction_type={auction_type}")  
        if offset is not None:
            req_str.append(f"&offset={offset}") if len(req_str) >= 0 else req_str.append(f"offset={offset}")  
        if limit is not None:
            req_str.append(f"&limit={limit}") if len(req_str) >= 0 else req_str.append(f"limit={limit}")             
        if occurred_before is not None:
            req_str.append(f"&occurred_before={occurred_before}") if len(req_str) >= 0 else req_str.append(f"occurred_before={occurred_before}")             
        if occurred_after is not None:
            req_str.append(f"&occurred_after={occurred_after}") if len(req_str) >= 0 else req_str.append(f"occurred_after={occurred_after}")

        url_request_string = self._baseurl_events + ''.join(req_str) 
        self._make_request(url_request_string)            
 
    #REF: https://docs.opensea.io/reference/retrieving-collections 
    def get_collections(self, asset_owner: typing.Union[str, None] = None, offset: typing.Union[str, None] = None, limit: typing.Union[str, None] = None):
        req_str = []

        if asset_owner is not None:
            req_str.append(f"asset_owner={asset_owner}")
        if offset is not None:
            req_str.append(f"&offset={offset}") if len(req_str) >= 0 else req_str.append(f"&offset={offset}")
        if limit is not None:
            req_str.append(f"&limit={limit}") if len(req_str) >= 0 else req_str.append(f"&limit={limit}")

        url_request_string = self._baseurl_events + ''.join(req_str) 
        self._make_request(url_request_string)            
        

    #TODO: write
    def get_bundles(self, on_sale: typing.Union[str, None] = None, owner: typing.Union[str, None] = None, asset_contract_address: typing.Union[str, None] = None, 
    token_ids: typing.Union[str, None] = None, limit: typing.Union[str, None] = None, offset: typing.Union[str, None] = None):
        req_str = []
        if on_sale is not None:
            req_str.append(f"on_sale={on_sale}")
        if owner is not None:
            req_str.append(f"&owner={owner}") if len(req_str) >= 0 else req_str.append(f"owner={owner}") 
        if asset_contract_address is not None:
            req_str.append(f"&asset_contract_address={asset_contract_address}") if len(req_str) >= 0 else req_str.append(f"asset_contract_address={asset_contract_address}") 
        if token_ids is not None:
            req_str.append(f"&token_ids={token_ids}") if len(req_str) >= 0 else req_str.append(f"token_ids={token_ids}") 
        if limit is not None:
            req_str.append(f"&limit={limit}") if len(req_str) >= 0 else req_str.append(f"limit={limit}") 
        if offset is not None:
            req_str.append(f"&offset={offset}") if len(req_str) >= 0 else req_str.append(f"offset={offset}") 

        url_request_string = self._baseurl_events + ''.join(req_str) 
        self._make_request(url_request_string)            

    def get_asset_single(self, asset_contract_address: typing.Union[str, None] = None, token_id: typing.Union[str, None] = None, account_address: typing.Union[str, None] = None):
        req_str = []
        
        if asset_contract_address is not None:
            req_str.append(f"asset_contract_address={asset_contract_address}")
        if token_id is not None:
            req_str.append(f"&token_id={token_id}") if len(req_str) >= 0 else req_str.append(f"token_id={token_id}")
        if account_address is not None:
            req_str.append(f"&account_address={account_address}") if len(req_str) >= 0 else req_str.append(f"account_address={account_address}")
        url_request_string = self._baseurl_events + ''.join(req_str) 
        self._make_request(url_request_string)            

    # REF: https://docs.opensea.io/reference/retrieving-a-single-contract 
    def get_contract_single(self, asset_contract_address: typing.Union[str, None] = None):
        if asset_contract_address is not None:
            url_request_string = self._baseurl_events + "asset_contract_address=" + asset_contract_address
        else:
            url_request_string = self._baseurl_events
        self._make_request(url_request_string)            
        

    def get_collection_single(self, collection_slug):
        if collection_slug is not None:
            url_request_string = self._baseurl_events + "collection_slug=" + collection_slug
        else:
            url_request_string = self._baseurl_events
        self._make_request(url_request_string)            
        

    #REF: https://docs.opensea.io/reference/retrieving-collection-stats 
    def get_collection_stats(self, collection_slug):
        if collection_slug is not None:
            url_request_string = self._baseurl_events + "collection_slug=" + collection_slug + "/stats"
        else:
            url_request_string = self._baseurl_events
        self._make_request(url_request_string)            
        


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

        

    
    
