# -*- coding: utf-8 -*-

"""
IND 290C: Project Kiva Zip

Authors:
    - Mehdi Rifai
    
"""


def parse_repayment(soup):
    """
    Given a Kiva zip loan page,
    returns a dict containing the info displayed in the repayment tab
    """    
    

    temp_dict = {}

    repayment_lists = []
    div_tag = soup.find('div',{'class':'grid_8 alpha'}).find('div',{'id':'tab_repayments'})

    if div_tag == None:				
    # If loan event is over, there is no repayment tab
        print "Loan is expired"
        return temp_dict
    else:							
    # If loan event is in progress, repayment tab exists
        value_list = div_tag.findAll('b')
        for element in value_list:
            repayment_lists.append(element.text.strip())

    temp_dict['loan_amount'] = repayment_lists[0]
    temp_dict['monthly_installment'] = repayment_lists[2]
    temp_dict['loan_term'] = repayment_lists[3]
    temp_dict['grace_period'] = repayment_lists[4]
    
    return temp_dict

