from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "submitted_forms"
EMAIL_SENDER = "eayashshah@gmail.com"
EMAIL_PASSWORD = "cujs dfld hfta egjp"  # Use an App Password if using Gmail
EMAIL_RECEIVER = "eayashshah@gmail.com"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET"])
def home():
    return "PDF Submission API is Running!"


@app.route("/upload", methods=["POST"])
def upload_file():
    print("🔄 Received request from PDF form...")
    print(f"📥 Request Headers: {request.headers}")

    # ✅ Fix: Check if Content-Type is None before calling .startswith()
    content_type = request.content_type
    if not content_type:
        print("❌ Error: No Content-Type in request!")
        return "<h1>Error: No Content-Type in request</h1>", 400

    # ✅ Handle Raw PDF Data (Adobe Desktop)
    if content_type == "application/pdf":
        pdf_data = request.data
        if not pdf_data:
            print("❌ Error: No data received!")
            return "<h1>Error: No data received</h1>", 400

        filename = "submitted_form.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as f:
            f.write(pdf_data)

        print(f"✅ File saved at {file_path}")
        send_email(file_path, filename)
        return "<h1>Form submitted successfully!</h1>", 200

    # ✅ Handle File Uploads (Mobile/Web Adobe)
    elif content_type.startswith("multipart/form-data"):
        if "file" not in request.files:
            print("❌ Error: No file received in request.files!")
            return "<h1>Error: No file received!</h1>", 400

        file = request.files["file"]
        filename = file.filename if file.filename else "submitted_form.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        print(f"✅ File uploaded at {file_path}")
        send_email(file_path, filename)
        return "<h1>Form submitted successfully!</h1>", 200

    # ❌ Handle Unknown Content-Type
    print(f"❌ Error: Unsupported Content-Type {content_type}")
    return f"<h1>Error: Unsupported Content-Type {content_type}</h1>", 400


def send_email(pdf_path, filename):
    msg = EmailMessage()
    msg["Subject"] = "New Submitted Form"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(
        "A new form has been submitted. The filled PDF is attached.")

    with open(pdf_path, "rb") as pdf_file:
        msg.add_attachment(pdf_file.read(), maintype="application",
                           subtype="pdf", filename=filename)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent successfully with {filename}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
