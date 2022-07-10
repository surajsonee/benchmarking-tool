def monthly_comparison(month1, month1cat, month2, month2cat):
    # first get the on off usage comparison
    r_dict = {}

    for k1 in month1:
        name1 = k1 + '-savings'
        try:
            r_dict[name1] = (month1[k1] - month2[k1]) /month2[k1]
        except:
            # means it divided by zero
            if month2cat[k1] == 0 and month1cat[k1] != 0:
                r_dict[name1] = 1
            else:
                r_dict[name1] = 0

    for k in month1cat:
        name = k + '-savings'
        try:

            r_dict[name] = (month1cat[k] - month2cat[k])/month2cat[k]
        except:
            # means it divided by zero
            if month2cat[k] == 0 and month1cat[k] != 0:
                r_dict[name] = 1
            else:
                r_dict[name] = 0

    return r_dict