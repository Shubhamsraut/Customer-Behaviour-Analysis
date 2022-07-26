import streamlit as st
import pickle
import pandas as pd

# st.set_page_config(layout='wide')
Data = pickle.load(open('customers.pkl', 'rb'))
Dataset = pd.DataFrame(Data)
st.title("Dataset")
st.table(Data)