# 🚀 LLM Project Structure

A clean, reusable project template for quickly prototyping and demoing LLM-powered applications using **FastAPI**, **OpenAI**, **Gemini**, and optional **ngrok** and **VAPI** support.

## 📦 Features

- ✅ Clean and modular Python project layout
- ⚡ FastAPI backend for receiving requests
- 🧠 LLM abstraction layer supporting OpenAI & Gemini
- 🔐 Secure config via `.env` + `pydantic.BaseSettings`
- 🌍 Optional `ngrok` tunneling for local development
- 🎙️ VAPI integration-ready (for voice agent demos)

---
## 🧪 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/zjubirdfly/LLM_project_structure.git
cd LLM_project_structure

2. Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

3. Install Dependencies
poetry install

4. Set Up Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=sk-...
GEMINI_API_KEY=your-gemini-key

5. Run the Server
poetry run uvicorn src.main:app --reload

6. test the Feature

curl -X POST http://localhost:8000/api/v1/outbound   -H "Content-Type: application/json"   -d '{
    "phoneNumberId": "XXXX",
    "assistantId": "XXXXX",
    "customerNumber": "+XXXXX"
}'

🤝 Contributions
Feel free to fork, submit PRs, or open issues.