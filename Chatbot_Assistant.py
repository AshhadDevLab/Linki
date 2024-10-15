import streamlit as st
from openai import OpenAI

endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

# Read the data from an environment variable
with open("data/system_prompt.txt", "r") as file:
    system_prompt = file.read()

with st.sidebar:
    token = st.text_input(
        "API Key (GitHub Token or OpenAI API Key)",
        key="chatbot_api_key",
        type="password",
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/AshhadDevLab/AI-Portfolio/blob/master/Chatbot_Assistant.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/AshhadDevLab/AI-Portfolio?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

with open("data/intro_message.txt", "r") as file:
    intro_message = file.read()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": system_prompt}]
    st.session_state["messages"].append({"role": "assistant", "content": intro_message})

# Display only user and assistant messages
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not token:
        st.info("Please add your API key to continue.")
        st.stop()

    client = OpenAI(base_url=endpoint, api_key=token)
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        model=model_name, messages=st.session_state["messages"]
    )
    msg = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
