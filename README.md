# AutoStream Agent 
An AI-powered customer support chatbot for a video streaming platform. It detects user intent, answers questions using RAG, and captures leads through a conversational flow — all powered by Mistral AI and LangGraph.

---

## 1. How to Run the Project Locally

### Prerequisites
- Python 3.8+
- A [Mistral AI](https://mistral.ai) API key

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/autostream-agent.git
cd autostream-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root of the project and add your Mistral API key:
```
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 4. Run the Agent
```bash
python main.py
```

### 5. Start Chatting
Once running, you'll see:
```
AutoStream Agent (type 'exit')

You:
```
Type your message and press Enter. Type `exit` to quit.

---

## 2. Architecture

AutoStream Agent is built using a **graph-based conversational architecture** powered by **LangGraph**, where each step in the conversation is a node and the flow between them is controlled by conditional routing logic.

### Why LangGraph?
LangGraph was chosen because it makes **multi-step, stateful conversations** easy to manage. Unlike simple chatbots that handle one prompt at a time, this agent needs to remember what it has already collected (name, email, platform) and decide what to ask next. LangGraph lets us define this as a proper graph — with clear nodes, edges, and routing conditions — making the logic transparent, modular, and easy to extend.

### How State is Managed
State is a plain Python **dictionary** that is passed through every node in the graph. Each node reads from the state and returns an updated copy of it. For example, the `lead_node` checks whether `name`, `email`, and `platform` are already present in the state before deciding what to ask next. The state persists across turns in the conversation loop in `main.py`, so nothing is lost between messages. This design keeps the agent **context-aware** across the full conversation without needing an external database or session manager.

---

## 3. WhatsApp Integration via Webhooks

The idea is to put a web server like FastAPI in front of my existing agent. When a user messages on WhatsApp, Meta's Cloud API forwards it to my server, which extracts the message and phone number, passes it into my LangGraph agent, and sends the response back through Meta's API.

The main thing I need to handle is session state — since multiple users can message at the same time, I need to maintain a separate state per user keyed by their phone number. For production I would use Redis so state is not lost if the server restarts.

The best part is my core agent code stays exactly the same. The webhook is just a new entry point into the same graph I already built.

