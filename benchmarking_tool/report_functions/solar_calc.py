def solar_calc(number_of_pannels, solar_capacity_kw, kwh_used):

    power_generated_month = solar_capacity_kw * 200 # average 200 hours of sunlight a month in alberta 

    power_savings = power_generated_month - kwh_used

    
    r = {}

    r['solar capacity'] = solar_capacity_kw
    r['power_gererated_month'] = power_generated_month
    r['savings_kwh'] = power_savings
    
    return r