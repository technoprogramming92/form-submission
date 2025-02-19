from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "submitted_forms"
EMAIL_SENDER = "rhtindia123@gmail.com"
EMAIL_PASSWORD = "qmvs zkuv dnle yepp"
EMAIL_RECEIVER = "rhtindia123@gmail.com"

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET"])
def home():
    return "PDF Submission API is Running!"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "pdf" not in request.files:
        return jsonify({"error": "No file found"}), 400

    file = request.files["pdf"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    send_email(file_path, filename)

    return jsonify({"message": "Form submitted successfully!"}), 200


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
    app.run(host="0.0.0.0", port=5000)
