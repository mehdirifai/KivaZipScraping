# -*- coding: utf-8 -*-

"""
IND 290C: Project Kiva Zip

Authors:
    - Mehdi Rifai
    
"""



# -------------------------------------------
# Boolean: integer or not
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
# -------------------------------------------

def parse_lenders(soup):
    """
    Given a Kiva Zip loan page,
    returns the content of the lenders tab
    """
    
     

    temp_dict = {}

    lenders_tab = soup.find('div',{'id':'tab_lenders'})

    # To get the total number of lenders and number of invited
    total_and_invited = lenders_tab.find('div',{'class':'counts clearfix'})
    if total_and_invited:
        total_and_invited = total_and_invited.text.split()
        
        temp_list = []
        for element in total_and_invited:
            if is_int(element):
                temp_list.append(element)
    
        temp_dict['number_of_lenders'] = temp_list[0]
        if len(temp_list) > 1:
            temp_dict['number_of_invited'] = temp_list[1]

    else:
        print "No lenders for this project"
        temp_dict['number_of_lenders'] = 0
    
    
    # --------------------------------------------------------------------------
    # To get the name and location of lenders
    lenders_tab2 = lenders_tab.findAll('div',{'class':'card card_grid clearfix '})

    name_list = []	# Store list of Lenders' names
    loc_list = []	# Store list of Lenders' locations

    for lenders in lenders_tab2:
        name_list.append(lenders.find('span',{'class':'name'}).text.strip())
        loc_list.append(lenders.find('div',{'class':'where'}).text.strip())

    # Organize Lenders' information in dictionary
    temp_dict['lenders_info'] = []
    for info in range(len(name_list)):
        temp_dict['lenders_info'].append(( name_list[info] , loc_list[info] ))
    
    return temp_dict
    

