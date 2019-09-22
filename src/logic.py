import json
from datetime import datetime
import calendar
from pymongo import MongoClient
import yelp_api as yelp
import qrcode as qr

client = MongoClient('mongodb+srv://db_user:Password1@uniwards-9pud4.mongodb.net/test?retryWrites=true&w=majority')
db = client.uniwards_db
promos = db.promotions
trans = db.transactions


def create_promo(promotion_request):
    """
    :param promotion: (json object) promotion information as a JSON object
    """
    categories = yelp.search(promotion_request["name"])["businesses"][0]
    categories = categories['categories']
    categories = [category["alias"] for category in categories]

    promotion_request["categories"] = categories
    promotion_request["curr_amount"] = 0
    promotion_request["qualify"] = "false"

    # push to database
    result = promos.insert_one(promotion_request)

    return True

        
def does_qualify(promotion, transaction):
    """
    Checks if a transaction qualifies for this promo
    """
    if promotion["qualify"] == "true":
        # already satsified this
        return True
    
    # check that in the right month
    if promotion["month"] != transaction["month"]:
        return False
    # check that dealing with right company if "monthly specific"
    if promotion["type"] == "monthly_specific" and promotion["name"] != transaction["name"]:
        return False
    # check that if dealing with categories, some match
    if promotion["type"] == "monthly_category" and any([category for category in promotion["categories"] if category in transaction["categories"]]) == False:
        return False
    # check that if dealing with daily, the days match
    if promotion["type"] == "daily_specific" and promotion["day"] != transaction["day"]:
        return False
    elif promotion["type"] == "daily_specific":
        return True

    curr_amount = promotion["curr_amount"]
    qualifier = promotion["minimum"]
    amt = transaction["amount"]

    # update amount
    curr_amount += amt
    result = promos.update_one({'desc': promotion["desc"]}, {"$set": {"curr_amount":curr_amount}}, upsert=True)
    
    if curr_amount >= qualifier:
        # update qualify param
        result = promos.update_one({'desc': promotion["desc"]}, {"$set": {"qualify":"true"}}, upsert=True)
        return True
    else:
        return False


def get_qr_code(promotion):
    """
    Creates a QR code with given discount + saves it to "qrcodes" directory
    """
    discount = "{}%".format(promotion["discount_percent"])
    qr_code = qr.make("{} at {}".format(discount, promotion["name"]))
    qr_code.save('qrcodes/{}_{}_qr_code.jpg'.format(promotion["name"].replace(" ","_"), promotion["_id"]))

    return qr_code


def check_transactions():
    """
    Checks all database transactions against all promotions
    """
    # check if any apply
    for transaction in trans.find():
        for promo in promos.find():
            if does_qualify(promo, transaction):
                print("You qualified for the {} at {}".format(promo["desc"], promo["name"]))

    # return QR codes for qualifying deals
    codes = []
    for promo in promos.find():
        if promo["qualify"] == "true":
            codes.append(get_qr_code(promo))

    return codes


test_transaction = {
    "name": "Mos Mos",
    "categories": [
        "coffeeshop"
    ],
    "amount": 60,
    "month": "january",
    "day": 21,
} 

test_promotions = {
    "test_promos": [
        {
            "name": "Mos Mos",
            "type": "monthly_category",
            "desc": "10_percent_discount",
            "month": "january",
            "minimum": 50,
            "discount_percent": 10,
        },
        {
            "name": "Starbucks",
            "type": "monthly_specific",
            "desc": "20_percent_discount",
            "month": "january",
            "minimum": 50,
            "discount_percent": 20,
        },
        {
            "name": "McDonalds",
            "type": "daily_specific",
            "desc": "30_percent_discount",
            "month": "january",
            "day": 31,
            "discount_percent": 30,
        }
    ],
}

# for promo in test_promotions["test_promos"]:
#     create_promo(promo)
check_transactions()

