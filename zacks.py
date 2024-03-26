import numpy as np
import requests
from bs4 import BeautifulSoup
import re

def get_value(job_element):
    if re.findall("\d+\.\d+", job_element.parent.text) != []:
        result = float(re.findall("\d+\.\d+", job_element.parent.text)[0])
    else:
        result= 'NaN'
    return result
def import_zacks_earnings(symbol):

    try:
        print(f'Fetching Zacks data for {symbol}')
        class zacks_result:
            def __init__(self):
                market_cap = None
                dividend = None
                beta = None
                Exp_EPS_GR = np.nan
                prior_eps = None
                forward_pe = None
                TTM_high = None
                TTM_low = None
        _ZACKS_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        _ZACKS_URL = "https://www.zacks.com/stock/quote/"+ symbol+"/"
        # _ZACKS_URL = 'https://www.zacks.com/stock/quote/%s/detailed-estimates'
        page = requests.get(_ZACKS_URL, headers=_ZACKS_HEADER)
        soup = BeautifulSoup(page.content, "html.parser")
        stock_activity = soup.find(id="stock_activity")
        job_elements = stock_activity.find_all("dt")
        for job_element in job_elements:
            if "Market Cap" in job_element.parent.text:
                # market_cap = re.sub("[^0-9]", "", job_element.parent.text)
                zacks_result.market_cap = np.NAN if get_value(job_element) == 'NaN' else get_value(job_element)
            elif "Dividend" in job_element.parent.text:
                zacks_result.dividend = np.NAN if get_value(job_element) == 'NaN' else get_value(job_element)
            elif "Beta" in job_element.parent.text:
                zacks_result.beta = np.NAN if get_value(job_element) == 'NaN' else get_value(job_element)
            elif "Open" in job_element.parent.text:
                zacks_result.stock_price = np.NAN if get_value(job_element) == 'NaN' else get_value(job_element)
            elif "52 Wk High" in job_element.parent.text:
                zacks_result.TTM_high = np.NAN if get_value(job_element) == 'NaN' else round(get_value(job_element),2)
            elif "52 Wk Low" in job_element.parent.text:
                zacks_result.TTM_low = np.NAN if get_value(job_element) == 'NaN' else round(get_value(job_element),2)

        stock_key_earnings = soup.find(id="stock_key_earnings")
        job_elements = stock_key_earnings.find_all("dt")

        for job_element in job_elements:
            if "Exp EPS Growth (3-5yr)" in job_element.parent.text:
                zacks_result.Exp_EPS_GR = get_value(job_element)
            elif "Prior Year EPS" in job_element.parent.text:
                zacks_result.prior_eps = get_value(job_element)
            elif "Forward PE" in job_element.parent.text:
                zacks_result.forward_pe = get_value(job_element)

        # company_description = soup.find(id="comp_desc")  #TODO: not working, try to get company data
    except Exception as e:
        print(f'Fetching from Zacks Failed for {symbol}: {e}')
    return zacks_result


if __name__ == "__main__":
    symbol ="aapl"
    zacks_result = import_zacks_earnings(symbol)
    print(vars(zacks_result))
    print(zacks_result)