import streamlit as st
import google.generativeai as genai

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO
from datetime import datetime
import random

# ==========================================
# PAGE
# ==========================================

st.set_page_config(
    page_title="AI Invoice Generator",
    page_icon="🧾"
)

# ==========================================
# GEMINI
# ==========================================

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================================
# PDF FUNCTION
# ==========================================

def create_pdf(text):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):

        if line.strip():

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1,5)
            )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

# ==========================================
# UI
# ==========================================

st.title("🧾 AI Invoice Generator")

invoice_no = f"INV-{random.randint(1000,9999)}"

client_name = st.text_input(
    "Client Name"
)

company = st.text_input(
    "Company"
)

service = st.text_area(
    "Service Description"
)

amount = st.number_input(
    "Amount",
    min_value=0.0
)

tax = st.number_input(
    "Tax %",
    min_value=0.0
)

generate = st.button(
    "Generate Invoice"
)

# ==========================================
# GENERATE
# ==========================================

if generate:

    prompt = f"""
Create a professional invoice.

Invoice Number:
{invoice_no}

Date:
{datetime.now().strftime('%d-%m-%Y')}

Client:
{client_name}

Company:
{company}

Service:
{service}

Amount:
{amount}

Tax:
{tax}%

Include:
- Subtotal
- Tax Amount
- Total Amount
- Payment Notes

Return only invoice content.
"""

    response = model.generate_content(
        prompt
    )

    invoice = response.text

    st.markdown(invoice)

    pdf = create_pdf(invoice)

    st.download_button(
        "📄 Download Invoice PDF",
        data=pdf,
        file_name="invoice.pdf",
        mime="application/pdf"
    )