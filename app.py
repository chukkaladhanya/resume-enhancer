"""
Smart Resume Enhancer - AI-powered resume improvement tool
Uses Google Gemini AI to enhance, evaluate, and summarize resumes.
"""

import streamlit as st
import google.generativeai as genai
import re
from typing import Dict, List, Optional
import config
from resume_utils import extract_resume_text, validate_file_size

# Validate configuration on startup
is_valid, error_msg = config.validate_config()
if not is_valid:
    st.error(error_msg)
    st.stop()

# Configure Gemini API
genai.configure(api_key=config.GEMINI_API_KEY)

# Page configuration
st.set_page_config(
    page_title="Smart Resume Enhancer",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📄 Smart Resume Enhancer</h1>', unsafe_allow_html=True)
st.markdown("---")


# --- Helper Functions ---

def convert_bold_markdown_to_latex(text: str) -> str:
    """Convert markdown bold syntax to LaTeX bold commands."""
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    return text


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
        '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\^{}'
    }
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text


def lines_to_latex_items(text: str) -> str:
    """Convert text lines to LaTeX itemize format."""
    lines = text.split('\n')
    latex_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('* ') or line.startswith('- '):
            latex_lines.append(r'  \item ' + line[2:].strip())
        elif line:
            latex_lines.append(r'  \item ' + line.strip())
    return '\n'.join(latex_lines)


def process_section_content(text: str, use_list: bool = False) -> str:
    """Process section content for LaTeX output."""
    text = convert_bold_markdown_to_latex(text)
    text = escape_latex(text)
    if use_list:
        return lines_to_latex_items(text)
    return text


def section_block(title: str, content: str, use_list: bool = False) -> str:
    """Generate a LaTeX section block."""
    body = process_section_content(content, use_list)
    if use_list:
        return f"\\section*{{{title}}}\n\\begin{{itemize}}\n{body}\n\\end{{itemize}}\n"
    else:
        return f"\\section*{{{title}}}\n{body}\n"


def parse_sections(text: str) -> Dict[str, str]:
    """Parse improved resume text into sections."""
    sections = {section: "No relevant data found" for section in config.RESUME_SECTIONS}
    current_section = None
    collected = []

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Check if line is a section heading
        if any(heading.lower() in line.lower() for heading in sections):
            if current_section and collected:
                sections[current_section] = '\n'.join(collected)
                collected = []
            for key in sections:
                if key.lower() in line.lower():
                    current_section = key
                    break
        elif current_section:
            collected.append(line)

    if current_section and collected:
        sections[current_section] = '\n'.join(collected)

    return sections


@st.cache_data(show_spinner=False)
def get_quality_scores(text: str) -> Dict[str, int]:
    """
    Evaluate resume quality using AI.
    Cached to avoid redundant API calls.
    """
    try:
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        prompt = (
            "Evaluate the following resume based on these 5 criteria. "
            "Return ONLY scores (0 to 100) for each in this exact format:\n\n"
            "Grammar & Spelling: [score]\n"
            "Clarity & Conciseness: [score]\n"
            "Structure & Formatting: [score]\n"
            "Keyword Optimization: [score]\n"
            "Completeness of Sections: [score]\n\n"
            "Resume:\n" + text
        )
        response = model.generate_content(prompt).text

        scores = {}
        for line in response.splitlines():
            parts = line.split(":")
            if len(parts) == 2:
                label = parts[0].strip()
                try:
                    score = int(parts[1].strip().replace('%', '').split()[0])
                    scores[label] = max(0, min(score, 100))
                except:
                    pass
        return scores
    except Exception as e:
        st.error(f"Failed to get quality scores: {str(e)}")
        return {}


def parse_corrections(text: str) -> List[str]:
    """Extract corrections from AI response."""
    lines = text.split('\n')
    corrections = []
    capture = False
    
    for line in lines:
        if "corrections" in line.lower() or "changes" in line.lower():
            capture = True
            continue
        if capture:
            if line.startswith("-") or line.startswith("*") or line.startswith("•"):
                corrections.append(line.lstrip("-*• ").strip())
            elif line.strip() == "":
                if corrections:  # Stop if we have corrections and hit empty line
                    break
            elif line.strip():
                corrections.append(line.strip())
    
    return corrections if corrections else ["General improvements applied to grammar, structure, and clarity"]


@st.cache_data(show_spinner=False)
def get_resume_summary(text: str) -> str:
    """
    Generate AI summary of resume.
    Cached to avoid redundant API calls.
    """
    try:
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        prompt = (
            "Summarize the following resume in 2-3 concise paragraphs. "
            "Highlight key skills, experience, education, and notable achievements. "
            "Be specific and professional:\n\n" + text
        )
        response = model.generate_content(prompt).text
        return response.strip()
    except Exception as e:
        st.error(f"Failed to generate summary: {str(e)}")
        return ""


@st.cache_data(show_spinner=False)
def enhance_resume(resume_text: str) -> tuple[str, List[str]]:
    """
    Enhance resume using AI.
    Cached to avoid redundant API calls.
    """
    try:
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        prompt = (
            "You are an expert resume writer. Enhance the following resume by:\n"
            "1. Fixing all grammar and spelling errors\n"
            "2. Improving clarity and conciseness\n"
            "3. Enhancing word choice and professional tone\n"
            "4. Optimizing structure and formatting\n"
            "5. Adding impactful action verbs where appropriate\n\n"
            "Return your response in this EXACT format:\n\n"
            "IMPROVED RESUME:\n"
            "[Enhanced resume organized into sections: Objective, Education, Experience, Skills, Projects, Certifications, Extracurricular Activities, Declaration]\n\n"
            "CORRECTIONS MADE:\n"
            "- Correction 1\n"
            "- Correction 2\n"
            "...\n\n"
            "Original Resume:\n" + resume_text
        )
        
        response = model.generate_content(prompt)
        response_text = response.text

        # Parse response
        if "CORRECTIONS" in response_text.upper():
            parts = re.split(r'CORRECTIONS?\s*(?:MADE)?:', response_text, flags=re.IGNORECASE)
            improved_resume = parts[0].replace("IMPROVED RESUME:", "").strip()
            corrections_text = parts[1].strip() if len(parts) > 1 else ""
        else:
            improved_resume = response_text.strip()
            corrections_text = ""

        sections = parse_sections(improved_resume)
        corrections = parse_corrections(corrections_text)

        return sections, corrections
    except Exception as e:
        st.error(f"Failed to enhance resume: {str(e)}")
        return {}, []


def generate_latex(sections: Dict[str, str]) -> str:
    """Generate LaTeX document from sections."""
    latex_code = (
        "\\documentclass[11pt]{article}\n"
        "\\usepackage[margin=0.75in]{geometry}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{enumitem}\n"
        "\\usepackage{titlesec}\n"
        "\\usepackage{hyperref}\n"
        "\\titleformat{\\section}{\\large\\bfseries}{}{0em}{}\n"
        "\\setlist[itemize]{leftmargin=*, itemsep=2pt}\n\n"
        "\\title{\\textbf{Enhanced Resume}}\n"
        "\\author{}\n"
        "\\date{}\n\n"
        "\\begin{document}\n"
        "\\maketitle\n\n"
    )
    
    # Add sections
    latex_code += section_block("Objective", sections.get("Objective", ""), use_list=False)
    latex_code += section_block("Education", sections.get("Education", ""), use_list=True)
    latex_code += section_block("Experience", sections.get("Experience", ""), use_list=True)
    latex_code += section_block("Skills", sections.get("Skills", ""), use_list=True)
    latex_code += section_block("Projects", sections.get("Projects", ""), use_list=True)
    latex_code += section_block("Certifications", sections.get("Certifications", ""), use_list=True)
    latex_code += section_block("Extracurricular Activities", sections.get("Extracurricular Activities", ""), use_list=True)
    latex_code += section_block("Declaration", sections.get("Declaration", ""), use_list=False)
    latex_code += "\\end{document}"
    
    return latex_code


def generate_markdown(sections: Dict[str, str]) -> str:
    """Generate Markdown document from sections."""
    markdown = "# Enhanced Resume\n\n"
    
    for section_name in config.RESUME_SECTIONS:
        content = sections.get(section_name, "")
        if content and content != "No relevant data found":
            markdown += f"## {section_name}\n\n{content}\n\n"
    
    return markdown


# --- Main UI ---

st.markdown("### 📤 Upload Your Resume")
uploaded_file = st.file_uploader(
    "Choose a PDF or DOCX file",
    type=config.SUPPORTED_FORMATS,
    help=f"Maximum file size: {config.MAX_FILE_SIZE_MB}MB"
)

if uploaded_file:
    # Validate file size
    is_valid_size, size_error = validate_file_size(uploaded_file, config.MAX_FILE_SIZE_BYTES)
    if not is_valid_size:
        st.error(size_error)
        st.stop()
    
    # Extract text
    with st.spinner("📖 Reading your resume..."):
        resume_text = extract_resume_text(uploaded_file, uploaded_file.name)
    
    if not resume_text:
        st.stop()
    
    # Show file info
    st.success(f"✅ Successfully loaded **{uploaded_file.name}** ({len(resume_text)} characters)")
    
    st.markdown("---")
    
    # Tabbed interface
    tab1, tab2, tab3 = st.tabs(["🚀 Enhance Resume", "📊 Quality Analysis", "📝 Quick Summary"])
    
    with tab1:
        st.markdown("### ✨ AI-Powered Resume Enhancement")
        st.info("Click the button below to improve your resume with AI suggestions")
        
        if st.button("🎯 Enhance My Resume", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing and enhancing your resume..."):
                sections, corrections = enhance_resume(resume_text)
            
            if sections and corrections:
                st.success("✅ Resume enhanced successfully!")
                
                # Show corrections
                st.markdown("### 🛠️ Improvements Made")
                for idx, correction in enumerate(corrections, 1):
                    st.markdown(f"**{idx}.** {correction}")
                
                st.markdown("---")
                
                # Generate outputs
                latex_code = generate_latex(sections)
                markdown_code = generate_markdown(sections)
                
                # Download options
                st.markdown("### 📥 Download Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        "📄 Download LaTeX (.tex)",
                        latex_code,
                        file_name="enhanced_resume.tex",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    st.download_button(
                        "📝 Download Markdown (.md)",
                        markdown_code,
                        file_name="enhanced_resume.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                st.info("💡 **Tip:** Use [Overleaf](https://www.overleaf.com) to compile your LaTeX resume to PDF")
    
    with tab2:
        st.markdown("### 📊 Resume Quality Evaluation")
        st.info("Get detailed quality metrics for your resume")
        
        if st.button("📈 Analyze Quality", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyzing resume quality..."):
                quality_scores = get_quality_scores(resume_text)
            
            if quality_scores:
                st.markdown("### 📊 Quality Metrics")
                
                # Calculate average
                avg_score = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0
                
                # Show average with color coding
                if avg_score >= 80:
                    st.success(f"### Overall Score: {avg_score:.0f}% - Excellent! 🎉")
                elif avg_score >= 60:
                    st.warning(f"### Overall Score: {avg_score:.0f}% - Good, but room for improvement 👍")
                else:
                    st.error(f"### Overall Score: {avg_score:.0f}% - Needs significant improvement 📝")
                
                st.markdown("---")
                
                # Individual metrics
                for criterion, score in quality_scores.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{criterion}**")
                        st.progress(score / 100)
                    with col2:
                        st.metric("Score", f"{score}%")
    
    with tab3:
        st.markdown("### 📝 AI-Generated Summary")
        st.info("Get a concise professional summary of your resume")
        
        if st.button("✍️ Generate Summary", type="primary", use_container_width=True):
            with st.spinner("✨ Generating summary..."):
                summary = get_resume_summary(resume_text)
            
            if summary:
                st.markdown("### 📄 Resume Summary")
                st.markdown(f"> {summary}")
                
                st.download_button(
                    "💾 Download Summary",
                    summary,
                    file_name="resume_summary.txt",
                    mime="text/plain"
                )

else:
    st.info("👆 Please upload a resume (PDF or DOCX) to get started")
    
    # Help section
    with st.expander("ℹ️ How to use this tool"):
        st.markdown("""
        1. **Upload** your resume in PDF or DOCX format
        2. Choose one of three options:
           - **Enhance Resume**: Get AI-powered improvements and download enhanced version
           - **Quality Analysis**: See detailed quality metrics
           - **Quick Summary**: Generate a professional summary
        3. Download your enhanced resume in LaTeX or Markdown format
        
        **Note:** All processing happens securely. Your resume is not stored.
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by Google Gemini AI | "
    "<a href='https://github.com/chukkaladhanya/resume-enhancer' target='_blank'>View on GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)
