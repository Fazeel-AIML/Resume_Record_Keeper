import pdfplumber
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

# Suppress pdfplumber warnings
logging.getLogger("pdfplumber").setLevel(logging.ERROR)

# Load a lightweight summarization model (distilbart-cnn-6-6)
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-6-6")
model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-6-6")
#soe
def extract_text_from_pdf(pdf_path):
    """Extracts raw text from PDF using pdfplumber."""
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
    except Exception as e:
        text = f"Error extracting text: {str(e)}"
    return text.strip() if text else "No text extracted"

def summarize_text(text):
    """Generates a summary using the lightweight DistilBART model."""
    try:
        # Tokenize input text, truncate to 512 tokens (suitable for low-end CPU)
        inputs = tokenizer(text, max_length=512, truncation=True, return_tensors="pt")
        # Generate summary (limit output to 100 tokens for brevity)
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=500,
            min_length=400,
            length_penalty=5.0,
            num_beams=20,  # Reduced from 4 to speed up on low-end CPU
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        return f"Error summarizing text: {str(e)}"

def extract_and_summarize_resume(pdf_path):
    """Extracts text from PDF and generates a summary."""
    text = extract_text_from_pdf(pdf_path)
    if text and not text.startswith("Error"):
        summary = summarize_text(text)
        return summary
    return "No summary generated"