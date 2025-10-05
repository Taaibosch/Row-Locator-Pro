🚀 Built a Simple AI-Powered File Scanner App with Python

Have you ever received a long pass list or document and struggled to find your name?
I decided to automate that process using AI + Python.

🔍 About the App
This tool allows you to upload any file or image (like a scanned school pass list or report) and simply type your name.
The app then scans the entire document using OCR (Optical Character Recognition) and instantly returns the exact row or line where your name appears — showing your ranking or result without manually scrolling through hundreds of lines.

⚙️ Technologies Used

🧠 Python – the core logic

🧩 PyTesseract – for AI-based text extraction (OCR from images)

📄 Pandas – for searching inside text, CSV, or Excel files

🌐 Streamlit – for building a simple, interactive web app interface

📊 Methodology

Upload your file (image, text, or Excel).

The app detects the file type automatically.

If it’s an image, PyTesseract extracts text using OCR.

The system searches for your name or keyword in the content.

The exact row/line containing your name is displayed in seconds.

✨ Why I Built It
This was inspired by real-world situations like school pass lists or result sheets, where I just wanted to find my name quickly. It’s a small project, but it shows how AI can simplify everyday tasks.
