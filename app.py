import fitz
import streamlit as st

# Extract PDF text
def extract_pdf_content(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Simple structured extraction
def extract_data(text):
    data = []
    
    lines = text.lower().split("\n")
    
    for line in lines:
        
        if "dampness" in line:
            data.append({"area": "Wall/Room", "issue": "Dampness"})
            
        elif "leakage" in line:
            data.append({"area": "Plumbing/Wall", "issue": "Leakage"})
            
        elif "crack" in line:
            data.append({"area": "Wall", "issue": "Crack"})
            
        elif "seepage" in line:
            data.append({"area": "Parking/Wall", "issue": "Seepage"})
            
        elif "tile" in line and "gap" in line:
            data.append({"area": "Bathroom", "issue": "Tile Joint Issue"})
    
    return data

# Generate DDR
def generate_ddr(data):
    report = "## Detailed Diagnostic Report\n\n"
    
    report += "### 1. Property Issue Summary\n"
    report += f"Total Issues Found: {len(data)}\n\n"
    
    report += "### 2. Area-wise Observations\n"
    for item in data:
        report += f"- Area: {item['area']}\n"
        report += f"  Issue: {item['issue']}\n\n"
    
    report += "### 3. Probable Root Cause\nGeneral wear and tear or maintenance issues.\n\n"
    
    report += "### 4. Severity Assessment\nMedium (based on observed issues)\n\n"
    
    report += "### 5. Recommended Actions\n- Repair damaged areas\n- Conduct detailed inspection\n\n"
    
    report += "### 6. Additional Notes\nNot Available\n\n"
    
    report += "### 7. Missing Information\nNot Available\n"
    
    return report

# UI
st.title("AI DDR Report Generator (No API Version)")

inspection_file = st.file_uploader("Upload Inspection Report", type=["pdf"])
thermal_file = st.file_uploader("Upload Thermal Report", type=["pdf"])

if st.button("Generate DDR"):
    if inspection_file and thermal_file:
        
        text1 = extract_pdf_content(inspection_file)
        text2 = extract_pdf_content(thermal_file)
        
        combined_text = text1 + "\n" + text2
        
        data = extract_data(combined_text)
        ddr = generate_ddr(data)
        
        st.subheader("DDR Report")
        st.write(ddr)
        
    else:
        st.error("Upload both files")