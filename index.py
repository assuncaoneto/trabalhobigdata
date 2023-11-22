import streamlit as st
import investpy as inv
import datetime
import history as hist
import bollinger_bands as bollinger
import styles
import streamlit_toggle as tog
import time
import pandas as pd  # Certifique-se de importar o pandas

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
        "Select an initial period",
        datetime.datetime.today()
    )

    number_of_days = st.number_input('Insert a number of days', value=30)

    sleep_time = st.select_slider(
        'Select update time (seconds)',
        options=[5, 10, 15, 30, 60]
    )

    init_date = date_reference + datetime.timedelta(days=-(30 + number_of_days))
    end_date = date_reference

    toogle_column1, toogle_column2 = st.columns(2)

    with toogle_column1:
        st.write(f"Auto Refresh ({sleep_time}s)")
    with toogle_column2:
        toogle = tog.st_toggle_switch(
            key="Key1",
            default_value=False,
            label_after=False,
            inactive_color='rgba(255, 75, 75, .5)',
            active_color="rgb(255, 75, 75)",
            track_color="rgba(255, 75, 75, .5)"
        )

# Defina as variáveis antes de usar
current_value = st.empty()
min_value = st.empty()
max_value = st.empty()
graph = st.empty()

def prepare_history_visualization():
    history, instance = hist.get(ticker, init_date=init_date, end_date=end_date) if init_date else hist.get(ticker)

    max_index = history.index.max()
    if pd.notna(max_index):
        max_value = history['Close'][max_index]

        # Use st.write ou st.metric para exibir informações na interface gráfica
        current_value.metric("Current Value", f"R$ {round(max_value, 2)}", f"{round((max_value / history['Close'][history.index[-2]] - 1) * 100, 2)}%")
        min_value.metric("Minimum Value", f"R$ {round(history['Close'].min(), 2)}", f"{round((history['Close'].min() / max_value - 1) * 100, 2)}")
        max_value.metric("Maximum Value", f"R$ {round(max_value, 2)}", f"{round((max_value / history['Close'][max_index] - 1) * 100, 2)}")

        bollinger_figure = bollinger.get(ticker, history)
        graph.plotly_chart(bollinger_figure, use_container_width=True, sharing="streamlit")
    else:
        st.write("No data available for visualization.")

if ticker and sleep_time:
    col1, col2, col3 = st.columns(3)

    with col1:
        current_value = st.empty()
    with col2:
        min_value = st.empty()
    with col3:
        max_value = st.empty()
    graph = st.empty()

    while toogle:
        prepare_history_visualization()
        time.sleep(sleep_time)
    else:
        prepare_history_visualization()
