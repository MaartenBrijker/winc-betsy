__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
from peewee import *
from datetime import date

# Searches product based on search term in name and description. Returns a list of dictionary matches.
def search(term):
    matches = Products.select().where(Products.name.contains(term) | Products.description.contains(term))
    return list(matches.dicts()) 

# Returns a list of dictionaries of products of requested user.
def list_user_products(user_id):
    products = Products.select().where(Products.seller == user_id)
    return list(products.dicts())

# Returns a list of dictionaries of products per specified tag.
def list_products_per_tag(tag_id):
    if type(tag_id) is not str:
        print('Tag needs to be a string.. \n Try list_products_per_tag("textiel")')
        return
    
    match = Products.select().join(ProductTags).where(ProductTags.tag_id == tag_id).dicts()
    return list(match)

# Adds a product to the catalog (Products table), takes a user id and the product details as a dictionary.
def add_product_to_catalog(user_id, product: dict):
    if not 'name' in product.keys():
        print("Please specify a name, as 'name': 'your_product_name'")
        return
    if not 'description' in product.keys():
        print("Please specify a description, as 'description': 'your_product_description'")
        return
    if not 'price' in product.keys():
        print("Please specify the price, as 'price': 'your_product_price'")
        return
    if not 'stock' in product.keys():
        print("Please specify the stock, as 'stock': 'your_product_stock'")
        return
    if not 'tags' in product.keys():
        print("Please specify tags, as 'tags': 'list_of_tags'")
        return  
        
    product_id = Products.create(name=product['name'], 
                    seller=user_id, 
                    description=product['description'], 
                    unit_price=product['price'], 
                    current_stock=product['stock'])
    
    # Gets all the existing tags.
    existing_tags = []
    for tag in Tags.select():
        existing_tags.append(tag.name)
    
    # Adds new tags, then adds the product tags to the ProductTags table connecting tags to products.
    for tag in product['tags']:
        if tag not in existing_tags:
            print('ADDING TAG ', tag)
            Tags.create(name=tag)
        check = ProductTags.create(product_id=product_id, tag_id=tag)

# Updates the current_stock variable of a product.
def update_stock(product_id, new_quantity):
    try:
        product = Products.select().where(Products.product_id == product_id).get()
        product.current_stock = new_quantity
        product.save()    
    except DoesNotExist:
        print("Error!: ", DoesNotExist)    
            
# Checks if product in stock. Then adds a tranction to the Transactions table and reduces the available stock of product.
def purchase_product(product_id, buyer_id, quantity: int):
    available_quantity = Products.select().where(Products.product_id == product_id).get().current_stock
    print('Available quantity: ', available_quantity)
    if quantity <= available_quantity and quantity > 0:
        Transactions.create(date=date.today(), buyer_id=buyer_id, product_id=product_id, quantity=quantity)
        new_quantity = available_quantity - quantity
        update_stock(product_id, new_quantity)
        print('New quantity: ', new_quantity)

    else:
        print(f"Not enough stock for {quantity} products. Available quantity: {available_quantity} products")

# Deletes the specific product (row) from the Products Table. 
def remove_product(product_id):
    try:
        Products.get_by_id(product_id).delete_instance()
    except DoesNotExist:
        print("Error!: ", DoesNotExist)
