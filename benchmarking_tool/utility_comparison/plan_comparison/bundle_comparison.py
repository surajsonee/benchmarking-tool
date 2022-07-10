# bundled plan comparison 
# gas function 
def bundle_comparison(bundle_df,user_gj,user_kwh):
    dee = bundle_df['details'].values
    retailers = bundle_df['retailer'].values
    plan_deets = bundle_df['plan_details'].values
    user_gj = float(user_gj)
    user_kwh = float(user_kwh)
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
                    elec_admin_fee = ret["Electricity Admin Fee"]
                    elec_admin_fee = elec_admin_fee.strip('/month')
                    elec_admin_fee = elec_admin_fee.strip('/30 days')
                    elec_admin_fee = elec_admin_fee.strip('$')
                    elec_admin_fee = float(elec_admin_fee)
                except:
                    elec_admin_fee = float(0) 

                try:
                    gas_admin_fee = ret["Natural Gas Admin Fee"]
                    gas_admin_fee = gas_admin_fee.strip('/month')
                    gas_admin_fee = gas_admin_fee.strip('/30 days')
                    gas_admin_fee = gas_admin_fee.strip('$')
                    gas_admin_fee = float(gas_admin_fee)
                except:
                    gas_admin_fee = float(0) 

                try:
                    admin_fee = ret['Admin Fee']
                    admin_fee = admin_fee.strip('/month')
                    admin_fee = admin_fee.strip('/30 days')
                    admin_fee = admin_fee.strip('$')
                    admin_fee = float(admin_fee)
                except:
                    admin_fee = float(0)
                    
                try:
                    elec_retail_charge = ret["Electricity Retail Charge"]
                    elec_retail_charge = elec_retail_charge.strip('/kWh')
                    elec_retail_charge = elec_retail_charge.strip('$')
                    elec_retail_charge = float(elec_retail_charge)
                    elec_retail_charge /= 100
                except:
                    elec_retail_charge = float(0)

                try:
                    gas_retail_charge = ret["Natural Gas Retail Charge"]
                    gas_retail_charge = gas_retail_charge.strip('/GJ')
                    gas_retail_charge = gas_retail_charge.strip('$')
                    gas_retail_charge = float(gas_retail_charge)
                except:
                    gas_retail_charge = float(0)
                
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
                    elec_trans_charge = ret["Electricity Transaction Charge"]
                    elec_trans_charge = elec_trans_charge.strip('/kWh')
                    elec_trans_charge = elec_trans_charge.strip('$')
                    elec_trans_charge = float(elec_trans_charge)
                except:
                    elec_trans_charge = float(0)

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
        
        gas_total_cost =  (gas_retail_charge * user_gj)
        relec_total_cost = (elec_retail_charge * user_kwh) + (elec_trans_charge * user_kwh)
        admin_fees = admin_fee + elec_admin_fee + gas_admin_fee

        elec_variable_dist_charges = (variable_elec_dist * user_kwh)
        elec_fixed_dist_charges = (fixed_elec_dist * 30)
        elec_variable_trans_charges = (variable_trans * user_kwh)
        balance_pool_charge = (balance_pool_rider * user_kwh)
        per_kwh_rate_rider_charge = (per_kwh_rate_rider * user_kwh)
        access_fee_charge = local_access_fee

        total_elec_variable_rate = elec_variable_dist_charges + relec_total_cost + elec_variable_trans_charges + balance_pool_charge + per_kwh_rate_rider + access_fee_charge

        total_elec_fixed_rate = elec_fixed_dist_charges + relec_total_cost + elec_variable_trans_charges + balance_pool_charge + per_kwh_rate_rider + access_fee_charge

        gas_variable_dist_charge = (variable_gas_dist * user_gj)
        gas_fixed_dist_charge = (fixed_gas_dist * 30)
        per_day_rider_charge = (per_day_rider * user_gj)
        per_gj_rate_charge = (per_gj_rider * user_gj)
        municipal_fees = muni_fran_fee


        carbon_tax = fed_tax * user_gj

        tax = 1 + gst

        total_gas_variable_rate = (gas_variable_dist_charge + gas_total_cost + per_day_rider_charge + per_gj_rate_charge + municipal_fees + carbon_tax)

        total_gas_fixed_rate = (gas_fixed_dist_charge + gas_total_cost + per_day_rider_charge + per_gj_rate_charge + municipal_fees + carbon_tax)

        total_bill_fixed = (total_gas_fixed_rate + total_elec_fixed_rate + admin_fees) * tax

        total_bill_variable = (total_gas_variable_rate + total_elec_variable_rate + admin_fees) * tax

        if 'Variable Rate Plan' in plan_deets[count]:
            r_dict =   {'retailer': retailers[count], 
                        'plan details': plan_deets[count],
                        '$/gj':  gas_retail_charge, 
                        '$/kwh': elec_retail_charge,
                        'admin fees': admin_fees, 
                        'total variable rate':total_bill_variable, 
                        }
        if 'Fixed Rate Plan' in plan_deets[count]:
            r_dict =   {'retailer': retailers[count], 
                        'plan details': plan_deets[count],
                        '$/gj':  gas_retail_charge, 
                        '$/kwh': elec_retail_charge,
                        'admin fees': admin_fees,  
                        'total fixed rate': total_bill_fixed
                        }
        else:
            r_dict =   {'retailer': retailers[count], 
                        'plan details': plan_deets[count],
                        '$/gj':  gas_retail_charge, 
                        '$/kwh': elec_retail_charge,
                        'admin fees': admin_fees, 
                        'total variable rate':total_bill_variable, 
                        'total fixed rate': total_bill_fixed
                        }


        retter[count] = r_dict

        count += 1

    return retter