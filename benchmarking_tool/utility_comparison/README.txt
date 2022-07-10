april 29, 2021 


This is a function that will return a list of different bill comparisons based on a users kwh used and gj used 

ive made a test.py function to show how to import and use the functions 
main functions imported are get_new_bills and print_bills 

print_bills 
    just used to show the structure of the bills returned 

print_bills(db, city, user_kwh, user_gj)
    db 
        the database string to connnect to the database
    city    
        string of city name dosnt need to be capatalized 
    user_kwh and user_gj
        a float int or string that (gets changed to a float in the program)

    returns:
        a list = [electrical_plans , gas_plans , bundled_plans]
        each of the 3 plans is a list of dictionaries
        
        electrical_plans = dictionaries keys are:
            {'retailer': 'Abode Power', 
             'plan details': 'Variable Electricity Rate - Variable Rate Plan', 
             '$/kwh': 0.08779999999999999, 
             'retail charge': 261.7306, 
             'admin fee': 6.2, 
             'variable distribution': 8.7841, 
             'total variable rate cost': 303.2974172445 or total fixed rate cost 
             }
        gas_plans = dictionarues
            {'retailer': 'Abode Power', 
             'plan details': 'Variable Electricity Rate - Variable Rate Plan', 
             '$/kwh': 0.08779999999999999, 
             'retail charge': 261.7306, 
             'admin fee': 6.2, 
             'variable distribution': 8.7841, 
             'total variable rate cost': 303.2974172445 or total fixed rate}
        bundled_plans = 
            {'retailer': 'EasyMax by ENMAX Energy Corp.', 
            'plan details': 'EasyMax 3-Year Fixed Electricity and Fixed Gas - Fixed Rate Plan', 
            '$/gj': 3.79, 
            '$/kwh': 0.0639, 
            'admin fees': 14.2, 
            'total fixed rate': 171.48137999999997 or total variable rate
            }



updates needed 
    it dose not return the lists in any order only the order they are processed in the data base