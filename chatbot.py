import streamlit as st
from openai import OpenAI

endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

with open("data/system_prompt.txt", "r") as file:
    system_prompt = file.read()

st.set_page_config(
    page_title="Linki - Your Personal Profile Guide",
    layout="wide",
    page_icon="./assets/linki_char_msg.png",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://github.com/AshhadDevLab/Linki/issues",
        "Report a bug": "https://github.com/AshhadDevLab/Linki/issues",
        "About": """
            ## Linki - Your Personal Profile Guide
            ### Powered using GitHub Models

            **GitHub**: https://github.com/AshhadDevLab/

            The AI Assistant named Linki is designed to provide detailed insights about your LinkedIn profile,
            generate code snippets, and assist with technical questions. Linki specializes in offering
            professional updates, analyzing projects, and troubleshooting code. It is continually improving to
            handle a wide range of queries, from AI concepts to app generation. Linki has been crafted to act
            as your personalized digital assistant, blending expertise with approachability.
        """,
    },
)

with st.sidebar:
    st.image(
        "assets/linki_char.png",
        use_container_width=True,
        output_format="PNG",
    )
    st.markdown(
        """
        <style>
        [data-testid="stImage"] img {
            border-radius: 45px;
            box-shadow: 
                0 0 5px #002D3F,
                0 0 10px #005A7F,
                0 0 15px #0087BF,
                0 0 20px #00B4FF,
                0 0 25px #33C2FF,
                0 0 30px #66D1FF,
                0 0 35px #99E0FF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    token = st.text_input(
        "API Key (GitHub Token)",
        key="chatbot_api_key",
        type="password",
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/AshhadDevLab/AI-Portfolio/blob/master/Chatbot_Assistant.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/AshhadDevLab/AI-Portfolio?quickstart=1)"

    st.sidebar.markdown("---")

    show_basic_info = st.sidebar.checkbox("Show Basic Interactions", value=True)
    if show_basic_info:
        st.sidebar.markdown("""
        ### Basic Interactions
        - Ask Linki to provide details from your LinkedIn profile, including your experience, skills, or recent activities.
        - Use keywords like `sample code`, `how-to`, or `example` to get code snippets relevant to common programming questions.
        - Ask about generative AI, data processing, or other AI topics, and Linki will give a brief overview or direct you to helpful resources.
        """)

    # Display advanced interactions
    show_advanced_info = st.sidebar.checkbox("Show Advanced Interactions", value=False)
    if show_advanced_info:
        st.sidebar.markdown("""
        ### Advanced Interactions
        - Use phrases like `generate code for me` or `create script` to have Linki draft simple code snippets, including Streamlit app starters.
        - Ask Linki to `analyze my project` or `review my approach` for technical insights and optimization tips based on your project’s structure.
        - Use keywords like `debug this code`, `fix error`, or `help with issue` to get help troubleshooting specific problems.
        - Use commands like `build custom app`, `make an app for`, or `generate Streamlit app` for more tailored app templates.
        """)

    st.sidebar.markdown("---")

    st.image(
        "assets/streamlit_sidebar.png",
        use_container_width=True,
        output_format="PNG",
    )
    st.markdown(
        """
        <style>
        [data-testid="stImage"] img {
            border-radius: 45px;
            box-shadow: 
                0 0 5px #002D3F,
                0 0 10px #005A7F,
                0 0 15px #0087BF,
                0 0 20px #00B4FF,
                0 0 25px #33C2FF,
                0 0 30px #66D1FF,
                0 0 35px #99E0FF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title("💬 Linki LinkedIn Assistant")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

with open("data/intro_message.txt", "r") as file:
    intro_message = file.read()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": system_prompt}]
    st.chat_message("assistant", avatar="assets/linki_char_msg.png").write(
        intro_message
    )

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
    st.chat_message("assistant", avatar="assets/linki_char_msg.png").write(msg)
