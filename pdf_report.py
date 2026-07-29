from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


def create_pdf(filename, data):
    print("PDF DATA =", data)
    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(
        Paragraph(
            "AI Phishing Detection Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 10))

    # Date Time
    content.append(
    Paragraph(
        f"<b>Generated On:</b> {datetime.now()}",
        styles["Normal"]
    )
)

    content.append(Spacer(1, 5))

    content.append(
    Paragraph(
        "<b>Best Algorithm Used:</b> XGBoost",
        styles["Normal"]
    )
)

    content.append(Spacer(1, 20))

    # Scan Details
    content.append(
        Paragraph(
            "Scan Details",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 10))

    for key, value in data.items():

        content.append(
            Paragraph(
                f"<b>{key}</b>: {value}",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 5))

    # Website Screenshot

    if os.path.exists("static/website.png"):

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                "Website Screenshot",
                styles["Heading2"]
            )
        )

        content.append(Spacer(1, 10))

        content.append(
            Image(
                "static/website.png",
                width=450,
                height=250
            )
        )

    # Statistics Chart

    if os.path.exists("static/chart.png"):

        content.append(PageBreak())

        content.append(
            Paragraph(
                "Scan Statistics Chart",
                styles["Heading2"]
            )
        )

        content.append(Spacer(1, 10))

        content.append(
            Image(
                "static/chart.png",
                width=350,
                height=350
            )
        )

    # Confusion Matrix

    if os.path.exists("static/confusion_matrix.png"):

        content.append(PageBreak())

        content.append(
            Paragraph(
                "Machine Learning Confusion Matrix",
                styles["Heading2"]
            )
        )

        content.append(Spacer(1, 10))

        content.append(
            Image(
                "static/confusion_matrix.png",
                width=400,
                height=350
            )
        )

    # Model Comparison Graph

    if os.path.exists("static/model_comparison.png"):

        content.append(PageBreak())

        content.append(
        Paragraph(
            "Machine Learning Model Comparison",
            styles["Heading2"]
        )
    )

        content.append(Spacer(1, 10))

        content.append(
        Image(
            "static/model_comparison.png",
            width=500,
            height=250
        )
    )
        if os.path.exists("static/feature_importance.png"):

            content.append(PageBreak())

            content.append(
        Paragraph(
            "Feature Importance Analysis",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1,10))

    content.append(
        Image(
            "static/feature_importance.png",
            width=500,
            height=300
        )
    )
# Model Metrics

    if os.path.exists("model_metrics.txt"):

        content.append(PageBreak())

        content.append(
        Paragraph(
            "Model Performance",
            styles["Heading2"]
        )
    )

        content.append(Spacer(1, 10))

    with open("model_metrics.txt", "r") as f:

        metrics = f.readlines()

    for line in metrics:

        content.append(
            Paragraph(
                line.strip(),
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 5))

    doc.build(content)