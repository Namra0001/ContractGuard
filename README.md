# ContractGuard AI

An Autonomous Multi-Agent System for Contract Analysis, Risk Detection, Comparison and Deadline Management.

ContractGuard AI is a beginner-friendly AI-assisted web application that allows users to upload contracts and automatically analyze them. 

## Features

- **Automated Contract Analysis**: Upload PDF contracts and extract text for AI analysis.
- **Risk Detection**: Identify financial, termination, compliance, and other risks, generating an overall risk score.
- **Clause & Obligation Extraction**: Detect important clauses, user obligations, missing clauses, and ambiguous terms.
- **Deadline Tracking**: Identify important dates (start, expiry, notice periods) and track deadlines (only for accepted contracts).
- **AI Contract Chat**: Chat with a contract-specific AI to ask questions about the uploaded document.
- **Contract Comparison**: Upload multiple contracts and compare them side-by-side to find the best option.
- **Downloadable Reports**: Generate detailed PDF analysis reports using ReportLab.
- **Accept/Reject Workflow**: Manage contract statuses easily.

## Technology Stack

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- Fetch API for backend communication
- Responsive design

### Backend
- Python
- FastAPI

### Database
- SQLite

### AI & Processing
- Gemini API (AI Analysis & Chat)
- PyMuPDF (PDF Text Extraction)
- ReportLab (PDF Report Generation)

## Project Architecture

The project is structured into three main layers:
1. **Frontend**: Clean, responsive SaaS-style UI built with Vanilla JS.
2. **Backend**: FastAPI REST API handling logic, database operations, and external services.
3. **Services**: Specific python modules handling distinct tasks like PDF processing, Gemini AI integration, analysis, comparison, and report generation.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Namra0001/ContractGuard.git
   cd ContractGuard
   ```

2. **Set up the virtual environment (Backend):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the root directory (you can copy `.env.example` if available) and add your secrets:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*Note: Never commit your `.env` file to Git.*

## Database Setup

SQLite is used for the database. When you run the FastAPI backend for the first time, the required tables (users, contracts, analyses, deadlines, chat_messages, reports) will be created automatically in the `database/contractguard.db` file.

## Running Backend

Start the FastAPI development server:

```bash
cd backend
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

## Running Frontend

You can serve the frontend locally using Python's built-in HTTP server or any preferred local server:

```bash
cd frontend
python -m http.server 3000
```
Open your browser and navigate to `http://localhost:3000`.

## Gemini API Setup

The application uses the Gemini API for contract analysis and Q&A. You must obtain an API key from Google AI Studio and place it in the `.env` file as `GEMINI_API_KEY`. The backend services will securely load this key to authenticate requests.

## PDF Processing

Text extraction from uploaded PDF contracts is handled by **PyMuPDF**. When a user uploads a contract, the backend `pdf_service` reads the PDF file, extracts all textual content, and prepares it for AI analysis.

## Report Generation

Downloadable PDF reports are generated using **ReportLab**. The `report_service` takes the structured JSON analysis output from the Gemini API and dynamically constructs a professional, well-formatted PDF report containing the risk score, clauses, obligations, and recommendations.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive a token
- `GET /api/auth/me` - Get current user details

### Contracts
- `POST /api/contracts/upload` - Upload a new contract PDF
- `GET /api/contracts` - Get all user contracts
- `GET /api/contracts/{contract_id}` - Get contract details
- `POST /api/contracts/{contract_id}/accept` - Accept a contract
- `POST /api/contracts/{contract_id}/reject` - Reject a contract

### Analysis & Reporting
- `POST /api/contracts/{contract_id}/analyze` - Trigger AI analysis
- `GET /api/contracts/{contract_id}/analysis` - Retrieve analysis results
- `GET /api/contracts/{contract_id}/report/download` - Download PDF report

### Chat & Comparison
- `POST /api/chat` - Send a message to the contract AI
- `POST /api/compare` - Compare two or more contracts

### Deadlines
- `GET /api/deadlines` - Get all deadlines for accepted contracts

## Project Workflow

1. **Upload**: User uploads a PDF contract.
2. **Extract**: PyMuPDF extracts text from the document.
3. **Analyze & Risk Detection**: Gemini API analyzes the text for risks, obligations, clauses, and missing terms, returning a structured JSON response and calculating a risk score.
4. **Recommendations**: AI provides practical recommendations based on the analysis.
5. **Report**: ReportLab generates a downloadable PDF summary.
6. **Accept/Reject**: User reviews the analysis and decides to accept or reject the contract.
7. **Deadline Tracking**: If accepted, important dates become active deadlines tracked on the dashboard.

## Disclaimer

**ContractGuard AI provides AI-generated informational analysis and is NOT a substitute for professional legal advice.** Always consult with a qualified legal professional before signing any legally binding agreements.
