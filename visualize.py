import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def plot_profit_loss(profit_loss_df):
    # Generate a list of colors based on the 'Profit Loss' values
    colors = ['red' if value < 0 else 'blue' for value in profit_loss_df['Profit Loss']]

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(profit_loss_df['Period'], profit_loss_df['Profit Loss'], color=colors)
    plt.title('Monthly Profit/Loss')
    plt.xlabel('Period (MM-YYYY)')
    plt.ylabel('Profit/Loss')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Display the plot
    plt.tight_layout()
    plt.show()


def save_profit_loss(profit_loss_df, filename="profit_loss.png"):
    plt.figure(figsize=(15, 7))
    colors = ['red' if value < 0 else 'blue' for value in profit_loss_df['Profit Loss']]
    plt.bar(profit_loss_df['Period'], profit_loss_df['Profit Loss'], color=colors)
    plt.title('Monthly Profit/Loss')
    plt.xlabel('Period (MM-YYYY)')
    plt.ylabel('Profit/Loss ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y')
    plt.savefig(filename, dpi=300)  # Save the figure to a file
    plt.close()


def plot_cashflow(cashflow_df):
    plt.figure(figsize=(15, 7))
    
    # Plotting the cash flow using a line chart
    plt.plot(cashflow_df['Period'], cashflow_df['Cash On Hand'], 
             color='blue', marker='o', linestyle='-')
    
    # Coloring the areas below and above the x-axis
    plt.fill_between(cashflow_df['Period'], cashflow_df['Cash On Hand'], where=(cashflow_df['Cash On Hand'] >= 0), 
                     color='blue', alpha=0.2, interpolate=True)
    plt.fill_between(cashflow_df['Period'], cashflow_df['Cash On Hand'], where=(cashflow_df['Cash On Hand'] < 0), 
                     color='red', alpha=0.2, interpolate=True)
    
    # Adding title and labels
    plt.title('Cash Flow Over Time')
    plt.xlabel('Period (MM-YYYY)')
    plt.ylabel('Cash On Hand ($)')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    
    # Display the plot
    plt.tight_layout()
    plt.grid(axis='y')
    plt.show()

def save_cashflow(cashflow_df, filename="cashflow.png"):
    plt.figure(figsize=(15, 7))
    plt.plot(cashflow_df['Period'], cashflow_df['Cash On Hand'], color='blue', marker='o', linestyle='-')
    plt.fill_between(cashflow_df['Period'], cashflow_df['Cash On Hand'], where=(cashflow_df['Cash On Hand'] >= 0), 
                     color='blue', alpha=0.2, interpolate=True)
    plt.fill_between(cashflow_df['Period'], cashflow_df['Cash On Hand'], where=(cashflow_df['Cash On Hand'] < 0), 
                     color='red', alpha=0.2, interpolate=True)

    # Find and annotate the minimum data point
    min_value = cashflow_df['Cash On Hand'].min()
    min_date = cashflow_df[cashflow_df['Cash On Hand'] == min_value]['Period'].iloc[0]
    plt.annotate(f"{min_value}$", 
                 (min_date, min_value), 
                 textcoords="offset points", 
                 xytext=(-10,-10), 
                 ha='center', 
                 fontsize=9, 
                 arrowprops=dict(arrowstyle="->"))

    plt.title('Cash Flow Over Time')
    plt.xlabel('Period (MM-YYYY)')
    plt.ylabel('Cash On Hand ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y')
    plt.savefig(filename, dpi=300)  # Save the figure to a file
    plt.close()

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def save_profit_loss_with_students(profit_loss_df, students_df, filename):
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Plotting profit/loss as a bar chart
    colors = ['blue' if value >= 0 else 'red' for value in profit_loss_df['Profit Loss']]
    ax1.bar(profit_loss_df['Period'], profit_loss_df['Profit Loss'], color=colors, label='Profit/Loss')
    ax1.set_xlabel('Period')
    ax1.set_ylabel('Profit/Loss')
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left')

    # Creating a second y-axis for the student count as a line
    ax2 = ax1.twinx()
    ax2.plot(students_df['Period'], students_df['Student_Count'], color='purple', linestyle='-', label='Student Count')
    ax2.set_ylabel('Student Count', color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')
    ax2.legend(loc='upper right')

    # Adjusting the x-axis labels for better visibility
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Set title and layout
    plt.title("Profit/Loss with Student Count")
    fig.tight_layout()

    plt.savefig(filename, dpi=300)
    plt.close()


def save_cashflow_with_students(cashflow_df, students_df, filename):
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Plotting the cashflow as a line
    ax1.plot(cashflow_df['Period'], cashflow_df['Cash On Hand'], color='blue', label='Cashflow')
    ax1.set_xlabel('Period')
    ax1.set_ylabel('Cashflow')
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left')

    # Creating a second y-axis for the student count as a line
    ax2 = ax1.twinx()
    ax2.plot(students_df['Period'], students_df['Student_Count'], color='purple', label='Student Count')
    ax2.set_ylabel('Student Count', color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')
    ax2.legend(loc='upper right')

    # Adjusting the x-axis labels for better visibility
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Resetting the y-axis major formatter to default
    ax1.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax2.yaxis.set_major_formatter(mticker.ScalarFormatter())

    # Set title and layout
    plt.title("Cashflow with Student Count")
    fig.tight_layout()

    plt.savefig(filename, dpi=300)
    plt.close()

