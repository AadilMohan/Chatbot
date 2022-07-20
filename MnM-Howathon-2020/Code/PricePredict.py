import numpy as np
import matplotlib.pyplot as mpl
from sklearn.preprocessing import scale
from TFANN import ANNR
import pandas as pd
import statistics
import os

def calculate_mean_std_dv_n_last_value(list_items):

    last_recorded_value = list_items[-1]
    mean_value = float(statistics.mean(list_items))
    std_dv_value = float(statistics.stdev(list_items))
    return last_recorded_value,mean_value,std_dv_value

def get_distance_from_mean_of_future_date(last_recorded_date,mean_date,std_dv_date):
    prediction_date = last_recorded_date + 365
    distance_from_mean_of_future_date = (prediction_date - mean_date)/std_dv_date
    return distance_from_mean_of_future_date

def get_expected_growth_on_predicted_date(predicted_price,last_recorded_price):
    percent_expected_growth = ((float(predicted_price[0]) - float(last_recorded_price)) / float(last_recorded_price)) * 100
    return percent_expected_growth




def get_fund_expected_growth(fund_name):
    # reads data from the file and ceates a matrix with only the dates and the prices
    base_path = r'C:\Users\aadmohan\Desktop\Howathon'
    final_path = os.path.join(base_path,fund_name +".csv")

    stock_data = np.loadtxt(final_path, delimiter=",", skiprows=1, usecols=(1, 4))
    list_prices = stock_data[:, 1]
    list_date = stock_data[:, 0]
    last_recorded_price,mean_prices,std_dv_prices = calculate_mean_std_dv_n_last_value(list_prices)
    last_recorded_date,mean_date,std_dv_date = calculate_mean_std_dv_n_last_value(list_date)
    distance_from_mean_of_future_date = get_distance_from_mean_of_future_date(last_recorded_date,mean_date,std_dv_date)

    #scales the data to smaller values
    stock_data=scale(stock_data)
    #gets the price and dates from the matrix
    prices = stock_data[:, 1].reshape(-1, 1)
    dates = stock_data[:, 0].reshape(-1, 1)
    # #creates a plot of the data and then displays it
    # mpl.plot(dates[:, 0], prices[:, 0])
    # mpl.show()

    #Number of neurons in the input, output, and hidden layers
    input = 1
    output = 1
    hidden = 50
    #array of layers, 3 hidden and 1 output, along with the tanh activation function
    layers = [('F', hidden), ('AF', 'tanh'), ('F', hidden), ('AF', 'tanh'), ('F', hidden), ('AF', 'tanh'), ('F', output)]
    #construct the model and dictate params
    mlpr = ANNR([input], layers, batchSize = 256, maxIter = 2000, tol = 0.2, reg = 1e-4, verbose = True)

    #number of days for the hold-out period used to access progress
    holdDays = 5
    totalDays = len(dates)
    #fit the model to the data "Learning"
    mlpr.fit(dates[0:(totalDays-holdDays)], prices[0:(totalDays-holdDays)])



    data = {'Predicted_date': [distance_from_mean_of_future_date]}
    df = pd.DataFrame(data)
    #Predict the stock price using the model
    #pricePredict = mlpr.predict(dates)
    predicted_price_in_distance_from_mean = mlpr.predict(df)
    predicted_price = mean_prices + predicted_price_in_distance_from_mean[0]*std_dv_prices
    expected_growth_on_predicted_date = get_expected_growth_on_predicted_date(predicted_price,last_recorded_price)
    print("expected_growth_on_predicted_date",expected_growth_on_predicted_date)


    #Display the predicted reuslts agains the actual data
    # mpl.plot(dates, prices)
    # mpl.plot(dates, pricePredict, c='#5aa9ab')
    # mpl.show()
    return expected_growth_on_predicted_date

def run_for_fund_type(df):

    list_funds = list(df['Fund Name'])

    for i in range(0, len(list_funds)):
        print("Running for fund:",list_funds[i])
        value = get_fund_expected_growth(list_funds[i])
        df.at[i,'Expected_return_1_yr']=float(value)
    list_expected_return = list(df['Expected_return_1_yr'])

    maxpos = int(list_expected_return.index(max(list_expected_return)))
    df.at[maxpos, 'Recommended'] = "Y"
    return df

def main():

    df = pd.read_csv(r'C:\Users\aadmohan\Desktop\Howathon\table.csv')
    df.loc[:, 'Recommended'] = 'No'
    df_equity = df[df['Type']=='Equity']
    df1 = run_for_fund_type(df_equity)
    print(df1)
    df_bond = df[df['Type'] == 'Bond']
    df_bond = df_bond.reset_index(drop=True)
    print(df_bond)
    df2 = run_for_fund_type(df_bond)
    print(df2)
    df= pd.concat([df1,df2])
    #df = pd.DataFrame.merge([df1, df2], left_index=True)
    df.to_csv(r'C:\Users\aadmohan\Desktop\Howathon\table.csv', index=False)

if __name__ == '__main__':
    main()




