from langgraph.graph import StateGraph, END
from nodes import detect_intent, greeting_node, rag_node, lead_node

def route(state):
    if state.get("lead_active"):
        return "lead"

    intent = state.get("intent", "query")

    if intent == "greeting":
        return "greeting"

    elif intent == "high_intent":
        return "lead"

    elif intent == "query":
        return "rag"

    return "rag"

def build_graph():
    builder = StateGraph(dict)

    builder.add_node("intent", detect_intent)
    builder.add_node("greeting", greeting_node)
    builder.add_node("rag", rag_node)
    builder.add_node("lead", lead_node)

    builder.set_entry_point("intent")

    builder.add_conditional_edges("intent", route, {
        "greeting": "greeting",
        "rag": "rag",
        "lead": "lead"
    })

    builder.add_edge("greeting", END)
    builder.add_edge("rag", END)
    builder.add_edge("lead", END)

    return builder.compile()