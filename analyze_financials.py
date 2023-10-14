# Common utilities
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Custom utilities
from expenses import *
#from expenses import combine_expenses
#from expenses import add_interest_payments
#from expenses import add_labor_costs_df
#from expenses import add_tax_and_royalty
#from expenses import add_depreciation_expense

from revenue import *
#from revenue import revenue_growth_df
#from revenue import combine_revenue
#from revenue import add_birthday_party
#from revenue import pad_revenues

from visualize import *
#from visualize import plot_profit_loss
#from visualize import save_profit_loss
#from visualize import plot_cashflow
#from visualize import save_cashflow

# Dataframe Options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.options.display.float_format = '{:,.0f}'.format

pl_plot = "Profit_Loss.png"
cf_plot = "Cash_Flow.png"

# Timeline Definition
FRAN_START_DATE = datetime(2024,1,15)
SIGN_LEASE = FRAN_START_DATE + relativedelta(months=2)
BUILDOUT_COMPLETE = SIGN_LEASE + relativedelta(weeks=10)
GRAND_OPENING = BUILDOUT_COMPLETE + relativedelta(weeks=3)
TRAINING_START = FRAN_START_DATE
TRAINING_COMPLETE = TRAINING_START + relativedelta(weeks=8)
DIRECTOR_HIRED = GRAND_OPENING - relativedelta(weeks=8)
STAFF_HIRING_START = GRAND_OPENING - relativedelta(weeks=6)
PERIOD_END = datetime(2026,12,31)

operating_dates = pd.date_range(GRAND_OPENING, periods=36, freq='M')

# Revenue Variables
GO_STUDENT_COUNT = 50
GROWTH_RATE = 0.1 # FIXME Get from Diane
SS_STUDENT_COUNT = 300 # FIXME Get from Diane
MONTHLY_STUDENT_PRICE = 225 # Dollars, 2x classes per week
camp_revenue = 300 * 15 # 15 kids at $300 # FIXME

# Expense Variables
SQ_FT = 1500
LEASE = 28 * SQ_FT
NNN = 10 * SQ_FT
RENT = (LEASE + NNN) / 12
DIR_SALARY = 65000 / 12 # FIXME
HOURLY_RATE = 30
INTEREST_RATE = 9
INST_COMP_COST = 17500
USEFUL_LIFE = 36 # 36 Months, 3 years

# CASHFLOW
STARTING_LIQUID = 50000
STARTING_HELOC = 115000
STARTING_CASH = STARTING_LIQUID + STARTING_HELOC


#######################################
##         E X P E N S E S           ##
#######################################
recurring_expenses_data = [
    {'Name': 'Rent'            , 'Amount': RENT},
    {'Name': 'Utilities'       , 'Amount': 150},  # FIXME
    {'Name': 'Internet'        , 'Amount': 150},  # FIXME
    {'Name': 'Director Salary' , 'Amount': DIR_SALARY},
    {'Name': 'Coach Labor'     , 'Amount': DIR_SALARY}, # FIXME
]
recurring_expenses_df = pd.DataFrame(recurring_expenses_data)

unique_expenses_data = [
    # Example data
    {'Date': FRAN_START_DATE - timedelta(weeks=2) , 'Name': 'CPA Fees'                          , 'Amount':            500 },
    {'Date': FRAN_START_DATE - timedelta(weeks=1) , 'Name': 'LLC Fees'                          , 'Amount':            500 },
    {'Date': FRAN_START_DATE                      , 'Name': 'Franchise Fee'                     , 'Amount':           4500 },
    {'Date': TRAINING_START                       , 'Name': 'Training Travel Expenses'          , 'Amount':           3000 },
    {'Date': SIGN_LEASE                           , 'Name': 'First Month Rent'                  , 'Amount':           RENT },
    {'Date': SIGN_LEASE                           , 'Name': 'Security Deposit'                  , 'Amount':           5000 },
    {'Date': SIGN_LEASE                           , 'Name': 'Utility Deposit'                   , 'Amount':            800 }, 
    {'Date': SIGN_LEASE + timedelta(weeks=1)      , 'Name': 'Furniture & Equipment (partial)'   , 'Amount':          15000 },
    {'Date': SIGN_LEASE + timedelta(weeks=2)      , 'Name': 'Furniture & Equipment (partial)'   , 'Amount':          15000 },
    {'Date': SIGN_LEASE + timedelta(weeks=2)      , 'Name': 'Computer Equipment (admin)'        , 'Amount':           1500 },
    {'Date': SIGN_LEASE + timedelta(weeks=2)      , 'Name': 'Computer Equipment (instructional)', 'Amount': INST_COMP_COST },
    {'Date': GRAND_OPENING - timedelta(weeks=4)   , 'Name': 'Initial Marketing Expense'         , 'Amount':          12500 },
    {'Date': GRAND_OPENING - timedelta(weeks=2)   , 'Name': 'Signage'                           , 'Amount':          12500 },
    {'Date': GRAND_OPENING - timedelta(weeks=1)   , 'Name': 'Insurance Deposit'                 , 'Amount':           1500 },
    {'Date': GRAND_OPENING - timedelta(weeks=1)   , 'Name': 'Licensing'                         , 'Amount':           1500 },
    {'Date': GRAND_OPENING                        , 'Name': 'Grand Opening Support'             , 'Amount':          12500 }
]
unique_expenses_df = pd.DataFrame(unique_expenses_data)

# Add recurring, monthly operating expenses to unique startup expenses
all_expenses_df = combine_expenses(recurring_expenses_df, unique_expenses_df, GRAND_OPENING, PERIOD_END)

# Account for interest-only payments toward HELOC
all_expenses_df = add_interest_payments(all_expenses_df, INTEREST_RATE)
all_expenses_df = all_expenses_df[['Date', 'Name', 'Amount']]

#######################################
##           R E V E N U E           ##
#######################################
unique_revenue_data = [
    # Example data
    {'Date': datetime(2024,6,1) , 'Name': 'Summer Camp 1' , 'Amount': camp_revenue },
    {'Date': datetime(2024,8,1) , 'Name': 'Summer Camp 2' , 'Amount': camp_revenue },
    {'Date': datetime(2025,6,1) , 'Name': 'Summer Camp 3' , 'Amount': camp_revenue },
    {'Date': datetime(2025,8,1) , 'Name': 'Summer Camp 4' , 'Amount': camp_revenue },
    {'Date': datetime(2026,6,1) , 'Name': 'Summer Camp 5' , 'Amount': camp_revenue },
    {'Date': datetime(2026,8,1) , 'Name': 'Summer Camp 6' , 'Amount': camp_revenue },
    {'Date': datetime(2026,8,1) , 'Name': 'Summer Camp 6' , 'Amount': camp_revenue }

]
unique_revenue_df = pd.DataFrame(unique_revenue_data)

# Assume we get 5 Birthday partys over 3 years?
add_birthday_party(unique_revenue_df, GRAND_OPENING, PERIOD_END, 300) # $300 for a party?  FIXME
add_birthday_party(unique_revenue_df, GRAND_OPENING, PERIOD_END, 300) # $300 for a party?  FIXME
add_birthday_party(unique_revenue_df, GRAND_OPENING, PERIOD_END, 300) # $300 for a party?  FIXME
add_birthday_party(unique_revenue_df, GRAND_OPENING, PERIOD_END, 300) # $300 for a party?  FIXME
add_birthday_party(unique_revenue_df, GRAND_OPENING, PERIOD_END, 300) # $300 for a party?  FIXME

# Model revenue growth through enrollment growth
recurring_revenue_df = revenue_growth_df(GO_STUDENT_COUNT, MONTHLY_STUDENT_PRICE, GROWTH_RATE, SS_STUDENT_COUNT, GRAND_OPENING, PERIOD_END)

# Combine with unique revenue occurances
all_revenue_df = combine_revenue(recurring_revenue_df, unique_revenue_df)

# Fill with leading zeros before we start making money
all_revenue_df = pad_revenues(all_expenses_df, all_revenue_df)

all_revenue_df = all_revenue_df[['Date', 'Name', 'Amount']]
#print(all_revenue_df)


# Add more expenses now that we have some revenue information
all_expenses_df = add_labor_costs_df(all_expenses_df, recurring_revenue_df, HOURLY_RATE)
all_expenses_df = add_tax_and_royalty(all_expenses_df, recurring_revenue_df)
all_expenses_df = add_depreciation_expense(all_expenses_df, USEFUL_LIFE, INST_COMP_COST, GRAND_OPENING, PERIOD_END)

#######################################
##     P R O F I T  &  L O S S       ##
#######################################
# Group revenues and expenses by month and sum them
monthly_revenues = all_revenue_df.resample('M', on='Date').sum(numeric_only=True)
#print("monthly revenue")
#print(monthly_revenues)
monthly_expenses = all_expenses_df.resample('M', on='Date').sum(numeric_only=True)
#print("monthly expenses")
#print(monthly_expenses)

# Subtract expenses from revenues to get profit-loss
profit_loss = monthly_revenues - monthly_expenses
# Prepare the resulting DataFrame
profit_loss_df = pd.DataFrame({
    'Period': profit_loss.index.strftime('%m-%Y'),
    'Profit Loss': profit_loss['Amount']
})

save_profit_loss(profit_loss_df, pl_plot)


#######################################
##         C A S H   F L O W         ##
#######################################
# Assuming profit_loss_df has 'Period' and 'Profit Loss' columns and is sorted by 'Period'
profit_loss_df.set_index('Period', inplace=True)

# Calculate cumulative sum of profit/loss
profit_loss_df['Cumulative'] = profit_loss_df['Profit Loss'].cumsum()

# Add starting cash to get cash on hand
profit_loss_df['Cash On Hand'] = STARTING_CASH + profit_loss_df['Cumulative']

# Reset index for display purposes
cashflow_df = profit_loss_df.reset_index()[['Period', 'Cash On Hand']]

#plot_cashflow(cashflow_df)
save_cashflow(cashflow_df, cf_plot)

