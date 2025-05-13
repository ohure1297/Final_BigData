# pages/page_mysql.py

import streamlit as st
import mysql.connector
from mysql.connector import Error

def page_mysql():
    st.title("Truy Vấn Dữ Liệu từ MySQL")
    
    # Textbox cho câu truy vấn SQL
    query = st.text_area("Nhập câu truy vấn SQL:", "SELECT * FROM jobs LIMIT 10;")
    
    # Nút thực hiện truy vấn
    if st.button("Truy vấn"):
        # Hiển thị câu truy vấn đã nhập
        st.write("Câu truy vấn SQL bạn đã nhập:")
        st.code(query)
        
        # Cố gắng kết nối với MySQL và thực hiện câu truy vấn
        try:
            # Kết nối tới MySQL
            connection = mysql.connector.connect(
                host="localhost",            # Địa chỉ host
                user="root",                 # Tên người dùng MySQL
                password="070204",           # Mật khẩu người dùng
                database="final_bigdata",    # Cơ sở dữ liệu
                charset="utf8mb4"            # Đảm bảo sử dụng UTF-8
            )
            
            if connection.is_connected():
                st.write("Kết nối MySQL thành công!")
                
                # Thực hiện câu truy vấn SQL
                cursor = connection.cursor()
                cursor.execute(query)
                
                # Lấy tất cả kết quả trả về
                result = cursor.fetchall()
                
                # Hiển thị kết quả
                if result:
                    st.write("Kết quả truy vấn:")
                    for row in result:
                        st.write(row)
                else:
                    st.write("Không có kết quả.")
                
                # Đóng con trỏ và kết nối
                cursor.close()
                connection.close()
        
        except Error as e:
            st.write(f"Đã xảy ra lỗi: {e}")
