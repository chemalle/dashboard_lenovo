import pandas as pd
import plotly.express as px
import streamlit as st





# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_icon=":bar_chart:",
                   layout="wide",
                   )

df = pd.read_excel('dashboard.xlsx', engine='openpyxl',  nrows=100,
                   )


st.sidebar.header("Please Filter Here:")

task= st.sidebar.multiselect(
    "Select the Activiy",
    options=df['Atividade'].unique(),
    default=df['Atividade'].unique()
)


spent= st.sidebar.multiselect(
    "Select the Time Spent",
    options=df['Total_Consumido'].unique(),
    default=df['Total_Consumido'].unique()
)


available= st.sidebar.multiselect(
    "Select the Time Available",
    options=df['Total_Contratado'].unique(),
    default=df['Total_Contratado'].unique()
)


df_selection = df.query(
    "Atividade == @task & Total_Consumido==@spent & Total_Contratado==@available"
)


st.dataframe(df_selection)

st.title(":bar_chart: SLA DASHBOARD")
st.markdown("##")

total_contrato = df_selection['Total_Contratado'].sum()
average_available = round(df_selection['Tempo'].mean(), 1)
star_available =  ":star:" * int(round(average_available*60, 0))
average_spent_by_transaction = round(df_selection['Total_Consumido'].mean())


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Contratado")
    st.subheader(f" Horas { total_contrato:,}")
with middle_column:
    st.subheader("Média Consumida:")
    st.subheader(f"{average_available} {star_available}")
with right_column:
    st.subheader("Average_Spent_By_Transactions:")
    st.subheader(f"{average_spent_by_transaction}") 

st.markdown("---")

hours_by_task = (
    df_selection.groupby(by=["Atividade"]).sum()[["Total_Consumido"]].sort_values(by="Total_Consumido")
)

fig_tasks_by_hour = px.bar(
    hours_by_task,
    x= "Total_Consumido",
    y= hours_by_task.index,
    orientation="h",
    title= "<b>Hours by Task</b>",
    color_discrete_sequence=["#008388"] * len(hours_by_task),
    template="plotly_white",
)

fig_tasks_by_hour.update_layout(
    plot_bgcolor= 'rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_tasks_by_hour)


hide_st_style = """"
                <style>
                #MainMenu {visibility: hiden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
"""


st.markdown(hide_st_style, unsafe_allow_html=True)