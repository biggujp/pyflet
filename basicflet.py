import flet as ft
import csv
import os

STUDENT_NAMES = [
    "สมชาย", "สมหญิง", "อนันต์", "วิภา", "กิตติ", 
    "พรทิพย์", "ศักดิ์ชัย", "สุภาพร", "ธีรศักดิ์", "จิราภรณ์"
]
CSV_FILE = "attendance.csv"

def main(page: ft.Page):
    page.title = "ระบบเช็คชื่อด้วย Flet"
    page.window_width = 400

    # Dropdown รายชื่อนักเรียน
    student_dropdown = ft.Dropdown(
        label="เลือกชื่อนักเรียน",
        options=[ft.dropdown.Option(name) for name in STUDENT_NAMES],
        width=300
    )

    # RadioGroup มา/ไม่มา
    status_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="มา", label="มา"),
            ft.Radio(value="ไม่มา", label="ไม่มา")
        ])
    )

    # ข้อความแสดงผล
    result_text = ft.Text("")

    # ฟังก์ชันบันทึกข้อมูล
    def save_data(e):
        name = student_dropdown.value
        status = status_radio.value
        if not name or not status:
            result_text.value = "กรุณาเลือกชื่อและสถานะ"
            page.update()
            return
        write_header = not os.path.exists(CSV_FILE)
        with open(CSV_FILE, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["ชื่อ", "สถานะ"])
            writer.writerow([name, status])
        result_text.value = f"บันทึกข้อมูลของ {name} เรียบร้อยแล้ว"
        page.update()

    # ฟังก์ชันแสดงข้อมูล
    def show_data(e):
        if not os.path.exists(CSV_FILE):
            result_text.value = "ยังไม่มีข้อมูล"
            page.update()
            return
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        if len(rows) <= 1:
            result_text.value = "ยังไม่มีข้อมูล"
        else:
            # แสดงข้อมูลในรูปแบบข้อความ
            result = ""
            for row in rows:
                result += " | ".join(row) + "\n"
            result_text.value = result
        page.update()

    # ปุ่มบันทึกและดูข้อมูล
    save_button = ft.ElevatedButton("บันทึกข้อมูล", on_click=save_data)
    show_button = ft.ElevatedButton("ดูข้อมูลที่บันทึกแล้ว", on_click=show_data)

    page.add(
        student_dropdown,
        status_radio,
        ft.Row([save_button, show_button]),
        result_text
    )

ft.app(target=main)