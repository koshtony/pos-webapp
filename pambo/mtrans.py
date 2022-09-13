import requests
from requests.auth import *
import json
from flask import Flask
def get_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    key="HP9NKPmw9tC8y5d8T7XrOPEF46xQDNE2"
    secret="8StFF1RCXyVqgqxA"
    res=requests.get(url,auth=HTTPBasicAuth(key,secret))
    return json.loads(res.text)["access_token"]
def stk_push():
    url='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers={"Authorization":f"Bearer {get_token()}","Content-type":"application/json"}
    req={
        "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwOTEzMTE0MjQ5",
    "Timestamp": "20220913114249",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254712110972,
    "PartyB": 174379,
    "PhoneNumber": 254712110972,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
    }
    resp=requests.post(url,json=req,headers=headers)
    return {"info":json.loads(resp.text)},200
