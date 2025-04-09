from flask import Flask, request, render_template, send_file
import os
from extract_tables import extract_pdf_tables

app = Flask(__name__)

# Define folders for uploading and output
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("pdf_file")
        if file:
            pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(pdf_path)
            output_excel = extract_pdf_tables(pdf_path, output_dir=OUTPUT_FOLDER)

            if output_excel:
                return send_file(output_excel, as_attachment=True)
            else:
                return "❌ Failed to extract table from the PDF.", 500
    return render_template("index.html")

# Ensure that the app is only run when this script is executed directly
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
