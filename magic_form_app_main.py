import streamlit as st
import numpy as np
import pandas as pd
import warnings
import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from agstyler import PINLEFT, PRECISION_TWO, draw_grid

## To run the app locally past in the Terminal:  python -m streamlit run "C:\Users\OHAD\Google Drive\Python\st_webapp\magic_form_app_main.py"
warnings.filterwarnings('ignore')
st.set_page_config(page_title='Simple stock screener', layout='wide', page_icon='logo2.png', initial_sidebar_state='auto')
class filters:
    def __init__(self):
        pass

def update_results_table(results_tbl, filters):
    filtered_tbl = results_tbl[results_tbl['Market Cap [B$]'] >= filters.mkt_cap_lower_limit]
    filtered_tbl = filtered_tbl[filtered_tbl['Market Cap [B$]'] <= filters.mkt_cap_upper_limit]
    filtered_tbl = filtered_tbl[filtered_tbl['AVG Net Profit Margin [%]'] >= filters.net_profit_margin_lower_limit]
    return filtered_tbl

    # getting data
def switch_plot_state(PLOT_FLAG):
    if PLOT_FLAG == True:
        PLOT_FLAG = False
    else:
        PLOT_FLAG = True

with pd.HDFStore('data_01.hdf5') as storedata:
    results_tbl = storedata['data_01']
    metadata = storedata.get_storer('data_01').attrs.metadata


if "PLOT_FLAG" not in st.session_state:
    print(f"Setting default print flag to False...")
    st.session_state.PLOT_FLAG = False

print(f"Loaded table {results_tbl.head(n=10)} with columns:")
for col in results_tbl.columns:
    print(col)
results_tbl["ROIC Score"] = np.nan
results_tbl["EPS Score"] = np.nan
results_tbl["Combined Score"] = np.nan
temp = results_tbl.sort_values(by=['AVG ROIC'])
for ticker in results_tbl.index:
    results_tbl.at[ticker, "ROIC Score"] = temp.index.get_loc(ticker)+1  # change from 0-base to 1-base

temp = results_tbl.sort_values(by=['AVG EPS'])
for ticker in results_tbl.index:
    results_tbl.at[ticker, "EPS Score"] = temp.index.get_loc(ticker)+1  # change from 0-base to 1-base

for ticker in results_tbl.index:
    results_tbl.at[ticker, "Combined Score"] = results_tbl.at[ticker, "ROIC Score"] + results_tbl.at[ticker, "EPS Score"]

results_tbl_date = metadata['Date']
url = "https://www.magicformulainvesting.com/"
# prepare website
# st.markdown("<h1 style='text-align: right; color: black;'>נוסחאת הקסם של גרינבלט - מורחב", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    with st.expander("Description and disclaimer"):
        st.markdown("<h20 style='text-align: left; color: black;'> This is an interactive table with some analyzed stocks data.   \n"
                    "The raw data is fetched freely from different websites across the web and key metric are computed and shown. \n"
                    "You can use the built-in sort, search and filter options in the top of each column and then download the filtered or selected list using one of the buttons below. \n"
                    "ad·di·tion·al·ly a graphical view is available based each comapnie's relative ROIC and EPS rank, as proposed by Joel's Greenblatt Magic Formula (link below).\n" 
                    "DISCLAIMER: The creator of this app cannot and will not be responsible for the validity of the raw data or calculations, as well as any harm that may come to the user from using this app on his computer or making decisions based on it.\n"
                    "Some user interaction may be recorded or monitored for further development and improvemnts of the app",
                    unsafe_allow_html=True)

        st.markdown("[magicformulainvesting.com](%s)" % url)
# with col2:
#     with st.expander("הסבר"):
#         st.markdown("<h6 style='text-align: right; color: black;'> נוסחאת הקסם של ג'ואל גרינבלט מביאה שיטה לסינון ראשוני של מניות העשויות להימצא בתמחור   \n נוח לפני ביצוע הערכה מקיפה", unsafe_allow_html=True)
#         st.markdown("<h6 style='text-align: right; color: black;'> על פי הנוסחא, מדרגים את כל המניות בשוק בסדר יורד על פי התשואה על ההשקעה שלהם. כל חברה מקבלת ניקוד לפי מיקומה ברשימה (1 לחברה הטובה ביותר)", unsafe_allow_html=True)
#         st.markdown("<h6 style='text-align: right; color: black;'> באופן דומה, מבצעים את הדירוג גם לפי הרווחים-למנייה (EPS) של כל חברה", unsafe_allow_html=True)
#         st.markdown("<h6 style='text-align: right; color: black;'> לבסוף, כל חברה מקבלת ציון משוקלל שהוא הסכום של שני הציונים שהוזכרו מעלה", unsafe_allow_html=True)
#         st.markdown( "<h6 style='text-align: right; color: black;'> גרסא מקורית לנוסחאת הקסם אפשר למצוא באתר ",unsafe_allow_html=True)
#         st.markdown("[magicformulainvesting.com](%s)" % url)

max_market_cap = max(results_tbl['Market Cap [B$]'])
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    filters.mkt_cap_lower_limit = st.number_input('Market Cap lower limit [B$]', min_value=0, value=1)
with col2:
    filters.mkt_cap_upper_limit = st.number_input('Market Cap upper limit [B$]', value=max_market_cap)
with col3:
    filters.net_profit_margin_lower_limit = st.number_input('Profit Margin lower limit [%]', min_value=0)
with col4:
    # m = st.markdown("""
    # <style>
    # div.stButton > button:first-child {
    #     background-color: rgb(237, 170, 100);
    # }
    # </style>""", unsafe_allow_html=True)

    if st.button('Show/Hide Plot'):
        # switch_plot_state(PLOT_FLAG)
        if st.session_state.PLOT_FLAG == True:
            print("Switching PLOT_FLAG from True to False")
            st.session_state.PLOT_FLAG = False
        else:
            print("Switching PLOT_FLAG from False to True")
            st.session_state.PLOT_FLAG = True

filtered_tbl = update_results_table(results_tbl, filters)
filtered_tbl.sort_values(by=['Combined Score'])
tbl_to_show = filtered_tbl
tbl_to_show['Company Ticker'] = tbl_to_show.index

# Re-arrange column order:
tbl_to_show = tbl_to_show[['Company Ticker', 'Combined Score', 'ROIC Score', 'EPS Score', 'ShareHolders Equity [B$]', 'Market Cap [B$]',
                           'AVG Net Profit Margin [%]','Shareholders Eq. AVG YoY GR [%]','Revenue AVG YoY GR [%]',
                           'Operating Income AVG YoY GR [%]', 'Net Income AVG YoY GR [%]', 'EPS AVG YoY GR [%]','Free Cash Flow AVG YoY GR [%]',
                           'Cash Equiv [B$]', 'Long Term Debt [B$]', 'Zacks Expected GR [%]']]

st.write('Last Update:', results_tbl_date, 'Number of stocks (unfiltered):', len(results_tbl), 'Number of stocks (after filtering):', len(filtered_tbl) )
data = tbl_to_show

if st.session_state.PLOT_FLAG == True:
    col1, col2 = st.columns(2)
    with col1:
        gb = GridOptionsBuilder.from_dataframe(data)
        # gb.configure_pagination(paginationAutoPageSize=True) # Add pagination
        gb.configure_side_bar() #Add a sidebar
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        gridOptions = gb.build()


        grid_response = AgGrid(
            data,
            # gridOptions=gridOptions,
            # data_return_mode='AS_INPUT',
            # update_mode='MODEL_CHANGED',
            # fit_columns_on_grid_load=True,
            # sizeColumnsToFit = True,
            # # theme='alpine',  # Add theme color to the table
            # enable_enterprise_modules=True,
            # height=300,
            # width='100%',
            # reload_data=False,
            # wrap_text=True,
            # alwaysShowHorizontalScroll= True,
            # resizeable=True
        )
        data = draw_grid(
            df.head(row_number),
            formatter=formatter,
            fit_columns=True,
            selection='multiple',  # or 'single', or None
            use_checkbox='True',  # or False by default
            max_height=300
        )
    with col2:
        fig = px.scatter(
            tbl_to_show,
            x="ROIC Score",
            y="EPS Score",
            size="Market Cap [B$]",
            color='AVG Net Profit Margin [%]',
            hover_name=tbl_to_show.index,
            color_continuous_scale="greens"
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

else:
    col1, col2 = st.columns([9, 1])
    with col1:
        gb = GridOptionsBuilder.from_dataframe(data)
        # gb.configure_pagination(paginationAutoPageSize=True) # Add pagination
        gb.configure_side_bar()  # Add a sidebar
        gb.configure_selection('multiple', use_checkbox=True,
                               groupSelectsChildren = "Group checkbox select children")  # Enable multi-row selection
        gridOptions = gb.build()

        grid_response = AgGrid(
            data,
            gridOptions=gridOptions,
            data_return_mode = 'AS_INPUT',
            update_mode = 'MODEL_CHANGED',
            fit_columns_on_grid_load=True,
            sizeColumnsToFit= True,
            # theme='alpine',  # Add theme color to the table
            enable_enterprise_modules=True,
            height=300,
            width='100%',
            reload_data=False,
            wrap_text=True,
            alwaysShowHorizontalScroll= True,
            resizeable=False
        )

data = grid_response['data']
selected = grid_response['selected_rows']

df_selected_rows = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
st.write('Companies after filtering:', len(data),'Selected  Companies:', len(df_selected_rows))
col1, col2, col3, col4, col5, col6, col6, col6, col6, col6 = st.columns(10)
G = st.markdown("""
    <style>
    div.stButton > download_button:first-child {
        background-color: rgb(37, 190, 37);
    }
    </style>""", unsafe_allow_html=True)
with col1:
    st.download_button(
        label="Download filtered list as CSV",
        data=tbl_to_show.to_csv().encode('utf-8'),
        file_name='MagicFormula.csv',
        mime='text/csv',
    )
with col2:
    st.download_button(
        label="Download Selected companies as CSV",
        data=df_selected_rows.to_csv().encode('utf-8'),
        file_name='MagicFormula.csv',
        mime='text/csv',
    )
with col3:
    if st.button("Download Selected companies Valuation"):
        from main import get_single_stock
        class INPUTS():
            def __init__(self):
                self.statements = ["Cash+Flow", "Balance+Sheet", "Income+Statement", "Metrics", "Growth"]


        common_input = INPUTS()
        df_selected_rows = pd.DataFrame(selected)  # Pass the selected rows to a new dataframe df
        list_of_companies_to_evaluate = df_selected_rows['Company Ticker']
        if len(list_of_companies_to_evaluate):
            print("Too many companies selected, downloading only first 5")
            list_of_companies_to_evaluate = list_of_companies_to_evaluate[:5]
        print(f"Downloading companies: {list_of_companies_to_evaluate}")
        for ticker in list_of_companies_to_evaluate:
            print(f"Downloading valuation for {ticker} ")
            stock_summary = get_single_stock(common_input, ticker, MODE='ONLINE')

