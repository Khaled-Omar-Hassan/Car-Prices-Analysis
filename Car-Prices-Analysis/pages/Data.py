# importing needed libraries
import streamlit as st
import EDA

# Title
st.markdown(" <center>  <h1> Car Prices Dataset </h1> </font> </center> </h1> ",
            unsafe_allow_html=True)

# Link of Data
st.markdown(
    '<a href="https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data"> <center> Link to Dataset  </center> </a> ',
    unsafe_allow_html=True)

# Load data
df = EDA.df_source.sample(1000).reset_index(drop=True)
# Show data
st.write(df)
