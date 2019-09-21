import json
from datetime import datetime


business_request = {
    "name": "Mos Mos",
    "parent_aliases": [
        "coffeeshop"
    ],
    "promotions": [
        {
            "alias": "monthly_category",
            "specific_month": "current",
            "minimum_cad": "50",
            "discount_percent": "10",
        },
        {
            "alias": "monthly_specific",
            "specific_month": "current",
            "minimum_cad": "50",
            "discount_percent": "20",
        },
        {
            "alias": "day_specific",
            "specific_month": "october",
            "specific_day": "31",
            "discount_percent": "10"
        }
    ]
}

test_transaction = {
    "name": "Mos Mos",
    "parent_aliases": [
        "coffeeshop"
    ],
    "amount_cad": "45",
    "month": "september",
    "day": "19",
}

months = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


class Promo():

    def __init__(self, name, category, promo):

        self.name = name
        self.category = category

        self.alias = promo["alias"]
        self.discount = promo["discount_percent"]
        self.month = promo["specific_month"]

        try:
            self.qualifier = promo["specific_day"]
        except:
            self.qualifier = promo["minimum_cad"]

        self.qualify = False


    def __call__(self, transaction):
        """
        Checks if a transaction qualifies for this promo
        """
        today = datetime.today()

        if transaction.name != self.name and self.alias == "monthly_specific":
            return False
        if today.month != month[self.month]:
            return False
        if self.alias == "day_specific" and today.day != self.qualifier:
            return False
        
        

def create_promotions(business_json):
    name = business_json["name"]
    aliases = business_json["parent_aliases"] # list of categories
    promotions = business_json["promotions"]
    valid_promotions = []

    for promo in promotions:
        valid_promotions.append(Promo(name, aliases, promo))

    today = datetime.today()
    print(today.month)
    datem = datetime(today.year, today.month, today.day)
    print(datem)

        

create_promotions(business_request)

