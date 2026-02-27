# CyePro - Notification Prioritization Engine

An AI-native prioritization system that intelligently categories notifications into **Now**, **Later**, or **Never** using **Llama 3** (via Groq) and **Semantic Analysis**.

## Key Features
- **Semantic Deduplication**: Uses vector embeddings (MiniLM) and FAISS to catch redundant alerts.
- **Smart Fatigue Management**: Employs an exponential decay model to track user alert volume.
- **Explainable AI (XAI)**: Generates clear reasoning for every decision made by the engine.
- **High-Performance Backend**: Built with Python/FastAPI for low-latency dispatching.
- **Premium Dashboard**: Real-time metrics and audit logs via a React/Vite frontend.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq Cloud API Key

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
Create a `.env` file in the `backend` directory:
```env
GROQ_API_KEY=your_actual_key_here
```
Initialize the DB:
```bash
python app/database/db_init.py
```
Start the server:
```bash
uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Testing the Engine
1. Open the React Dashboard (`http://localhost:5173`).
2. Dispatch some "Transactional" events (NOW).
3. Dispatch the same event multiple times to see **Semantic Deduplication** in action.
4. Dispatch "Promotional" events rapidly to trigger the **Fatigue Model**.
5. Check the **Audit Feed** for AI-generated reasoning.
