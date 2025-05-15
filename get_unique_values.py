import pandas as pd
import os

# Danh sách đường dẫn đến các file Excel
excel_files = [
    r"D:\13_21133021_NguyenTrongDung_LuuTruMonHoc\data_KLTN\giao_duc\metadata.xlsx",
    r"D:\13_21133021_NguyenTrongDung_LuuTruMonHoc\data_KLTN\giaoThong_VanTai\metadata.xlsx",
    r"D:\13_21133021_NguyenTrongDung_LuuTruMonHoc\data_KLTN\honNhan_GiaDinh\metadata.xlsx",
    r"D:\13_21133021_NguyenTrongDung_LuuTruMonHoc\data_KLTN\laoDong_TienLuong\metadata.xlsx",
    r"D:\13_21133021_NguyenTrongDung_LuuTruMonHoc\data_KLTN\trachNhiem_HinhSu\metadata.xlsx"
]

# Tạo set để lưu trữ các giá trị duy nhất cho từng cột
unique_loai_van_ban = set()
unique_noi_ban_hanh = set()
unique_so_hieu = set()

# Đọc từng file Excel và lấy dữ liệu từ 3 cột cần thiết
for file_path in excel_files:
    try:
        df = pd.read_excel(file_path)
        # Thêm các giá trị vào set tương ứng
        unique_loai_van_ban.update(df['Loại Văn Bản'].dropna().unique())
        unique_noi_ban_hanh.update(df['Nơi Ban Hành'].dropna().unique())
        unique_so_hieu.update(df['Số Hiệu'].dropna().unique())
    except Exception as e:
        print(f"Lỗi khi đọc file {file_path}: {str(e)}")

# Chuyển set thành list và sắp xếp
loai_van_ban_list = sorted(list(unique_loai_van_ban))
noi_ban_hanh_list = sorted(list(unique_noi_ban_hanh))
so_hieu_list = sorted(list(unique_so_hieu))

# Tìm độ dài lớn nhất của các list
max_length = max(len(loai_van_ban_list), len(noi_ban_hanh_list), len(so_hieu_list))

# Điền None vào các list ngắn hơn để có cùng độ dài
loai_van_ban_list.extend([None] * (max_length - len(loai_van_ban_list)))
noi_ban_hanh_list.extend([None] * (max_length - len(noi_ban_hanh_list)))
so_hieu_list.extend([None] * (max_length - len(so_hieu_list)))

# Tạo DataFrame từ 3 list
df_result = pd.DataFrame({
    'Loại Văn Bản': loai_van_ban_list,
    'Nơi Ban Hành': noi_ban_hanh_list,
    'Số Hiệu': so_hieu_list
})

# Lưu vào file Excel
output_file = 'unique_values.xlsx'
df_result.to_excel(output_file, index=False)

print(f"Đã lưu kết quả vào file {output_file}")
print(f"Số lượng loại văn bản duy nhất: {len(unique_loai_van_ban)}")
print(f"Số lượng nơi ban hành duy nhất: {len(unique_noi_ban_hanh)}")
print(f"Số lượng số hiệu duy nhất: {len(unique_so_hieu)}") 