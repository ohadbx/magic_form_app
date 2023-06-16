import requests, csv, os, subprocess
import pandas as pd,  numpy as np
import time
def getfields(response):
    # input: response file of stockrow api of a specific company and financial statement
    # output: list of all available headers of financial information on that response file
    company_data = response.json()
    company_fields = []
    for dics in company_data:
        for keys in dics:
            company_fields.append(keys)
    company_fields = (dict.fromkeys(company_fields))
    return company_fields


def create_id_name_dict(indicators):
    stockrow_codes = {}
    for indicators_dict in indicators:
        stockrow_codes[indicators_dict['id']] = indicators_dict['name']
    return stockrow_codes


def write_company_rawdata(ticker, state, RawResults):
    indicators = requests.get("https://stockrow.com/api/indicators.json")
    indicators = indicators.json()
    stockrow_codes = create_id_name_dict(indicators)
    response = requests.get(
        f"https://stockrow.com/api/companies/{ticker}/financials.json?ticker={ticker}&dimension=A&section={state}")


def write_company_data(ticker, state, RawResults,RawResDataFrame, WRITE_FLAG=True):
    try:
        indicators = requests.get("https://stockrow.com/api/indicators.json")
        indicators = indicators.json()
        stockrow_codes = create_id_name_dict(indicators)
        response = requests.get(f"https://stockrow.com/api/companies/{ticker}/financials.json?ticker={ticker}&dimension=A&section={state}")
        if response.status_code == 404:
            print(f'Status 404 for {ticker}: {state}')
            return 404
        fieldnames = getfields(response)
        datalst = response.json()

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        response.status_code = 404
        raise SystemExit(e)

    if response.status_code == 404:
        print(f'Status 404 for {ticker}: {state}')
        return 404

    fieldnames = getfields(response)
    datalst = response.json()
    temp_dataframe =pd.DataFrame.from_dict(datalst)
    temp_dataframe.head()

    for i, row in temp_dataframe.iterrows():
        id =temp_dataframe['id'][i]
        new_idx = stockrow_codes[id]
        as_list = temp_dataframe.index.tolist()
        idx = as_list.index(i)
        as_list[idx] = new_idx
        temp_dataframe.index = as_list

    RawResDataFrame = pd.concat([RawResDataFrame, temp_dataframe])
    if WRITE_FLAG is True:
        with open(r'C:\Users\OHAD\Google Drive\StockrowScraper-main\webscraper\Book1.csv', mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_file.writelines("{} Data:\n\n".format(state))
            writer.writeheader()

            for dicts in datalst:
                try:
                    dicts['id'] = stockrow_codes[dicts['id']]
                    if dicts['id'] == "Book Value per Share Growth":
                        RawResults.BVPS_Growth = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "EPS Growth (diluted)":
                        RawResults.EPS_Growth = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "ROIC":
                        RawResults.ROIC = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Free Cash Flow Growth":
                        RawResults.FCF_Growth = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Revenue Growth":
                        RawResults.Revenue_Growth = {k: v for k, v in dicts.items() if k != "id"}

                    elif dicts['id'] == "5Y Operating Income Growth  (CAGR)":
                        RawResults.FiveYr_Operating_Income_Growth = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "10Y Operating Income Growth  (CAGR)":
                        RawResults.TenYr_Operating_Income_Growth = {k: v for k, v in dicts.items() if k != "id"}

                    elif dicts['id'] == "Shareholders Equity (Total)":
                        RawResults.Shareholders_Equity = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Operating Income":
                        RawResults.Operating_Income = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Net Income":
                        RawResults.Net_Income = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "EPS (Diluted)":
                        RawResults.EPS = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Free Cash Flow":
                        RawResults.FreeCashFlow = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Revenue":
                        RawResults.Revenue = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Dividends Paid (Total)":
                        RawResults.Dividends = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Net Profit Margin":
                        RawResults.Net_Profit_Margin = {k: v for k, v in dicts.items() if k != "id"}

                    elif dicts['id'] == "Cash and Short Term Investments":
                        RawResults.Cash_Equiv = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Long Term Debt (Total)":
                        RawResults.Long_Term_Debt = {k: v for k, v in dicts.items() if k != "id"}

                    elif dicts['id'] == "Operating Cash Flow":
                        RawResults.CashFlow_Operations = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Investing cash flow":
                        RawResults.CashFlow_Investments = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Total Assets":
                        RawResults.Total_Assets = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Capital Expenditures":
                        RawResults.Capital_Expenditures = {k: v for k, v in dicts.items() if k != "id"}
                    elif dicts['id'] == "Income Tax Provision":
                        RawResults.IncomeTaxProvision = {k: v for k, v in dicts.items() if k != "id"}

                    writer.writerow(dicts)

                except KeyError as e:
                    print(e)
                    pass
    else:
        for dicts in datalst:
            try:
                dicts['id'] = stockrow_codes[dicts['id']]
                if dicts['id'] == "Book Value per Share Growth":
                    RawResults.BVPS_Growth = {k: v for k, v in dicts.items() if k != "id"}
                elif dicts['id'] == "EPS Growth (diluted)":
                    RawResults.EPS_Growth = {k: v for k, v in dicts.items() if k != "id"}
                elif dicts['id'] == "ROIC":
                    RawResults.ROIC = {k: v for k, v in dicts.items() if k != "id"}
                elif dicts['id'] == "Free Cash Flow Growth":
                    RawResults.FCF_Growth = {k: v for k, v in dicts.items() if k != "id"}
                elif dicts['id'] == "Revenue Growth":
                    RawResults.Revenue_Growth = {k: v for k, v in dicts.items() if k != "id"}

            except KeyError as e:
                print(e)
                pass
    return RawResults, RawResDataFrame


def ScarpeStockrow(Symbol, WRITE_FLAG=False):
    class RawResultsClass:
        def __init__(self):
            self.BVPS_Growth = []
            self.EPS_Growth = []
            self.Sales_Growth = []
            self.FCF_Growth = []
            self.ROIC = []
            self.Revenue_Growth = []
            self.CashFlow = []
            self.BalanceSheet = []
            self.IncomeStatement = []
            self.Metrics = []
            self.Growth = []
            self.Dividends = []
            self.Cash_Equiv = []
            self.Long_Term_Debt = []
            self.CashFlow_Operations = []
            self.CashFlow_Investments = []
            self.Total_Assets = []

    RawResults = RawResultsClass()
    df = []
    failed_list = []

    statements = ["Cash+Flow", "Balance+Sheet", "Income+Statement", "Metrics", "Growth"]
    # statements = ["Cash+Flow", "Balance+Sheet", "Income+Statement", "Metrics"]
    RawResDataFrame = pd.DataFrame()
    for state in statements:
        # print(f"Fetching {state} for {Symbol}...")
        RawRes, RawResDataFrame = write_company_data(Symbol, state, RawResults, RawResDataFrame, WRITE_FLAG)

    RawResDataFrame = RawResDataFrame.drop(['id'], axis=1)
    if WRITE_FLAG is True:
        raw_name = r"C:\Users\OHAD\Google Drive\StockrowScraper-main\webscraper\\" + Symbol + '_rawdata.xlsx'
        RawResDataFrame.to_excel(raw_name, na_rep='NaN')
    if RawRes != 404:  # TODO: handle situation where company has only partial data
        try:
            # Process Results - Calculate Alon Haze's parameters
            RawRes.Shareholders_Equity = ([float(x) for x in list(RawRes.Shareholders_Equity.values())])
            I = np.max(np.nonzero(RawRes.Shareholders_Equity)[:])
            RawRes.Shareholders_Equity7YrCAGR = (RawRes.Shareholders_Equity[0]/RawRes.Shareholders_Equity[min(7, I)])**(1/min(7, I))-1
            RawRes.Shareholders_Equity5YrCAGR = (RawRes.Shareholders_Equity[0] / RawRes.Shareholders_Equity[min(5, I)]) ** (1/min(5, I))- 1
            RawRes.Shareholders_Equity3YrCAGR = (RawRes.Shareholders_Equity[0] / RawRes.Shareholders_Equity[min(3, I)]) ** (1/min(3, I))- 1

            RawRes.Revenue = [float(x) for x in list(RawRes.Revenue.values())]
            I = np.max(np.nonzero(RawRes.Revenue)[:])
            RawRes.Revenue7YrCAGR = (RawRes.Revenue[0]/RawRes.Revenue[min(7, I)])**(1/min(7, I))-1
            RawRes.Revenue5YrCAGR = (RawRes.Revenue[0] / RawRes.Revenue[min(5, I)]) ** (1/min(5, I)) - 1
            RawRes.Revenue3YrCAGR = (RawRes.Revenue[0] / RawRes.Revenue[min(3, I)]) ** (1/min(3, I)) - 1

            RawRes.Net_Income = [float(x) for x in list(RawRes.Net_Income.values())]
            I = np.max(np.nonzero(RawRes.Net_Income)[:])
            RawRes.NetIncome7YrCAGR = (RawRes.Net_Income[0]/RawRes.Net_Income[min(7, I)])**(1/min(7, I))-1
            RawRes.NetIncome5YrCAGR = (RawRes.Net_Income[0] / RawRes.Net_Income[min(5, I)]) ** (1/min(5, I)) - 1
            RawRes.NetIncome3YrCAGR = (RawRes.Net_Income[0] / RawRes.Net_Income[min(3, I)]) ** (1/min(3, I)) - 1

            RawRes.Operating_Income = [float(x) for x in list(RawRes.Operating_Income.values())]
            I = np.max(np.nonzero(RawRes.Operating_Income)[:])
            RawRes.Operating_Income7YrCAGR = (RawRes.Operating_Income[0]/RawRes.Operating_Income[min(7, I)])**(1/min(7, I))-1
            RawRes.Operating_Income5YrCAGR = (RawRes.Operating_Income[0] / RawRes.Operating_Income[min(5, I)]) ** (1/min(5, I)) - 1
            RawRes.Operating_Income3YrCAGR = (RawRes.Operating_Income[0] / RawRes.Operating_Income[min(3, I)]) ** (1/min(3, I)) - 1

            RawRes.EPS = [float(x) for x in list(RawRes.EPS.values())]
            I = np.max(np.nonzero(RawRes.EPS)[:])
            RawRes.EPS7YrCAGR = (RawRes.EPS[0]/RawRes.EPS[min(7, I)])**(1/min(7, I))-1
            RawRes.EPS5YrCAGR = (RawRes.EPS[0] / RawRes.EPS[min(5, I)]) ** (1/min(5, I)) - 1
            RawRes.EPS3YrCAGR = (RawRes.EPS[0] / RawRes.EPS[min(3, I)]) ** (1/min(3, I)) - 1

            RawRes.FreeCashFlow = [float(x) for x in list(RawRes.FreeCashFlow.values())]
            I = np.max(np.nonzero(RawRes.FreeCashFlow)[:])
            RawRes.FreeCashFlow7YrCAGR = (RawRes.FreeCashFlow[0]/RawRes.FreeCashFlow[min(7, I)])**(1/min(7, I))-1
            RawRes.FreeCashFlow5YrCAGR = (RawRes.FreeCashFlow[0] / RawRes.FreeCashFlow[min(5, I)]) ** (1/min(5, I)) - 1
            RawRes.FreeCashFlow3YrCAGR = (RawRes.FreeCashFlow[0] / RawRes.FreeCashFlow[min(3, I)]) ** (1/min(3, I)) - 1

            # if RawRes.BVPS_Growth:
            #     RawRes.BVPS_Growth = np.fromiter(RawRes.BVPS_Growth.values(), dtype=float)
            #     RawRes.TenYr_BVPS_Growth = np.mean(RawRes.BVPS_Growth[0:9]) * 100
            #     RawRes.FiveYr_BVPS_Growth = np.mean(RawRes.BVPS_Growth[0:3]) * 100
            #     RawRes.Last_BVPS_Growth = RawRes.BVPS_Growth[0] * 100
            #
            # if RawRes.EPS_Growth:
            #     RawRes.EPS_Growth = np.fromiter(RawRes.EPS_Growth.values(), dtype=float)
            #     RawRes.TenYr_EPS_Growth = np.mean(RawRes.EPS_Growth[0:9]) * 100
            #     RawRes.FiveYr_EPS_Growth = np.mean(RawRes.EPS_Growth[0:3]) * 100
            #     RawRes.Last_EPS_Growth = RawRes.EPS_Growth[0] * 100
            #
            # if RawRes.FCF_Growth:
            #     RawRes.FCF_Growth = np.fromiter(RawRes.FCF_Growth.values(), dtype=float)
            #     RawRes.TenYr_FCF_Growth = np.mean(RawRes.FCF_Growth[0:9]) * 100
            #     RawRes.FiveYr_FCF_Growth = np.mean(RawRes.FCF_Growth[0:3]) * 100
            #     RawRes.Last_FCF_Growth = RawRes.FCF_Growth[0] * 100
            #
            # if RawRes.Revenue_Growth:
            #     RawRes.Revenue_Growth = np.fromiter(RawRes.Revenue_Growth.values(), dtype=float)
            #     RawRes.TenYr_Revenue_Growth = np.mean(RawRes.Revenue_Growth[0:9]) * 100
            #     RawRes.FiveYr_Revenue_Growth = np.mean(RawRes.Revenue_Growth[0:3]) * 100
            #     RawRes.Last_Revenue_Growth = RawRes.Revenue_Growth[0] * 100

            d_alon = {"Symbol": Symbol,     #
            # if RawRes.ROIC:
            #     RawRes.ROIC = np.fromiter(RawRes.ROIC.values(), dtype=float)
            #     RawRes.TenYr_ROIC = np.mean(RawRes.ROIC[0:9]) * 100
            #     RawRes.FiveYr_ROIC = np.mean(RawRes.ROIC[0:3]) * 100
            #     RawRes.Last_ROIC = RawRes.ROIC[0] * 100

            # Arrange Raw results in table
            # d = {"Symbol": Symbol,
            #      'Last_BVPS_Growth': RawRes.Last_BVPS_Growth,
            #      '5Yr_BVPS_Growth': RawRes.FiveYr_BVPS_Growth,
            #      "10Yr_BVPS_Growth": RawRes.TenYr_BVPS_Growth,
            #      'Last_EPS_Growth': RawRes.Last_EPS_Growth,
            #      '5Yr_EPS_Growth': RawRes.FiveYr_EPS_Growth,
            #      "10Yr_EPS_Growth": RawRes.TenYr_EPS_Growth,
            #      'Last_FCF_Growth': RawRes.Last_FCF_Growth,
            #      '5Yr_FCF_Growth': RawRes.FiveYr_FCF_Growth,
            #      "10Yr_FCF_Growth": RawRes.TenYr_FCF_Growth,
            #      'Last_ROIC': RawRes.Last_ROIC,
            #      '5Yr_ROIC': RawRes.FiveYr_ROIC,
            #      "10Yr_ROIC": RawRes.TenYr_ROIC,
            #      'Last_Revenue_Growth': RawRes.Last_Revenue_Growth,
            #      '5Yr_Revenue_Growth': RawRes.FiveYr_Revenue_Growth,
            #      "10Yr_Revenue_Growth": RawRes.TenYr_Revenue_Growth,
            #      'Operating Income': RawRes.Operating_Income, 'Net Income': RawRes.Net_Income,
            #      'EPS': RawRes.EPS, 'Free Cash Flow': RawRes.FreeCashFlow, 'Revenue':  RawRes.Revenue, 'Dividends': RawRes.Dividends,
            #      'Net Profit Margin': RawRes.Net_Profit_Margin}
                      'Shareholders_Equity7YrCAGR': RawRes.Shareholders_Equity7YrCAGR,
                      'Shareholders_Equity5YrCAGR': RawRes.Shareholders_Equity5YrCAGR,
                      'Shareholders_Equity3YrCAGR': RawRes.Shareholders_Equity3YrCAGR,
                      'Revenue7YrCAGR': RawRes.Revenue7YrCAGR,
                      'Revenue5YrCAGR': RawRes.Revenue5YrCAGR,
                      'Revenue3YrCAGR': RawRes.Revenue3YrCAGR,
                      'NetIncome7YrCAGR': RawRes.NetIncome7YrCAGR,
                      'NetIncome5YrCAGR': RawRes.NetIncome5YrCAGR,
                      'NetIncome3YrCAGR': RawRes.NetIncome3YrCAGR,
                      'Operating_Income7YrCAGR': RawRes.Operating_Income7YrCAGR,
                      'Operating_Income5YrCAGR': RawRes.Operating_Income5YrCAGR,
                      'Operating_Income3YrCAGR': RawRes.Operating_Income3YrCAGR,
                      'EPS7YrCAGR': RawRes.EPS7YrCAGR,
                      'EPS5YrCAGR': RawRes.EPS5YrCAGR,
                      'EPS3YrCAGR': RawRes.EPS3YrCAGR,
                      'FreeCashFlow7YrCAGR': RawRes.FreeCashFlow7YrCAGR,
                      'FreeCashFlow5YrCAGR': RawRes.FreeCashFlow5YrCAGR,
                      'FreeCashFlow3YrCAGR': RawRes.FreeCashFlow3YrCAGR
                      }
            for key, val in d_alon.items():
                if isinstance(val, complex):
                    d_alon[key] = np.nan

            df = pd.DataFrame(data=d_alon, index=[0])
        except Exception as e:
            print(f"something failed with symobl {Symbol}: {e}")
            df = []
    return df, RawRes, RawResDataFrame

def build_stocks_DB_OLD(common_input):
    start_time = time.time()
    wroking_dir = common_input.wroking_dir
    Symbol_list_filepath = wroking_dir + "\SymbolList.xlsx"
    SymbolList = pd.read_excel(Symbol_list_filepath)
    ResultsTable = []
    failed_list = []
    for idx, row in SymbolList.iterrows():
        print(f"Running {row['Symbol']} ({idx + 1}/{len(SymbolList)})")
        Results, RawRes, RawResDataFrame = ScarpeStockrow(row['Symbol'], WRITE_FLAG = False)
        if idx == 0:
            ResultsTable = Results
        elif isinstance(Results, pd.DataFrame):
            ResultsTable = pd.concat([ResultsTable, Results], ignore_index=True)
        else:
            failed_list.append(row['Symbol'])
    print(f'{len(ResultsTable)} companies added to DB')
    print(f'{len(failed_list)} companies failed to get data: {failed_list}')
    # Saving Results to CSV
    print(f'Saving results to {wroking_dir}')
    save_path = wroking_dir + "\ResultsTable.csv"
    SAVE_PICKLE = True
    if SAVE_PICKLE is True:
        import pickle
        with open(r'C:\Users\OHAD\Google Drive\StockrowScraper-main\webscraper\stocks_DB.pkl', 'wb') as f:  # open a text file
            pickle.dump(ResultsTable, f)  # serialize the list
            f.close()
            print(f'Saved results to pickle')

    print(f'Saved results to {save_path}')
    ResultsTable.to_csv(save_path, index=False)

    with open(r'C:\Users\OHAD\Google Drive\StockrowScraper-main\webscraper\failed_list.txt', 'w') as fp:
        for item in failed_list:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')
    end_time = time.time()
    print(f'Done build stocks DB. took {end_time-start_time}')
    # subprocess.Popen(f'explorer {wroking_dir}')
    # ScrapeYahoo(Symbol)

def update_shortlist(common_input):
    wroking_dir = r"C:\Users\OHAD\Google Drive\StockrowScraper-main\webscraper"
    Shortlist_filepath = wroking_dir + "\Shortlist.xlsx"
    Shortlist = pd.read_excel(Shortlist_filepath)
    print(Shortlist)
    for symbol in Shortlist['Symbol']:
        print (symbol)

def get_single_stock(common_input, ticker, MODE):
    from zacks import import_zacks_earnings
    from update_excel_template import update_template
    try:
        print(f'Getting single stock {ticker}')
        Growths, RawRes, RawResDataFrame = ScarpeStockrow(ticker, WRITE_FLAG = True)
        # Put RawRes in desired format
        years = list(RawRes.Total_Assets.keys())
        years = [year.split("-")[0] for year in years]
        RawResTable = pd.DataFrame(columns=RawRes.Total_Assets.keys(), index=[0])
        # RawResTable.dropna(*, axis=0, how=_NoDefault.no_default, thresh=_NoDefault.no_default, subset=None, inplace=False)
        RawResTable = RawResTable.drop(labels=None, axis=0, index=0, columns=None, level=None, inplace=False, errors='raise')
        MaxLen = max(len(years), len(RawRes.Shareholders_Equity))
        RawRes.Buybacks = [0] * MaxLen
        if RawRes.Dividends == []:
            RawRes.Dividends = [0] * MaxLen

        RawResTable.loc[len(RawResTable)] = RawRes.Shareholders_Equity
        RawResTable.loc[len(RawResTable)] = RawRes.Dividends
        RawResTable.loc[len(RawResTable)] = RawRes.Buybacks
        RawResTable.loc[len(RawResTable)] = RawRes.Revenue
        RawResTable.loc[len(RawResTable)] = RawRes.Operating_Income
        RawResTable.loc[len(RawResTable)] = RawRes.Net_Income
        RawResTable.loc[len(RawResTable)] = RawRes.EPS
        RawResTable.loc[len(RawResTable)] = RawRes.FreeCashFlow
        RawResTable.loc[len(RawResTable)] = RawRes.ROIC
        RawResTable.loc[len(RawResTable)] = RawRes.Net_Profit_Margin
        RawResTable.loc[len(RawResTable)] = RawRes.Cash_Equiv
        RawResTable.loc[len(RawResTable)] = RawRes.Long_Term_Debt
        RawResTable.loc[len(RawResTable)] = RawRes.CashFlow_Operations
        RawResTable.loc[len(RawResTable)] = RawRes.CashFlow_Investments
        RawResTable.loc[len(RawResTable)] = RawRes.Total_Assets
        RawResTable.loc[len(RawResTable)] = RawRes.IncomeTaxProvision
        RawResTable.loc[len(RawResTable)] = RawRes.Capital_Expenditures

        RawResTable.columns = years
        RawResTable.index = ['Shareholders Equity', 'Dividends', 'Buybacks', 'Revenue', 'Operating Income', 'Net Income',
                             'EPS', 'Free Cash Flow', 'ROIC', 'Net Profit Margin', 'Cash Equiv.', 'Long Term Debt',
                             'Cash Flow from Operations', 'Cash Flow from Investments', 'Total Assets', 'Income Tax Provisions','Capital Expenditures']

        print('Stock fetched successfully!')
        if MODE == 'single':
            # save_path = f"{common_input.wroking_dir}" + "\\" + ticker + '.xlsx'
            save_path = f"{common_input.wroking_dir}" + "\\" + ticker + '.xlsx'
            RawResTable.to_excel(save_path)
            # subprocess.Popen(f'explorer {common_input.wroking_dir}')
            os.startfile(save_path)

        # Build Summary
        YearsToAVG = 5
        RawResTable = RawResTable.astype(float)
        zacks_result = import_zacks_earnings(ticker)
        d = {'ShareHolders Equity [B$]': int(RawResTable.loc['Shareholders Equity'][0]/10**6),
            'Long Term Debt [B$]': int(RawResTable.loc['Long Term Debt'][0]/10**9),
            'Cash Equiv [B$]': int(RawResTable.loc['Cash Equiv.'][0]/10**9),
            'AVG ROIC': round(np.average(RawResTable.loc['ROIC'][0:YearsToAVG-1].to_list())*100, 1),
            'AVG EPS': round(np.average(RawResTable.loc['EPS'][0:YearsToAVG-1].to_list()), 1),
            'AVG Net Profit Margin [%]': round(100*np.average(RawResTable.loc['Net Profit Margin'][0:YearsToAVG-1].to_list()),1),
            'Market Cap [B$]': zacks_result.market_cap,
            'Dividend [$/sh]': zacks_result.dividend,
            'beta': zacks_result.beta,
            'Zacks Expected GR [%]': zacks_result.Exp_EPS_GR,
            'Prior EPS': zacks_result.prior_eps,
            'Forward PE': zacks_result.forward_pe}

        stock_summary = pd.DataFrame(data=d, index=[0])
        stock_summary.index = [ticker]
        if MODE != 'DB':
            update_template(stock_summary,RawResTable)
    except Exception as e:
        stock_summary = "ERROR"
        print(e)
    return stock_summary

def build_stocks_DB(common_input):
    from datetime import date
    import pickle
    start_time = time.time()
    print(f"Building stocks DB... ")
    # working_dir = common_input.wroking_dir
    # Symbol_list_filepath = working_dir + "\SymbolList.xlsx"
    # SymbolList = pd.read_excel(Symbol_list_filepath)
    SymbolList = pd.read_excel("SymbolList.xlsx")
    ResultsTable = []
    failed_list = []
    for idx, row in SymbolList.iterrows():
        ticker = row['Symbol']
        print(f"Running {row['Symbol']} ({idx + 1}/{len(SymbolList)})")
        stock_summary = get_single_stock(common_input, ticker, MODE='DB')
        # if stock_summary == 'ERROR':
        #     print('Something is wrong with results summary')
        if not(isinstance(stock_summary, pd.DataFrame)):
            print(f'Problem with {ticker}')
            continue
        if len(ResultsTable) > 0:
            ResultsTable = ResultsTable.append(stock_summary)
        else:
            ResultsTable = stock_summary

    ResultsTable.Date = date.today()
    print('Storing data in pkl format')
    with open(r'C:\Users\OHAD\Google Drive\StockrowScraper-main\webscraper\stocks_DB.pkl','wb') as f:  # open a text file
        pickle.dump(ResultsTable, f)  # serialize the list
        f.close()
        print(f'Saved results to pickle')

    # store in hdf5 file format
    print('Storing data in hdf5 format')
    storedata = pd.HDFStore('data_01.hdf5')
    storedata.put('data_01', ResultsTable) # data
    metadata = {'Date': date.today(), }  # including metadata
    storedata.get_storer('data_01').attrs.metadata = metadata # getting attributes
    storedata.close() # closing the storedata
    duration = time.time()-start_time
    print(f"Finished building stocks DB took {duration/60:.0f} minutes")


if __name__ == '__main__':
    class INPUTS():
        def __init__(self):
            self.wroking_dir = r"C:\Users\OHAD\Google Drive\StockrowScraper-main\webscraper"
            self.statements = ["Cash+Flow", "Balance+Sheet", "Income+Statement", "Metrics", "Growth"]

    common_input = INPUTS()
    OPTION = input(f"Select option:\n 1- Build stocks Database \n 2- update shortlist\n 3-get single stock data\n")

    if OPTION == '1':
        build_stocks_DB(common_input)
    elif OPTION == '2':
        update_shortlist(common_input)
    elif OPTION == 4:
        current_directory = os.getcwd()
        print(current_directory)
        # url = "http://127.0.0.1:8050/:8080/"
        # webbrowser.open_new(url)
        working_dir = r'C:\Users\OHAD\Google Drive\StocksScraper'
        resultsTable_filepath = working_dir + "/" + "SResultsTable.csv"
        # os.startfile(resultsTable_filepath)
        Watchlist = pd.read_csv(resultsTable_filepath)
        print(Watchlist)
        # subprocess.Popen(r'explorer C:\Users\OHAD\Google Drive\StocksScraper')


    else:
        ticker = OPTION
        try:
            stock_summary = get_single_stock(common_input, ticker, MODE='single')
        except Exception as e:
            print(f'Something went wrong with fetching ticker data {e}')
