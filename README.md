🧠 Aurora QA Service

A lightweight question-answering API built with FastAPI that answers natural-language questions about member data fetched from Aurora’s public messages endpoint.

🚀 Live Demo

Base URL:
👉 https://aurora-qa-pnwt.onrender.com

Example Queries:

GET /ask?q=When%20is%20Layla%20planning%20her%20trip%20to%20London%3F
GET /ask?q=How%20many%20cars%20does%20Vikram%20Desai%20have%3F
GET /ask?q=What%20are%20Amira%27s%20favorite%20restaurants%3F


Sample Responses

{ "answer": "May 14, 2025" }
{ "answer": "2" }
{ "answer": "Sushi Samba, Nando’s, The Ivy" }

🧩 Features

Simple /ask endpoint that accepts natural language questions

Retrieves member messages dynamically from Aurora’s API

Uses fuzzy string matching to find relevant messages

Extracts dates, counts, and lists intelligently

Returns clean JSON { "answer": "..." }

🛠️ Installation (run locally)
git clone https://github.com/vallapureddygreeshma02/aurora-qa.git
cd aurora-qa
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app:app --reload --port 8000


Then visit:
👉 http://127.0.0.1:8000/ask?q=When%20is%20Layla%20planning%20her%20trip%20to%20London%3F

🧠 API Overview
Endpoint
GET /ask?q=<your question>

Response
{ "answer": "..." }

Error Example
{ "detail": "No messages from API" }

📄 File Structure
aurora-qa/
├── app.py              # Main FastAPI application
├── requirements.txt    # Dependencies
├── README.md           # Documentation
└── .gitignore

💡 Design Notes (Bonus 1)
Approach	Description	Pros	Cons
Rule-based (current)	Custom regex & logic for date, count, and list questions	Simple, fast, transparent	Needs new rules for new patterns
Embedding retrieval	Use sentence-transformers to match semantically similar messages	Handles phrasing changes	Slightly heavier dependencies
RAG with LLM	Retrieve top-k messages, then query an LLM for the answer	Most flexible, high accuracy	Needs API keys / cost
NER-based IE	Extract entities like PERSON, DATE, LOCATION	Interpretable, extendable	More code & libraries
📊 Data Insights (Bonus 2)

While exploring the /messages data:

Some members have duplicate entries with conflicting details.

Date formats vary (e.g., “12/06/25”, “June 12th 2025”).

Minor inconsistencies in spelling of member names (“Layla” vs “Laila”).

A few entries contain null or empty message fields.

🧩 These can be normalized in preprocessing if scaling to a larger QA system.

🧰 Future Enhancements

Add SQLite caching to avoid repeated API calls.

Integrate embedding-based retrieval for more flexible question matching.

Extend extractors for locations, budgets, and event types.

Add unit tests for extractor functions.

🧑‍💻 Author

Greeshma Reddy Vallapureddy Gari
