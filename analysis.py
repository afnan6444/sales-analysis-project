
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# 1. Project Setup
# -----------------------------
DATA_PATH = r"C:\Users\khana\.vscode\personal_intro\sales_data.csv"
VIS_PATH = "visualizations/"
REPORT_PATH = "report/"

os.makedirs(VIS_PATH, exist_ok=True)
os.makedirs(REPORT_PATH, exist_ok=True)

# -----------------------------
# 2. Load Data
# -----------------------------
try:
    df = pd.read_csv(DATA_PATH)
    print("✅ Data loaded successfully!")
except FileNotFoundError:
    print("❌ Error: Data file not found. Please check path.")
    exit()

# -----------------------------
# 3. Data Cleaning
# -----------------------------
# Normalize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Convert date/months to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['months'] = pd.to_datetime(df['months'], errors='coerce')

# Ensure numeric columns
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['total_sales'] = pd.to_numeric(df['total_sales'], errors='coerce')

df.dropna(inplace=True)

print("✅ Data cleaned and ready.")

# -----------------------------
# 4. Basic Analysis
# -----------------------------
print("\n📊 Basic Statistics:")
print(df.describe())

# Total sales by product
sales_by_product = df.groupby("product")['total_sales'].sum().sort_values(ascending=False)
print("\nSales by Product:\n", sales_by_product)

# Monthly sales trend
monthly_sales = df.groupby(df['months'].dt.to_period("M"))['total_sales'].sum()

# Regional sales
sales_by_region = df.groupby("region")['total_sales'].sum().sort_values(ascending=False)

# -----------------------------
# 5. Visualizations
# -----------------------------

# Bar Chart: Sales by Product
plt.figure(figsize=(8,6))
sns.barplot(x=sales_by_product.index, y=sales_by_product.values, palette="viridis")
plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(VIS_PATH + "sales_by_product.png")
plt.close()

# Line Chart: Monthly Sales Trend
plt.figure(figsize=(8,6))
monthly_sales.plot(kind="line", marker="o", color="blue")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.grid(True)
plt.tight_layout()
plt.savefig(VIS_PATH + "monthly_sales_trend.png")
plt.close()

# Pie Chart: Regional Sales Distribution
plt.figure(figsize=(6,6))
sales_by_region.plot(kind="pie", autopct="%1.1f%%", startangle=90, cmap="Set3")
plt.title("Regional Sales Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig(VIS_PATH + "regional_sales_distribution.png")
plt.close()

print("✅ Visualizations created and saved in 'visualizations/' folder.")

# -----------------------------
# 6. Report Generation (Markdown)
# -----------------------------
report_text = f"""
# 📊 Sales Analysis Report

## Key Insights
- **Top Product:** {sales_by_product.index[0]} with sales of {sales_by_product.values[0]:,.2f}
- **Monthly Peak:** {monthly_sales.idxmax()} with {monthly_sales.max():,.2f}
- **Top Region:** {sales_by_region.index[0]} contributing {sales_by_region.values[0]:,.2f}

## Visualizations
- Bar chart: Sales by product
- Line chart: Monthly sales trend
- Pie chart: Regional sales distribution
"""

with open(REPORT_PATH + "analysis_report.md", "w", encoding="utf-8") as f:
    f.write(report_text)

print("Report generated in 'report/' folder.")
