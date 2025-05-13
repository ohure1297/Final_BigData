import streamlit as st
import subprocess
import pandas as pd

def page_mapreduce():
    st.title("🎯 Phân Tích Dữ Liệu Tuyển Dụng với MapReduce")

    # Định nghĩa các tính năng phân tích
    features = {
        "Những công việc có lương hơn 10 triệu": "Luong",
        "Những Công ty ở Hà Nội hoặc Hồ Chí Minh": "DiaDiem",
        "Những công việc không yêu cầu kinh nghiệm": "KinhNghiem",
        "Những công việc cần ngôn ngữ python": "Skill",
        "Lương trung bình theo từng thành phố": "TinhTrungBinhLuong",
        "Top 10 công việc có mức lương cao nhất": "Top10CV",
        "Những kĩ năng tuyển dụng theo số lượng": "KiNangCanThiet",
    }

    # Tên cột tương ứng với từng job
    column_names = {
        "Luong": ["Công việc", "Lương (triệu VND)"],
        "DiaDiem": ["Công ty", "Thành phố"],
        "KinhNghiem": ["Công việc", "Kinh Nghiem"],
        "Skill": ["Công việc", "Ngôn Ngữ"],
        "TinhTrungBinhLuong": ["Thành phố", "Lương trung bình"],
        "Top10CV": ["Công việc", "Lương"],
        "KiNangCanThiet": ["Kĩ năng", "Số lượng"],
    }

    # Cho phép người dùng chọn tính năng phân tích
    selected_feature = st.selectbox("Chọn tính năng phân tích", list(features.keys()))

    if st.button("Thực thi"):
        job_folder = features[selected_feature]
        map_path = f"/home/hadoopcong/Final_BigData/my_streamlit_app/mapreduce_jobs/{job_folder}/map.py"
        reduce_path = f"/home/hadoopcong/Final_BigData/my_streamlit_app/mapreduce_jobs/{job_folder}/reduce.py"
        input_path = "/user/hadoopcong/topcv.csv"
        output_path = f"/user/hadoopcong/output/{job_folder}"

        # Xóa output cũ nếu tồn tại
        subprocess.run(["hadoop", "fs", "-rm", "-r", output_path])

        # Thực thi Hadoop Streaming
        result = subprocess.run(
            ["hadoop", "jar", "/home/hadoopcong/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar",
             "-files", f"{map_path},{reduce_path}",
             "-mapper", f"python3 {map_path}",
             "-reducer", f"python3 {reduce_path}",
             "-input", input_path,
             "-output", output_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # In log thực thi
        st.subheader("📄 Log Thực Thi:")
        st.code(result.stdout + result.stderr)

        if result.returncode != 0:
            st.error(f"❌ Lỗi khi chạy job Hadoop: {result.stderr}")
            return

        # Đọc dữ liệu từ HDFS
        try:
            hdfs_output = subprocess.check_output(
                ["hadoop", "fs", "-cat", f"{output_path}/part-00000"], text=True
            )

            # Xử lý dữ liệu đầu ra
            data = []
            for line in hdfs_output.splitlines():
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    key, value = parts
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                    data.append((key, value))

            if data:
                columns = column_names.get(job_folder, ["Key", "Value"])
                df = pd.DataFrame(data, columns=columns)

                st.subheader("📋 Dữ liệu chi tiết")
                st.dataframe(df)
            else:
                st.warning("⚠️ Không có dữ liệu hiển thị.")
        except subprocess.CalledProcessError:
            st.error("❌ Không thể đọc kết quả từ HDFS!")
