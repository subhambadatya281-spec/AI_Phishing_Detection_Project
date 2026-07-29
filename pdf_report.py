import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(filename, report_data):
    # Safely handle missing model_metrics.txt file
    model_metrics = "Model metrics data unavailable."
    if os.path.exists("model_metrics.txt"):
        try:
            with open("model_metrics.txt", "r") as f:
                model_metrics = f.read()
        except Exception as e:
            print(f"Error reading model_metrics.txt: {e}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)

    # Generate PDF Document
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "AI Phishing Detection Report")

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, "-" * 80)

    # Report Content
    y = height - 100
    c.setFont("Helvetica", 11)

    for key, value in report_data.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50

    # Append Model Metrics Section
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Model Performance Metrics:")
    y -= 20

    c.setFont("Helvetica", 9)
    for line in model_metrics.splitlines():
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return True
