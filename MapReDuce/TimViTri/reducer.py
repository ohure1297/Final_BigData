#!/usr/bin/env python3
import sys

current_company = None
current_address = None

# Đọc các dòng đầu vào từ mapper
for line in sys.stdin:
    company, address = line.strip().split('\t')

    # Nếu công ty mới, in ra kết quả của công ty cũ
    if company != current_company:
        if current_company:
            print(f"{current_company}\t{current_address}")
        current_company = company
        current_address = address

# In kết quả cuối cùng
if current_company:
    print(f"{current_company}\t{current_address}")
