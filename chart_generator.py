import matplotlib

# GUI backend band
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os

def generate_chart(safe_count, suspicious_count):

    labels = ["Safe", "Suspicious"]
    values = [safe_count, suspicious_count]

    os.makedirs("static", exist_ok=True)

    plt.figure(figsize=(5, 5))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )

    plt.title("Website Scan Statistics")

    plt.savefig(
        "static/chart.png",
        bbox_inches="tight"
    )

    plt.close("all")

    if __name__ == "__main__":
        app.run(debug=False)