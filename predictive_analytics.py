###############################################################################
#                             Importing Libraries                             #
# import the necessary packages by using command: pip install <package_name>  #
###############################################################################
# For data processing
import pandas as pd
import numpy as np

# For date and time
import datetime as dt
import dateutil

# For Linear Regression & Linear-SVR
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn import metrics
from sklearn.svm import LinearSVR

# For graphs
import matplotlib.pyplot as plt
from matplotlib import pylab

###############################################################################
#                        Predictive Analytics Menu                           #
###############################################################################
def predictive_menu(stock_all_data,stock_closing_price):
    print("-" * 100)
    predictive_menu = ("\nLinear Models for Predictive Analysis:\n1. Linear Regression Model\n2. Linear SVR Model\n3. Go back to Previous Menu\n")
    print(predictive_menu)
    print("-" * 100)
    predictive_choice = input("Please enter your choice: ")
    while predictive_choice != "3":
        try:
            if predictive_choice == "1":
                linear_regression(stock_all_data,stock_closing_price)
            elif predictive_choice == "2":
                SVR_model(stock_all_data,stock_closing_price)
            else:
                print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
        except ValueError:
            print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
        except Exception as e:
            print("\n" , "*" * 10 , "Sorry an error occurred. Please try again with valid input." , "*" * 10, "\n")
            print(e)
        print("-" * 100)
        print(predictive_menu)
        print("-" * 100)
        predictive_choice = input("Please enter your choice: ")


###############################################################################
#            Stock Price Prediction using Linear Regression                   #
###############################################################################
def linear_regression(stock_all_data_lr,stock_closing_price):
        stock_all_data = stock_all_data_lr.copy()
        start_day = pd.to_datetime(np.min(stock_all_data.index))

        stock_all_data['index_days'] = (pd.to_datetime(stock_all_data.index) - start_day).days
        x_dates = stock_all_data['index_days'].tolist()
        y_prices = stock_all_data['Close'].tolist()

        linear_mod = linear_model.LinearRegression()
        x_dates = np.reshape(x_dates,(len(x_dates),1))
        y_prices = np.reshape(y_prices,(len(y_prices),1))

        linear_mod.fit(x_dates,y_prices)
        predicted_price1 = linear_mod.predict(x_dates)

        print("-" * 100)
        linear_menu = "\nLinear Regression Model:\n1. Enter date for prediction\n2. Go back to Previous Menu\n"
        print(linear_menu)
        print("-" * 100)

        choice_linear = input("Enter your choice: ")
        while choice_linear != "2":
            try:
                if choice_linear == "1":
                    predicted_date = input("Enter the date for prediction in YYYY-MM-DD format: ")
                    if(dt.datetime.strptime(predicted_date, '%Y-%m-%d')):
                        print("-" * 100)
                        print("Details on the Prediction and Error:")
                        print("-" * 100)
                        print("Co-efficient of Accuracy: ", linear_mod.score(x_dates,y_prices))
                        print("\nRoot Mean Squared Error: ",np.sqrt(metrics.mean_squared_error(y_prices,predicted_price1)))
                        print("\nR2 Score: ", (metrics.r2_score(y_prices,predicted_price1)))
                        print("\nMean Absolute Error: ", metrics.mean_absolute_error(y_prices,predicted_price1))
                        print("\nMean Squared Error: ", metrics.mean_squared_error(y_prices,predicted_price1))

                        predict_diff = (pd.to_datetime(predicted_date) - start_day).days

                        temp= np.reshape(predict_diff,(1,-1))
                        predicted_price2 = linear_mod.predict(temp)
                        print('\nSlope: ', np.asscalar(np.squeeze(linear_mod.coef_)))
                        print('\nIntercept: ', linear_mod.intercept_[0])
                        print(f"\nPredicted price for {predicted_date} date is :{predicted_price2[0][0]}")
                        print("-"* 100)

                        plt.figure(1, figsize=(15,10))
                        plt.title('Linear Regression | Closing Price vs Time', fontdict = {'fontsize' : 15})
                        plt.scatter(x_dates, y_prices, edgecolor='w', label='Actual Price')
                        plt.plot(x_dates, linear_mod.predict(x_dates), color='r', label='Predicted Price')
                        plt.xlabel('Integer Date', fontsize = 12)
                        plt.ylabel('Stock Price', fontsize = 12)
                        plt.legend()
                        plt.show()
                    else:
                        print("Please enter the date in YYYY-MM-DD format.")
                else:
                    print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
            except ValueError:
                print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
            except:
                print("\n" , "*" * 10 , "Sorry an error occurred. Please try again with valid input." , "*" * 10, "\n")
            print("-"* 100)
            print(linear_menu)
            print("-"* 100)
            choice_linear = input("Enter your choice: ")

###############################################################################
#                Stock Price Prediction using SVR Model                       #
###############################################################################

def SVR_model(stock_all_data_svr,stock_closing_price):
    stock_all_data = stock_all_data_svr.copy()
    x_dates = []
    y_prices = []
    start_day = pd.to_datetime(np.min(stock_all_data.index))

    stock_all_data['index_days'] = (pd.to_datetime(stock_all_data.index) - start_day).days
    x_dates = stock_all_data['index_days'].tolist()
    y_prices = stock_all_data['Close'].tolist()

    x_dates = np.reshape(x_dates,(len(x_dates),1))
    y_prices = np.reshape(y_prices,(len(y_prices),1))

    svr_lin = LinearSVR(C=1e3)
    svr_lin.fit(x_dates, y_prices.ravel())

    print("-" * 100)
    svr_menu = "\nLinear SVR Model:\n1. Enter date for prediction\n2. Go back to Previous Menu\n"
    print(svr_menu)
    print("-" * 100)
    choice_SVR = input("Enter your choice: ")
    while choice_SVR != "2":
        try:
            if choice_SVR == "1":
                predicted_date_SVR = input("Enter the date for prediction in YYYY-MM-DD format: ")
                if(dt.datetime.strptime(predicted_date_SVR, '%Y-%m-%d')):
                    plt.scatter(x_dates, y_prices, color = 'black', label = 'Data')
                    plt.plot(x_dates, svr_lin.predict(x_dates), color = 'red', label = 'Linear Model')
                    plt.xlabel('Date')
                    plt.ylabel("Price")
                    plt.title("Support Vector Regression (SVR)")
                    plt.legend()
                    plt.show()

                    predict_diff_svr = (pd.to_datetime(predicted_date_SVR) - start_day).days

                    print("-" * 100)
                    print(F"The Stock Close Price on {predicted_date_SVR}: ")
                    print("Linear Kernel: $", svr_lin.predict(np.array(predict_diff_svr).reshape(-1,1))[0])
                else:
                    print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
            else:
                print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
        except Exception as e:
            print("\n" , "*" * 10 , "Sorry an error occurred. Please try again with valid input." , "*" * 10, "\n")
            print(e.args[0])
        print("-" * 100)
        print(svr_menu)
        print("-" * 100)
        choice_SVR = input("Enter your choice: ")
