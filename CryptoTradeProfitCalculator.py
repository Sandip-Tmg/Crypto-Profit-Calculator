# Student Name: Sandip Tamang
# Student Number: 3005816

# standard imports
import sys
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox, \
    QGraphicsDropShadowEffect
from PyQt5 import QtCore
from decimal import Decimal


class StockTradeProfitCalculator(QDialog):

    def __init__(self):

        super().__init__()

        # setting up dictionary of stocks
        self.data = self.make_data()
        # sorting the dictionary of stocks by the keys. The keys at the high level are dates, so we are sorting by date
        # self.stocks contains the list of stocks
        self.stocks = sorted(self.data.keys())
        print("Self Stocks: ", self.stocks)

        # the following 2 lines of code are for debugging purpose and show you how to access the self.data to get dates and prices
        # print all the dates and close prices for BTC
        # print("all the dates and close prices for BTC", self.data['BTC'])
        # print the close price for BTC on 04/29/2013
        # print("the close price for BTC on 04/29/2013", self.data['AAVE'][QDate(2020, 10, 5)])
        # # The data in the file is in the following range
        # #  first date in dataset - 29th Apr 2013
        # #  last date in dataset - 6th Jul 2021
        # # When the calendars load we want to ensure that the default dates selected are within the date range above
        # #  we can do this by setting variables to store suitable default values for sellCalendar and buyCalendar.
        self.sellCalendarDefaultDate = sorted(self.data['BNB'].keys())[
            0]  # Accessing the last element of a python list is explained with method 2 on https://www.geeksforgeeks.org/python-how-to-get-the-last-element-of-list/
        print("self.sellCalendarStartDate", self.sellCalendarDefaultDate)
        # self.buyCalendarDefaultDate
        # print("self.buyCalendarStartDate", self.buyCalendarDefaultDate)

        # set the window title
        self.setWindowTitle("Crypto Trade Profit Calculator")

        # set the window icon to the picture provided
        self.setWindowIcon(QIcon('Icons/bitcoin.png'))

        # created a variable for the date range
        first_date = QDate(2013, 4, 29)
        last_date = QDate(2021, 7, 6)

        # created a label and combo box for stock purchased
        self.stockPurchasedLabel = QLabel("Stock Purchased: ")
        # set the font of the label to be times font of size 10
        self.stockPurchasedLabel.setFont(QFont('Times font', 10))
        self.listOfStocks = QComboBox()
        self.listOfStocks.addItems(self.stocks)

        # created a label and Spin box for how many quantity of stock to purchase
        self.quantityPurchasedLabel = QLabel("Quantity Purchased: ")
        # set the font of the label to be times font of size 10.
        self.quantityPurchasedLabel.setFont(QFont("Times font", 10))
        self.stockPurchasedQuantity = QSpinBox()
        self.stockPurchasedQuantity.setValue(1)

        # created a date label and calender for allowing the purchase date
        self.purchaseLabel = QLabel("Purchased Date: ")
        # set the font of the label to be times font of size 10.
        self.purchaseLabel.setFont(QFont("Times font", 10))
        self.purchaseDate = QCalendarWidget()
        # creating box shadow
        shadow = QGraphicsDropShadowEffect()
        # setting blur radius
        shadow.setBlurRadius(20)
        # adding shadow to the label
        self.purchaseDate.setGraphicsEffect(shadow)
        # pointer cursor when hovering over date
        self.purchaseDate.setCursor(Qt.PointingHandCursor)
        # code to set the default date of 2021/6/22 for purchase date
        self.purchaseDate.setSelectedDate(QDate(2021, 6, 22))
        # code to set the range from first date to last date so that user will only be able to purchased within that range of date
        self.purchaseDate.setDateRange(first_date, last_date)

        # create QLabels to show the stock purchase total
        self.purchaseTotalLabel = QLabel("Purchase Total: ")
        # set the font of the label to be times font of size 10.
        self.purchaseTotalLabel.setFont(QFont("Times font", 10))
        # setting the initial purchase value
        purchaseValue = self.data[self.listOfStocks.currentText()][self.purchaseDate.selectedDate()]
        self.purchaseTotalCalculation = QLabel("%.2f" % purchaseValue)
        # setting the top and bottom padding
        self.purchaseTotalCalculation.setStyleSheet("padding: 10px 0px 10px 0px;")

        # created a date label and calender for allowing the sell date
        self.sellLabel = QLabel("Sell Date: ")
        # set the font of the label to be times font of size 10.
        self.sellLabel.setFont(QFont("Times font", 10))
        self.sellDate = QCalendarWidget()
        # creating box shadow
        shadow = QGraphicsDropShadowEffect()
        # setting blur radius
        shadow.setBlurRadius(20)
        # adding shadow to the label
        self.sellDate.setGraphicsEffect(shadow)
        # pointer cursor when hovering over date
        self.sellDate.setCursor(Qt.PointingHandCursor)

        # code to set the range from purchase date to last date so that the user can't sell before purchase date
        self.sellDate.setDateRange(self.purchaseDate.selectedDate(), last_date)

        # created a sell total label and calculation
        self.sellTotalLabel = QLabel("Sell Total: ")
        # set the font of the label to be times font of size 10.
        self.sellTotalLabel.setFont(QFont("Times font", 10))
        # setting the initial sell value
        sellValue = self.data[self.listOfStocks.currentText()][self.sellDate.selectedDate()]
        self.sellTotalCalculation = QLabel("%.2f" % sellValue)
        # setting the top and bottom padding
        self.sellTotalCalculation.setStyleSheet("padding:10px 0px 10px 0px;")

        # created a profit label to display the total profit from the stock
        self.profitTotalLabel = QLabel("Profit Total: ")
        # set the font of the label to be times font of size 10.
        self.profitTotalLabel.setFont(QFont("Times font", 10))
        self.profitTotal = QLabel()

        # calculation for profit total
        profit = sellValue - purchaseValue
        self.profitTotal.setText(str(profit))

        # if the there is no profit ie. if profit becomes negative then show the label to be red else black
        if profit < 0:
            self.profitTotal.setStyleSheet("color:red")
        else:
            self.profitTotal.setStyleSheet("color:black")

        # initialize the layout grid for different widgets
        grid = QGridLayout()
        grid.addWidget(self.stockPurchasedLabel, 0, 0)
        grid.addWidget(self.listOfStocks, 0, 1)
        grid.addWidget(self.quantityPurchasedLabel, 2, 0)
        grid.addWidget(self.stockPurchasedQuantity, 2, 1)
        grid.addWidget(self.purchaseLabel, 3, 0)
        grid.addWidget(self.purchaseDate, 3, 1)
        grid.addWidget(self.purchaseTotalLabel, 4, 0)
        grid.addWidget(self.purchaseTotalCalculation, 4, 1)
        grid.addWidget(self.sellLabel, 5, 0)
        grid.addWidget(self.sellDate, 5, 1)
        grid.addWidget(self.sellTotalLabel, 6, 0)
        grid.addWidget(self.sellTotalCalculation, 6, 1)
        grid.addWidget(self.profitTotalLabel, 7, 0)
        grid.addWidget(self.profitTotal, 7, 1)
        self.setLayout(grid)

        # connecting signals to slots to that a change in one control updates the UI
        self.listOfStocks.currentIndexChanged.connect(self.updateUi)
        self.stockPurchasedQuantity.valueChanged.connect(self.updateUi)
        self.purchaseDate.clicked.connect(self.updateUi)
        self.sellDate.clicked.connect(self.updateUi)

    def updateUi(self):
        try:
            print("")
            # get the stock list
            stock = self.listOfStocks.currentText()
            print("Stock: ", stock)
            # get the value of quantity
            quantity = self.stockPurchasedQuantity.value()

            # returning the total of purchase from custom method purchaseTotal
            purchaseTotal = self.purchaseTotal(stock, quantity)
            self.purchaseTotalCalculation.setText("%.02f" % purchaseTotal)

            # getting the first date of the stock selected
            getDateFirstRange = sorted(self.data[stock].keys())[0]
            print(getDateFirstRange)

            """ setting the date range from the first date of the stock to last date 
                the main reason to include this method is because if there is no data then we don't want the user 
                to select the date where there is no data on that particular date
            """
            self.purchaseDate.setDateRange(getDateFirstRange, QDate(2021, 7, 6))

            """setting the update so that the sell date Calender date ranges 
            from purchase date to given date date so 
            that user won't be able to sell before purchase date """
            self.sellDate.setDateRange(self.purchaseDate.selectedDate(), QDate(2021, 7, 6))

            # returning the total of sell from custom method sellTotal
            sellTotal = self.sellTotal(stock, quantity)
            self.sellTotalCalculation.setText("%.02f" % sellTotal)

            """ setting the date range from the first date of the stock to last date 
                the main reason to include this method is because if there is no data then we don't want the user 
                to select the date where there is no data on that particular date
            """
            self.sellDate.setDateRange(getDateFirstRange, QDate(2021, 7, 6))

            # calculation for profit total
            profit = sellTotal - purchaseTotal
            self.profitTotal.setText(str(profit))

            # if the there is no profit ie. if profit becomes negative then show the label to be red else black
            if profit < 0:
                self.profitTotal.setStyleSheet("color:red")
            else:
                self.profitTotal.setStyleSheet("color:black")

        except Exception as e:
            print(e)

    def purchaseTotal(self, stock, quantity):
        # calculation for purchase total
        purchaseDate = self.purchaseDate.selectedDate()
        purchaseValue = self.data[stock][purchaseDate]
        print("Purchase Value:", purchaseValue)
        purchaseTotal = purchaseValue * quantity
        return purchaseTotal

    def sellTotal(self, stock, quantity):
        # calculation for sell total
        sellDate = self.sellDate.selectedDate()
        sellValue = self.data[stock][sellDate]
        sellTotal = sellValue * quantity
        return sellTotal

    ################ YOU DO NOT HAVE TO EDIT CODE BELOW THIS POINT  ########################################################

    def make_data(self):
        '''
        This code is complete
        Data source is derived from https://www.kaggle.com/camnugent/sandp500/download but use the provided file to avoid confusion

        Converts a CSV file to a dictonary fo dictionaries like

            Stock   -> Date      -> Close
            AAL     -> 08/02/2013 -> 14.75
                    -> 11/02/2013 -> 14.46
                    ...
            AAPL    -> 08/02/2013 -> 67.85
                    -> 11/02/2013 -> 65.56

        Helpful tutorials to understand this
        - https://stackoverflow.com/questions/482410/how-do-i-convert-a-string-to-a-double-in-python
        - nested dictionaries https://stackoverflow.com/questions/16333296/how-do-you-create-nested-dict-in-python
        - https://www.tutorialspoint.com/python3/python_strings.htm
        :return: a dictionary of dictionaries
        '''
        file = open("./CryptoCoins_Prices/combined.csv",
                    "r")  # open a CSV file for reading https://docs.python.org/3/library/functions.html#open
        data = {}  # empty data dictionary
        file_rows = []  # empty list of file rows
        # add rows to the file_rows list
        for row in file:
            file_rows.append(row.strip())  # https://www.geeksforgeeks.org/python-string-strip-2/
        # print("len(file_rows):" + str(len(file_rows)))

        # get the column headings of the CSV file
        row0 = file_rows[0]
        line = row0.split(",")
        column_headings = line
        # print(column_headings)

        # get the unique list of stocks from the CSV file
        non_unique_stocks = []
        file_rows_from_row1_to_end = file_rows[1:len(file_rows) - 1]
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            non_unique_stocks.append(line[6])
        stocks = self.unique(non_unique_stocks)
        # print("len(stocks):" + str(len(stocks)))
        # print("stocks:" + str(stocks))

        # build the base dictionary of stocks
        for stock in stocks:
            data[stock] = {}

        # build the dictionary of dictionaries
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            date = self.string_date_into_QDate(line[0])
            stock = line[6]
            close_price = line[4]
            # include error handling code if close price is incorrect
            data[stock][date] = float(close_price)
        print("len(data):", len(data))
        return data

    def string_date_into_QDate(self, date_String):
        '''
        This method is complete
        Converts a data in a string format like that in a CSV file to QDate Objects for use with QCalendarWidget
        :param date_String: data in a string format
        :return:
        '''
        date_list = date_String.split("-")
        date_QDate = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        return date_QDate

    def unique(self, non_unique_list):
        '''
        This method is complete
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        '''
        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list


# This is complete
if __name__ == '__main__':
    app = QApplication(sys.argv)
    currency_converter = StockTradeProfitCalculator()
    currency_converter.show()
    sys.exit(app.exec_())
