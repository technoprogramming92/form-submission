from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "submitted_forms"
EMAIL_SENDER = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVER = "receiver_email@example.com"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET"])
def home():
    return "PDF Submission API is Running!"


@app.route("/upload", methods=["POST"])
def upload_file():
    print("🔄 Received request from PDF form...")

    if "pdf" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    print(f"✅ File {filename} saved successfully!")

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
