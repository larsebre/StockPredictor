import altair as alt
import data_analysis as da
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Stock Analysis",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="expanded",
)


end_date = datetime.datetime.strptime(st.text_input("Enter Date here:   year:month:day", datetime.datetime.now().strftime('%y-%m-%d')), '%y-%m-%d')
start_date = end_date - datetime.timedelta(days=1000)
ticker_input = st.text_input("Enter TICKER here: ", "EQNR.OL")


analyst = da.DataAnalysis(ticker_input, days_forecast=20, start_date=start_date, end_date=end_date)
analyst.generate_data()
st.line_chart(analyst.price_data)


# Scatter plot for ADI/ Price Change and histogram to visualize the data distribution around ADI Now
st.write('ADI Analysis')
TI = 'ADI'
type_list = ['Previous Data'] * len(analyst.TI.index)
type_list.append('Now')
adi_list = analyst.TI[TI].to_list()
adi_list.append(analyst.TI_past_day[TI].to_list()[0])
TI = 'Price Change'
change_list = analyst.TI[TI].to_list()
change_list.append(0)
df_adi = pd.DataFrame({ 'Type' : type_list,
                        'ADI' : adi_list,
                        'Price Change': change_list})
dom = ['Previous Data', 'Now']
rng = ['lightblue', 'red']
chart = alt.Chart(df_adi).mark_circle(size=120).encode(
    alt.X('ADI', scale=alt.Scale(zero=False)),
    alt.Y('Price Change', scale=alt.Scale(zero=False, padding=1)),
    color=alt.Color('Type', scale=alt.Scale(domain=dom, range=rng)),
    tooltip=['Type']
)
st.write(chart)

TI = 'ADI'
min = analyst.TI[TI].min()
max = analyst.TI[TI].max()
val_range = (max - min)

mask = (analyst.TI[TI] >= (analyst.TI_past_day[TI].mean() - val_range*0.025))
TI_hist = analyst.TI[mask]
mask = (analyst.TI[TI] <= (analyst.TI_past_day[TI].mean() + val_range*0.025))
TI_hist = TI_hist[mask]
chart = alt.Chart(TI_hist)
bar = chart.mark_bar().encode(
    alt.X('Price Change', bin=True),
    y='count()',
)
rule = chart.mark_rule(color='red').encode(
    x='mean(Price Change):Q',
    size=alt.value(5)
)
st.write(bar + rule)


# Scatter plot for MFI/ Price Change and histogram to visualize the data distribution around ADI Now
st.write('MFI Analysis')
TI = 'MFI'
type_list = ['Previous Data'] * len(analyst.TI.index)
type_list.append('Now')
adi_list = analyst.TI[TI].to_list()
adi_list.append(analyst.TI_past_day[TI].to_list()[0])
TI = 'Price Change'
change_list = analyst.TI[TI].to_list()
change_list.append(0)
df_adi = pd.DataFrame({ 'Type' : type_list,
                        'MFI' : adi_list,
                        'Price Change': change_list})
dom = ['Previous Data', 'Now']
rng = ['lightblue', 'red']
chart = alt.Chart(df_adi).mark_circle(size=120).encode(
    alt.X('MFI', scale=alt.Scale(zero=False)),
    alt.Y('Price Change', scale=alt.Scale(zero=False, padding=1)),
    color=alt.Color('Type', scale=alt.Scale(domain=dom, range=rng)),
    tooltip=['Type']
)
st.write(chart)

TI = 'MFI'
min = analyst.TI[TI].min()
max = analyst.TI[TI].max()
val_range = (max - min)

mask = (analyst.TI[TI] >= (analyst.TI_past_day[TI].mean() - val_range*0.025))
TI_hist = analyst.TI[mask]
mask = (analyst.TI[TI] <= (analyst.TI_past_day[TI].mean() + val_range*0.025))
TI_hist = TI_hist[mask]
chart = alt.Chart(TI_hist)
bar = chart.mark_bar().encode(
    alt.X('Price Change', bin=True),
    y='count()',
)
rule = chart.mark_rule(color='red').encode(
    x='mean(Price Change):Q',
    size=alt.value(5)
)
st.write(bar + rule)


# Scatter plot for CCI/ Price Change and histogram to visualize the data distribution around ADI Now
st.write('CCI Analysis')
TI = 'CCI'
type_list = ['Previous Data'] * len(analyst.TI.index)
type_list.append('Now')
adi_list = analyst.TI[TI].to_list()
adi_list.append(analyst.TI_past_day[TI].to_list()[0])
TI = 'Price Change'
change_list = analyst.TI[TI].to_list()
change_list.append(0)
df_adi = pd.DataFrame({ 'Type' : type_list,
                        'CCI' : adi_list,
                        'Price Change': change_list})
dom = ['Previous Data', 'Now']
rng = ['lightblue', 'red']
chart = alt.Chart(df_adi).mark_circle(size=120).encode(
    alt.X('CCI', scale=alt.Scale(zero=False)),
    alt.Y('Price Change', scale=alt.Scale(zero=False, padding=1)),
    color=alt.Color('Type', scale=alt.Scale(domain=dom, range=rng)),
    tooltip=['Type']
)
st.write(chart)

TI = 'CCI'
min = analyst.TI[TI].min()
max = analyst.TI[TI].max()
val_range = (max - min)

mask = (analyst.TI[TI] >= (analyst.TI_past_day[TI].mean() - val_range*0.025))
TI_hist = analyst.TI[mask]
mask = (analyst.TI[TI] <= (analyst.TI_past_day[TI].mean() + val_range*0.025))
TI_hist = TI_hist[mask]
chart = alt.Chart(TI_hist)
bar = chart.mark_bar().encode(
    alt.X('Price Change', bin=True),
    y='count()',
)
rule = chart.mark_rule(color='red').encode(
    x='mean(Price Change):Q',
    size=alt.value(5)
)
st.write(bar + rule)


# Scatter plot for RSI/ Price Change and histogram to visualize the data distribution around ADI Now
st.write('RSI Analysis')
TI = 'RSI'
type_list = ['Previous Data'] * len(analyst.TI.index)
type_list.append('Now')
adi_list = analyst.TI[TI].to_list()
adi_list.append(analyst.TI_past_day[TI].to_list()[0])
TI = 'Price Change'
change_list = analyst.TI[TI].to_list()
change_list.append(0)
df_adi = pd.DataFrame({ 'Type' : type_list,
                        'RSI' : adi_list,
                        'Price Change': change_list})
dom = ['Previous Data', 'Now']
rng = ['lightblue', 'red']
chart = alt.Chart(df_adi).mark_circle(size=120).encode(
    alt.X('RSI', scale=alt.Scale(zero=False)),
    alt.Y('Price Change', scale=alt.Scale(zero=False, padding=1)),
    color=alt.Color('Type', scale=alt.Scale(domain=dom, range=rng)),
    tooltip=['Type']
)
st.write(chart)

TI = 'RSI'
min = analyst.TI[TI].min()
max = analyst.TI[TI].max()
val_range = (max - min)

mask = (analyst.TI[TI] >= (analyst.TI_past_day[TI].mean() - val_range*0.025))
TI_hist = analyst.TI[mask]
mask = (analyst.TI[TI] <= (analyst.TI_past_day[TI].mean() + val_range*0.025))
TI_hist = TI_hist[mask]
chart = alt.Chart(TI_hist)
bar = chart.mark_bar().encode(
    alt.X('Price Change', bin=True),
    y='count()',
)
rule = chart.mark_rule(color='red').encode(
    x='mean(Price Change):Q',
    size=alt.value(5)
)
st.write(bar + rule)