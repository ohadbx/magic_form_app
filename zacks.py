import requests
from bs4 import BeautifulSoup
import re
def import_zacks_earnings(symbol):
    class zacks_result:
        def __init__(self):
            market_cap = []
            dividend = []
            beta = []
            Exp_EPS_GR = []
            prior_eps = []
            forward_pe = []
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
            zacks_result.market_cap = float(re.findall("\d+\.\d+", job_element.parent.text)[0])
        elif "Dividend" in job_element.parent.text:
            zacks_result.dividend = float(re.findall("\d+\.\d+", job_element.parent.text)[0])
        elif "Beta" in job_element.parent.text:
            zacks_result.beta = float(re.findall("\d+\.\d+", job_element.parent.text)[0])

    stock_key_earnings = soup.find(id="stock_key_earnings")
    job_elements = stock_key_earnings.find_all("dt")
    for job_element in job_elements:
        if "Exp EPS Growth (3-5yr)" in job_element.parent.text:
            zacks_result.Exp_EPS_GR = float(re.findall("\d+\.\d+", job_element.parent.text)[0])
        elif "Prior Year EPS" in job_element.parent.text:
            zacks_result.prior_eps = float(re.findall("\d+\.\d+", job_element.parent.text)[0])
        elif "Forward PE" in job_element.parent.text:
            zacks_result.forward_pe = float(re.findall("\d+\.\d+", job_element.parent.text)[0])

    # company_description = soup.find(id="comp_desc")  #TODO: not working, try to get company data
    return zacks_result


if __name__ == "__main__":
    symbol ="aapl"
    zacks_result = import_zacks_earnings(symbol)
    print(vars(zacks_result))
    print(zacks_result)