#!/usr/bin/env python3
import sys
import json

# Đọc từng dòng từ đầu vào
for line in sys.stdin:
    try:
        data = json.loads(line.strip())  # Phân tích từng dòng JSON

        company = data.get('company', '').replace('\n', ' ').strip()
        salary_range = data.get('salary', '').strip()

        # Kiểm tra nếu lương là "Thoả thuận", "Thỏa thuận", hoặc viết hoa
        if 'thoả thuận' in salary_range.lower() or 'thỏa thuận' in salary_range.lower():
            print(f"{company}\t{salary_range}")

    except Exception as e:
        # In lỗi nếu có vấn đề với dữ liệu
        sys.stderr.write(f"Error: {str(e)}\n")
