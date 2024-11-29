import ollama
import time

def create_chat_bot():
    # Initialize conversation history
    conversation_history = []
    
    # System prompt to set the behavior of the chatbot
    system_prompt = """You are a helpful and friendly AI assistant. 
    You provide clear, accurate, and concise responses while maintaining a conversational tone.
    If you're unsure about something, please say so rather than making assumptions."""
    
    print("Chatbot: Hello! I'm your AI assistant. How can I help you today? (Type 'quit' to exit)")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check for exit condition
        if user_input.lower() == 'quit':
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        try:
            # Create the message structure
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ]
            
            # Add conversation history
            for msg in conversation_history:
                messages.append(msg)
                
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get response from Ollama
            response = ollama.chat(
                model='llama3',
                messages=messages,
                stream=False
            )
            
            # Extract the response content
            assistant_response = response['message']['content']
            
            # Update conversation history
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Print the response
            print("Chatbot:", assistant_response)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    create_chat_bot()