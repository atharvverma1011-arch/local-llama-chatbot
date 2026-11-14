import streamlit as st
from ollama import Client

MODEL = "llama3.2:1b"
st.set_page_config(page_title="Local Llama Chat", page_icon="{}")
st.title("Local Llama Chat")
st.caption("Free local model; chat history is temporary..")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear conversation"):
    st.session_state.messages = []
    st.rerun()

for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.write(item["content"])

prompt = st.chat_input("Ask a question")
if prompt and prompt.strip():
    st.session_state.messages.append(
        {"role": "user","content": prompt.strip()}
    )
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
                client = Client(host="http://localhost:11434")

                result = client.chat(
                                    model=MODEL,
                                    messages=st.session_state.messages
                        )

                answer = result.message.content

                st.write(answer)

                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": answer
                                    })

            except Exception as e:
                st.error(f"Error occurred: {e}")
                st.exception(e)