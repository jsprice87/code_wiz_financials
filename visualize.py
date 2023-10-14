import matplotlib.pyplot as plt

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

