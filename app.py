import os
import re  # Added for strict URL verification pattern matching
import pandas as pd
from flask import Flask, render_template, request, send_file, session, redirect

from auth import create_users_table, register_user, validate_user
from brand_detector import detect_brand
from chart_generator import generate_chart
from database import get_history, get_stats, init_db, save_scan
from domain_age import get_domain_age
from domain_intelligence import get_domain_info
from email_alert import send_alert
from pdf_report import create_pdf
from predict_url import predict_url
from risk_engine import calculate_risk
from ssl_checker import check_ssl
from url_feature_extractor_v2 import extract_features
from virustotal_checker import check_virustotal
from website_screenshot import capture_screenshot

app = Flask(__name__)
app.secret_key = "phishing_project_secret"

# Initialize database schemas on application startup
init_db()
create_users_table()

# Global dictionary placeholder to store the latest scan data for PDF export
report_data = {}


@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    global report_data

    # Default state initializations for UI template rendering
    result = ""
    score = ""
    risk = 0
    entered_url = ""
    ssl_status = ""
    brands = []
    reasons = []
    url_features = {}
    vt_result = ""
    screenshot_status = False

    domain_info = {"Domain": "", "IP": ""}
    domain_age = {"Domain": "", "Creation Date": "", "Age Days": ""}
    geo_info = {"Country": "", "Region": "", "City": "", "ISP": ""}

    if request.method == "POST":
        entered_url = request.form["url"].strip()

        # -----------------------------------------------------------------
        # CORE VALIDATION LAYER: Regex to intercept incomplete/fake domains
        # -----------------------------------------------------------------
        url_pattern = re.compile(
            r'^(?:http|https)://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        # Pre-emptively append scheme protocol to test structural match integrity
        temp_url = entered_url
        if not temp_url.startswith(("http://", "https://")):
            temp_url = "https://" + temp_url

        # Explicitly block meaningless top-level edge cases like www.com or com
        is_invalid_edge_case = temp_url.lower() in [
            "https://www.com", "http://www.com", "https://com", "http://com", 
            "https://www.in", "https://in", "https://www.net", "https://net"
        ]

        if not url_pattern.match(temp_url) or is_invalid_edge_case:
            # Terminate execution pipeline immediately and send a validation alert to UI
            result = "❌ INVALID INPUT"
            score = "Risk Score: N/A"
            reasons = ["Please provide a valid active website URL or Domain (e.g., google.com, steamcommunity.com)"]
            
            return render_template(
                "index.html", result=result, score=score, risk=risk, url=entered_url,
                ssl_status="N/A", brands=[], domain_info=domain_info, domain_age=domain_age,
                reasons=reasons, vt_result="N/A", url_features={}, screenshot_status=False, geo_info=geo_info
            )
        
        # If input passes the validation layer cleanly, update the master variable
        entered_url = temp_url

        # Process predictive machine learning models and heuristics
        prediction, probability = predict_url(entered_url)
        risk, reasons = calculate_risk(entered_url, prediction)

        # Threshold classification logic
        if risk >= 80:
            result = "🚨 PHISHING WEBSITE"
        elif risk >= 50:
            result = "⚠️ SUSPICIOUS WEBSITE"
        else:
            result = "✅ LEGITIMATE WEBSITE"

        score = f"Risk Score: {risk}%"

        # Cryptographic SSL verification handshake execution
        ssl_info = check_ssl(entered_url)
        ssl_status = (
            "Valid SSL Certificate" if ssl_info.get("SSL") else "No SSL / SSL Error"
        )

        # Multi-modular sequential data extraction pipeline
        brands = detect_brand(entered_url)
        domain_age = get_domain_age(entered_url)
        url_features = extract_features(entered_url)

        # VirusTotal Integration API Layer
        vt_result = check_virustotal(entered_url)
        if "HTTPSConnectionPool" in str(vt_result):
            vt_result = "VirusTotal Service Unavailable"

        # Core Domain Intelligence Infrastructure Fetch
        domain_info = get_domain_info(entered_url)
        
        geo_info = {
            "Country": domain_info.get("Country", "Not Available"),
            "Region": domain_info.get("Region", "Not Available"),
            "City": domain_info.get("City", "Not Available"),
            "ISP": domain_info.get("ISP", "Not Available")
        }
        
        # Automated headless browser screenshot capture
        screenshot_status = capture_screenshot(entered_url)

        # Real-time critical incident response email alert trigger
        if risk >= 70:
            send_alert(entered_url, result, risk)

        # Persistent storage commit operations for history tracking
        if entered_url and result:
            save_scan(session["user"], entered_url, result, risk)

        # Compilation of master document data structure for PDF generation
        report_data = {
            "URL": entered_url,
            "Result": result,
            "Risk Score": f"{risk}%",
            "SSL Status": ssl_status,
            "VirusTotal": vt_result,
            "Detected Brand": ", ".join(brands) if brands else "None",
            "Domain": domain_info.get("Domain", ""),
            "IP Address": domain_info.get("IP", ""),
            "Country": geo_info.get("Country", ""),
            "Region": geo_info.get("Region", ""),
            "City": geo_info.get("City", ""),
            "ISP": geo_info.get("ISP", ""),
            "Domain Age": domain_age.get("Age Days", "Not Available"),
            "Creation Date": domain_age.get("Creation Date", "Not Available"),
            "Risk Reasons": (
                ", ".join(reasons) if reasons else "No suspicious indicators found"
            ),
        }

    return render_template(
        "index.html",
        result=result,
        score=score,
        risk=risk,
        url=entered_url,
        ssl_status=ssl_status,
        brands=brands,
        domain_info=domain_info,
        domain_age=domain_age,
        reasons=reasons,
        vt_result=vt_result,
        url_features=url_features,
        screenshot_status=screenshot_status,
        geo_info=geo_info,
    )


@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    records = get_history(session["user"])
    total_scans, safe_count, phishing_count = get_stats()
    generate_chart(safe_count, phishing_count)

    return render_template(
        "history.html",
        records=records,
        total_scans=total_scans,
        safe_count=safe_count,
        phishing_count=phishing_count,
    )


@app.route("/download_report")
def download_report():
    if "user" not in session:
        return redirect("/login")

    filename = "phishing_report.pdf"
    create_pdf(filename, report_data)
    return send_file(filename, as_attachment=True)


@app.route("/download_csv")
def download_csv():
    if "user" not in session:
        return redirect("/login")

    records = get_history(session["user"])
    try:
        df = pd.DataFrame(
            records, columns=["ID", "URL", "Result", "Risk Score", "Scan Time"]
        )
    except Exception:
        df = pd.DataFrame(records)

    filename = "scan_history.csv"
    df.to_csv(filename, index=False)
    return send_file(filename, as_attachment=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success = register_user(username, password)
        if success:
            return redirect("/login")
        else:
            return "Username already exists"
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = validate_user(username, password)
        if user:
            session["user"] = username
            return redirect("/")
        else:
            error = "Invalid Username or Password"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)