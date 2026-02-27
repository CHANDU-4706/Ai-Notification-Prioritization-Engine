# CyePro - Notification Prioritization Engine

An AI-native prioritization system that intelligently categories notifications into **Now**, **Later**, or **Never** using **Llama 3** (via Groq) and **Semantic Analysis**.

## Key Features
- **Semantic Deduplication**: Uses vector embeddings (MiniLM) and FAISS to catch redundant alerts.
- **Smart Fatigue Management**: Employs an exponential decay model to track user alert volume.
- **Explainable AI (XAI)**: Generates clear reasoning for every decision made by the engine.
- **High-Performance Backend**: Built with Python/FastAPI for low-latency dispatching.
- **Premium Dashboard**: Real-time metrics and audit logs via a React/Vite frontend.

## Visual Showcase

### 1. Unified Intelligence Dashboard
The primary dashboard provides a high-level overview of the engine's performance, including real-time suppression rates and categorization distributions.
![Full Dashboard](./Photos%20of%20working%20application/Screenshot%202026-02-27%20124050.png)

### 2. Live Audit Feed (XAI)
Transparency is core to CyePro. The Audit Feed shows every decision made by the AI, including the "AI Reasoning" which explains *why* a notification was prioritized as NOW, LATER, or NEVER.
> [!NOTE]
> Notice in the screenshot how "Semantic Deduplication" catches near-identical messages even when the source is the same.
![Audit Feed](./Photos%20of%20working%20application/Screenshot%202026-02-27%20124158.png)

### 3. Interactive Test Engine
Developers can simulate high-volume events using the built-in test panel, adjusting priority hints and message content to see how the Brain reacts.
![Test Panel](./Photos%20of%20working%20application/Screenshot%202026-02-27%20124223.png)

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq Cloud API Key

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```env
GROQ_API_KEY=your_actual_key_here
```

**Initialize the DB:**
```bash
python app/database/db_init.py
```

**Run the Server (Option A - Standard):**
```bash
python main.py
```
*Note: This runs the server at `http://localhost:8001`.*

**Run the Server (Option B - Development with Auto-reload):**
```bash
uvicorn main:app --reload --port 8001
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Note: The frontend is configured to communicate with the backend at `http://localhost:8001`.*

## Constraint Fulfillment

| Constraint | Implementation Strategy |
| :--- | :--- |
| **High Event Volume** | Asynchronous processing via FastAPI/Uvicorn and efficient LiteDB indexing. |
| **Low-Latency Decisions** | 2-second strict timeout on AI calls with local rule-based fallback logic. |
| **Time-Sensitivity** | Stage 3 Expiry Check filters out stale notifications before expensive processing. |
| **Optional/Promotional Noise** | LLM classification identifies "Promotional" intent; Fatigue Model suppresses it during busy periods. |
| **Multi-Service Events** | User-centric History Service tracks fatigue across all service sources. |
| **Missing Duplicate Keys** | FAISS-powered Semantic Deduplication catches redundant alerts even without IDs. |
| **Explainable & Auditable** | Every decision includes an AI-generated `reason` and is stored in the Audit Log. |
| **No Silent Loss** | All notifications (including suppressed ones) are visible in the Audit Dashboard. |

## Documentation
- [Architecture Deep-Dive](ARCHITECTURE.md): Detailed 9-stage pipeline and mathematical models.

## Testing the Engine
1. Open the React Dashboard (`http://localhost:5173`).
2. Dispatch some "Transactional" events (NOW).
3. Dispatch the same event multiple times to see **Semantic Deduplication** in action.
4. Dispatch "Promotional" events rapidly to trigger the **Fatigue Model**.
5. Check the **Audit Feed** for AI-generated reasoning.
