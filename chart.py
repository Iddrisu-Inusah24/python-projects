import openai

# Replace 'your_api_key_here' with your actual OpenAI API key
client = openai.OpenAI(api_key="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")

def chat_with_ai():
    print("🤖 AI Chatbot (Type 'exit' to stop)")
    
    conversation = []  # Stores chat history
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break
        
        # Add user message to conversation history
        conversation.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change to "gpt-4" if you have access
                messages=conversation
            )

            ai_reply = response.choices[0].message.content
            print("AI:", ai_reply)

            # Add AI response to conversation history
            conversation.append({"role": "assistant", "content": ai_reply})

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chat_with_ai()