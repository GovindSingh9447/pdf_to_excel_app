import os
import camelot
import tabula
import pdfplumber
import pytesseract
import pandas as pd


def extract_with_camelot(pdf_path, output_dir):
    print("[1] Trying with Camelot...")
    try:
        tables = camelot.read_pdf(pdf_path, pages='all')
        if tables and tables.n > 0:
            output_file = os.path.join(output_dir, "output_camelot.xlsx")
            tables.export(output_file, f="excel")
            print(f"✅ Camelot: {tables.n} tables extracted to {output_file}")
            return output_file
    except Exception as e:
        print("❌ Camelot failed:", e)
    return None


def extract_with_tabula(pdf_path, output_dir):
    print("[2] Trying with Tabula...")
    try:
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        if tables and len(tables) > 0:
            output_file = os.path.join(output_dir, "output_tabula.xlsx")
            with pd.ExcelWriter(output_file) as writer:
                for i, table in enumerate(tables):
                    table.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
            print(f"✅ Tabula: {len(tables)} tables extracted to {output_file}")
            return output_file
    except Exception as e:
        print("❌ Tabula failed:", e)
    return None


def extract_with_ocr(pdf_path, output_dir):
    print("[3] Trying with OCR...")
    try:
        data = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                image = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(image)
                print(f"📄 Page {i+1} OCR text extracted.")

                lines = [line.strip() for line in text.split("\n") if line.strip()]
                rows = [line.split() for line in lines]
                data.extend(rows)

        if data:
            df = pd.DataFrame(data)
            output_file = os.path.join(output_dir, "output_ocr.xlsx")
            df.to_excel(output_file, index=False)
            print("✅ OCR: Text extracted and saved to", output_file)
            return output_file
    except Exception as e:
        print("❌ OCR failed:", e)
    return None


def extract_pdf_tables(pdf_path, output_dir="outputs"):
    print(f"🔍 Starting table extraction from: {pdf_path}\n")
    os.makedirs(output_dir, exist_ok=True)

    if result := extract_with_camelot(pdf_path, output_dir):
        return result
    if result := extract_with_tabula(pdf_path, output_dir):
        return result
    if result := extract_with_ocr(pdf_path, output_dir):
        return result

    print("❌ Failed to extract tables using all methods.")
    return None

