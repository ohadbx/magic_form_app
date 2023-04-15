import streamlit as st
import numpy as np
import pandas as pd
import warnings
import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
warnings.filterwarnings('ignore')
st.set_page_config(page_title='Magic Formula Expanded', layout='wide', page_icon='logo2.png', initial_sidebar_state='auto')
class filters:
    def __init__(self):
        pass

def update_results_table(results_tbl, filters):
    filtered_tbl = results_tbl[results_tbl['Market Cap [B$]'] >= filters.mkt_cap_lower_limit]
    filtered_tbl = filtered_tbl[filtered_tbl['Market Cap [B$]'] <= filters.mkt_cap_upper_limit]
    filtered_tbl = filtered_tbl[filtered_tbl['AVG Net Profit Margin [%]'] >= filters.net_profit_margin_lower_limit]
    return filtered_tbl

    # getting data

with pd.HDFStore('data_01.hdf5') as storedata:
    results_tbl = storedata['data_01']
    metadata = storedata.get_storer('data_01').attrs.metadata

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
st.markdown("<h1 style='text-align: right; color: black;'>נוסחאת הקסם של גרינבלט - מורחב", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col2:
    with st.expander("הסבר"):
        st.markdown("<h6 style='text-align: right; color: black;'> נוסחאת הקסם של ג'ואל גרינבלט מביאה שיטה לסינון ראשוני של מניות העשויות להימצא בתמחור   \n נוח לפני ביצוע הערכה מקיפה", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: right; color: black;'> על פי הנוסחא, מדרגים את כל המניות בשוק בסדר יורד על פי התשואה על ההשקעה שלהם. כל חברה מקבלת ניקוד לפי מיקומה ברשימה (1 לחברה הטובה ביותר)", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: right; color: black;'> באופן דומה, מבצעים את הדירוג גם לפי הרווחים-למנייה (EPS) של כל חברה", unsafe_allow_html=True)
        st.markdown("<h6 style='text-align: right; color: black;'> לבסוף, כל חברה מקבלת ציון משוקלל שהוא הסכום של שני הציונים שהוזכרו מעלה", unsafe_allow_html=True)
        st.markdown( "<h6 style='text-align: right; color: black;'> גרסא מקורית לנוסחאת הקסם אפשר למצוא באתר ",unsafe_allow_html=True)
        st.markdown("[magicformulainvesting.com](%s)" % url)

max_market_cap = max(results_tbl['Market Cap [B$]'])
col1, col2, col3, col4 = st.columns(4)
with col1:
    filters.mkt_cap_lower_limit = st.number_input('Market Cap lower limit [B$]', min_value=0, value=1)
with col2:
    filters.mkt_cap_upper_limit = st.number_input('Market Cap upper limit [B$]', value=max_market_cap)
with col3:
    filters.net_profit_margin_lower_limit = st.number_input('Profit Margin lower limit [%]', min_value=0)
text_contents = 'This is some text'

filtered_tbl = update_results_table(results_tbl, filters)
filtered_tbl.sort_values(by=['Combined Score'])
tbl_to_show = filtered_tbl
tbl_to_show['Company Ticker'] = tbl_to_show.index

# Re-arange column order:
tbl_to_show = tbl_to_show[['Company Ticker', 'Combined Score', 'ROIC Score', 'EPS Score', 'ShareHolders Equity [B$]', 'Market Cap [B$]',
                           'AVG Net Profit Margin [%]',
                           'Cash Equiv [B$]', 'Long Term Debt [B$]']]

st.write('Last Update:', results_tbl_date, 'Number of stocks (unfiltered):', len(results_tbl), 'Number of stocks (after filtering):', len(filtered_tbl) )


data = tbl_to_show
gb = GridOptionsBuilder.from_dataframe(data)
# gb.configure_pagination(paginationAutoPageSize=True) # Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=True,
    # theme='alpine',  # Add theme color to the table
    enable_enterprise_modules=True,
    height=300,
    width='100%',
    reload_data=False,
    wrap_text=True,
    resizeable=False
)

data = grid_response['data']
selected = grid_response['selected_rows']

df_selected_rows = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
st.write('Companies after filtering:', len(data),'Selected  Companies:', len(df_selected_rows))
col1, col2, col3, col4, col5, col6, col6, col6, col6, col6 = st.columns(10)
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
# st.dataframe(tbl_to_show, width=1600)
# fig = px.scatter(
#     tbl_to_show,
#     x="ROIC Score",
#     y="EPS Score",
#     size="Market Cap [B$]",
#     color='AVG Net Profit Margin [%]',
#     hover_name=tbl_to_show.index,
#     color_continuous_scale="greens"
# )
# fig.update_layout({
#     'plot_bgcolor': 'rgba(255,0,0,0)',
#     'paper_bgcolor': 'rgba(0,255,0,0)'
# })
# st.plotly_chart(fig, theme="streamlit", use_container_width=True)
#
# fig.update_layout({
#     'plot_bgcolor': 'rgba(255,0,0,200)',
#     'paper_bgcolor': 'rgba(0,255,0,200)'
# })

