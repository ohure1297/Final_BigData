#!/usr/bin/env python3
import sys

current_company = None
salaries = set()  # Dùng set để lưu các mức lương duy nhất

for line in sys.stdin:
    company, salary_range = line.strip().split('\t')

    # Nếu là công ty mới, in kết quả của công ty cũ và reset
    if company != current_company:
        if current_company:
            # In tất cả các mức lương cho công ty hiện tại
            for salary in salaries:
                print(f"{current_company}\t{salary}")
        current_company = company
        salaries = set()  # Reset lại các mức lương
    salaries.add(salary_range)  # Thêm mức lương vào set

# In kết quả cuối cùng cho công ty cuối cùng
if current_company:
    for salary in salaries:
        print(f"{current_company}\t{salary}")
