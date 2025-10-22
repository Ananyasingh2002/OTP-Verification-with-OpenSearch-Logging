# OTP Verification with OpenSearch Logging

**Short Description:**  
A secure OTP (One-Time Password) verification system built with Flask, Twilio, and OpenSearch. It allows sending OTPs to users’ phone numbers, verifying them, and logging all events to OpenSearch for analytics and monitoring.

---

## Features

* Send OTPs to phone numbers using Twilio API.  
* Verify OTPs with session-based authentication.  
* Log all OTP events (sent, verified, failed) in OpenSearch.  
* Flask web interface for requesting and verifying OTPs.  
* Dockerized setup for easy deployment with OpenSearch and OpenSearch Dashboards.

---

## Tech Stack

* **Backend:** Python, Flask, Flask-Session  
* **Messaging:** Twilio API  
* **Database & Search:** OpenSearch  
* **Containerization:** Docker, Docker Compose  
* **Frontend:** HTML/CSS (Jinja2 templates)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "OTP Verification with OpenSearch Logging"
   ```

2. **Create a `.env` file** in the root directory:
   ```env
   TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
   TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN
   TWILIO_PHONE_NUMBER=YOUR_TWILIO_PHONE_NUMBER
   ```

3. **Run with Docker Compose**

   **starting**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

   **stopping**
   ```bash
   docker-compose down
   ```

5. **Access the App**
   * Flask App: `http://localhost:5000`  
   * OpenSearch Dashboard: `http://localhost:5601`

---

## Usage

1. Enter your phone number in the form.  
2. Receive the OTP on your phone via Twilio.  
3. Enter the OTP to verify.  
4. All events are logged in OpenSearch (`otp_logs` index).

---

## Project Structure
```
OTP Verification with OpenSearch Logging/
├── app.py                 # Flask application
├── templates/             # HTML templates
│   └── index.html
├── static/                # Static files (CSS, JS, images)
│   └── style.css
├── Dockerfile             # Dockerfile for Flask app
├── docker-compose.yml     # Docker Compose setup
├── .env                   # Environment variables (Twilio credentials)
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies

```

---

## Contributing

1. Fork the repository.  
2. Create a new branch: `git checkout -b feature-name`  
3. Make your changes and commit: `git commit -m "Description"`  
4. Push to your branch: `git push origin feature-name`  
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License.
