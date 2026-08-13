# EscudoFlow AI

### Intelligent Phishing Detection & Threat Intelligence Platform

EscudoFlow AI is an AI-powered cybersecurity platform designed to detect, analyze, and explain phishing and other security threats across URLs, emails, attachments, and website screenshots.

The platform combines machine learning, rule-based detection, threat intelligence, computer vision, reputation analysis, and risk fusion to provide a unified security analysis experience.


---

## 📌 Overview

Phishing attacks continue to evolve beyond simple malicious URLs. Attackers increasingly use cloned login pages, suspicious emails, malicious attachments, domain impersonation, and social engineering techniques to deceive users.

EscudoFlow AI is being developed as a unified threat intelligence platform that analyzes multiple types of suspicious content and combines different security signals to determine the potential risk.

The platform currently includes several intelligence modules:

- 🔗 URL Intelligence
- 📧 Email Intelligence
- 📎 Attachment Intelligence
- 👁️ Visual Intelligence
- 🛡️ Threat Intelligence
- 🤖 Machine Learning-based phishing detection
- 📊 Security dashboard and reporting
- 🔐 User authentication and password reset
- 🧠 Explainable security analysis

---

## ✨ Key Features

### 🔗 URL Intelligence

The URL Intelligence module analyzes suspicious URLs using multiple security signals.

**Analysis includes:**

- URL structure and lexical analysis
- Domain information
- DNS analysis
- WHOIS information
- SSL certificate analysis
- Redirect analysis
- Hosting information
- Domain reputation
- Threat intelligence
- Rule-based detection
- Risk scoring
- Security explanation

Multiple signals can be combined to produce a more comprehensive assessment rather than relying on a single detection technique.

---

### 📧 Email Intelligence

The Email Intelligence module analyzes suspicious emails and extracts security-relevant information.

**Analysis includes:**

- Email parsing
- Header analysis
- Sender analysis
- Reply-To analysis
- Email authentication checks
- Suspicious URL extraction
- Suspicious keyword detection
- Pattern and rule-based analysis
- URL reputation analysis
- Threat intelligence
- Risk aggregation

The goal is to identify phishing indicators across both the email content and the URLs contained within the message.

---

### 📎 Attachment Intelligence

The Attachment Intelligence module analyzes potentially suspicious files and identifies security indicators.

**Current analysis components include:**

- File hashing
- Script analysis
- Macro analysis
- Attachment risk analysis
- Rule-based detection
- Security indicators
- Risk scoring

The architecture is designed so additional attachment analysis techniques can be added in future development.

---

### 👁️ Visual Intelligence

Visual Intelligence focuses on detecting phishing websites and brand impersonation through screenshot analysis.

Instead of analyzing only the URL, the system examines the visual appearance of a website.

**Visual analysis components include:**

- Screenshot capture
- Image preprocessing
- OCR
- Logo detection
- Brand detection
- Brand reference matching
- CLIP-based visual analysis
- Image similarity
- Color similarity
- Layout similarity
- Form detection
- QR detection
- Domain matching
- Visual risk analysis
- Explainable visual results

#### Brand Clone Detection

The system maintains reference brand assets and compares a captured website against known legitimate brand interfaces.

The comparison can use multiple visual signals such as:

```text
Captured Website
       │
       ├── Logo Similarity
       ├── Color Similarity
       ├── Layout Similarity
       ├── Visual Similarity
       ├── Form Detection
       └── Domain Analysis
                │
                ▼
        Risk / Similarity Analysis
                │
                ▼
       Explainable Security Result
```

This helps identify websites that visually imitate legitimate brands.

---

### 🛡️ Threat Intelligence

EscudoFlow AI integrates external threat intelligence and reputation sources to improve security analysis.

The current architecture includes integrations/services for:

- VirusTotal
- PhishTank
- AbuseIPDB
- Google Safe Browsing
- AlienVault

Threat intelligence results can be combined with internal rules and other security signals to improve the overall assessment.

---

### 🤖 Machine Learning

EscudoFlow AI also contains a dedicated machine learning module for phishing URL detection.

The ML pipeline is maintained separately under the `ml/` directory.

**Machine learning workflow:**

```text
Dataset
   │
   ▼
Data Preparation
   │
   ▼
Feature Extraction
   │
   ▼
Model Training
   │
   ▼
Model Evaluation
   │
   ▼
Prediction
```

**ML directory contains:**

- Feature extraction
- Training pipeline
- Prediction pipeline
- Exploratory data analysis
- Model development notebooks
- ML-specific requirements

The machine learning component is being continuously improved as part of the project.

---

### 🧠 Risk & Fusion Analysis

One of the core concepts of EscudoFlow AI is combining multiple security signals instead of depending on a single indicator.

For example:

```text
URL Analysis
     │
     ├── DNS
     ├── WHOIS
     ├── SSL
     ├── Redirects
     ├── Reputation
     └── Threat Intelligence
              │
              ▼
        Fusion / Rules
              │
              ▼
        Risk Assessment
```

Similarly, visual analysis can combine:

```text
Screenshot
    │
    ├── Logo Similarity
    ├── Color Similarity
    ├── Layout Similarity
    ├── OCR
    ├── Form Detection
    └── Domain Matching
             │
             ▼
       Visual Risk Analysis
```

This multi-signal approach is intended to provide more meaningful and explainable security results.

---

### 🔐 Authentication & User Management

The platform includes an authentication layer for user accounts.

**Current functionality includes:**

- User registration
- Login
- Session handling
- Authentication dependencies
- Password reset flow
- User-related models and schemas
- Protected backend functionality

Authentication functionality is integrated into the FastAPI backend.

---

### 📊 Dashboard & Reporting

EscudoFlow AI includes a dashboard and reporting architecture for presenting security analysis results.

The dashboard is designed to provide a centralized view of:

- Security scans
- Detection results
- Risk information
- Threat intelligence
- Analysis history
- Security statistics

The reporting module provides a foundation for generating and presenting security reports.

---

## 🏗️ System Architecture

The project follows a frontend-backend architecture with dedicated services for different security intelligence modules.

```text
                         ┌────────────────────────┐
                         │       Frontend         │
                         │   React + TypeScript    │
                         └────────────┬───────────┘
                                      │
                                      │ REST API
                                      ▼
                         ┌────────────────────────┐
                         │       FastAPI          │
                         │        Backend         │
                         └────────────┬───────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ▼                        ▼                        ▼
      URL Intelligence       Email Intelligence       Visual Intelligence
             │                        │                        │
             ▼                        ▼                        ▼
      DNS / WHOIS / SSL        Email Parser              OCR
      Reputation               Rules                     CLIP
      Threat Intel             URL Analysis              Logo Detection
      Redirects                Authentication            Similarity
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │   Risk / Fusion Layer  │
                         └────────────┬───────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │ Explainable Analysis &  │
                         │      Security Results   │
                         └────────────────────────┘
```

---

## 🛠️ Technology Stack

**Frontend**
- React
- TypeScript
- Vite
- Tailwind CSS
- Axios

**Backend**
- Python
- FastAPI
- Pydantic
- REST APIs

**Machine Learning**
- Python
- Scikit-learn
- Pandas
- Jupyter Notebook
- XGBoost / ML experimentation

**Computer Vision**
- OpenCV
- CLIP
- OCR
- Image processing
- Image similarity techniques

**Threat Intelligence**
- VirusTotal
- PhishTank
- AbuseIPDB
- Google Safe Browsing
- AlienVault

**Database**
- MongoDB

**Development Tools**
- Git
- GitHub
- Visual Studio Code

---

## 📁 Project Structure

```text
EscudoFlow-AI/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   │
│   │   ├── services/
│   │   │   ├── attachment/
│   │   │   ├── dashboard/
│   │   │   ├── reputation/
│   │   │   ├── threat/
│   │   │   └── visual/
│   │   │
│   │   └── utils/
│   │
│   ├── vision/
│   │   ├── logos/
│   │   └── reference_brands/
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── lib/
│   │   ├── routes/
│   │   └── services/
│   │
│   ├── package.json
│   └── package-lock.json
│
├── ml/
│   ├── notebooks/
│   ├── feature_extraction.py
│   ├── train.py
│   ├── predict.py
│   └── requirements.txt
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure the following are installed:

- Python 3.11+
- Node.js
- npm
- MongoDB
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Aruna-l/escudoflow-ai.git
cd escudoflow-ai
```

### ⚙️ Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

### 🔑 Environment Variables

Create a `.env` file inside the `backend` directory.

The application uses environment variables for sensitive configuration such as API credentials and service configuration.

Example:

```env
GOOGLE_SAFE_BROWSING_API_KEY=your_api_key
VIRUSTOTAL_API_KEY=your_api_key
ABUSEIPDB_API_KEY=your_api_key
```

Additional environment variables may be required depending on the services enabled in the application.

> **Important:** Never commit `.env` files or API keys to GitHub.

### ▶️ Run the Backend

From the backend directory:

```bash
uvicorn main:app --reload
```

The backend API will run at:
http://127.0.0.1:8000

### 💻 Frontend Setup

Open another terminal and navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available through the Vite development server.

### 🤖 Machine Learning Setup

Navigate to the project root and install the ML dependencies:

```bash
pip install -r ml/requirements.txt
```

The ML module contains separate scripts for feature extraction, training, and prediction.

**Training**
```bash
python ml/train.py
```

**Prediction**
```bash
python ml/predict.py
```

Exploratory and experimental notebooks are available under:
ml/notebooks/

---

## 🔒 Security Considerations

EscudoFlow AI is intended for cybersecurity research, defensive security analysis, and educational purposes.

**Important security practices**

- Never commit API keys.
- Never commit `.env` files.
- Do not expose database credentials.
- Keep third-party API credentials in environment variables.
- Validate uploaded files before processing.
- Use authentication for protected application functionality.
- Do not use the platform to perform unauthorized security testing.

---

## 🎯 Project Goals

The long-term goal of EscudoFlow AI is to provide a unified platform capable of analyzing different forms of phishing and security threats through a combination of:

```text
Machine Learning
       +
Rule-Based Detection
       +
Threat Intelligence
       +
Computer Vision
       +
Reputation Analysis
       +
Risk Fusion
       ↓
Unified Threat Assessment
```

The project aims to make security analysis more comprehensive, explainable, and accessible through a single platform.

---

## 📚 Learning Outcomes

This project provides practical experience in:

- Full-stack application development
- REST API development
- FastAPI backend architecture
- React and TypeScript development
- Machine learning
- Feature engineering
- Computer vision
- OCR
- Image similarity
- Threat intelligence APIs
- Cybersecurity analysis
- Authentication and authorization
- Database integration
- API integration
- Risk scoring
- Git and GitHub
- Software architecture

---

## 👩‍💻 Author

**Aruna L**

Bachelor of Engineering in Computer Science & Engineering

GitHub: [https://github.com/Aruna-l](https://github.com/Aruna-l)

Project Repository: [https://github.com/Aruna-l/escudoflow-ai](https://github.com/Aruna-l/escudoflow-ai)

---

## 📄 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
