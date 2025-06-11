from flet import *
import csv
from datetime import datetime

def write_csv(text):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('data.csv','a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([ts,text])

def read_csv():
    rows = []
    try:
        with open('data.csv', 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        pass
    return rows

def main(page: Page):
    output = Text(size=30)
    friend = TextField(label="ใส่ชื่อเพื่อนของคุณ")
    csv_output = Text(size=20)

    def showtext(e):
        output.value = f"สวัสดี {friend.value}!"
        write_csv(friend.value)
        friend.value = ""
        page.update()
    
    def read_data(e):
        rows = read_csv()
        if rows:
            csv_output.value = "\n".join([f"{ts} - {name}" for ts, name in rows])
        else:
            csv_output.value = "ไม่มีข้อมูล"
        page.update()

    btn = ElevatedButton("เพิ่มช้อมูล", on_click=showtext)
    read_btn = ElevatedButton("อ่านข้อมูล", on_click=read_data)

    page.add(friend, btn, read_btn, output, csv_output)

app(target=main)