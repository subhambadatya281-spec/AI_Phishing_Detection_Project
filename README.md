# AI-Powered Hybrid Phishing Website Detector

A robust security solution that detects phishing URLs in real-time by combining Random Forest Machine Learning with dynamic live heuristic telemetry.

## Key Features
- **Machine Learning Engine**: Random Forest classification model trained to detect phishing patterns with 98.2% accuracy.
- **Heuristic Analysis**: Real-time checking of Domain Age (WHOIS/RDAP), SSL/TLS certificates over raw sockets, and GeoIP hosting location.
- **Brand Protection**: Identifies brand spoofing and typosquatting attempts.
- **Input Filtering**: Custom Regex validation layer to prevent malformed URL processing.
- **Interactive Dashboard**: Modern UI built with Flask, Bootstrap, and dynamic risk scoring.

## Tech Stack
- **Backend**: Python, Flask, SQLite
- **Machine Learning**: Scikit-Learn (Random Forest), Pandas
- **Security & Utilities**: Socket Programming, Regex, GeoIP, SSL verification
- **Frontend**: HTML5, CSS3, Bootstrap

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/subhambadatya281-spec/AI_Phishing_Detection_Project.git](https://github.com/subhambadatya281-spec/AI_Phishing_Detection_Project.git)
