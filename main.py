from langchain.agents import Tool, AgentExecutor, initialize_agent
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from flask import Flask, request, jsonify

# Custom tools implementation
def get_company_info(input_text: str) -> str:
    """Get information about a company"""
    # Mock implementation - replace with actual database queries
    company_database = {
        "datixity": "Datixity is a data automation and analytics company specializing in custom solutions.",
        "default": "Company information not found in database."
    }
    return company_database.get(input_text.lower(), company_database["default"])

def get_service_details(input_text: str) -> str:
    """Get details about specific services"""
    # Mock implementation - replace with actual service data
    services = {
        "data automation": "Our data automation service includes ETL pipeline development, workflow automation, and real-time processing.",
        "analytics": "We provide advanced analytics solutions including predictive modeling and business intelligence dashboards.",
        "default": "Service details not found."
    }
    return services.get(input_text.lower(), services["default"])

def get_support_info(input_text: str) -> str:
    """Get support information"""
    return "For technical support, please contact support@datixity.com or call our helpdesk at 1-800-DATIXITY"

# Initialize tools
tools = [
    Tool(
        name="Company Information",
        func=get_company_info,
        description="Use this to get information about the company and its background"
    ),
    Tool(
        name="Service Details",
        func=get_service_details,
        description="Use this to get specific information about services offered"
    ),
    Tool(
        name="Support Information",
        func=get_support_info,
        description="Use this to get support contact information"
    )
]

# Setup chatbot
def setup_chatbot():
    # Initialize LLM
    llm = Ollama(model="llama3")  # Using llama3
    
    # Setup memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant for Datixity, a data automation company. "
                  "Provide clear and professional responses based on the available tools. "
                  "If you don't know something than don't answer"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    # Initialize agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-conversational-react-description",
        verbose=True,
        memory=memory,
        prompt=prompt
    )
    
    return agent

# Initialize Flask app
app = Flask(__name__)
agent = setup_chatbot()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get response from agent
        response = agent.run(user_message)
        
        return jsonify({
            "response": response,
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    6756aed76280d5284c0d66ff

    6756aec88fdfc44b58ac6d59

