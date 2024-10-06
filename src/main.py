import streamlit as st
import requests
import json

# Docker endpoint.
LLM_API_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title=f"LocalLlamas", page_icon="🦙")

# Initialize session state variables.
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'context' not in st.session_state:
    st.session_state['context'] = None

# Sidebar model selection.
st.sidebar.title("⚙️ Settings")
selected_model = st.sidebar.selectbox("Model selection:", ["llama3.2", "llama3", "llama2-uncensored"], index=0)

# Buttons to clear.
with st.sidebar.expander("Maintenance"):
    if st.button("Wipe Context"):
        st.session_state['context'] = None
    if st.button("Clear History"):
        st.session_state['messages'] = []

st.title(f"🦙 {selected_model}")

# Send prompt to LLM.
def post_prompt(prompt, model, context=None):
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        if context:
            payload["context"] = context
        response = requests.post(LLM_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip(), response.json().get("context", None)
    except (requests.RequestException, json.JSONDecodeError) as e:
        st.error(f"Error: {str(e)}")
        return None, None

# Display chat messages from history.
for message in st.session_state['messages']:
    avatar = "🥩" if message['role'] == 'user' else "🦙"
    with st.chat_message(message['role'], avatar=avatar):
        st.markdown(message['content'])

# Accept user input.
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history.
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🥩"):
        st.markdown(prompt)

    # Generate response from LLM.
    with st.spinner(f'{selected_model} generating response...'):
        response, new_context = post_prompt(prompt, selected_model, st.session_state['context'])
        if response:
            st.session_state['messages'].append({"role": "ai", "content": response})
            st.session_state['context'] = new_context
            with st.chat_message("ai", avatar="🦙"):
                st.markdown(response)