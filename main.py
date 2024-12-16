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
        "services": """Datixity offers the following key services:
1. Data Automation: ETL pipeline development and workflow automation
2. Analytics: Predictive modeling and BI dashboards
3. Custom Solutions: Tailored data solutions for business needs
4. Real-time Processing: Stream processing and real-time analytics""",
        "default": """Our main services include:
- Data Automation and ETL Solutions
- Advanced Analytics and Business Intelligence
- Custom Data Solutions
- Real-time Data Processing
For specific service details, please ask about a particular service."""
    }
    
    # If input is empty or None, return default services list
    if not input_text:
        return services["default"]
    
    return services.get(input_text.lower(), services["default"])
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
    # In the setup_chatbot function, modify the system prompt:
    prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant for Datixity, a data automation company. 
    When asked about services, use the Service Details tool to provide information.
    When asked about the company, use the Company Information tool.
    When asked about support, use the Support Information tool.
    Always provide clear and professional responses based on the available tools."""),
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
        prompt=prompt,
        handle_parsing_errors=True
    )
    
    return agent


if __name__ == "__main__":
    # Initialize the chatbot
    agent = setup_chatbot()
    
    print("Chatbot initialized! Type 'quit' to exit.")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check for quit command
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        
        try:
            # Get response from agent
            response = agent.invoke({"input": user_input})
            print("\nBot:", response['output'])
        except Exception as e:
            print("\nError:", str(e))
    

