import streamlit as st
import pandas as pd
import easyocr
from PIL import Image
import io

def extract_text_from_image(image):
    """Extract text from image using EasyOCR"""
    try:
        reader = easyocr.Reader(['en'])
        # Convert image to bytes
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=image.format or "PNG")
        img_bytes = img_bytes.getvalue()
        text_list = reader.readtext(img_bytes, detail=0)
        text = "\n".join(text_list)
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
    df_str = df.astype(str)
    mask = df_str.apply(lambda row: row.str.contains(query, case=False, na=False).any(), axis=1)
    matches = df[mask]
    return matches

def main():
    st.set_page_config(page_title="File Scanner", page_icon="🔍", layout="wide")
    
    st.title("🔍 AI File Scanner App")
    st.write("Upload a file (image or document) and search for specific text using AI OCR!")

    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=['txt', 'csv', 'xlsx', 'xls', 'jpg', 'jpeg', 'png'],
        help="Supported: Text, CSV, Excel, and Image files"
    )
    
    if uploaded_file is not None:
        st.write("**File details:**", {
            "Filename": uploaded_file.name,
            "Size": f"{uploaded_file.size / 1024:.2f} KB",
            "Type": uploaded_file.type
        })

        query = st.text_input("Enter text to search for:", placeholder="e.g., your name, student ID, etc.")

        if query:
            try:
                if uploaded_file.type.startswith("image"):
                    # Handle image files
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Image", use_container_width=True)

                    with st.spinner("🔍 Extracting text using AI..."):
                        extracted_text = extract_text_from_image(image)

                    if extracted_text:
                        st.subheader("🧠 Extracted Text:")
                        st.text_area("OCR Result", extracted_text, height=200)

                        matches = search_in_text(extracted_text, query)
                        if matches:
                            st.success(f"✅ Found {len(matches)} match(es):")
                            for i, m in enumerate(matches, 1):
                                st.write(f"{i}. {m}")
                        else:
                            st.warning("No matches found.")
                    else:
                        st.error("No text extracted from the image.")
                
                elif uploaded_file.type in ['text/plain', 'application/octet-stream']:
                    # Handle text files
                    text = uploaded_file.getvalue().decode("utf-8")
                    st.text_area("File Content", text, height=300)

                    matches = search_in_text(text, query)
                    if matches:
                        st.success(f"✅ Found {len(matches)} match(es):")
                        for i, m in enumerate(matches, 1):
                            st.write(f"{i}. {m}")
                    else:
                        st.warning("No matches found.")

                elif uploaded_file.type in ['text/csv', 
                                            'application/vnd.ms-excel', 
                                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                    # Handle CSV/Excel
                    df = pd.read_csv(uploaded_file) if uploaded_file.type == 'text/csv' else pd.read_excel(uploaded_file)
                    st.dataframe(df.head())

                    matches = search_in_csv(df, query)
                    if not matches.empty:
                        st.success(f"✅ Found {len(matches)} row(s)!")
                        st.dataframe(matches)
                        csv = matches.to_csv(index=False)
                        st.download_button("📥 Download results", csv, "search_results.csv", "text/csv")
                    else:
                        st.warning("No matches found in the data.")
                else:
                    st.error("Unsupported file type.")

            except Exception as e:
                st.error(f"Error processing file: {e}")

    else:
        st.info("👆 Please upload a file to get started.")

        st.subheader("Example Usage:")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**For School Pass List:**")
            st.write("1️⃣ Upload CSV/Excel file\n2️⃣ Search your name\n3️⃣ See your ranking row")
        with col2:
            st.write("**For Images:**")
            st.write("1️⃣ Upload a photo of text\n2️⃣ AI extracts it\n3️⃣ Search within extracted content")

if __name__ == "__main__":
    main()
