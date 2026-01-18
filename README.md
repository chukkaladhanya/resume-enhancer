# 📄 Smart Resume Enhancer

An intelligent Streamlit-based web application that enhances, evaluates, and summarizes resumes using **Google Gemini AI**. Get professional resume improvements with AI-powered suggestions, quality metrics, and export options in LaTeX and Markdown formats.

## ✨ Features

### 🚀 AI-Powered Resume Enhancement
- **Grammar & Style Improvements**: Fix grammar, spelling, and improve professional tone
- **Content Optimization**: Enhance clarity, conciseness, and impact
- **Action Verb Optimization**: Replace weak verbs with strong, impactful alternatives
- **Structure Refinement**: Improve organization and formatting
- **Detailed Corrections List**: See exactly what was improved

### 📊 Quality Analysis
Get comprehensive quality scores across 5 key dimensions:
- **Grammar & Spelling** - Professional language quality
- **Clarity & Conciseness** - Clear and concise communication
- **Structure & Formatting** - Logical organization
- **Keyword Optimization** - Industry-relevant keywords
- **Completeness of Sections** - All necessary sections included

### 📝 AI Summary Generation
Generate a professional summary highlighting:
- Key skills and competencies
- Professional experience highlights
- Educational background
- Notable achievements

### 📥 Export Options
- **LaTeX Format** (.tex) - Professional typesetting for PDF generation
- **Markdown Format** (.md) - Easy to edit and convert
- **Text Summary** - Quick professional overview

## 🖼️ User Interface

The application features a clean, modern interface with three main tabs:

1. **Enhance Resume** - Upload, improve, and download enhanced resume
2. **Quality Analysis** - Visual quality metrics with progress bars
3. **Quick Summary** - AI-generated professional summary

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Google Gemini API](https://ai.google.dev/)** - AI-powered text generation
- **[PyMuPDF](https://pymupdf.readthedocs.io/)** - PDF text extraction
- **[python-docx](https://python-docx.readthedocs.io/)** - DOCX text extraction
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment variable management

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/chukkaladhanya/resume-enhancer.git
   cd resume-enhancer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example env file
   copy .env.example .env   # Windows
   cp .env.example .env     # macOS/Linux
   ```

5. **Add your Gemini API key**
   
   Edit the `.env` file and replace `your_api_key_here` with your actual API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   MAX_FILE_SIZE_MB=10
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Open in browser**
   
   The application will automatically open in your default browser at `http://localhost:8501`

## 🚀 Usage

1. **Upload Resume**
   - Click the upload button and select your resume (PDF or DOCX)
   - Maximum file size: 10MB

2. **Choose an Action**
   - **Enhance Resume**: Get AI improvements and download enhanced version
   - **Quality Analysis**: View detailed quality metrics
   - **Quick Summary**: Generate professional summary

3. **Download Results**
   - Download enhanced resume in LaTeX or Markdown format
   - Compile LaTeX to PDF using [Overleaf](https://www.overleaf.com) or local TeX distribution

## 📁 Project Structure

```
resume-enhancer/
├── app.py                  # Main Streamlit application
├── config.py              # Configuration management
├── resume_utils.py        # Text extraction utilities
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .env                  # Your API key (git-ignored)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔒 Security Notes

- **Never commit your `.env` file** - It contains your API key
- The `.env` file is automatically git-ignored
- If you accidentally commit your API key, regenerate it immediately at [Google AI Studio](https://makersuite.google.com/app/apikey)

## ⚡ Performance Features

- **Smart Caching**: Results are cached to avoid redundant API calls
- **Efficient Processing**: Optimized text extraction and processing
- **Session State**: Maintains state across interactions

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found" Error
- Ensure you created a `.env` file (copy from `.env.example`)
- Add your actual API key to the `.env` file
- Restart the application

### PDF/DOCX Extraction Issues
- Ensure your file is not corrupted
- Check if the file contains extractable text (not just images)
- Try converting scanned PDFs to text-based PDFs

### File Size Error
- Default limit is 10MB
- You can increase this in `.env` by changing `MAX_FILE_SIZE_MB`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request




