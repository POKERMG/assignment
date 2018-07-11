# -*- coding: utf-8 -*-

"""


Created for JPM Assignment - Super Simple Stock Market for (Beverage Trading Companies)



Friday 18th of May 2018 : 


@author: MILAN GOHIL
"""




import time

import csv



DEFAULT_TIME_MINUTES = 5



class stockFactor:

  symbol_=""

  properties_={} # key:value array

  

  def __init__(self, symbol,properties):

    self.symbol_ = symbol

    self.properties_ = properties  

  

class Trade:

  symbol_=""

  timestamp_= None

  quantity_= None

  buy_sell_= None

  price_= None



  def __init__(self, symbol, timestamp, quantity, buy_sell, price):

    self.symbol_ = symbol

    self.timestamp_ = timestamp

    self.quantity_ = quantity

    self.buy_sell_ = buy_sell

    self.price_ = price    

  

def calculateDividendYield(stockFactor, price):

  #Receives a stockFactor object and a price

  #Returns the value of Dividend Yield  

  if stockFactor.properties_['Type'] == "Common":

      divYield = float(stockFactor.properties_['Last Dividend'])/price

  else:

    divYield = float(stockFactor.properties_['Fixed Dividend'].strip("%"))*float(stockFactor.properties_['Par Value'])/(100*price)

  return divYield



def calculatePERatio(stockFactor, price):

  #Receives a stockFactor object and a price

  #Returns the value of P/E Ratio 

  if float(stockFactor.properties_['Last Dividend']) == 0:

    return ("Last Dividend Is 0, P/E Ratio Cannot Be Computed\n")

  else:    

    return price/float(stockFactor.properties_['Last Dividend'])

  

def calculateVWSP(tradesArray):

  #Receives an array with Trade objects

  #Returns the value of the VWSP

  num = den = 0  

  for i in range(0,len(tradesArray)):

    num+= tradesArray[i].quantity_*tradesArray[i].price_

    den+= tradesArray[i].quantity_

  return num/den   

    

def calculateGBCE(volumesArray):

  #Receives an array

  #Returns the geometric mean  

  n = len(volumesArray)

  p = 1

  for i in range(0, n):

    p *= volumesArray[i]

  return pow(p,1/n)           

    

def loadingStocks():

  #Loads stock file path and calls parseLines() to save stocks to an array

  #Returns stockArray

  #Symbol's name is assumed to be 'Stock Symbol'

  stockArrayAux = []  

  StockIn=input("\nPlease Select Path For Stocks CSV file \n(Locate And Select File: './Your_Location/SSSM.csv'): ")

  with open(StockIn, 'r') as inputFile:

    inputRows = csv.DictReader(inputFile, delimiter=';')
    
    for row in inputRows:

      symbol=row['Stock Symbol']

      symbolArray.append(symbol)

      del row['Stock Symbol']

      stockArrayAux.append(stockFactor(symbol, dict(row)))  

    print("Beverage Stocks Have Been Loaded Succesfully\n")  

  return stockArrayAux  

  

def extractTradesSymbol(tradesArray, stock):

  #Receives an array of Trade objects and a stock's symbol

  #Returns an array of Trades corresponding to that stock's symbol  

  tradesAux = []

  for i in range(0, len(tradesArray)):

    if tradesArray[i].symbol_ == stock:

      tradesAux.append(tradesArray[i])  

  return tradesAux 



def extractTradesTime(tradesArray, minutes):

  #Receives an array of Trade objects and a time in minutes

  #Returns an array of Trades in the last 'x' minutes     

  tradesAux = []

  for i in range(0, len(tradesArray)):

    if (time.time() - tradesArray[i].timestamp_) <= minutes*60 :

      tradesAux.append(tradesArray[i])  

  return tradesAux      

   

if __name__ == '__main__':

    

    #Data arrays for stocks

    stockArray = []

    symbolArray = []

    tradeRecordArray = []    

    # Main Menu for SSSM

    mainMenu = {'1': "Load Beverage Stocks.", '2': "Select Stock To Engage.", '3': "Calculate (GBCE) All Share Index.", '4': "Exit Stock Market"}

    while True:

      options=list(mainMenu.keys())

      options.sort()

      print("\n") 

      for entry in options:         

        print (entry, mainMenu[entry])

      selection=input("\nPlease Select An Option : ")

      if selection =='1':

        #Loading Stock Information  

        if len(stockArray) == 0:  

          stockArray=loadingStocks()  

        else:

          answer=input("Loading A New File Will Erase Previous Information, Are You Sure You Wish To Continue? (y/n): ")

          while answer not in ['y','n']:

            answer = input("Please enter only 'y' or 'n' for YES or NO: ")

          if answer=='y':

            stockArray=loadingStocks()

      elif selection == '2':  

        #Select a stock to operate with  

        if len(stockArray) == 0:

          print ("\nPlease Load Stocks FIRST To Engage With\n")

        else:

          selectedStock=input("\nSelect A Stock To Engage On\n(Select A Stock (Upper Case) :  TEA | POP | ALE | GIN | JOE): ")

          if selectedStock in symbolArray:

            operationsMenu = {'1': "Calculate Dividend Yield.", '2': "Calculate P/E Ratio.",
                              '3': "Initiate A BUY/SELL Trade.", '4': "Calculate Volume Weighted Stock Price.", '5': "Go back."}

            while True:

              options=list(operationsMenu.keys())

              options.sort()

              print("\n")

              for entry in options:                  

                print (entry, operationsMenu[entry])

              selection=input("\nPlease Select A Function From The Menu: ")

              if selection == '1':

                #Calculating dividend yield

                for i in range(0,len(stockArray)):

                  if selectedStock == stockArray[i].symbol_:

                    stockFactorAux = stockArray[i]

                    break

                while True:

                  try:

                    price = float(input("Enter Price For The Dividend Yield Calculation: "))    

                  except ValueError:

                    print("Please Verify Quantity You Are Entering Is A Float ")

                    continue

                  else:

                    if price <= 0:

                      print("Please Enter A Positive Price")  

                      continue

                    else:

                      break    

                print("Result Is: ",calculateDividendYield(stockFactorAux, float(price)))

              elif selection == '2':

                #Calculating P/E Ratio = Price Earnings Ratio

                for i in range(0,len(stockArray)):

                  if selectedStock == stockArray[i].symbol_:

                    stockFactorAux = stockArray[i]

                    break

                while True:

                  try:

                    price = float(input("Enter Price For P/E Ratio Calculation: "))    

                  except ValueError:

                    print("Please Verify Quantity You Are Entering Is A Float  ")

                    continue

                  else:

                    if price <= 0:

                      print("Please Enter A Positive Price")  

                      continue

                    else:

                      break    

                print("Result Is: ",calculatePERatio(stockFactorAux, float(price)))

              elif selection == '3':

                #Recording and confirming a BUY or SELL of a trade

                buy_sell = input("Select 'b' for BUY or 's' for SELL: ")

                while buy_sell not in ['b','s']:

                  buy_sell = input("Please Enter Only 'b' or 's' For BUY or SELL: ")  

                while True:

                  try:

                    quantity = int(input("Enter The Quantity To BUY Or SELL: "))    

                  except ValueError:

                    print("Please Verify The Quantity You Are Entering Is An Integer ")

                    continue

                  else:

                    if quantity <= 0:

                      print("Please Verify The Quantity You Are Entering Is Positive")

                      continue

                    else:

                      break

                while True:

                  try:

                    price = float(input("Enter Price Of The Operation: "))    

                  except ValueError:

                    print("Please Verify  The Quantity You Are Entering Is A Float ")

                    continue

                  else:

                    if price <= 0:

                      print("Please Enter A Positive Price")  

                      continue

                    else:

                      break    

                tradeRecordArray.append(Trade(selectedStock, time.time(), quantity, buy_sell, price))

                tradeAux = Trade(selectedStock, time.time(), quantity, buy_sell, price)             

                print("Your BUY/SELL Trade Has Been Recorded Succesfully\n")

              elif selection == '4':  

                #Calculating VWSP = Volume Weighted Stock Price

                tradesAux = extractTradesSymbol(tradeRecordArray, selectedStock)

                if len(tradesAux) == 0:

                  print("Please Record Trades For This Stock Before Trying To Obtain VWSP")

                else:

                  tradesAux = extractTradesTime(tradesAux,DEFAULT_TIME_MINUTES)

                  if len(tradesAux) == 0:

                    print("There Are No Records In Under 5 Minutes For This Stock")

                  else:

                    print("VWSP is: ", calculateVWSP(tradesAux))    

              elif selection == '5':

                break     

              else:

                print("Error, Unknown Option Selected!")    

          else:

            print("Entered Stock Is Not An Option. Please Try Again")               

      elif selection == '3':

        #Calculate GBCE

        if len(stockArray) == 0:

          print ("\nFirst You Must Load Stocks To Operate With\n")

        else:

          if len(tradeRecordArray) == 0:

            print("\nFirst You Must Initiate BUY/SELL Trades\n")

          else:  

            volumeWSP = [] 

            for i in range(0, len(stockArray)):

              tradesAux = extractTradesSymbol(tradeRecordArray, stockArray[i].symbol_)

              if len(tradesAux) > 0:

                volumeWSP.append(calculateVWSP(tradesAux)) 

            print("(GBCE) All Share Index Is: ", calculateGBCE(volumeWSP))

      elif selection == '4': 

        #End program  

        print("Stock Market Program Has Ended")

        break

      else: 

        print ("Error, Unknown Option Selected! - Please Try Again!")
