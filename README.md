# Vintervu - AI Career Preparation Platform

A comprehensive career preparation platform combining AI-powered interview practice with intelligent resume enhancement.

![Platform](https://img.shields.io/badge/Platform-Full--Stack-blue)
![Frontend](https://img.shields.io/badge/Frontend-React-61dafb)
![Backend](https://img.shields.io/badge/Backend-Node.js-339933)
![Database](https://img.shields.io/badge/Database-MongoDB-47A248)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-4285F4)

---

## 🎯 What is Vintervu?

**Vintervu** is an all-in-one career preparation platform that helps job seekers excel in their job search journey. It combines:

- 🎤 **AI Interview Practice** - Practice interviews with AI-generated questions
- 📋 **Resume Analysis** - Analyze your resume against specific job roles
- ✨ **Resume Enhancement** - AI-powered resume improvements with corrections
- 📊 **Quality Scoring** - Get detailed quality metrics across 5 dimensions
- 📝 **AI Summaries** - Generate professional resume summaries
- 👤 **User Accounts** - Track your progress and history
- 💾 **Resume History** - Save and access previous resume versions

---

## 🚀 Key Features

### 1. AI Interview Bot
- Upload your resume and get AI-generated interview questions
- Practice answering questions with speech-to-text
- Receive real-time feedback and scoring
- Track your interview performance over time

### 2. Resume Analyzer
- Analyze your resume for specific job roles
- Get skill match scores
- Identify missing keywords
- Receive personalized improvement suggestions

### 3. Resume Enhancer (NEW!)
- **AI-Powered Enhancement**: Improve grammar, clarity, and professional tone
- **Quality Analysis**: 5-metric evaluation system
  - Grammar & Spelling
  - Clarity & Conciseness
  - Structure & Formatting
  - Keyword Optimization
  - Completeness of Sections
- **Professional Summaries**: AI-generated executive summaries
- **Multiple Export Formats**: LaTeX and Markdown
- **Corrections Tracking**: See exactly what was improved

---

## �️ Technology Stack

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **React Router** - Navigation
- **Axios** - API calls

### Backend
- **Node.js** - Runtime
- **Express.js** - Web framework
- **MongoDB** - Database
- **Mongoose** - ODM
- **Multer** - File uploads

### AI & Processing
- **Google Gemini AI** - Natural language processing
- **PDF-Parse** - PDF text extraction
- **python-docx** - DOCX processing

---

## 📦 Installation

### Prerequisites
- Node.js (v20 or higher)
- MongoDB (local or Atlas)
- Google Gemini API key

### Step 1: Clone the Repository
```bash
git clone https://github.com/hassurashaik/vintervu-mini-.git
cd vintervu-mini
```

### Step 2: Backend Setup
```bash
cd server
npm install
```

Create a `.env` file in the `server` directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URI=your_mongodb_connection_string
PORT=5000
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password
```

Start the backend:
```bash
npm start
```

### Step 3: Frontend Setup
Open a new terminal:
```bash
cd client
npm install
npm run dev
```

### Step 4: Access the Application
Open your browser and navigate to:
```
http://localhost:5173
```

---

## 🎯 Usage Guide

### Getting Started
1. **Sign Up** - Create an account to save your progress
2. **Login** - Access your personalized dashboard

### Using Resume Enhancer
1. Navigate to **Resume Enhancer** from the main menu
2. **Upload** your resume (PDF or DOCX, max 10MB)
3. Choose your action:
   - **Enhance Resume**: Get AI improvements and download LaTeX/Markdown
   - **Quality Analysis**: View detailed metrics with visual progress bars
   - **Quick Summary**: Generate a professional summary

### Using Interview Practice
1. **Upload Resume** - Start with your resume
2. **Select Skills** - Choose your skill areas
3. **Start Interview** - Answer AI-generated questions
4. **Get Feedback** - Review your performance and scores

### Using Resume Analyzer
1. Select your **target job role**
2. **Upload** your resume
3. View **skill match score** and missing keywords
4. Get **actionable suggestions** for improvement

---

## 📊 Features Overview

| Feature | Description | Authentication Required |
|---------|-------------|------------------------|
| **Home** | Landing page and overview | No |
| **Interview Practice** | AI-powered mock interviews | Yes |
| **Resume Analyzer** | Job-specific resume analysis | Yes |
| **Resume Enhancer** | AI resume improvements | Yes |
| **Quality Scoring** | 5-metric evaluation | Yes |
| **AI Summaries** | Professional summary generation | Yes |
| **Dashboard** | User progress tracking | Yes |

---

## 🔑 Environment Variables

### Backend (`server/.env`)
```env
# Required
GEMINI_API_KEY=your_gemini_api_key
MONGO_URI=mongodb://localhost:27017/vintervu  # or Atlas connection string

# Optional
PORT=5000
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

### Getting a Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy and paste into your `.env` file

---

## 📁 Project Structure

```
vintervu-mini/
├── server/                      # Backend
│   ├── models/                  # MongoDB models
│   │   ├── User.js
│   │   ├── Feedback.js
│   │   └── EnhancedResume.js
│   ├── routes/                  # API routes
│   │   ├── interview.js
│   │   └── resume.js
│   ├── services/                # Business logic
│   │   ├── resumeProcessor.js
│   │   ├── resumeEnhancer.js
│   │   ├── interviewService.js
│   │   └── questionGenerator.js
│   └── index.js                 # Entry point
│
└── client/                      # Frontend
    ├── src/
    │   ├── components/
    │   │   ├── Home.jsx
    │   │   ├── Interview.jsx
    │   │   ├── ResumeAnalyzer.jsx
    │   │   ├── Dashboard.jsx
    │   │   └── ResumeEnhancer/  # Resume enhancement feature
    │   │       ├── ResumeEnhancerPage.jsx
    │   │       ├── UploadSection.jsx
    │   │       ├── EnhanceTab.jsx
    │   │       ├── QualityTab.jsx
    │   │       └── SummaryTab.jsx
    │   ├── App.jsx
    │   └── main.jsx
    └── package.json
```

---

## � API Endpoints

### Resume Enhancement
- `POST /api/resume/enhance` - Enhance resume with AI
- `POST /api/resume/quality` - Get quality scores
- `POST /api/resume/summarize` - Generate summary
- `GET /api/resume/download/:type/:id` - Download LaTeX/Markdown
- `GET /api/resume/history/:userId` - Get resume history
- `GET /api/resume/:id` - Get specific resume

### Interview
- `POST /api/interview/upload-resume` - Upload resume for interview
- `POST /api/interview/start` - Start interview session
- `GET /api/interview/next-question` - Get next question
- `POST /api/interview/record-response` - Submit answer
- `POST /api/interview/end-interview` - End and get results

### Authentication
- `POST /api/login` - User login
- `POST /api/signup` - User registration
- `GET /api/feedback/:email` - Get user feedback history

---

## 🚀 Deployment

### Backend Deployment
1. Deploy to services like Heroku, Railway, or Render
2. Set environment variables
3. Connect to MongoDB Atlas for production

### Frontend Deployment
1. Build the production bundle:
   ```bash
   cd client
   npm run build
   ```
2. Deploy to Vercel, Netlify, or similar
3. Update API base URL to production backend

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Submit a Pull Request

---

## � License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Google Gemini AI** - For powerful language model capabilities
- **Streamlit** - Inspiration for UI patterns
- **Open Source Community** - For excellent libraries and tools

---

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting guide

---

**Built with ❤️ for helping people succeed in their careers**
