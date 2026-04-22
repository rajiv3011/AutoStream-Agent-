from graph import build_graph


graph = build_graph()

state = {
    "name": None,
    "email": None,
    "platform": None,
    "lead_active": False
}

print("AutoStream Agent (type 'exit')\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    state["input"] = user_input

    result = graph.invoke(state)

    print("Bot:", result["response"])

    state.update(result)

    if result.get("done"):
        break
