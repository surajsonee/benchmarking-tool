# this is a test program to see if the package works 

from .plan_comparison import get_new_bills, print_bills, electrical_comparison

user_kwh = 377
user_gj = 6
city = 'acme'
db = 'benchmarking_tool/utility_comparison/plan_comparison/usahelps.db'

bills = get_new_bills(db, city, user_kwh, user_gj)

elec_bills = bills[0]
for i in bills[2]:

    print(i)

#print_bills(bills)