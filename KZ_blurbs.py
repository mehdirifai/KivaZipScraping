# -*- coding: utf-8 -*-

"""
IND 290C: Project Kiva Zip

Authors:
    - Mehdi Rifai

    
"""


import re

# To handle numbers with commas, we import another lib
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 



def parse_blurb(soup):
    """
    Given a Kiva Zip loan URL,
    returns a dict with all the info contained in the blurbs
    on the right side of the loan page.
    
    Return Format: dict
    {
        description: str
        percentage_raised: int
        amount_to_go: int
        listed_date: str
        indusry: [ str ] 
        years_in_operation: str
        trustee: str
        trustee_type: str
        trustee_location: str
        trustee_on_zip_since: str
        trustee_loans_endorsed: int
        trustee_total_endorsed_value: int
        trustee_raised: int
        trustee_paying_on_time: int
        trustee_paying_back_late: int
        trustee_repaid_in_full: int
        trustee_defaulted: int
        trustee_repayment_rate: int
        trustee_why_endorsing: str
    }    
    """
        
    result = {}
    
    # Parsing the first blurb
    first_blurb = soup.find('div', {'class': 'about loan_summary box box_round'})
    
    result['description'] = first_blurb.find('p').text.lower()
    
    # For the loan progress, we have to check if the loan is over
    # In which case the info is displayed a bit differently
    progress = first_blurb.find('div', {'class': 'progress progress_loan'})
    disbursed = progress.find('div', {'class': 'progress_general box_round'})
    if disbursed:
        result['percentage_raised'] = 100
        result['amount_to_go'] = 0
    else:
        result['percentage_raised'] = int(progress.find('span', {'class': 'text_number'}).text[:-1])
        regex = re.compile('[0-9,]*')        
    
        amount = regex.findall( progress.find('div', {'class': 'progress_status'} ).text )
        amount = filter(None, amount)
        if len(amount) > 1:
            result['amount_to_go'] = locale.atoi(amount[2])
        else:
            result['amount_to_go'] = 0
    
    
    # Next 3 pieces of info are gathered in a list
    # But they are already scraped in the repayment tab
    # So we only store the listed date
    summary = soup.find('dl', {'class': 'summary'})
    dds = summary.findAll('dd')
    # result['repayment_term'] = dds[0].text
    # result['grace_period'] = dds[1].text
    result['listed_date'] = dds[2].span.text
    
    
    # Parsing the second blurb
    sec_blurb = soup.find('div', {'class': 'loan_business box box_round'})
    dds2 = sec_blurb.findAll('dd')
    
    result['industry'] = dds2[0].text.split(' / ')
    result['years_in_operation'] = dds2[1].text


    # Parsing the third blurb
    thd_blurb = soup.find('div', {'class': 'loan_trustee box box_round'})
    
    result['trustee'] = thd_blurb.find('div', {'class': 'who'}).a.text
    
    dds3 = thd_blurb.findAll('dd')
    
    result['trustee_type'] = dds3[0].text
    result['trustee_location'] = dds3[1].text
    result['trustee_on_zip_since'] = dds3[3].text[1:13]
    result['trustee_loans_endorsed'] = int(dds3[4].text[1:])
    result['trustee_total_endorsed_value'] = locale.atoi(dds3[5].text[2:])
    
    # For the following data, the page doesn't necessarily display a int
    # Therefore, we must verify the string before adding it to the dict    
    if dds3[6].text.startswith(' Not enough data'):
        result['trustee_raised'] = dds3[6].text[1:]
    else:
        result['trustee_raised'] = int(dds3[6].text[1:])
    
    if dds3[7].text.startswith(' Not enough data'):
        result['trustee_paying_on_time'] = dds3[7].text[1:]
    else:
        result['trustee_paying_on_time'] = int(dds3[7].text[1:])
    
    if dds3[8].text.startswith(' Not enough data'):
        result['trustee_paying_back_late'] = dds3[8].text[1:]
    else:
        result['trustee_paying_back_late'] = int(dds3[8].text[1:])
    
    if dds3[9].text.startswith(' Not enough data'):
        result['trustee_repaid_in_full'] = dds3[9].text[1:]
    else:
        result['trustee_repaid_in_full'] = int(dds3[9].text[1:])
    
    if dds3[10].text.startswith(' Not enough data'):
        result['trustee_defaulted'] = dds3[10].text[1:]
    else:
        result['trustee_defaulted'] = int(dds3[10].text[1:])
    
    if dds3[11].text.startswith(' Not enough data'):
        result['trustee_repayment_rate'] = dds3[11].text[1:]
    elif dds3[11].text.startswith(" Less than 50%"):
        result['trustee_repayment_rate'] = dds3[11].text[1:]
    else:
        result['trustee_repayment_rate'] = int(dds3[11].text[1:-1])

    result['trustee_why_endorsing'] = thd_blurb.find('div', {'class': 'answer'}).p.text
    
    
    return result



