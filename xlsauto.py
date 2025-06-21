import pdfplumber
import pandas as pd

pdf_path = "your_file.pdf"  # เปลี่ยนเป็น path ของไฟล์ PDF ของคุณ
excel_path = "output.xlsx"

data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split('\n')
            for line in lines:
                data.append([line])

df = pd.DataFrame(data, columns=["Text"])
df.to_excel(excel_path, index=False)
print(f"บันทึกข้อความจาก PDF ไปยัง {excel_path} เรียบร้อยแล้ว")