from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "submitted_forms"
EMAIL_SENDER = "rhtindia123@gmail.com"
EMAIL_PASSWORD = "odmx pabh lvtg srwj"  # Use an App Password if using Gmail
EMAIL_RECEIVER = "rhtrivedi92@outlook.com"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET"])
def home():
    return "PDF Submission API is Running!"


@app.route("/upload", methods=["POST"])
def upload_file():
    print("🔄 Received request from PDF form...")

    # Debugging: Print request headers
    print(f"📥 Request Headers: {request.headers}")

    # Check if the request contains a PDF file (Acrobat sends raw PDF data)
    if request.content_type != "application/pdf":
        print("❌ Error: Incorrect Content-Type! Expected application/pdf")
        return jsonify({"error": "Invalid Content-Type. Expected application/pdf"}), 400

    # Read the raw PDF data
    pdf_data = request.data
    if not pdf_data:
        print("❌ Error: No data received in request!")
        return jsonify({"error": "No data received"}), 400

    # Save the raw PDF file
    filename = "submitted_form.pdf"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as f:
        f.write(pdf_data)

    print(f"✅ File saved successfully at {file_path}")

    # Send email with the attached PDF
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
    app.run(host="0.0.0.0", port=5000, debug=True)
