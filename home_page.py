###############################################################################
#                             Importing Libraries                             #
# import the necessary packages by using command: pip install <package_name>  #
###############################################################################
# For reading stock data from web
import pandas_datareader as web

# For data processing
import pandas as pd
import numpy as np

# For date and time
from datetime import datetime, timedelta, date

# For reading files and file directory
import os, sys
from os import path

# For downloading file using URL
import requests

# For importing customized packages
import descriptive_analysis as da
import predictive_analytics as pa

#For ignoring the warnings
import warnings
warnings.filterwarnings("ignore")

# For plotting graph
import matplotlib.pyplot as plt

###############################################################################
#                Fetch & Validate user entered ticker                         #
###############################################################################
def accept_ticker():
    print("\n")
    print ("+" * 110)
    print( "+" * 23 , "Welcome to Yahoo Finance Stock Market Analysis and Predictions" , "+" * 23)
    menu = "1. Enter Company Ticker for Analysis \n2. View Help Documents \n3. Abort Application"
    print ("+" * 110)
    print("\n")
    print(menu)
    choice = input("\nPlease enter your preference: ")
    while choice != "3":
        try:
            if choice == "1":
                ticker_symbol = input("\nPlease enter company ticker: ").upper()
                fetch_company_details(ticker_symbol)
                startdate, enddate = date_inputs()
                stock_all_data, stock_closing_price = getCompanyInfo(ticker_symbol, startdate, enddate)
                mainMenu(stock_all_data,stock_closing_price, startdate, enddate,ticker_symbol)
            elif choice == "2":
                documents_menu()
            else:
                print("\n" , "*" * 10 , "Please enter a valid option." , "*" * 10, "\n")
        except ValueError as ve:          
            print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
            print(ve.args[0])
        print ("-" * 100)
        print(menu)
        print ("-" * 100)
        choice = input("\nPlease enter your preference: ")

###############################################################################
#             Fetch start & end date (validate date format & range)           #
###############################################################################
def date_inputs():
    try:
        startdate_str = input("Enter start date in YYYY-MM-DD format:")
        startdate = datetime.strptime(startdate_str, "%Y-%m-%d")
        enddate_str = input("Enter end date in YYYY-MM-DD format:")
        enddate = datetime.strptime(enddate_str, "%Y-%m-%d")

        if startdate >= enddate :
            raise ValueError("\nEntered start date is greater than end date. Please re-enter dates.\n")
        if startdate > datetime.today() or enddate > datetime.today():
            raise ValueError("\nFuture is yet to happen my friend! Please enter a valid start/end date.\n")
        return startdate, enddate

    except ValueError as ve:
        raise ValueError(ve.args[0])
        print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
    except Exception as e:
        print(e.args[0])
        raise ValueError("Please enter date in YYYY-MM-DD format.\n")

###############################################################################
#                   Validate the user entered ticker on NASDAQ                #
###############################################################################

def fetch_company_details(company_ticker):
    today_date = str(date.today())
    if path.exists("nasdaq" + '_' + today_date + '.csv'):
        company_details = pd.read_csv("nasdaq" + '_' + today_date + '.csv', usecols = [*range(0,7)])
        symbols_list =  company_details['Symbol']
    else:
        url = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
        r = requests.get(url, allow_redirects=True)
        company_details = open('nasdaq'+ '_' + today_date + '.csv', 'wb').write(r.content)
        print("\n" , "*" * 10 , "NASDAQ symbol list updated for Today!", "*" * 10 , "\n")
        company_details = pd.read_csv("nasdaq" + '_' + today_date + '.csv',usecols = [*range(0,7)])
        symbols_list =  company_details['Symbol']

    symbols = list(symbols_list)
    if company_ticker in symbols:
        company_details = company_details.loc[company_details['Symbol'] == company_ticker]
        company_details.index = range(len(company_details))
        symbol_details = symbols_list.loc[symbols_list == company_ticker]
        symbol_details.index = range(len(symbol_details))
        company_name = company_details["Name"][0]
        print("\n")
        print("-" *100)
        print(f"\t\t\tGeneral Information about {company_name}")
        print("-" *100)
        print("Company  Name                  : ",company_details["Name"][0])
        print("Last Sale Information          : ",company_details["LastSale"][0])
        print("Market Cap                     : ",company_details["MarketCap"][0])
        print("IPO years                      : ",company_details["IPOyear"][0])
        print("Sector of the company          : ",company_details["Sector"][0])
        print("Industry the company belong to : ",company_details["industry"][0])
        print("-" *100)
    else:
        raise ValueError("Invalid Ticker Symbol.")

###############################################################################
#           Create dataframe based on ticker, start date and end date         #
###############################################################################
def getCompanyInfo(ticker_symbol, startdate, enddate):
    try:
        stock_all_data = web.DataReader(ticker_symbol,'yahoo',startdate,enddate)
        stock_all_data.index = pd.to_datetime(stock_all_data.index)
        stock_all_data.sort_index(inplace=True)
        stock_all_data.rename(columns={"Adj Close": "Adj_Close"}, inplace =True)
        stock_closing_price = stock_all_data.drop(['Open', 'High', 'Low', 'Adj_Close', 'Volume'], axis=1)
        stock_closing_price.reset_index(inplace = True)
        return stock_all_data,stock_closing_price
    except:
        raise ValueError("Cannot find any data for the company, Please enter a valid ticker and date range")

###############################################################################
#                          View Help Documents                                #
###############################################################################
def documents_menu():
    print("-" * 100)
    print("\nLet's get some insights about the project!\n")
    documents_menu = "1. View User Manual\n2. View Flow Diagram\n3. Go back to Previous Menu\n"
    print(documents_menu)
    print("-" * 100)
    documents_choice = input("Please enter your choice: ")
    while documents_choice != "3":
        try:
            if documents_choice == "1":
                if sys.platform == "win32":
                    os.startfile('user_manual.pdf')
                else:
                    os.system("open user_manual.pdf")
            elif documents_choice == "2":
                if sys.platform == "win32":
                    os.startfile('UML_Diagram.png')
                else:
                    os.system("open UML_Diagram.png")
            else:
                print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
        except ValueError:
            print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
        except:
            print("\n" , "*" * 10 , "Sorry an error occurred. Please try again with valid input." , "*" * 10, "\n")
        print("-" * 100)
        print(documents_menu)
        print("-" * 100)
        documents_choice = input("Please enter your choice: ")

###############################################################################
#                  Statistical and Graphical Comprison between two Stocks     #
###############################################################################
def compare_stocks(stock_all_data,stock_closing_price,startdate,enddate,ticker_symbol):
    
    try:
        ticker_symbol_2 = input(f"\nPlease enter a company ticker to compare with {ticker_symbol}: ").upper()
        fetch_company_details(ticker_symbol_2)
        stock_all_data_2 = web.DataReader(ticker_symbol_2,'yahoo',startdate,enddate)
        stock_all_data_2.index = pd.to_datetime(stock_all_data_2.index)
        stock_all_data_2.sort_index(inplace=True)
        stock_all_data_2.rename(columns={"Adj Close": "Adj_Close"}, inplace =True)

        comparison_menu = "\nSelect any one option for Comparison: \n1. Statistical Comparison\n2. Graphical Comparison\n3. Go back to Previous Menu\n"
        print(comparison_menu)
        print("-" * 100)
        comparison_choice = input("\nPlease enter your choice: ")
        while comparison_choice != "3":
            try:
                if comparison_choice == "1":
                    print("-" * 100)
                    print(f"Statistical figures for {ticker_symbol} are: \n")
                    print(stock_all_data.describe())
                    print(f"\nStatistical figures for {ticker_symbol_2} are: \n")
                    print(stock_all_data_2.describe())
                elif comparison_choice == "2":
                    stock_all_data['Close'].plot(label=ticker_symbol,figsize=(15,10),color="red", linestyle =":")
                    stock_all_data_2['Close'].plot(label=ticker_symbol_2,figsize=(15,10),color="blue", linestyle ="-.")
                    plt.title(f"Closing Price Comparison for {ticker_symbol} & {ticker_symbol_2}" , fontdict = {'fontsize' : 17})
                    plt.xlabel("Date", fontsize = 12)
                    plt.ylabel("Closing Price", fontsize = 12)
                    plt.legend()
                    plt.show()
                else:
                    print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
            except ValueError:
                print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10, "\n")
            except:
                print("\n" , "*" * 10 , "Sorry an error occurred. Please try again with valid input." , "*" * 10, "\n")
            print("-" * 100)
            print(comparison_menu)
            print("-" * 100)
            comparison_choice = input("\nPlease enter your choice: ")
    except:
        print("\n" , "*" * 10 , "Sorry an error occurred. Please try again with valid input." , "*" * 10, "\n")


###############################################################################
#                   Main Menu to select type of Analytics                     #
###############################################################################

def mainMenu(stock_all_data,stock_closing_price, startdate, enddate, ticker_symbol):
            print ("-" * 100)
            menu = "\nChoose any one Analytics Technique: \n1. Descriptive Analytics \n2. Predictive Analytics \n3. Comparison of stocks\n4. Go back to Previous Menu\n"
            print(menu)
            print ("-" * 100)
            technique_selection = input("Enter your choice: ")
            while technique_selection != "4":
                try:
                    if technique_selection == "1":
                        da.descriptive_menu(stock_all_data,stock_closing_price)
                    elif technique_selection == "2":
                        pa.predictive_menu(stock_all_data,stock_closing_price)
                    elif technique_selection == "3":
                        compare_stocks(stock_all_data,stock_closing_price,startdate,enddate,ticker_symbol)
                    else:
                        print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10)
                except ValueError:
                    print("\n" , "*" * 10 , "Input Error: Please enter a valid option." , "*" * 10)
                except:
                    print("\n" , "*" * 10 , "Sorry an error occurred. Please try again with valid input." , "*" * 10, "\n")
                print ("-" * 100)
                print(menu)
                print ("-" * 100)
                technique_selection = input("Enter your choice: ")


if __name__ == "__main__":
    accept_ticker()
