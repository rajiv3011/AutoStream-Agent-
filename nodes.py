from tools import mock_lead_capture
from rag import retrieve
from mistral_llm import generate_response
import json

# -----------------------
# Intent Node (LLM-based)
# -----------------------
def detect_intent(state):
    user_input = state["input"]

    prompt = f"""
    Classify the intent:
    greeting, query, high_intent

    Input: {user_input}
    Answer only one word.
    """

    intent = generate_response(prompt).strip().lower().split()[0]

    return {**state, "intent": intent}

# -----------------------
# Greeting Node
# -----------------------
def greeting_node(state):
    return {**state, "response": "Hello! How can I help you today?"}

# -----------------------
# RAG Node
# -----------------------
def rag_node(state):
    answer = retrieve(state["input"])
    return {**state, "response": answer}


    

# -----------------------
# Lead Flow Node
# -----------------------


def lead_node(state):
    current_state = state.copy()
    current_state["lead_active"] = True 
    user_input = current_state.get("input", "")

    prompt = f"""
    Extract fields from: {user_input}
    Fields: name, email, platform. 
    Return JSON only.

    Rules:
    - Do NOT hallucinate
    - Platform must be one of: Instagram, LinkedIn, Twitter, YouTube, Facebook (or similar)
    - Do NOT extract email domain as platform
    - If any field is missing, return null
    """

    try:
        raw_output = generate_response(prompt)
        clean_json = raw_output.replace("```json", "").replace("```", "").strip()
        extracted = json.loads(clean_json)
    except Exception as e:
        print(f"Extraction failed: {e}")
        extracted = {}

    for key in ["name", "email", "platform"]:
        if extracted.get(key):
            current_state[key] = extracted[key]

    if not current_state.get("name"):
        return {**current_state, "response": "What's your name?"}

    if not current_state.get("email"):
        return {**current_state, "response": "What's your email?"}

    if not current_state.get("platform"):
        return {**current_state, "response": "Which platform do you use?"}
            

    mock_lead_capture(
        current_state["name"],
        current_state["email"],
        current_state["platform"]
    )

    return {
        **current_state,
        "response": "Thanks! We'll contact you soon.",
        "done": True,
        "lead_active": False
    }
