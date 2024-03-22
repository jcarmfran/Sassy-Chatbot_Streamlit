### Streamlit code ###
st.title("Sassy Chatbot :face_with_rolling_eyes:")

# Sidebar
st.sidebar.header("Options")

# Initialize the ConversationManager object
if 'chat_manager' not in st.session_state:
    st.session_state['chat_manager'] = ConversationManager(api_key)

chat_manager = st.session_state['chat_manager']

# Set the token budget, max tokens per message, and temperature with sliders
max_tokens_per_message = st.sidebar.slider("Max Tokens Per Message", min_value=10, max_value=500, value=50)
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)

# Select and set system message with a selectbox
system_message = st.sidebar.selectbox("System message", ['Sassy', 'Angry', 'Thoughtful', 'Custom'])

if system_message == 'Sassy':
    chat_manager.set_persona('sassy_assistant')
elif system_message == 'Angry':
    chat_manager.set_persona('angry_assistant')
elif system_message == 'Thoughtful':
    chat_manager.set_persona('thoughtful_assistant')
# Open text area for custom system message if "Custom" is selected
elif system_message == 'Custom':
    custom_message = st.sidebar.text_area("Custom system message")
    if st.sidebar.button("Set custom system message"):
        chat_manager.set_custom_system_message(custom_message)

if st.sidebar.button("Reset conversation history", on_click=chat_manager.reset_conversation_history):
    st.session_state['conversation_history'] = chat_manager.conversation_history

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = chat_manager.conversation_history

conversation_history = st.session_state['conversation_history']

# Chat input from the user
user_input = st.chat_input("Write a message")

# Call the chat manager to get a response from the AI. Uses settings from the sidebar.
if user_input:
    response = chat_manager.chat_completion(user_input, temperature=temperature, max_tokens=max_tokens_per_message)

# Display the conversation history
for message in conversation_history:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])