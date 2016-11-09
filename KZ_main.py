# -*- coding: utf-8 -*-

"""
IND 290C: Project Kiva Zip

Authors:
    - Mehdi Rifai

"""


import requests
from bs4 import BeautifulSoup
from KZ_overview import parse_overview
from KZ_blurbs import parse_blurb
from KZ_lenders import parse_lenders
from KZ_repayment import parse_repayment
import json



test_url = "https://zip.kiva.org/loans/3764"
test_url2 = "https://zip.kiva.org/loans/4507"


data = {}
loan_number = 3071
base_url = "https://zip.kiva.org/loans/{0}"

while True: 
    print ""    
    print "Attempting parse of loan {0}".format(loan_number)
    
    url = base_url.format(loan_number) 
    
    r = requests.get(url)
    sc = r.status_code
    if sc != 200:
        print "Got status code {0} for url {1}".format(sc, url)
        loan_number += 1
        continue
    
    soup = BeautifulSoup(r.content)
    
    if soup.find('h1').text.startswith("We're Sorry"):
        print "No more pages"
        break
    
    if not soup.findAll('a',{'href':'#tab_overview'}):
        print "No interesting content for url {0}".format(url)
        loan_number += 1
        continue
    
    overview = parse_overview(soup)
    blurb = parse_blurb(soup)
    lenders = parse_lenders(soup)
    repayment = parse_repayment(soup)
    
    data[url] = dict(overview.items() + blurb.items() + lenders.items() + repayment.items())
    
    loan_number += 1
    
         
     
json.dump(data, open('kiva_zip_data.json', 'w'))     
