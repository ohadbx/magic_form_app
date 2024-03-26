import time
import webbrowser, shutil
from os import listdir
from os.path import isfile, join
import pandas as pd

import pandas as pd

from stock_results import update_template, get_data_from_stock_excel, get_stock_data

# TODO: fix crash when missing income tax provision, for example AAT and SB
# TODO: fix crash when missing income tax provision, for example AAT and SB
def download_stockrow_excel(tickers):
    failed = []
    success = 0
    for ticker in tickers:
        try:
            ticker = ticker.upper()
            url = "https://stockrow.com/vector/exports/financials/" + ticker + "?direction=desc "
            x = webbrowser.open(url)
            if x is True:
                success += 1
        except Exception as e:
            print(f"failed to dowload {ticker}, reason {e}")
    return success, failed


def make_stock_valuations(raw_excel_filename):
    ticker = raw_excel_filename.split("financials_export_")[1]
    ticker = ticker.split("_")[0]
    stock = get_stock_data(ticker, raw_excel_filename)
    stock.ticker = ticker
    result = update_template(stock)
    return 0

if __name__ == '__main__':
    working_dir  = r"C:\Users\OHAD\Google Drive\QualityInvetments"
    download_path = r"C:\Users\OHAD\Downloads"
    added_files = []
    tickers = []
    failed_list = []
    success_list = []
    existing_files = [f for f in listdir(download_path) if isfile(join(download_path, f))]

    while True:
        tickers = []
        OPTION = input(f"Select option:\n "
                       f"1- Build stocks Database with updated values\n "
                       f"2- valuate shortlist\n "
                       f"3- update stocks list\n "
                       f"4 - produce valuations for financial files in \Downloads \n "
                       f"Or enter ticker to get single stock data\n")


        if OPTION == '1':
            print()
        elif OPTION == '2':
            shortlist = pd.read_excel(r'C:\Users\OHAD\Google Drive\QualityInvetments\Valuations\Shortlist.xlsx')
            tickers = shortlist["Ticker"]
            print(f"Loaded {len(tickers)} from shortlis")

        elif OPTION == '4':
            for file in listdir(download_path):
                if "financials_export_" in file:
                    downloaded_file = download_path + "\\" + file
                    try:

                        result = make_stock_valuations(downloaded_file)
                        print(f"Valuating {file} Completed!")
                    except Exception as e:
                        filename = file.split("_")[2]
                        failed_list.append(file)

                print(f"Failed to produce Valuation for {failed_list}")
        else:
            tickers.append(OPTION.upper())

        success, failed = download_stockrow_excel(tickers)
        SLEEP_AFTER_DOWNLOAD = 4 # sec
        time.sleep(SLEEP_AFTER_DOWNLOAD)
        new_files = [f for f in listdir(download_path) if isfile(join(download_path, f))]
        if len(failed)>0:
            print(failed)

        for element in new_files: # Create a list of new files that were downloaded
            if element not in existing_files:
                added_files.append(element)

        if len(added_files) != len(tickers):
            print(f"Not all files found in download folder!")

        # Produce valuations of files in folder
        print(f"Performing valuations")
        for file in added_files:
            downloaded_file = download_path + "\\" +file
            try:
                result = make_stock_valuations(downloaded_file)
            except Exception as e:
                filename = file.split("_")[2]
                failed_list.append(file)

        print(f"Failed to produce Valuation for {failed_list}")
        # Clean up - Move files to a new desired location
        print(f"Moving files to \stockrow_excels")
        for file in added_files:
            try:
                destination_path = working_dir+"\stockrow_excels"
                source_path = download_path + "\\" +file
                shutil.move(source_path, destination_path)
            except Exception as e:
                print(f"failed to move file {source_path}, reason {e}")