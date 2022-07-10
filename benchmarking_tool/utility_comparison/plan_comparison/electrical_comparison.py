def electrical_comparison(elec_df,user_kwh):
    d = elec_df['details'].values
    retailers = elec_df['retailer'].values
    plan_deets = elec_df['plan_details'].values
    user_kwh = float(user_kwh)
    retter = [dict() for _ in range(len(d))]
    count = 0
    for i in d:
        det_dict = eval(i)
        
        if det_dict == {"": {}}:
            count += 1
            continue

        
        for j in det_dict:
            ret = det_dict[j]
            if j == 'Retail':
                try:
                    retail_per_kwh = ret["Retail Charge"]
                    retail_per_kwh = retail_per_kwh.strip('/kWh')
                    retail_per_kwh = float(retail_per_kwh)
                    retail_per_kwh /= 100
                except:
                    retail_per_kwh = float(0)
                    
                    
                try:
                    admin_fee = ret['Admin Fee']
                    admin_fee = admin_fee.strip('/month')
                    admin_fee = admin_fee.strip('/30 days')
                    admin_fee = admin_fee.strip('$')
                    admin_fee = float(admin_fee)
                except:
                    admin_fee = float(0)
                    
                try:
                    elec_trans_charge = ret["Electricity Transaction Charge"]
                    elec_trans_charge = elec_trans_charge.strip('/kWh')
                    elec_trans_charge = elec_trans_charge.strip('$')
                    elec_trans_charge = float(elec_trans_charge)
                except:
                    elec_trans_charge = float(0)

            if j == 'Electricity Distributor Fees - FortisAlberta':
                try:
                    variable_elec_dist = ret["Variable Distribution"]
                    variable_elec_dist = variable_elec_dist.strip('/kWh')
                    variable_elec_dist = float(variable_elec_dist)
                    variable_elec_dist /= 100
                except:
                    variable_elec_dist = float(0)

                try:
                    fixed_elec_dist = ret["Fixed Distribution"]
                    fixed_elec_dist = fixed_elec_dist.strip('/day')
                    fixed_elec_dist = fixed_elec_dist.strip('$')
                    fixed_elec_dist = float(fixed_elec_dist)
                except:
                    fixed_elec_dist = float(0)

                try:
                    variable_trans = ret["Variable Transmission"]
                    variable_trans = variable_trans.strip('/kWh')
                    variable_trans = variable_trans.strip('$')
                    variable_trans = float(variable_trans)
                    variable_trans /= 100
                except:
                    variable_trans = float(0)

                try:
                    balance_pool_rider = ret["Balancing Pool Rider"]
                    balance_pool_rider = balance_pool_rider.strip('/kWh')
                    balance_pool_rider = float(balance_pool_rider)
                    balance_pool_rider /= 100
                except:
                    balance_pool_rider = float(0)

                try:
                    per_kwh_rate_rider = ret["Per kWh Rate Rider"]
                    per_kwh_rate_rider = per_kwh_rate_rider.strip('/kWh')
                    per_kwh_rate_rider = float(per_kwh_rate_rider)
                    per_kwh_rate_rider /= 100
                except:
                    per_kwh_rate_rider = float(0)
                
                try:
                    trans_rate_rider = ret["Transmission Rate Rider"]
                    trans_rate_rider = trans_rate_rider.strip('%')
                    trans_rate_rider = float(trans_rate_rider)
                    trans_rate_rider /= 100
                except:
                    trans_rate_rider = float(0)

                try:
                    local_access_fee = ret["Local Access Fee"]
                    local_access_fee = local_access_fee.strip('/month')
                    local_access_fee = local_access_fee.strip('$')
                    local_access_fee = float(local_access_fee)
                except:
                    local_access_fee = float(0)
            if j == 'Taxes':

                try:
                    gst = ret["GST"]
                    gst = gst.strip('%')
                    gst = float(gst)
                    gst /= 100
                except:
                    gst = float(0)
        
        retail_charge = (retail_per_kwh * user_kwh) + (elec_trans_charge * user_kwh) + admin_fee
        variable_dist = (variable_elec_dist * user_kwh)
        fixed_dist = (fixed_elec_dist * 30)
        variable_transmission = (variable_trans * user_kwh)
        balanceing_pool = (balance_pool_rider * user_kwh)
        per_kwh_rate = (per_kwh_rate_rider * user_kwh)
        trans_rate = (trans_rate_rider * variable_transmission)
        tax = 1 + gst

        total_variable_rate = (variable_dist + retail_charge + variable_transmission + balanceing_pool + per_kwh_rate + trans_rate) * tax

        total_fixed_rate = (fixed_dist + retail_charge + variable_transmission + balanceing_pool + per_kwh_rate + trans_rate) * tax

        if 'Variable Rate Plan' in plan_deets[count]:
            r_dict = {'retailer': retailers[count], 
                    'plan details': plan_deets[count],
                    '$/kwh': retail_per_kwh, 
                    'retail charge': retail_charge, 
                    'admin fee': admin_fee, 
                    'variable distribution': variable_dist, 
                    'total variable rate cost': total_variable_rate}

        elif 'Fixed Rate Plan' in plan_deets[count]:
            r_dict = {'retailer': retailers[count], 
                    'plan details': plan_deets[count],
                    '$/kwh': retail_per_kwh, 
                    'retail charge': retail_charge, 
                    'admin fee': admin_fee,  
                    'fixed distribution': fixed_dist,   
                    'total fixed rate cost': total_fixed_rate,}
        else:
            r_dict = {'retailer': retailers[count], 
                    'plan details': plan_deets[count],
                    '$/kwh': retail_per_kwh, 
                    'retail charge': retail_charge, 
                    'admin fee': admin_fee, 
                    'variable distribution': variable_dist, 
                    'fixed distribution': fixed_dist,   
                    'total fixed rate cost': total_fixed_rate,
                    'total variable rate cost': total_variable_rate}

        #print(type(r_dict))
        
        retter[count] = r_dict
        count += 1

        
    return retter