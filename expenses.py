import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def add_expense(df, name, date, amount):
    """
    Add a unique expense to the dataframe.
    
    Args:
    - df (pd.DataFrame): The dataframe to which the expense should be added.
    - name (str): Name of the expense.
    - date (str or datetime): Date of the expense.
    - amount (float): Amount of the expense.
    
    Returns:
    - pd.DataFrame: Updated dataframe with the new expense.
    """
    new_expense = pd.DataFrame({
        'Name': [name],
        'Date': [date],
        'Amount': [amount]
    })
    return pd.concat([df, new_expense], ignore_index=True)


def combine_expenses(recurring_expenses, unique_expenses, start_date, end_date):
    """
    Processes recurring expenses to create monthly copies of them for each month, 
    starting from the given start date and going for 3 years. 
    Then combines them with unique expenses.

    Parameters:
    - recurring_expenses (DataFrame): Contains all recurring expenses.
    - unique_expenses (DataFrame): Contains unique expenses.
    - start_date (str): Start date in 'YYYY-MM-DD' format.

    Returns:
    - DataFrame: Combined dataframe of processed expenses.
    """
    all_dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Generate a dataframe for each month's recurring expenses
    monthly_expenses = [recurring_expenses.assign(Date=date.strftime('%Y-%m-%d')) for date in all_dates]

    # Combine all monthly dataframes
    recurring_expenses_df = pd.concat(monthly_expenses, ignore_index=True)

    # Combine recurring expenses with unique expenses
    all_expenses = pd.concat([recurring_expenses_df, unique_expenses], ignore_index=True)

    # Ensure the 'Date' column is of type Timestamp
    all_expenses['Date'] = pd.to_datetime(all_expenses['Date'])
 
    # Sort and return
    return all_expenses.sort_values(by='Date')



def interest_payment(total_debt, interest_rate):
    return total_debt * (interest_rate / 100) / 12 # Divided by 12 to get the monthly interest amount


def add_interest_payments(all_expenses, interest_rate):
    """
    Processes all expenses, accrues debt, and calculates interest payment.
    
    Parameters:
    - all_expenses (DataFrame): Contains all recurring and unique expenses.
    - interest_rate (float): The annual interest rate in percentage (e.g., 5 for 5%).
    
    Returns:
    - DataFrame: Updated all_expenses dataframe with interest payments added.
    """
    all_expenses.sort_values(by='Date', inplace=True)

    accrued_debt = 0
    processed_months = set()
    interest_payments = []

    for row in all_expenses.itertuples(index=False):
        date = row.Date
        next_month_date = (date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        accrued_debt += row.Amount

        if date.month not in processed_months:
            payment = interest_payment(accrued_debt, interest_rate)
            
            interest_payments.append({
                'Date': next_month_date.strftime('%Y-%m-%d'),
                'Name': 'Interest Payment',
                'Amount': payment
            })
            
            processed_months.add(date.month)

    interest_payments_df = pd.DataFrame(interest_payments)

    all_expenses = pd.concat([all_expenses, interest_payments_df], ignore_index=True)

    # Ensure the 'Date' column is of type Timestamp
    all_expenses['Date'] = pd.to_datetime(all_expenses['Date']) 

    return all_expenses.sort_values(by='Date')


def calculate_teachers_per_month(student_count):
    """
    Calculate the number of teachers required for a given student count per month.
    
    Parameters:
    - student_count (int): Number of students enrolled in a month.

    Returns:
    - int: Number of teachers required.
    """
    # Constants  ## FIXME
    MAX_STUDENTS_PER_TEACHER = 4
    MAX_STUDENTS_PER_SESSION = 16
    SESSIONS_PER_NIGHT = 3
    NIGHTS_PER_WEEK = 5
    WEEKS_PER_MONTH = 4
    SESSIONS_PER_STUDENT_WEEKLY = 2

    # Calculate total sessions a student attends per month
    sessions_per_student_monthly = SESSIONS_PER_STUDENT_WEEKLY * WEEKS_PER_MONTH
    
    # Total sessions for all students
    total_sessions_monthly = student_count * sessions_per_student_monthly
    
    # Teachers required for each session
    teachers_per_session = MAX_STUDENTS_PER_SESSION / MAX_STUDENTS_PER_TEACHER
    
    # Total teacher sessions required monthly
    total_teacher_sessions_monthly = teachers_per_session * total_sessions_monthly
    
    # Given there are multiple sessions per night and multiple nights per week,
    # calculate the number of sessions a single teacher can conduct in a month
    sessions_per_teacher_monthly = SESSIONS_PER_NIGHT * NIGHTS_PER_WEEK * WEEKS_PER_MONTH

    # Calculate total number of teachers needed monthly
    num_teachers = total_teacher_sessions_monthly / sessions_per_teacher_monthly

    return int(num_teachers)



def add_labor_costs_df(all_expenses_df, recurring_revenue_df, hourly_rate):
    """
    Adds labor costs to the all_expenses_df based on recurring_revenue_df and teacher hourly rates.
    
    Parameters:
    - all_expenses_df (DataFrame): The existing dataframe of all expenses.
    - recurring_revenue_df (DataFrame): The dataframe of recurring revenues with student counts.
    - hourly_rate (float): Hourly rate of each teacher.

    Returns:
    - DataFrame: Updated all_expenses_df with labor costs added.
    """
    labor_costs = []

    for _, row in recurring_revenue_df.iterrows():
        student_count = row['Student_Count']
        num_teachers = calculate_teachers_per_month(student_count)
        
        total_labor_cost = num_teachers * hourly_rate
        
        labor_costs.append({
            'Date': row['Date'],
            'Name': 'Labor Cost',
            'Amount': total_labor_cost
        })

    labor_costs_df = pd.DataFrame(labor_costs)

    # Combine labor costs with existing expenses
    combined_expenses = pd.concat([all_expenses_df, labor_costs_df], ignore_index=True)
    
    # Sort by date for better organization
    return combined_expenses.sort_values(by='Date')


def add_tax_and_royalty(all_expenses_df, all_revenue_df):
    """
    Adds tax and royalty expenses to the all_expenses_df based on the revenue.

    Parameters:
    - all_expenses_df (pd.DataFrame): The dataframe containing all the expenses.
    - all_revenue_df (pd.DataFrame): The dataframe containing all the revenues.

    Returns:
    - pd.DataFrame: Updated all_expenses_df with tax and royalty expenses added.
    """
    TAX_RATE = 0.029  # 2.9% tax
    ROYALTY_RATE = 0.09  # 9% royalty

    # Group the revenues by Date and calculate the sum for each date.
    grouped_revenues = all_revenue_df.groupby('Date').sum(numeric_only=True)

    # Calculate tax and royalty based on the grouped revenues.
    grouped_revenues['Tax'] = grouped_revenues['Amount'] * TAX_RATE
    grouped_revenues['Royalty'] = (grouped_revenues['Amount'] - grouped_revenues['Tax']) * ROYALTY_RATE

    # Create separate DataFrames for tax and royalty expenses to merge with all_expenses_df.
    tax_df = grouped_revenues[['Tax']].reset_index()
    tax_df.columns = ['Date', 'Amount']
    tax_df['Name'] = 'Tax Expense'

    royalty_df = grouped_revenues[['Royalty']].reset_index()
    royalty_df.columns = ['Date', 'Amount']
    royalty_df['Name'] = 'Royalty Expense'

    # Combine the tax and royalty dataframes and then concatenate with all_expenses_df.
    tax_and_royalty_df = pd.concat([tax_df, royalty_df], ignore_index=True)
    all_expenses_df = pd.concat([all_expenses_df, tax_and_royalty_df], ignore_index=True)

    return all_expenses_df.sort_values(by='Date')


def add_depreciation_expense(all_expenses_df, USEFUL_LIFE, INST_COMP_COST, start_date, end_date):
    """
    Adds monthly straight-line depreciation expenses to the all_expenses_df.

    Parameters:
    - all_expenses_df (pd.DataFrame): The dataframe containing all the expenses.
    - USEFUL_LIFE (int): The number of months over which the asset is to be depreciated.
    - INST_COMP_COST (float): The total cost of the instrument/component to be depreciated.
    - start_date (str or datetime): The starting date for the depreciation expense.
    - end_date (str or datetime): The ending date for the depreciation expense.

    Returns:
    - pd.DataFrame: Updated all_expenses_df with depreciation expenses added.
    """
    # Convert start_date and end_date to datetime if they're not already
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    # Calculate monthly depreciation amount
    monthly_depreciation = INST_COMP_COST / USEFUL_LIFE

    # Create a date range for the specified depreciation period
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')

    # Create a DataFrame for the depreciation expenses
    depreciation_df = pd.DataFrame({
        'Date': date_range,
        'Name': 'Depreciation Expense',
        'Amount': [monthly_depreciation for _ in range(min(len(date_range), USEFUL_LIFE))]  # Ensure we don't exceed USEFUL_LIFE
    })

    # Concatenate the depreciation dataframe with all_expenses_df
    all_expenses_df = pd.concat([all_expenses_df, depreciation_df], ignore_index=True)

    return all_expenses_df.sort_values(by='Date')
