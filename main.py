import streamlit as st
from process import explain_code, debug_code
import io

st.set_page_config(layout="wide", page_title="AI Code Explainer and Debugger", page_icon="💻")

# Custom CSS for styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    body {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    
    .main .block-container {
        padding-top: 4rem;
        padding-bottom: 3rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    .stButton > button {
        background-color: #00FF00 !important;
        color: #000000 !important;
    }
    
    .typewriter {
        overflow: hidden;
        border-right: .15em solid #00FF00;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        animation: 
            typing 3.5s steps(40, end),
            blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #00FF00; }
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Controls")
    
    # New Chat button
    if st.button("New Chat ➕", help="Start a new chat"):
        st.session_state.messages = []
        st.session_state.code_to_process = None  # Reset code_to_process
        st.rerun()
    
    # Add file uploader
    uploaded_file = st.file_uploader("Upload a code file here...📁", type=["py", "js", "java", "cpp","html", "txt"])

    # Determine the language based on file extension or user selection
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        language_map = {
            "py": "Python",
            "js": "JavaScript",
            "java": "Java",
            "cpp": "C++",
            "html": "HTML",
            "txt": "Text"
        }
        language = language_map.get(file_extension, "Other")
    else:
        language = st.selectbox("Programming Language:", ["Python", "JavaScript", "Java", "C++", "HTML", "Text", "Other"])

    if language == "Other":
        language = st.text_input("Specify the language:")

    action = st.radio("Choose action:", ("Explain Code", "Debug Code"))
    button = st.button("Process Code")

# Title with typewriter animation
st.html("<h1 class='typewriter' style='color: #00FF00;'>C:|AI_Code_Explainer_and_Debugger👨🏻‍💻></h1>")

# Initialize chat history and code_to_process in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "code_to_process" not in st.session_state:
    st.session_state.code_to_process = None

# Code input section
code_input = st.text_area("Write your code here...⌨️", height=300)

if button:
    # Determine which code to process
    if uploaded_file is not None:
        # Read the contents of the uploaded file
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.session_state.code_to_process = stringio.read()
    elif code_input:
        st.session_state.code_to_process = code_input
    else:
        st.error("Please either upload a file or enter code manually.")
        st.stop()

    user_message = f"Please {action.lower()} the following {language} code:\n\n```{language.lower()}\n{st.session_state.code_to_process}\n```"
    # st.session_state.messages.append({"role": "user", "content": user_message})
    
    if action == "Explain Code":
        response_stream = explain_code(st.session_state.code_to_process, language)
    else:
        response_stream = debug_code(st.session_state.code_to_process, language)
    
    response = ""
    message_placeholder = st.empty()
    for chunk in response_stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
            message_placeholder.markdown(response + "▌", unsafe_allow_html=True)
    message_placeholder.markdown(response, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
# prompt = st.chat_input("Ask a question about the code or request further explanation:")

# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt, unsafe_allow_html=True)

#     with st.chat_message("assistant"):
#         if st.session_state.code_to_process is not None:
#             response_stream = explain_code(st.session_state.code_to_process, language, st.session_state.messages)
#             response = ""
#             message_placeholder = st.empty()
#             for chunk in response_stream:
#                 if chunk.choices[0].delta.content is not None:
#                     response += chunk.choices[0].delta.content
#                     message_placeholder.markdown(response + "▌", unsafe_allow_html=True)
#             message_placeholder.markdown(response, unsafe_allow_html=True)
#         else:
#             response = "Sorry, there's no code to process. Please upload or enter some code first."
#             st.markdown(response)
    
#     st.session_state.messages.append({"role": "assistant", "content": response})






#---------------------------------------------------------------------------------------#


