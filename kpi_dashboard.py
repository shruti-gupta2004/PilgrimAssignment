import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os


def load_data(filepath="sales_data.csv"):
    """Load and validate the dataset."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} not found. Place it in the same directory as the script.")

    # Load the data
    data = pd.read_csv(filepath)

    # Validate required columns
    required_columns = ["Date", "ProductID", "ProductName", "Category", "QuantitySold", "PricePerUnit", "TotalSales"]
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    return data


def calculate_kpis(data):
    """Calculate KPIs: Total Sales, ROMS, and AOV per Category."""
    # Total Sales per Category
    total_sales = data.groupby('Category')['TotalSales'].sum()

    # Simulate Marketing Spend as 5% of Total Sales
    marketing_spend = total_sales * 0.05
    roms = total_sales / marketing_spend

    # Average Order Value (AOV = TotalSales / QuantitySold)
    aov = data.groupby('Category').apply(lambda x: x['TotalSales'].sum() / x['QuantitySold'].sum())

    return total_sales, roms, aov


def create_visualizations(total_sales, roms, aov):
    """Create and save visualizations to a PDF."""
    if total_sales.empty or roms.empty or aov.empty:
        raise ValueError("One or more KPI calculations returned empty results. Check the dataset.")

    with PdfPages("kpi_dashboard.pdf") as pdf:
        # Total Sales Bar Chart
        total_sales.plot(kind="bar", title="Total Sales per Category", color="skyblue")
        plt.ylabel("Total Sales")
        pdf.savefig()
        plt.close()

        # ROMS Bar Chart
        roms.plot(kind="bar", title="ROMS per Category", color="orange")
        plt.ylabel("ROMS")
        pdf.savefig()
        plt.close()

        # AOV Bar Chart
        aov.plot(kind="bar", title="AOV per Category", color="green")
        plt.ylabel("AOV")
        pdf.savefig()
        plt.close()

        print("Dashboard saved to kpi_dashboard.pdf")


if __name__ == "__main__":
    try:
        # Load the data
        data = load_data()
        print("Dataset loaded successfully.")

        # Calculate KPIs
        total_sales, roms, aov = calculate_kpis(data)
        print("KPI calculations completed.")

        # Create and save visualizations
        create_visualizations(total_sales, roms, aov)
    except Exception as e:
        print(f"An error occurred: {e}")


