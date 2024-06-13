import streamlit as st
from run import query_bot

# Function to get response from your chatbot
def get_chatbot_response(user_input):
    response = query_bot(user_input)
    return response

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("RAG Chatbot")
st.write("Ask anything!")

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        with st.spinner('Processing...'):
            response = get_chatbot_response(user_input)
        st.session_state.history.append((user_input, response))
        user_input = ""  # Clear input after sending

# Display conversation history
for user_query, bot_response in st.session_state.history:
    st.write(f"You: {user_query}")
    st.write(f"Chatbot: {bot_response}")
    st.write("---")
