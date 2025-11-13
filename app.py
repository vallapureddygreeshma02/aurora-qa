from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import httpx
import re
from rapidfuzz import fuzz, process
import dateparser

API_URL = "https://november7-730026606190.europe-west1.run.app/messages"

app = FastAPI(title="Aurora Member QA", version="1.0")

def normalize_text(s: str) -> str:
    return (s or "").strip().replace("\n", " ")

def extract_person_name(question: str) -> str:
    m = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'s\b", question)
    if m:
        return m.group(1)
    candidates = re.findall(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+){0,2})\b", question)
    bad = {"When","How","What","Which","Does","Is","Are","To","In","On","Of","The"}
    candidates = [c for c in candidates if c not in bad]
    return sorted(candidates, key=len, reverse=True)[0] if candidates else ""

def fetch_messages():
    try:
        with httpx.Client(timeout=30) as client:
            r = client.get(API_URL)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict) and "messages" in data:
                return data["messages"]
            if isinstance(data, list):
                return data
            return []
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"API error: {e}")

def stringify_message(msg: dict) -> str:
    parts = []
    for key in ("member","name","text","message","content","timestamp","date"):
        if key in msg and msg[key]:
            parts.append(str(msg[key]))
    return normalize_text(" | ".join(parts))

def select_top_messages(question, corpus, k=5):
    strings = [stringify_message(m) for m in corpus]
    results = process.extract(question, strings, scorer=fuzz.token_set_ratio, limit=k)
    return [corpus[i] for _,_,i in results]

def extract_date_phrase(text: str) -> str:
    m = re.search(r"\b(?:on\s+)?([A-Z][a-z]+\s+\d{1,2}(?:,\s*\d{4})?)", text)
    if m:
        phrase = m.group(1)
        dt = dateparser.parse(phrase)
        return dt.strftime("%B %d,  %Y") if dt else phrase
    return ""

@app.get("/ask")
def ask(q: str = Query(...)):
    messages = fetch_messages()
    if not messages:
        raise HTTPException(status_code=502, detail="No messages from API")

    person = extract_person_name(q)
    if person:
        messages = [m for m in messages if person.lower() in stringify_message(m).lower()] or messages

    top_msgs = select_top_messages(q, messages)
    texts = [stringify_message(m) for m in top_msgs]

    q_low = q.lower()
    if "when" in q_low and "trip" in q_low:
        for t in texts:
            d = extract_date_phrase(t)
            if d:
                return JSONResponse({"answer": d})
    if "how many" in q_low and "car" in q_low:
        for t in texts:
            m = re.search(r"(\d+)\s+car", t, re.IGNORECASE)
            if m:
                return JSONResponse({"answer": m.group(1)})
    if "favorite" in q_low and "restaurant" in q_low:
        for t in texts:
            idx = t.lower().find("favorite")
            if idx != -1:
                after = t[idx:]
                items = re.split(r",| and ", after)
                if len(items) > 1:
                    return JSONResponse({"answer": ", ".join(items[:5])})
    return JSONResponse({"answer": texts[0][:200] if texts else "Sorry, no answer found."})

@app.get("/")
def root():
    return {"ok": True, "hint": "Use /ask?q=Your+Question"}
