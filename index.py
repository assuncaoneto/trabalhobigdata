import streamlit as st
import investpy as inv
import datetime
import history as hist
import bollinger_bands as bollinger
import styles
import time

tickers = inv.get_stocks_list("brazil")

st.set_page_config(
    page_title='Stock Exchange',
    page_icon=':bar_chart:',
    layout='wide')

styles.set()

with st.sidebar:
    ticker = st.selectbox(
        'Select the Action or Real Estate Fund',
        tickers,
    )

    date_reference = st.date_input(
        "Select an init of period",
        datetime.datetime.today()
    )

    number_of_days = st.number_input('Insert a number of days', value=30)

    sleep_time = st.slider(
        'Select update time (seconds)',
        min_value=5, max_value=60, step=5,
        value=10
    )

    init_date = date_reference + datetime.timedelta(days=-(30 + number_of_days))
    end_date = date_reference

    toogle = st.checkbox("Auto Refresh", value=False)

def prepare_history_visualization():
    history, instance = hist.get(ticker, init_date=init_date, end_date=end_date) if init_date else hist.get(ticker)
    
    if not history.empty:
        print("CURRENT PRICE ->", history["Close"].iat[-1])
        bollinger_figure = bollinger.get(ticker, history)

        current_value.metric("Current Value", f"R$ {round(history['Close'].iloc[-1], 2)}", f"{round(((history['Close'].iloc[-1] / history['Close'].iloc[-2]) - 1) * 100, 2)}%")
        min_value.metric("Minimum Value", f"R$ {round(history['Close'].min(), 2)}", f"{round(((history['Close'].min() / history['Close'].iloc[-1]) - 1) * 100, 2)}%")
        max_value.metric("Maximum Value", f"R$ {round(history['Close'].max(), 2)}", f"{round(((history['Close'].max() / history['Close'].iloc[-1]) - 1) * 100, 2)}%")

        graph.plotly_chart(bollinger_figure, use_container_width=True, sharing="streamlit")
    else:
        st.write("No data available for visualization.")

if ticker and sleep_time:

    col1, col2, col3 = st.columns(3)

    with col1:
        current_value = st.metric(label="Current Value", value="-")
    with col2:
        min_value = st.metric(label="Minimum Value", value="-")
    with col3:
        max_value = st.metric(label="Maximum Value", value="-")
    graph = st.empty()

    while toogle:
        prepare_history_visualization()
        time.sleep(sleep_time)
    else:
        prepare_history_visualization()

