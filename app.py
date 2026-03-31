import fitz
import streamlit as st
from collections import Counter
import io
from PIL import Image

# =========================
# Extract PDF text
# =========================
def extract_pdf_content(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# =========================
# Extract images from PDF
# =========================
def extract_images(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    images = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)

        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)

    return images


# =========================
# Extract issues using keywords
# =========================
def extract_data(text):
    data = []
    lines = text.lower().split("\n")

    for line in lines:

        if "dampness" in line:
            data.append("Dampness")

        elif "leakage" in line:
            data.append("Leakage")

        elif "crack" in line:
            data.append("Crack")

        elif "seepage" in line:
            data.append("Seepage")

        elif "tile" in line and "gap" in line:
            data.append("Tile Joint Issue")

    return data


# =========================
# Generate DDR Report
# =========================
def generate_ddr(data):
    report = "## Detailed Diagnostic Report\n\n"

    count = Counter(data)

    # 1. Summary
    report += "### 1. Property Issue Summary\n"
    report += f"Total Issues Found: {len(data)}\n\n"

    # 2. Observations
    report += "### 2. Area-wise Observations\n"
    for issue, freq in count.items():
        report += f"- {issue} ({freq} cases)\n"
    report += "\n"

    # 3. Root Cause
    report += "### 3. Probable Root Cause\n"
    report += "Moisture intrusion, plumbing leakage, and structural wear.\n\n"

    # 4. Severity
    report += "### 4. Severity Assessment\n"
    report += "Moderate (multiple recurring issues observed)\n\n"

    # 5. Actions
    report += "### 5. Recommended Actions\n"
    report += "- Repair leakage sources\n"
    report += "- Re-seal tile joints\n"
    report += "- Apply waterproofing treatment\n\n"

    # 6. Notes
    report += "### 6. Additional Notes\nNot Available\n\n"

    # 7. Missing Info
    report += "### 7. Missing Information\nNot Available\n"

    return report


# =========================
# Streamlit UI
# =========================
st.title("AI DDR Report Generator")

inspection_file = st.file_uploader("Upload Inspection Report", type=["pdf"])
thermal_file = st.file_uploader("Upload Thermal Report", type=["pdf"])

if st.button("Generate DDR"):
    if inspection_file and thermal_file:

        # ✅ Read files ONCE (FIXED BUG)
        inspection_bytes = inspection_file.read()
        thermal_bytes = thermal_file.read()

        # Extract text
        text1 = extract_pdf_content(inspection_bytes)
        text2 = extract_pdf_content(thermal_bytes)
        combined_text = text1 + "\n" + text2

        # Extract issues
        data = extract_data(combined_text)

        # Extract images
        inspection_images = extract_images(inspection_bytes)
        thermal_images = extract_images(thermal_bytes)

        # Generate report
        ddr = generate_ddr(data)

        # Display report
        st.subheader("DDR Report")
        st.markdown(ddr)

        # Display images
        st.subheader("Supporting Visual Evidence")

        all_images = inspection_images + thermal_images

        if all_images:
            for i, img in enumerate(all_images[:6]):  # limit for clean UI
                st.image(img, caption=f"Observation Image {i+1}")
        else:
            st.write("Image Not Available")

    else:
        st.error("Please upload both files")