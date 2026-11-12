"""
MSME AI Cash Flow Estimator – Starter Script
==========================================
Practical demo for Indian MSMEs:
- Loads sample transaction data
- Calculates cash inflows / outflows
- Estimates runway and simple insights
- Ready to extend with real AI models

Usage:
    python cashflow_estimator.py
"""

import pandas as pd
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Demo transaction data (in real use, load from CSV / bank / UPI export)
# Columns: date, description, amount, type (credit/debit), category
# ---------------------------------------------------------------------------
DEMO_DATA = [
    {"date": "2026-10-01", "description": "Customer Invoice #1024", "amount": 85000, "type": "credit", "category": "sales"},
    {"date": "2026-10-03", "description": "UPI - Supplier Payment", "amount": -22000, "type": "debit", "category": "purchase"},
    {"date": "2026-10-05", "description": "GST Payment Q2", "amount": -12500, "type": "debit", "category": "gst"},
    {"date": "2026-10-10", "description": "Customer Invoice #1025", "amount": 64000, "type": "credit", "category": "sales"},
    {"date": "2026-10-12", "description": "UPI - Office Rent", "amount": -18000, "type": "debit", "category": "opex"},
    {"date": "2026-10-15", "description": "UPI - Raw Material", "amount": -31000, "type": "debit", "category": "purchase"},
    {"date": "2026-10-20", "description": "Customer Invoice #1026", "amount": 92000, "type": "credit", "category": "sales"},
    {"date": "2026-10-25", "description": "UPI - Staff Salary", "amount": -45000, "type": "debit", "category": "opex"},
    {"date": "2026-10-28", "description": "GST Input Credit", "amount": 4800, "type": "credit", "category": "gst"},
]

def load_transactions(data=None):
    """Load transactions into a DataFrame."""
    if data is None:
        data = DEMO_DATA
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = df["amount"].astype(float)
    return df

def calculate_cashflow(df):
    """Compute summary cash-flow metrics."""
    total_inflow = df.loc[df["amount"] > 0, "amount"].sum()
    total_outflow = abs(df.loc[df["amount"] < 0, "amount"].sum())
    net_cashflow = total_inflow - total_outflow
    
    # Simple monthly burn (assume 30-day period in demo)
    period_days = (df["date"].max() - df["date"].min()).days or 30
    avg_daily_burn = total_outflow / period_days if period_days else 0
    
    # Assume current cash balance for runway demo (in real app, user inputs this)
    current_cash = 120000  # ₹1.2 lakh example
    runway_days = current_cash / avg_daily_burn if avg_daily_burn > 0 else float("inf")
    
    return {
        "total_inflow": round(total_inflow, 2),
        "total_outflow": round(total_outflow, 2),
        "net_cashflow": round(net_cashflow, 2),
        "avg_daily_burn": round(avg_daily_burn, 2),
        "runway_days": round(runway_days, 1),
        "current_cash_assumed": current_cash,
    }

def gst_aware_insights(df):
    """Simple GST-related observations (demo rules)."""
    gst_debits = df[(df["category"] == "gst") & (df["amount"] < 0)]["amount"].sum()
    gst_credits = df[(df["category"] == "gst") & (df["amount"] > 0)]["amount"].sum()
    return {
        "gst_paid": abs(gst_debits),
        "gst_input_credit": gst_credits,
        "net_gst_outflow": abs(gst_debits) - gst_credits,
    }

def print_report(metrics, gst_info):
    """Pretty-print the cash-flow report."""
    print("=" * 55)
    print("  MSME AI CASH FLOW ESTIMATOR – DEMO REPORT")
    print("  (Indian MSME focused | Starter version)")
    print("=" * 55)
    print(f"Total Inflows (Sales etc.) : ₹{metrics['total_inflow']:,.0f}")
    print(f"Total Outflows             : ₹{metrics['total_outflow']:,.0f}")
    print(f"Net Cash Flow              : ₹{metrics['net_cashflow']:,.0f}")
    print(f"Assumed Current Cash       : ₹{metrics['current_cash_assumed']:,.0f}")
    print(f"Average Daily Burn         : ₹{metrics['avg_daily_burn']:,.0f}")
    print(f"Estimated Runway           : {metrics['runway_days']} days")
    print("-" * 55)
    print("GST Snapshot:")
    print(f"  GST Paid                 : ₹{gst_info['gst_paid']:,.0f}")
    print(f"  Input Tax Credit         : ₹{gst_info['gst_input_credit']:,.0f}")
    print(f"  Net GST Outflow          : ₹{gst_info['net_gst_outflow']:,.0f}")
    print("-" * 55)
    if metrics["runway_days"] < 45:
        print("⚠️  Alert: Runway under 45 days. Consider accelerating collections or negotiating supplier terms.")
    else:
        print("✅ Cash position looks manageable. Monitor delayed invoices closely.")
    print("=" * 55)
    print("\nNext steps: Replace DEMO_DATA with real CSV, add forecasting model, or integrate UPI/GST parsers.")

def main():
    print("Loading sample MSME transactions...")
    df = load_transactions()
    print(f"Processed {len(df)} transactions from {df['date'].min().date()} to {df['date'].max().date()}\n")
    
    metrics = calculate_cashflow(df)
    gst_info = gst_aware_insights(df)
    print_report(metrics, gst_info)

if __name__ == "__main__":
    main()
