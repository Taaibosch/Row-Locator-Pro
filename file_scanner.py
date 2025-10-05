import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import io
import tempfile
import os

# Set tesseract path (Windows users might need to uncomment and adjust this)
# Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Install and add to PATH, or set the path below
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def extract_text_from_image(image):
    """Extract text from image using OCR"""
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return ""

def search_in_text(text, query):
    """Search for query in text and return matching lines"""
    lines = text.split('\n')
    matches = [line.strip() for line in lines if query.lower() in line.lower() and line.strip()]
    return matches

def search_in_csv(df, query):
    """Search for query in CSV/Excel data and return matching rows"""
    # Convert all columns to string for searching
    df_str = df.astype(str)
    
    # Find rows where any column contains the query
    mask = df_str.apply(lambda row: row.str.contains(query, case=False, na=False).any(), axis=1)
    matches = df[mask]
    
    return matches

def main():
    st.set_page_config(page_title="File Scanner", page_icon="🔍", layout="wide")
    
    st.title("🔍 File Scanner App")
    st.write("Upload a file (image or document) and search for specific text!")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=['txt', 'csv', 'xlsx', 'xls', 'jpg', 'jpeg', 'png', 'bmp', 'pdf'],
        help="Supported formats: Text, CSV, Excel, Images (JPG, PNG, BMP)"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        st.write("File details:", file_details)
        
        # Search query
        query = st.text_input("Enter text to search for:", placeholder="e.g., your name, student ID, etc.")
        
        if query:
            try:
                # Process based on file type
                if uploaded_file.type.startswith('image'):
                    # Handle image files
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Image", use_container_width=True)
                    
                    # Extract text from image
                    with st.spinner("Extracting text from image..."):
                        extracted_text = extract_text_from_image(image)
                    
                    if extracted_text:
                        st.subheader("Extracted Text:")
                        st.text_area("OCR Result", extracted_text, height=200)
                        
                        # Search in extracted text
                        matches = search_in_text(extracted_text, query)
                        
                        if matches:
                            st.success(f"🎉 Found {len(matches)} match(es)!")
                            st.subheader("Matching Lines:")
                            for i, match in enumerate(matches, 1):
                                st.write(f"{i}. {match}")
                        else:
                            st.warning("No matches found in the extracted text.")
                    else:
                        st.error("No text could be extracted from the image.")
                
                elif uploaded_file.type in ['text/plain', 'application/octet-stream']:
                    # Handle text files
                    text = uploaded_file.getvalue().decode('utf-8')
                    
                    st.subheader("File Content:")
                    st.text_area("Content", text, height=300)
                    
                    # Search in text
                    matches = search_in_text(text, query)
                    
                    if matches:
                        st.success(f"🎉 Found {len(matches)} match(es)!")
                        st.subheader("Matching Lines:")
                        for i, match in enumerate(matches, 1):
                            st.write(f"{i}. {match}")
                    else:
                        st.warning("No matches found in the file.")
                
                elif uploaded_file.type in ['application/vnd.ms-excel', 
                                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                          'text/csv']:
                    # Handle CSV and Excel files
                    if uploaded_file.type == 'text/csv':
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.subheader("Data Preview:")
                    st.dataframe(df.head())
                    
                    # Search in data
                    matches = search_in_csv(df, query)
                    
                    if not matches.empty:
                        st.success(f"🎉 Found {len(matches)} matching row(s)!")
                        st.subheader("Matching Rows:")
                        st.dataframe(matches)
                        
                        # Option to download results
                        csv = matches.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name="search_results.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("No matches found in the data.")
                
                else:
                    st.error("Unsupported file type. Please upload a text, CSV, Excel, or image file.")
                    
            except Exception as e:
                st.error(f"Error processing file: {e}")
    
    else:
        # Show example when no file is uploaded
        st.info("👆 Please upload a file to get started!")
        
        # Example section
        st.subheader("Example Usage:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**For School Pass List:**")
            st.write("1. Upload CSV/Excel with student data")
            st.write("2. Search for your name or ID")
            st.write("3. Get your complete ranking row")
        
        with col2:
            st.write("**For Images:**")
            st.write("1. Upload a screenshot or photo of text")
            st.write("2. The app will extract text using OCR")
            st.write("3. Search within the extracted text")

if __name__ == "__main__":
    main()