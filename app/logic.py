import json
from datetime import datetime
import calendar

business_request = {
    "name": "Mos Mos",
    "parent_aliases": [
        "coffeeshop"
    ],
    "promotions": [
        {
            "type": "monthly_category",
            "desc": "10_percent_discount",
            "specific_month": "current",
            "minimum": "50",
            "discount_percent": "10",
        },
        {
            "type": "monthly_specific",
            "desc": "20_percent_discount",
            "specific_month": "current",
            "minimum": "50",
            "discount_percent": "20",
        },
        {
            "type": "day_specific",
            "desc": "halloween_special",
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
    "amount": "45",
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

    def __init__(self, name, categories, promo):

        self.name = name
        self.promo_categories = categories

        self.type = promo["type"]
        self.description = promo["desc"]
        self.discount = promo["discount_percent"]
        self.month = promo["specific_month"]
        if self.month == "current":
            self.month = calendar.month_name[datetime.today().month].lower()

        try:
            self.qualifier = promo["specific_day"]
        except:
            self.qualifier = promo["minimum"]

        self.qualify = False


    def __call__(self, transaction):
        """
        Checks if a transaction qualifies for this promo
        """
        today = datetime.today()
        trans_categories = transaction["parent_aliases"]

        if transaction["name"] != self.name and self.type == "monthly_specific":
            return False
        if today.month != months[self.month]:
            return False
        if self.type == "day_specific" and today.day == int(self.qualifier):
            return True

        if self.type == "monthly_category" and not any([category for category in self.promo_categories if category in trans_categories]):
            # none of the categories match
            return False

        # update money spent
        # DO SOMETHING W/ DATABASE
        curr_amount = 0
        # check if it meets minimum requirement
        if curr_amount >= int(self.qualifier):
            return True
        else:
            return False

    
    def __str__(self):
        return "You qualified for the {} at {}".format(self.description, self.name)

        

def create_promotions(business_json):
    name = business_json["name"]
    aliases = business_json["parent_aliases"] # list of categories
    promotions = business_json["promotions"]
    valid_promotions = []

    for promo in promotions:
        valid_promotions.append(Promo(name, aliases, promo))

    return valid_promotions

def check_transaction(transaction, promos):
    do_qualify = [promo(transaction) for promo in promos]
    do_qualify = [True, False, True]
    if any(do_qualify):
        [print(promos[i]) for i in range(len(promos)) if do_qualify[i] == True]
        return True
        

# promotions = create_promotions(business_request)
# check_transaction(test_transaction, promotions)
