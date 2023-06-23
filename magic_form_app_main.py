import streamlit as st
import numpy as np
import pandas as pd
import warnings
import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

## To run the app locally paste in the Terminal:  python -m streamlit run "C:\Users\OHAD\Google Drive\Python\st_webapp\magic_form_app_main.py"
warnings.filterwarnings('ignore')
st.set_page_config(page_title='Simple stock screener', layout='wide', page_icon='logo2.png', initial_sidebar_state='auto')

## getting data
with pd.HDFStore('data_01.hdf5') as storedata:
    results_tbl = storedata['data_01']
    metadata = storedata.get_storer('data_01').attrs.metadata

results_tbl["ROIC Rank"] = np.nan
results_tbl["EPS Rank"] = np.nan
results_tbl["Combined Rank"] = np.nan
temp = results_tbl.sort_values(by=['AVG ROIC'])
for ticker in results_tbl.index:
    results_tbl.at[ticker, "ROIC Rank"] = temp.index.get_loc(ticker)+1  # change from 0-base to 1-base

temp = results_tbl.sort_values(by=['AVG EPS'])
for ticker in results_tbl.index:
    results_tbl.at[ticker, "EPS Rank"] = temp.index.get_loc(ticker)+1  # change from 0-base to 1-base

for ticker in results_tbl.index:
    results_tbl.at[ticker, "Combined Rank"] = results_tbl.at[ticker, "ROIC Rank"] + results_tbl.at[ticker, "EPS Rank"]

results_tbl_date = metadata['Date']
tbl_to_show= results_tbl
# df_selected_rows = results_tbl
url = "https://www.magicformulainvesting.com/"
# prepare website
if 'preset' not in st.session_state:
    st.session_state['preset'] = 'all'

tbl_to_show['Ticker'] = results_tbl.index
tbl_to_show = tbl_to_show[tbl_to_show.columns[::-1]] # reverse
tbl_all = tbl_to_show[['Ticker', 'Combined Rank', 'ROIC Rank', 'EPS Rank', 'Zacks Expected GR [%]', 'Market Cap [B$]','Shareholders Eq. AVG YoY GR [%]',
                           'AVG Net Profit Margin [%]','Revenue AVG YoY GR [%]', 'AVG ROIC', 'AVG EPS',
                           'Operating Income AVG YoY GR [%]', 'Net Income AVG YoY GR [%]', 'EPS AVG YoY GR [%]','Free Cash Flow AVG YoY GR [%]',
                           'Cash Equiv [B$]','Long Term Debt [B$]']]

# st.write('Last Update:', results_tbl_date, 'Number of stocks (unfiltered):', len(results_tbl), 'Number of stocks (after filtering):', len(filtered_tbl) )
data = tbl_all
col1, col2, col3 = st.columns([6,2,1])
with col1:
    with st.expander("Description and disclaimer"):
        st.markdown("<h20 style='text-align: left; color: black;'> This is an interactive table with some analyzed stocks data.   \n"
                    "The raw data is fetched freely from different websites across the web and key metric are computed and shown. \n"
                    "You can use the built-in sort, search and filter options in the top of each column and then download the filtered or selected list using one of the buttons below. \n"
                    "Additionally, a graphical view is available based each company's relative ROIC and EPS rank, as proposed by Joel's Greenblatt Magic Formula:.\n",
                    unsafe_allow_html=True)
        st.markdown("[magicformulainvesting.com](%s)" % url)
        st.markdown("<h20 style='text-align: left; color: black;'>"
                    "DISCLAIMER: The creator of this app cannot and will not be responsible for the validity of the raw data or calculations, as well as any harm that may come to the user from using this app on his computer or making decisions based on it.\n"
                    "Some user interaction may be recorded or monitored for further development and improvemnts of the app",
                    unsafe_allow_html=True)

with col2:
    preset_selection = st.selectbox('Table Preset', ('All', 'Megic Formula', 'YoY', 'CAGR'))

    if preset_selection== "All":
        data = tbl_to_show[['Ticker', 'Combined Rank', 'ROIC Rank', 'EPS Rank', 'Zacks Expected GR [%]', 'Market Cap [B$]','Shareholders Eq. AVG YoY GR [%]',
                           'AVG Net Profit Margin [%]','Revenue AVG YoY GR [%]', 'AVG ROIC', 'AVG EPS',
                           'Operating Income AVG YoY GR [%]', 'Net Income AVG YoY GR [%]', 'EPS AVG YoY GR [%]','Free Cash Flow AVG YoY GR [%]',
                           'Cash Equiv [B$]','Long Term Debt [B$]']]
        st.session_state['preset'] = 'all'
    elif preset_selection== "Magic Formula":
        data = tbl_to_show[
            ['Ticker', 'Combined Rank', 'ROIC Rank', 'EPS Rank', 'Market Cap [B$]', 'Zacks Expected GR [%]',
             'AVG Net Profit Margin [%]']]
        st.session_state['preset'] = 'magic_formula'
    elif preset_selection== "YoY":
        data  = tbl_to_show[['Ticker', 'Zacks Expected GR [%]', 'Market Cap [B$]','Shareholders Eq. AVG YoY GR [%]',
                           'AVG Net Profit Margin [%]','Revenue AVG YoY GR [%]', 'AVG ROIC', 'AVG EPS',
                           'Operating Income AVG YoY GR [%]', 'Net Income AVG YoY GR [%]', 'EPS AVG YoY GR [%]','Free Cash Flow AVG YoY GR [%]',
                           'Cash Equiv [B$]','Long Term Debt [B$]']]
        st.session_state['preset'] = 'yoy'
    elif preset_selection== "CAGR":
        data  = tbl_to_show[['Ticker', 'Zacks Expected GR [%]', 'Market Cap [B$]',
                           'AVG Net Profit Margin [%]', 'AVG ROIC', 'AVG EPS', 'Cash Equiv [B$]','Long Term Debt [B$]']]
        st.session_state['preset'] = 'cagr'
with col3:
    # theme_selection = st.selectbox('Table theme', ('default', 'light','dark', 'blue', 'fresh','material'))
    theme_selection = st.selectbox('Table theme', ('default', 'material'))
if theme_selection == 'default':
    theme_selection = 'streamlit'
# with col2:
#     with st.expander("הסבר"):
#         st.markdown("<h6 style='text-align: right; color: black;'> נוסחאת הקסם של ג'ואל גרינבלט מביאה שיטה לסינון ראשוני של מניות העשויות להימצא בתמחור   \n נוח לפני ביצוע הערכה מקיפה", unsafe_allow_html=True)
#         st.markdown("<h6 style='text-align: right; color: black;'> על פי הנוסחא, מדרגים את כל המניות בשוק בסדר יורד על פי התשואה על ההשקעה שלהם. כל חברה מקבלת ניקוד לפי מיקומה ברשימה (1 לחברה הטובה ביותר)", unsafe_allow_html=True)
#         st.markdown("<h6 style='text-align: right; color: black;'> באופן דומה, מבצעים את הדירוג גם לפי הרווחים-למנייה (EPS) של כל חברה", unsafe_allow_html=True)
#         st.markdown("<h6 style='text-align: right; color: black;'> לבסוף, כל חברה מקבלת ציון משוקלל שהוא הסכום של שני הציונים שהוזכרו מעלה", unsafe_allow_html=True)
#         st.markdown( "<h6 style='text-align: right; color: black;'> גרסא מקורית לנוסחאת הקסם אפשר למצוא באתר ",unsafe_allow_html=True)
#         st.markdown("[magicformulainvesting.com](%s)" % url)

gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_pagination() # Add pagination
gb.configure_side_bar()  # Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren = "Group checkbox select children")  # Enable multi-row selection
gridOptions = gb.build()
custom_css = {
    ".ag-header-cell-label": {"justify-content": "left"},
    # ".ag-header-cell-label": {"font-size": "22px"},
    ".ag-header-group-cell-label": {"justify-content": "left"}
    }
grid_response = AgGrid(
    data,
    gridOptions=gridOptions,
    # data_return_mode = 'AS_INPUT',
    data_return_mode='FILTERED',
    update_mode = 'MODEL_CHANGED',
    fit_columns_on_grid_load=False,
    sizeColumnsToFit=True,
    theme=theme_selection,  # Add theme color to the table
    enable_enterprise_modules=True,
    height=350,
    width='100%',
    reload_data=False,
    wrap_text=True,
    # alwaysShowHorizontalScroll= True,
    # ShowHorizontalScroll=True,
    custom_css=custom_css,
    resizeable=False)
gb.configure_side_bar()  # Add a sidebar

data = grid_response['data']
st.write('')
st.write('')
df_selected_rows = pd.DataFrame(grid_response['selected_rows']) #Pass the selected rows to a new dataframe df
col1, col2 = st.columns([8,1])
with col1:
    st.write('Data Update:', results_tbl_date,'Number of stocks (unfiltered):', len(results_tbl),'Number of stocks (filtered):', len(data),'Selected  Companies:', len(df_selected_rows))
with col2:
        st.download_button(label="Download Selected as CSV",
        data=df_selected_rows.to_csv().encode('utf-8'),
        file_name='MagicFormula.csv',mime='text/csv')

col1, col2, col3, col4, col5, col6, col6, col6, col6, col6 = st.columns(10)
col1, col2, = st.columns(2)
with col2:
    if len(data)>0 and (st.session_state['preset'] == 'all' or st.session_state['preset'] == 'magic_formula'):
        st.write('X,Y  - ROIC Rank Vs. EPS Rank (Higher is better), Profit Margin (color), Market Cap (size)')
        fig = px.scatter(data,
            x="ROIC Rank",
            y="EPS Rank",
            size="Market Cap [B$]",
            color='AVG Net Profit Margin [%]',
            hover_name=data['Ticker'],
            color_continuous_scale="greens")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
#     if st.button("Download Selected companies for Valuation"):
#         from main import get_single_stock
#         class INPUTS():
#             def __init__(self):
#                 self.statements = ["Cash+Flow", "Balance+Sheet", "Income+Statement", "Metrics", "Growth"]
#
#         common_input = INPUTS()
#         df_selected_rows = pd.DataFrame(selected)  # Pass the selected rows to a new dataframe df
#         list_of_companies_to_evaluate = df_selected_rows['Ticker']
#         if len(list_of_companies_to_evaluate):
#             print("Too many companies selected, downloading only first 5")
#             list_of_companies_to_evaluate = list_of_companies_to_evaluate[:5]
#         print(f"Downloading companies: {list_of_companies_to_evaluate}")
#         for ticker in list_of_companies_to_evaluate:
#             print(f"Downloading valuation for {ticker} ")
#             stock_summary = get_single_stock(common_input, ticker, MODE='ONLINE')