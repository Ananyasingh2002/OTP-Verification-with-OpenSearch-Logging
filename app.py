from flask import Flask, request, jsonify, session, render_template
from flask_session import Session
from twilio.rest import Client
from datetime import datetime
from opensearchpy import OpenSearch
import random
import os
import re
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

for attempt in range(20):
    try:
        opensearch_client = OpenSearch(
            hosts=[{"host": "opensearch", "port": 9200}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False
        )
        if opensearch_client.ping():
            print("Connected to OpenSearch")
            break
    except Exception as e:
        print(f"OpenSearch not ready, retrying ({attempt + 1}/20): {e}")
        time.sleep(5)
else:
    raise Exception("Failed to connect to OpenSearch after 20 attempts")

INDEX_NAME = "otp_logs"

if not opensearch_client.indices.exists(index=INDEX_NAME):
    opensearch_client.indices.create(index=INDEX_NAME)

def log_event(event_type, details):
    """Log an event to OpenSearch with timestamp."""
    doc = {
        "event_type": event_type,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    opensearch_client.index(index=INDEX_NAME, body=doc, refresh="true")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getOTP', methods=['POST'])
def get_otp():
    phone_number = request.form.get('phone-number', '').strip()

    if not phone_number.startswith('+'):
        phone_number = "+91" + phone_number

    if not re.match(r"^\+\d{10,15}$", phone_number):
        return jsonify({"error": "Invalid phone number format"}), 400

    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['phone'] = phone_number

    try:
        client.messages.create(
            body=f"Here's your OTP {otp}, Please do not share it with anyone.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        log_event("OTP_SENT", {"phone_number": phone_number})
        return jsonify({"status": "OTP sent successfully"})
    except Exception as e:
        log_event("OTP_SEND_FAILED", {"phone_number": phone_number, "error": str(e)})
        return jsonify({"error": f"Failed to send OTP: {str(e)}"}), 500

@app.route('/verifyOTP', methods=['POST'])
def verify_otp():
    print("DEBUG FORM DATA:", request.form)
    print("DEBUG SESSION OTP:", session.get('otp'))
    user_code = request.form.get('verification-code', '').strip()
    stored_code = session.get('otp')

    if not stored_code:
        log_event("VERIFY_FAILED", {"reason": "No OTP in session"})
        return jsonify({"error": "No OTP found. Please request a new one."}), 400
    if not user_code:
        log_event("VERIFY_FAILED", {"reason": "No OTP entered"})
        return jsonify({"error": "OTP is required"}), 400

    if user_code == stored_code:
        session.pop('otp', None)
        log_event("VERIFY_SUCCESS", {"phone_number": session.get("phone")})
        return jsonify({"status": "success"})
    else:
        log_event("VERIFY_FAILED", {"reason": "Invalid OTP"})
        return jsonify({"error": "Invalid OTP"}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", use_reloader=False)
