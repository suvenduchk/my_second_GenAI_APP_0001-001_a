# # -----------------------------------------------------------------------------
# # GenAI Web Application using Streamlit, LangChain, and Ollama's gemma:2b
# # -----------------------------------------------------------------------------
# # This app allows users to input questions, select a language model (gemma:2b, GPT-3, GPT-4),
# # adjust parameters, and get AI-generated answers. It uses Streamlit for the UI and LangChain
# # for model interaction. The code is fully documented and visually enhanced for clarity.
# # -----------------------------------------------------------------------------

# import streamlit as st
# from langchain.llms import Ollama, OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# # -------------------- Streamlit Page Config --------------------
# st.set_page_config(
#     page_title="GenAI Chat App - gemma:2b & More",
#     page_icon="🤖",
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# # -------------------- Custom CSS for Visual Appeal --------------------
# st.markdown("""
#     <style>
#     .main { background: linear-gradient(135deg, #232526 0%, #414345 100%); color: #fff; }
#     .stTextInput>div>div>input, .stTextArea textarea { background: #222; color: #fff; }
#     .stButton>button { background: #4e54c8; color: #fff; border-radius: 8px; }
#     .stSelectbox>div>div>div { background: #222; color: #fff; }
#     .stSlider>div>div>div { color: #fff; }
#     .stMarkdown { color: #fff; }
#     </style>
# """, unsafe_allow_html=True)

# # -------------------- Sidebar: Model & Params --------------------
# st.sidebar.title("⚙️ Model Settings")
# model_choice = st.sidebar.selectbox(
#     "Choose Language Model",
#     options=["gemma:2b (Ollama)", "GPT-3 (OpenAI)", "GPT-4 (OpenAI)"],
#     index=0
# )
# temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.05)
# max_tokens = st.sidebar.slider("Max Tokens", 32, 1024, 256, 8)
# st.sidebar.markdown("---")
# st.sidebar.info("Tip: gemma:2b runs locally via Ollama. GPT-3/4 require OpenAI API key.")

# # -------------------- Session State for Input/Output --------------------
# if "user_input" not in st.session_state:
#     st.session_state.user_input = ""
# if "response" not in st.session_state:
#     st.session_state.response = ""
# if "history" not in st.session_state:
#     st.session_state.history = []

# # -------------------- App Title & Description --------------------
# st.title("🤖 GenAI Chat App")
# st.markdown("""
# Welcome to the GenAI Chat App!  
# Ask any question and get answers from advanced language models.  
# - **Supports:** gemma:2b (local), GPT-3, GPT-4 (OpenAI)
# - **Adjust creativity and length with temperature & max tokens.**
# """)

# # -------------------- User Input Form --------------------
# with st.form(key="input_form"):
#     user_input = st.text_area("Enter your question or prompt:", value=st.session_state.user_input, height=100)
#     col1, col2 = st.columns([1,1])
#     with col1:
#         submit_btn = st.form_submit_button("Submit")
#     with col2:
#         clear_btn = st.form_submit_button("Clear")

# # -------------------- Clear Button Logic --------------------
# if clear_btn:
#     st.session_state.user_input = ""
#     st.session_state.response = ""
#     st.session_state.history = []
#     st.experimental_rerun()

# # # -------------------- Model Selection & LLM Setup --------------------
# # def get_llm(model_choice, temperature, max_tokens):
# #     if model_choice.startswith("gemma"):
# #         # Use Ollama's gemma:2b model (local)
# #         return Ollama(
# #             model="gemma:2b",
# #             temperature=temperature,
# #             max_tokens=max_tokens
# #         )
# #     elif model_choice.startswith("GPT-3"):
# #         # Use OpenAI GPT-3 (requires API key)
# #         return OpenAI(
# #             model_name="gpt-3.5-turbo",
# #             temperature=temperature,
# #             max_tokens=max_tokens
# #         )
# #     elif model_choice.startswith("GPT-4"):
# #         # Use OpenAI GPT-4 (requires API key)
# #         return OpenAI(
# #             model_name="gpt-4",
# #             temperature=temperature,
# #             max_tokens=max_tokens
# #         )
# #     else:
# #         raise ValueError("Invalid model selection.")

# # # -------------------- Prompt Template --------------------

# # ...existing code...
# def get_llm(model_choice, temperature, max_tokens):
#     if model_choice.startswith("gemma"):
#         # Use Ollama's gemma:2b model (local)
#         return Ollama(
#             model="gemma:2b",
#             temperature=temperature
#             # max_tokens is NOT a valid argument for Ollama
#         )
#     elif model_choice.startswith("GPT-3"):
#         # Use OpenAI GPT-3 (requires API key)
#         return OpenAI(
#             model_name="gpt-3.5-turbo",
#             temperature=temperature,
#             max_tokens=max_tokens
#         )
#     elif model_choice.startswith("GPT-4"):
#         # Use OpenAI GPT-4 (requires API key)
#         return OpenAI(
#             model_name="gpt-4",
#             temperature=temperature,
#             max_tokens=max_tokens
#         )
#     else:
#         raise ValueError("Invalid model selection.")
# # ...existing code...


# # -------------------------------------------------------------
# prompt_template = PromptTemplate(
#     input_variables=["question"],
#     template="You are a helpful AI assistant. Answer the following question:\n\n{question}"
# )

# # -------------------- Submit Button Logic --------------------
# if submit_btn:
#     if not user_input.strip():
#         st.warning("Please enter a question or prompt.")
#     else:
#         try:
#             llm = get_llm(model_choice, temperature, max_tokens)
#             chain = LLMChain(llm=llm, prompt=prompt_template)
#             with st.spinner("Generating response..."):
#                 response = chain.run({"question": user_input})
#             st.session_state.response = response
#             st.session_state.user_input = user_input
#             st.session_state.history.append({"question": user_input, "answer": response})
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#             st.session_state.response = ""

# # -------------------- Display Model's Response --------------------
# if st.session_state.response:
#     st.markdown("#### 📝 Model's Response")
#     st.success(st.session_state.response)

# # -------------------- Conversation History --------------------
# if st.session_state.history:
#     with st.expander("Show Conversation History"):
#         for idx, turn in enumerate(st.session_state.history[::-1], 1):
#             st.markdown(f"**Q{idx}:** {turn['question']}")
#             st.markdown(f"**A{idx}:** {turn['answer']}")

# # -------------------- Footer --------------------
# st.markdown("""
# ---
# <div style='text-align:center; color:#aaa;'>
#     <small>
#         Powered by <b>LangChain</b>, <b>Streamlit</b>, and <b>Ollama gemma:2b</b>.<br>
#         For educational use. <br>
#         <i>Tip: gemma:2b runs locally. For GPT-3/4, set your OpenAI API key as OPENAI_API_KEY env variable.</i>
#     </small>
# </div>
# """, unsafe_allow_html=True)





# -----------------------------------------------------------------------------
# GenAI Web Application using Streamlit, LangChain, and Ollama's gemma:2b
# -----------------------------------------------------------------------------
# This app allows users to input questions, select a language model (gemma:2b, GPT-3, GPT-4),
# adjust parameters, and get AI-generated answers. It uses Streamlit for the UI and LangChain
# for model interaction. The code is fully documented and visually enhanced for clarity.
# -----------------------------------------------------------------------------

import streamlit as st
from langchain.llms import Ollama, OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -------------------- Streamlit Page Config --------------------
st.set_page_config(
    page_title="GenAI Chat App - gemma:2b & More",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------- Custom CSS for Visual Appeal --------------------
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #232526 0%, #414345 100%); color: #fff; }
    .stTextInput>div>div>input, .stTextArea textarea { background: #222; color: #fff; }
    .stButton>button { background: #4e54c8; color: #fff; border-radius: 8px; }
    .stSelectbox>div>div>div { background: #222; color: #fff; }
    .stSlider>div>div>div { color: #fff; }
    .stMarkdown { color: #fff; }
    </style>
""", unsafe_allow_html=True)

# -------------------- Sidebar: Model & Params --------------------
st.sidebar.title("⚙️ Model Settings")
model_choice = st.sidebar.selectbox(
    "Choose Language Model",
    options=["gemma:2b (Ollama)", "GPT-3 (OpenAI)", "GPT-4 (OpenAI)"],
    index=0
)
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.05)
max_tokens = st.sidebar.slider("Max Tokens", 32, 1024, 256, 8)
st.sidebar.markdown("---")
st.sidebar.info("Tip: gemma:2b runs locally via Ollama. GPT-3/4 require OpenAI API key.")

# -------------------- Session State for Input/Output --------------------
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "response" not in st.session_state:
    st.session_state.response = ""
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------- App Title & Description --------------------
st.title("🤖 GenAI Chat App")
st.markdown("""
Welcome to the GenAI Chat App!  
Ask any question and get answers from advanced language models.  
- **Supports:** gemma:2b (local), GPT-3, GPT-4 (OpenAI)
- **Adjust creativity and length with temperature & max tokens.**
""")

# -------------------- User Input Form --------------------
with st.form(key="input_form"):
    user_input = st.text_area("Enter your question or prompt:", value=st.session_state.user_input, height=100)
    col1, col2 = st.columns([1,1])
    with col1:
        submit_btn = st.form_submit_button("Submit")
    with col2:
        clear_btn = st.form_submit_button("Clear")

# -------------------- Clear Button Logic --------------------
if clear_btn:
    st.session_state.user_input = ""
    st.session_state.response = ""
    st.session_state.history = []
    st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

# -------------------- Model Selection & LLM Setup --------------------
def get_llm(model_choice, temperature, max_tokens):
    if model_choice.startswith("gemma"):
        # Use Ollama's gemma:2b model (local)
        return Ollama(
            model="gemma:2b",
            temperature=temperature
            # max_tokens is NOT a valid argument for Ollama
        )
    elif model_choice.startswith("GPT-3"):
        # Use OpenAI GPT-3 (requires API key)
        return OpenAI(
            model_name="gpt-3.5-turbo",
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif model_choice.startswith("GPT-4"):
        # Use OpenAI GPT-4 (requires API key)
        return OpenAI(
            model_name="gpt-4",
            temperature=temperature,
            max_tokens=max_tokens
        )
    else:
        raise ValueError("Invalid model selection.")

# -------------------------------------------------------------
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful AI assistant. Answer the following question:\n\n{question}"
)

# -------------------- Submit Button Logic --------------------
if submit_btn:
    if not user_input.strip():
        st.warning("Please enter a question or prompt.")
    else:
        try:
            llm = get_llm(model_choice, temperature, max_tokens)
            chain = LLMChain(llm=llm, prompt=prompt_template)
            with st.spinner("Generating response..."):
                response = chain.run({"question": user_input})
            st.session_state.response = response
            st.session_state.user_input = user_input
            st.session_state.history.append({"question": user_input, "answer": response})
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.response = ""

# -------------------- Display Model's Response --------------------
if st.session_state.response:
    st.markdown("#### 📝 Model's Response")
    st.success(st.session_state.response)

# -------------------- Conversation History --------------------
if st.session_state.history:
    with st.expander("Show Conversation History"):
        for idx, turn in enumerate(st.session_state.history[::-1], 1):
            st.markdown(f"**Q{idx}:** {turn['question']}")
            st.markdown(f"**A{idx}:** {turn['answer']}")

# -------------------- Footer --------------------
st.markdown("""
---
<div style='text-align:center; color:#aaa;'>
    <small>
        Powered by <b>LangChain</b>, <b>Streamlit</b>, and <b>Ollama gemma:2b</b>.<br>
        For educational use. <br>
        <i>Tip: gemma:2b runs locally. For GPT-3/4, set your OpenAI API key as OPENAI_API_KEY env variable.</i>
    </small>
</div>
""", unsafe_allow_html=True)