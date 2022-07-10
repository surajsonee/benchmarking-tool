import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

def regressor(clean_df):
    x = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24]]
    x = np.array(x)

    poly_reg = PolynomialFeatures(degree=14)
    X_poly = poly_reg.fit_transform(x)

    
    dft_values = clean_df.values

    y = dft_values

    lin_reg = LinearRegression()

    for yy in y:

        lin_reg.fit(X_poly,yy)

    pred = lin_reg.predict(X_poly)

    for j in range(len(pred)): 
        if pred[j] < 0:
            pred[j] *= -1

    return lin_reg, pred