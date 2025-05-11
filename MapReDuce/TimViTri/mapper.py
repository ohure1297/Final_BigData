#!/usr/bin/env python3
import sys
import json

# Đọc từng dòng đầu vào
for line in sys.stdin:
    try:
        # Phân tích đối tượng JSON trong mỗi dòng
        data = json.loads(line.strip())

        company = data.get('company', '').replace('\n', ' ').strip()
        address = data.get('address', '').strip()

        # Kiểm tra nếu địa chỉ là "Hà Nội"
        if 'hà nội' in address.lower():
            print(f"{company}\t{address}")

    except Exception as e:
        sys.stderr.write(f"Error processing line: {line.strip()} - {str(e)}\n")
