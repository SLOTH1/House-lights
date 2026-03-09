import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scopes
)

client = gspread.authorize(creds)

sheet = client.open_by_key(
    "1n-eXUsHuDEWaLY4XYKAstwU2dyxE8XaAFbwbQ7WSlWk"
).sheet1

# เพิ่มแถวใหม่
#sheet.append_row(["Sirichai", "Test OK", "2026"])
#sheet.update("A1:C1", [["ว/ด/ป","สถานะ",""]]) อัพเดตข้อมูล
""" sheet.append_row(["01/03/69", "เปิด"])
data = sheet.get_all_values()
print(data)
print("เพิ่มข้อมูลเรียบร้อย") """

def appendsheet(status, day, time):
    sheet.append_row([status, day, time])

def deleterow(row):
    sheet.delete_rows(row)

def clear_except_first():
    # นับจำนวนแถวทั้งหมด
    total_rows = sheet.row_count
    
    # ถ้ามีมากกว่า 1 แถว ให้ลบตั้งแต่แถวที่ 2 ถึงแถวสุดท้าย
    if total_rows > 1:
        sheet.delete_rows(2, total_rows)

