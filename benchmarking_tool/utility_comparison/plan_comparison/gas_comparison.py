# gas function 
def gas_comparison(gas_df,user_gj):
    dee = gas_df['details'].values
    retailers = gas_df['retailer'].values
    plan_deets = gas_df['plan_details'].values
    user_gj = float(user_gj)
    retter = [dict() for _ in range(len(dee))]
    count = 0
    
    
    for i in dee:
        det_dict = eval(i)
        if det_dict == {"": {}}:
            count += 1
            continue
        
        for j in det_dict:
            ret = det_dict[j]

            if j == 'Retail':
                try:
                    gas_rate = ret["Retail Charge"]
                    gas_rate = gas_rate.strip('/GJ')
                    gas_rate = gas_rate.strip('$')
                    gas_rate = float(gas_rate)
                except:
                    gas_rate = float(0) 
                try:
                    admin_fee = ret['Admin Fee']
                    admin_fee = admin_fee.strip('/month')
                    admin_fee = admin_fee.strip('/30 days')
                    admin_fee = admin_fee.strip('$')
                    admin_fee = float(admin_fee)
                except:
                    admin_fee = float(0)
                    
                try:
                    gj_trans_charge = ret["Transaction Charge"]
                    gj_trans_charge = gj_trans_charge.strip('/GJ')
                    gj_trans_charge = gj_trans_charge.strip('$')
                    gj_trans_charge = float(gj_trans_charge)
                except:
                    gj_trans_charge = float(0)

            if j == 'Natural Gas Distributor Fees - ATCO Gas South':

                try:
                    variable_gas_dist = ret["Variable Distribution"]
                    variable_gas_dist = variable_gas_dist.strip('/GJ')
                    variable_gas_dist = variable_gas_dist.strip('$')
                    variable_gas_dist = float(variable_gas_dist)
                except:
                    variable_gas_dist = float(0)

                try:
                    fixed_gas_dist = ret["Fixed Distribution"]
                    fixed_gas_dist = fixed_gas_dist.strip('/day')
                    fixed_gas_dist = fixed_gas_dist.strip('$')
                    fixed_gas_dist = float(fixed_gas_dist)
                except:
                    fixed_gas_dist = float(0)

                try:
                    per_day_rider = ret["Per Day Rider"]
                    per_day_rider = per_day_rider.strip('/day')
                    per_day_rider = per_day_rider.strip('$')
                    per_day_rider = float(per_day_rider)
                except:
                    per_day_rider = float(0)

                try:
                    per_gj_rider = ret["Per GJ Rate Rider"]
                    per_gj_rider = per_gj_rider.strip('/GJ')
                    per_gj_rider = per_gj_rider.strip('$')
                    per_gj_rider = float(per_gj_rider)
                except:
                    per_gj_rider = float(0)

                try:
                    muni_fran_fee = ret["Municipal Franchise Fee"]
                    muni_fran_fee = muni_fran_fee.strip('/month')
                    muni_fran_fee = muni_fran_fee.strip('$')
                    muni_fran_fee = float(muni_fran_fee)
                except:
                    muni_fran_fee = float(0)

            if j == 'Taxes':
                
                try:
                    fed_tax = ret["Federal Carbon Tax"]
                    fed_tax = fed_tax.strip('/GJ')
                    fed_tax = fed_tax.strip('$')
                    fed_tax = float(fed_tax)
                except:
                    fed_tax = float(0)

                try:
                    gst = ret["GST"]
                    gst = gst.strip('%')
                    gst = float(gst)
                    gst /= 100
                except:
                    gst = float(0)

        retail_gas_charge =  (gas_rate * user_gj) + (gj_trans_charge * user_gj) + admin_fee
        variable_dist = (variable_gas_dist * user_gj)
        fixed_dist = (fixed_gas_dist * 30)
        variable_transmission = (variable_gas_dist * user_gj)
        per_day_r = (per_day_rider * user_gj)
        per_gj_rate = (per_gj_rider * user_gj)
        carbon_tax = fed_tax * user_gj
        tax = 1 + gst

        total_variable_rate = (variable_dist + gas_rate + variable_transmission + per_day_r + per_gj_rate + muni_fran_fee + carbon_tax) * tax

        total_fixed_rate = (fixed_dist + gas_rate + variable_transmission + per_day_rider + per_gj_rate + muni_fran_fee + carbon_tax) * tax


        if 'Variable Rate Plan' in plan_deets[count]:
            r_dict =   {'retailer': retailers[count], 
                        'plan details': plan_deets[count],
                        '$/gj':   gas_rate, 
                        'retail charge': retail_gas_charge, 
                        'admin fee': admin_fee, 
                        'variable distribution': variable_dist, 
                        'municipal franchise fee': muni_fran_fee,
                        'carbon tax': carbon_tax,
                        'total variable rate': total_variable_rate}

        elif 'Fixed Rate Plan' in plan_deets[count]:
            r_dict =   {'retailer': retailers[count], 
                        'plan details': plan_deets[count],
                        '$/gj':   gas_rate, 
                        'retail charge': retail_gas_charge, 
                        'admin fee': admin_fee,  
                        'fixed distribution': fixed_dist, 
                        'municipal franchise fee': muni_fran_fee,
                        'carbon tax': carbon_tax,
                        'total fixed rate': total_fixed_rate}

        else:
            r_dict =   {'retailer': retailers[count], 
                        'plan details': plan_deets[count],
                        '$/gj':   gas_rate, 
                        'retail charge': retail_gas_charge, 
                        'admin fee': admin_fee, 
                        'variable distribution': variable_dist, 
                        'fixed distribution': fixed_dist, 
                        'municipal franchise fee': muni_fran_fee,
                        'carbon tax': carbon_tax,
                        'total variable rate': total_variable_rate,
                        'total fixed rate': total_fixed_rate}

        retter[count] = r_dict

        count += 1

    return retter