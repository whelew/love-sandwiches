# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPEAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPEAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figure input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers seperated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter Your Data Here:\n")
        
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid")
            break
    
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raise ValueError, if strings cannot be converted to int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid Data: {e}, please try again.\n")
        return False
    
    return True
    
def update_worksheet(data, worksheet):
    """
    Recieves a list of integers to be inserted into a worksheet.
    Update the relevant worksheet with the data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")
        

def calculate_surplus_data(sales_row):
    """
     Compare sales with stock and calculate the surplus for each item type.

     The surplus is defined as the sales figure subtracted from the stock figure:
     -Positive surplus indicates waste
     -Negative surplus indicates extra made when stock sold out.
    """
    print("Calculating surplus date...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting 
    the last 5 entries for each sandwich and returns the data 
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    columns = []

    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])    
        
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each sandwich
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for i in data:
        int_column = [int(num) for num in i]
        stock_num = sum(int_column)
        avg_stock = (stock_num / len(int_column)) * 1.1
        new_stock_data.append(round(avg_stock))
    
    return new_stock_data  

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    
    

print("Welcome to Love Sandwiches data automation")
main()