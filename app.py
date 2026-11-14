import streamlit as st
from groq import Groq

# Page setup
st.set_page_config(
    page_title="Cloud AI Chat",
    page_icon="🤖"
)

st.title("Cloud AI Chat")
st.caption("Free cloud AI chatbot powered by Groq")

# Select the cloud AI model
MODEL = "openai/gpt-oss-20b"

# Load the private API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Groq API key is missing. Configure Streamlit Secrets.")
    st.stop()

# Create the Groq client
client = Groq(api_key=api_key)

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear conversation button
if st.sidebar.button("Clear conversation"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages
for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.write(item["content"])

# User input
prompt = st.chat_input("Ask a question")

if prompt and prompt.strip():

    # Save the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt.strip()
    })

    # Display the user's message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate the AI response
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
                result = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages[-16:],
                    max_completion_tokens=512
                )

                answer = result.choices[0].message.content

                if not answer:
                    answer = "No answer was generated. Please try again."

                st.write(answer)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Unable to generate a response: {e}")
