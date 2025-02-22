import os
import pdfkit

# ضبط المسار إلى `wkhtmltopdf`
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

# توليد ملف PDF
pdfkit.from_url("https://www.google.com", "output.pdf", configuration=config)

# فتح الملف تلقائيًا في Windows
pdf_path = os.path.abspath("output.pdf")
os.startfile(pdf_path)

print("✅ تم إنشاء ملف PDF وفتحه بنجاح!")
