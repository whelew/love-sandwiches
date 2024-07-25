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
    Get sales figure input from the user
    """
    print("Please enter data from the last market.")
    print("Data should be six numbers, seperated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter Your Data Here: ")
    print(f"The data provided is {data_str}")

get_sales_data()