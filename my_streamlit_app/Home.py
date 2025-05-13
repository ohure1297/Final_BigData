import streamlit as st
from page_mysql import page_mysql 
from page_mapreduce import page_mapreduce 
st.set_page_config(page_title="My Streamlit App", layout="wide")
st.sidebar.title("Home")
page = st.sidebar.radio("Chọn Tính Năng", ["MapReduce", "Truy vấn MySQL"])
if page == "MapReduce":
    page_mapreduce()  # Gọi hàm MapReduce
elif page == "Truy vấn MySQL":
    page_mysql()  # Gọi hàm MySQL
