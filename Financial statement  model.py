https://github.com/VBOHq/Financial-Modeling-Python-Project.git

# Import Required Packages
import pandas as pd
import json


# Financial_statement ========= work in progress.....! =============
class IncomeStatement:
    def __init__(self, assumptions, historical_data):
        self.assumptions = assumptions
        self.historical_data = historical_data

    def calculate_revenue(self):
        # Calculate revenue based on the revenue growth rate
        revenue_growth = self.assumptions["Revenue Growth Rate"]
        last_year_revenue = self.historical_data["Revenue"].iloc[-1]
        projected_years = [
            self.historical_data["Year"].iloc[-1] + i for i in range(1, 6)
        ]
        projected_revenue = [
            last_year_revenue * (1 + revenue_growth) ** i for i in range(1, 6)
        ]

        return pd.DataFrame({"Year": projected_years, "Revenue": projected_revenue})

    def calculate_cogs(self):
        # Calculate COGS based on the COGS as % of Revenue assumption
        projected_cogs = [
            self.calculate_revenue()["Revenue"].iloc[i]
            * self.assumptions["COGS as % of Revenue"]
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.calculate_revenue()["Year"],
                "Cost of Goods Sold (COGS)": projected_cogs,
            }
        )

    def calculate_gross_profit(self):
        revenue = self.calculate_revenue()["Revenue"]
        cogs = self.calculate_cogs()["Cost of Goods Sold (COGS)"]
        gross_profit = revenue - cogs

        return pd.DataFrame(
            {"Year": self.calculate_revenue()["Year"], "Gross Profit": gross_profit}
        )

    def calculate_sga_expenses(self):
        revenue = self.calculate_revenue()["Revenue"]
        sga_expenses = revenue * self.assumptions["SG&A as % of Sales"]

        return pd.DataFrame(
            {"Year": self.calculate_revenue()["Year"], "SG&A Expenses": sga_expenses}
        )

    def calculate_operating_income(self):
        gross_profit = self.calculate_gross_profit()["Gross Profit"]
        sga_expenses = self.calculate_sga_expenses()["SG&A Expenses"]
        operating_income = gross_profit - sga_expenses

        return pd.DataFrame(
            {
                "Year": self.calculate_revenue()["Year"],
                "Operating Income": operating_income,
            }
        )

    def calculate_interest_expense(self):
        net_debt = (
            self.historical_data["Total Liabilities"] - self.historical_data["Cash"]
        )
        interest_expense = net_debt * self.assumptions["LIBOR"]

        return pd.DataFrame(
            {
                "Year": self.calculate_revenue()["Year"],
                "Interest Expense": interest_expense,
            }
        )

    def calculate_net_income(self):
        operating_income = self.calculate_operating_income()["Operating Income"]
        interest_expense = self.calculate_interest_expense()["Interest Expense"]
        other_income_expense = self.historical_data["Other Income / (Expense)"].iloc[-1]
        taxes = (
            operating_income - interest_expense + other_income_expense
        ) * self.assumptions["Tax Rate"]
        net_income = operating_income - interest_expense + other_income_expense - taxes

        return pd.DataFrame(
            {"Year": self.calculate_revenue()["Year"], "Net Income": net_income}
        )

    def calculate_all_line_items(self):
        projected_revenue = self.calculate_revenue()
        projected_cogs = self.calculate_cogs()
        projected_gross_profit = self.calculate_gross_profit()
        projected_sga_expenses = self.calculate_sga_expenses()
        projected_operating_income = self.calculate_operating_income()
        projected_interest_expense = self.calculate_interest_expense()
        projected_net_income = self.calculate_net_income()

        return pd.DataFrame(
            {
                "Year": projected_revenue["Year"],
                "Revenue": projected_revenue["Revenue"],
                "Cost of Goods Sold (COGS)": projected_cogs[
                    "Cost of Goods Sold (COGS)"
                ],
                "Gross Profit": projected_gross_profit["Gross Profit"],
                "SG&A Expenses": projected_sga_expenses["SG&A Expenses"],
                "Operating Income": projected_operating_income["Operating Income"],
                "Interest Expense": projected_interest_expense["Interest Expense"],
                "Net Income": projected_net_income["Net Income"],
            }
        )

##=========================== Balance Sheet class=========================================
class BalanceSheet:
    def __init__(self, assumptions, historical_data):
        self.assumptions = assumptions
        self.historical_data = historical_data

    def calculate_inventory(self):
        # Calculate inventory based on the days inventory assumption
        days_inventory = self.assumptions["Days Inventory"]
        projected_inventory = [
            (self.historical_data["Cost of Goods Sold (COGS)"].iloc[i] / 365)
            * days_inventory
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Inventory": projected_inventory,
            }
        )

    def calculate_accounts_receivable(self):
        days_accounts_receivable = self.assumptions["Days Accounts Receivable"]
        projected_accounts_receivable = [
            (self.historical_data["Revenue"].iloc[i] / 365) * days_accounts_receivable
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Accounts Receivable": projected_accounts_receivable,
            }
        )

    def calculate_other_current_assets(self):
        other_current_assets = self.assumptions["Other Current Assets"]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Other Current Assets": [other_current_assets] * 5,
            }
        )

    def calculate_total_current_assets(self):
        inventory = self.calculate_inventory()["Inventory"]
        accounts_receivable = self.calculate_accounts_receivable()[
            "Accounts Receivable"
        ]
        other_current_assets = self.calculate_other_current_assets()[
            "Other Current Assets"
        ]

        total_current_assets = inventory + accounts_receivable + other_current_assets

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Current Assets": total_current_assets,
            }
        )

    def calculate_net_ppe(self):
        gross_ppe = self.historical_data["Gross PP&E"]
        accumulated_depreciation = self.historical_data["Accumulated Depreciation"]
        net_ppe = gross_ppe - accumulated_depreciation

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Net PP&E": net_ppe,
            }
        )

    def calculate_goodwill(self):
        goodwill = self.historical_data["Goodwill"].iloc[-1]
        projected_goodwill = [goodwill] * 5

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Goodwill": projected_goodwill,
            }
        )

    def calculate_other_assets(self):
        other_assets = self.assumptions["Other Assets"]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Other Assets": [other_assets] * 5,
            }
        )

    def calculate_total_assets(self):
        total_current_assets = self.calculate_total_current_assets()[
            "Total Current Assets"
        ]
        net_ppe = self.calculate_net_ppe()["Net PP&E"]
        goodwill = self.calculate_goodwill()["Goodwill"]
        other_assets = self.calculate_other_assets()["Other Assets"]

        total_assets = total_current_assets + net_ppe + goodwill + other_assets

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Assets": total_assets,
            }
        )

    def calculate_accounts_payable(self):
        days_payable = self.assumptions["Days Payable"]
        projected_accounts_payable = [
            (self.historical_data["Cost of Goods Sold (COGS)"].iloc[i] / 365)
            * days_payable
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Accounts Payable": projected_accounts_payable,
            }
        )

    def calculate_accrued_liabilities(self):
        accrued_liabilities_as_percentage_of_cogs = self.assumptions[
            "Accrued Liabilities as % of COGS"
        ]
        projected_accrued_liabilities = [
            self.historical_data["Cost of Goods Sold (COGS)"].iloc[i]
            * accrued_liabilities_as_percentage_of_cogs
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Accrued Liabilities": projected_accrued_liabilities,
            }
        )

    def calculate_other_current_liabilities(self):
        other_current_liabilities_as_percentage_of_cogs = self.assumptions[
            "Other Current Liabilities as % of COGS"
        ]
        projected_other_current_liabilities = [
            self.historical_data["Cost of Goods Sold (COGS)"].iloc[i]
            * other_current_liabilities_as_percentage_of_cogs
            for i in range(5)
        ]

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Other Current Liabilities": projected_other_current_liabilities,
            }
        )

    def calculate_total_current_liabilities(self):
        accounts_payable = self.calculate_accounts_payable()["Accounts Payable"]
        accrued_liabilities = self.calculate_accrued_liabilities()[
            "Accrued Liabilities"
        ]
        other_current_liabilities = self.calculate_other_current_liabilities()[
            "Other Current Liabilities"
        ]

        total_current_liabilities = (
            accounts_payable + accrued_liabilities + other_current_liabilities
        )

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Current Liabilities": total_current_liabilities,
            }
        )

    def calculate_total_liabilities(self):
        total_current_liabilities = self.calculate_total_current_liabilities()[
            "Total Current Liabilities"
        ]
        other_liabilities = self.assumptions["Other Liabilities"]

        total_liabilities = total_current_liabilities + other_liabilities

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Liabilities": total_liabilities,
            }
        )

    def calculate_common_stock(self):
        common_stock = self.assumptions["Common Stock"]
        projected_common_stock = [common_stock] * 5

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Common Stock": projected_common_stock,
            }
        )

    def calculate_total_shareholders_equity(self):
        common_stock = self.calculate_common_stock()["Common Stock"]
        retained_earnings = self.historical_data["Retained Earnings"]
        total_shareholders_equity = common_stock + retained_earnings

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Shareholders Equity": total_shareholders_equity,
            }
        )

    def calculate_total_liabilities_and_equity(self):
        total_liabilities = self.calculate_total_liabilities()["Total Liabilities"]
        total_shareholders_equity = self.calculate_total_shareholders_equity()[
            "Total Shareholders Equity"
        ]
        total_liabilities_and_equity = total_liabilities + total_shareholders_equity

        return pd.DataFrame(
            {
                "Year": self.historical_data["Year"].iloc[-1]
                + [i for i in range(1, 6)],
                "Total Liabilities and Equity": total_liabilities_and_equity,
            }
        )

    def calculate_all_line_items(self):
        projected_inventory = self.calculate_inventory()
        projected_accounts_receivable = self.calculate_accounts_receivable()
        projected_other_current_assets = self.calculate_other_current_assets()
        projected_total_current_assets = self.calculate_total_current_assets()
        projected_net_ppe = self.calculate_net_ppe()
        projected_goodwill = self.calculate_goodwill()
        projected_other_assets = self.calculate_other_assets()
        projected_total_assets = self.calculate_total_assets()
        projected_accounts_payable = self.calculate_accounts_payable()
        projected_accrued_liabilities = self.calculate_accrued_liabilities()
        projected_other_current_liabilities = self.calculate_other_current_liabilities()
        projected_total_current_liabilities = self.calculate_total_current_liabilities()
        projected_total_liabilities = self.calculate_total_liabilities()
        projected_common_stock = self.calculate_common_stock()
        projected_total_shareholders_equity = self.calculate_total_shareholders_equity()
        projected_total_liabilities_and_equity = (
            self.calculate_total_liabilities_and_equity()
        )

        return pd.DataFrame(
            {
                "Year": projected_inventory["Year"],
                "Inventory": projected_inventory["Inventory"],
                "Accounts Receivable": projected_accounts_receivable[
                    "Accounts Receivable"
                ],
                "Other Current Assets": projected_other_current_assets[
                    "Other Current Assets"
                ],
                "Total Current Assets": projected_total_current_assets[
                    "Total Current Assets"
                ],
                "Net PP&E": projected_net_ppe["Net PP&E"],
                "Goodwill": projected_goodwill["Goodwill"],
                "Other Assets": projected_other_assets["Other Assets"],
                "Total Assets": projected_total_assets["Total Assets"],
                "Accounts Payable": projected_accounts_payable["Accounts Payable"],
                "Accrued Liabilities": projected_accrued_liabilities[
                    "Accrued Liabilities"
                ],
                "Other Current Liabilities": projected_other_current_liabilities[
                    "Other Current Liabilities"
                ],
                "Total Current Liabilities": projected_total_current_liabilities[
                    "Total Current Liabilities"
                ],
                "Total Liabilities": projected_total_liabilities["Total Liabilities"],
                "Common Stock": projected_common_stock["Common Stock"],
                "Total Shareholders Equity": projected_total_shareholders_equity[
                    "Total Shareholders Equity"
                ],
                "Total Liabilities and Equity": projected_total_liabilities_and_equity[
                    "Total Liabilities and Equity"
                ],
            }
        )

#============================== Cash Flow Class ==================================================================
class CashFlow:
    def __init__(self, assumptions, historical_data, IncomeStatement):
        self.assumptions = assumptions
        self.historical_data = historical_data
        self.income_statement = IncomeStatement

    def calculate_cash_flow_from_operations(self):
        # Calculate cash flow from operations based on the net income and other assumptions
        net_income = income_statement.calculate_all_line_items()["Net Income"]
        depreciation_amortization = self.historical_data[
            "Depreciation and Amortization"
        ].iloc[-1]
        projected_cash_flow_from_operations = net_income + depreciation_amortization

        return pd.DataFrame(
            {
                "Year": income_statement.calculate_all_line_items()["Year"],
                "Cash Flow from Operations": projected_cash_flow_from_operations,
            }
        )

    def calculate_capital_expenditures(self):
        capex_as_percentage_of_sales = self.assumptions["Capex as % of Sales"]
        projected_revenue = income_statement.calculate_all_line_items()["Revenue"]
        projected_capital_expenditures = (
            projected_revenue * capex_as_percentage_of_sales
        )

        return pd.DataFrame(
            {
                "Year": income_statement.calculate_all_line_items()["Year"],
                "Capital Expenditures": projected_capital_expenditures,
            }
        )

    def calculate_asset_disposition(self):
        asset_disposition = self.assumptions["Asset Disposition"]
        projected_asset_disposition = [asset_disposition] * 5

        return pd.DataFrame(
            {
                "Year": income_statement.calculate_all_line_items()["Year"],
                "Asset Disposition": projected_asset_disposition,
            }
        )

    def calculate_cash_flow_from_investing(self):
        capital_expenditures = self.calculate_capital_expenditures()[
            "Capital Expenditures"
        ]
        asset_disposition = self.calculate_asset_disposition()["Asset Disposition"]
        cash_flow_from_investing = capital_expenditures - asset_disposition

        return pd.DataFrame(
            {
                "Year": income_statement.calculate_all_line_items()["Year"],
                "Cash Flow from Investing": cash_flow_from_investing,
            }
        )

    def calculate_change_in_unsecured_debt(self):
        unsecured_debt_amortization = self.assumptions["Unsecured Debt Amortization"]
        projected_change_in_unsecured_debt = [-unsecured_debt_amortization] * 5

        return pd.DataFrame(
            {
                "Year": income_statement.calculate_all_line_items()["Year"],
                "Change in Unsecured Debt": projected_change_in_unsecured_debt,
            }
        )

    def calculate_cash_flow_from_financing(self):
        cash_flow_from_investing = self.calculate_cash_flow_from_investing()[
            "Cash Flow from Investing"
        ]
        change_in_unsecured_debt = self.calculate_change_in_unsecured_debt()[
            "Change in Unsecured Debt"
        ]
        cash_flow_from_financing = cash_flow_from_investing + change_in_unsecured_debt

        return pd.DataFrame(
            {
                "Year": income_statement.calculate_all_line_items()["Year"],
                "Cash Flow from Financing": cash_flow_from_financing,
            }
        )

    def calculate_net_cash_flow(self):
        cash_flow_from_operations = self.calculate_cash_flow_from_operations()[
            "Cash Flow from Operations"
        ]
        cash_flow_from_investing = self.calculate_cash_flow_from_investing()[
            "Cash Flow from Investing"
        ]
        cash_flow_from_financing = self.calculate_cash_flow_from_financing()[
            "Cash Flow from Financing"
        ]
        net_cash_flow = (
            cash_flow_from_operations
            + cash_flow_from_investing
            + cash_flow_from_financing
        )

        return pd.DataFrame(
            {
                "Year": income_statement.calculate_all_line_items()["Year"],
                "Net Cash Flow": net_cash_flow,
            }
        )

    def calculate_ending_cash_position(self):
        beginning_cash_position = self.historical_data["Ending Cash Position"].iloc[-1]
        net_cash_flow = self.calculate_net_cash_flow()["Net Cash Flow"]
        ending_cash_position = beginning_cash_position + net_cash_flow

        return pd.DataFrame(
            {
                "Year": income_statement.calculate_all_line_items()["Year"],
                "Ending Cash Position": ending_cash_position,
            }
        )

    def calculate_all_line_items(self):
        projected_cash_flow_from_operations = self.calculate_cash_flow_from_operations()
        projected_cash_flow_from_investing = self.calculate_cash_flow_from_investing()
        projected_cash_flow_from_financing = self.calculate_cash_flow_from_financing()
        projected_net_cash_flow = self.calculate_net_cash_flow()
        projected_ending_cash_position = self.calculate_ending_cash_position()
        projected_assets_disposition = self.calculate_asset_disposition()
        projected_cash_flow_from_investing = self.calculate_cash_flow_from_investing()
        projected_change_in_unsecured_debt = self.calculate_change_in_unsecured_debt()
        projected_net_cash_flow = self.calculate_net_cash_flow()
        return pd.DataFrame(
            {
                "Year": projected_cash_flow_from_operations["Year"],
                "Cash Flow from Operations": projected_cash_flow_from_operations[
                    "Cash Flow from Operations"
                ],
                "Capital Expenditures": projected_cash_flow_from_investing[
                    "Cash Flow from Investing"
                ],
                "Asset Disposition": projected_assets_disposition["Asset Disposition"],
                "Cash Flow from Investing": projected_cash_flow_from_investing[
                    "Cash Flow from Investing"
                ],
                "Change in Unsecured Debt": projected_change_in_unsecured_debt[
                    "Change in Unsecured Debt"
                ],
                "Cash Flow from Financing": projected_cash_flow_from_financing[
                    "Cash Flow from Financing"
                ],
                "Net Cash Flow": projected_net_cash_flow["Net Cash Flow"],
                "Ending Cash Position": projected_ending_cash_position[
                    "Ending Cash Position"
                ],
            }
        )



        #========== Read in Required Data =====================================

with open("Asumptions.json", "r") as file:
    assumptions = json.load(file)

# Now 'assumptions' contains the data from the JSON file
print(assumptions)

# Read historical data into a DataFrame
historical_data = pd.read_csv("historical_data.csv")

# view the data
historical_data.T

#========================== create instance of the class ======================================

# Apply the input data
income_statement = IncomeStatement(assumptions, historical_data)
balance_sheet = BalanceSheet(assumptions, historical_data)
cash_flow = CashFlow(assumptions, historical_data, IncomeStatement)


# ================= get projected data  =========================

# Get the projected  income statement
projected_income_statement = income_statement.calculate_all_line_items()
# Print the projected data
print("Projected Income Statement:")
print(projected_income_statement)


# projected balance sheet
projected_balance_sheet = balance_sheet.calculate_all_line_items()
print("\nProjected Balance Sheet:")
print(projected_balance_sheet)

# Projected Cash Flow
projected_cash_flow = cash_flow.calculate_all_line_items()
print("\nProjected Cash Flow:")
print(projected_cash_flow)

