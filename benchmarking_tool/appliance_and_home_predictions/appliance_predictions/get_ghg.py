'''
 need to get the ghg emmissions for a kwh of electricity 
 https://www.nationalobserver.com/2019/02/20/news/albertas-ndp-government-says-emissions-reductions-prove-carbon-pricing-works#:~:text=The%20data%20show%20that%20coal,kWh%20for%20simple%20cycle%20processes.
 https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/provincial-territorial-energy-profiles-alberta.html#:~:text=About%2091%25%20of%20electricity%20in,capacity%20of%205%20555%20MW.
 91% of electricity from fossil fules 43% from coal and 49 from natural gas 8% renewables
 https://www.eia.gov/tools/faqs/faq.php?id=74&t=11
 takes 2.21 lb of coal to make 1 kwh
 takes 0.91 lb of natural gas to make 1 kwh 
 https://www.eia.gov/coal/production/quarterly/co2_article/co2.html#:~:text=For%20example%2C%20coal%20with%20a,million%20Btu%20when%20completely%20burned.
 5720(lb of co2)/2000(lb of coal) = 2.86 (lbco2/lbcoal)
 https://www.engineeringtoolbox.com/co2-emission-fuels-d_1085.html
 2.75(kgco2/kg natural gas) * 2.20462 = 6.0627
 50(kg co2/ GJ natural gas) * 2.20462 = 110.231
 how much ghg is let go per gj 

'''


def get_ghg(user_kwh, user_gj):
    # electricity ghg emmitions 
    coal_kwh = user_kwh * 0.43
    ng_kwh = user_kwh * 0.49
    coal_ghg = coal_kwh * 2.86
    ng_ghg = ng_kwh * 6.0527
    elec_ghg = coal_ghg + ng_ghg
    # gas ghg
    natural_gas_ghg = user_gj * 110.231

    return [elec_ghg, natural_gas_ghg]