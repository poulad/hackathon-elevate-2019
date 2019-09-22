# install the requests package using 'python -m pip install requests'
import requests
import json
import calendar
import transactions as t
from pymongo import MongoClient

client = MongoClient('mongodb+srv://db_user:Password1@uniwards-9pud4.mongodb.net/test?retryWrites=true&w=majority')
db = client.uniwards_db
trans_db = db.transactions

def make_transactions():
    # get list of customers
    response = requests.post(
        'https://api.td-davinci.com/api/raw-customer-data',
        headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiNjliMTBiNjgtMjNiNS0zMjAyLWIzZWItM2E3NWM0NTJjMDMwIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiI3MDdkYzM4Zi1lNzgzLTQwNGUtOWU4Zi04YTZhMDliMzVjNDcifQ.F1azY5cuo6fDo_IYpcpOVupieyf6WM7KNpr9GIisK24' },
        json={ 'continuationToken': '' }
    )
    response_data = response.json()

    # iterate through customer ids + collect transactions
    customers = response_data["result"]["customers"]
    for customer in customers:
        id = customer["id"]
        transactions = requests.get(
            'https://api.td-davinci.com/api/customers/{}/transactions'.format(id),
            headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiNjliMTBiNjgtMjNiNS0zMjAyLWIzZWItM2E3NWM0NTJjMDMwIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiI3MDdkYzM4Zi1lNzgzLTQwNGUtOWU4Zi04YTZhMDliMzVjNDcifQ.F1azY5cuo6fDo_IYpcpOVupieyf6WM7KNpr9GIisK24' },
            json={ 'continuationToken': '' }
        )
        transactions = transactions.json()["result"]
        for trans in transactions:
            trans_json = {}

            try:
                trans_json["name"] = trans["merchantName"]
            except KeyError:
                # not a purchase
                continue
            
            month_idx = int(trans["originationDateTime"][5:7])
            month = calendar.month_name[month_idx].lower()
            day = int(trans["originationDateTime"][8:10]) 
            trans_json["amount"] = trans["currencyAmount"]
            trans_json["month"] = month
            trans_json["day"] = day

            # add categories
            trans_json = t.trans_add_category(trans_json)

            # save to db
            if trans_json != False:
                result = trans_db.insert_one(trans_json)

        break

make_transactions()
