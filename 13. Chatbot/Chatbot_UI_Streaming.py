import streamlit as st
from Chatbot_Backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

# *************** Utility Functions ****************
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def restore_thread(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id': thread_id}}).values['messages']

#*********** Session Setup *****************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

# ****************** Sidebar UI *********************************
st.sidebar.title('LangGraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My Conversations')
for thread in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread)):
        st.session_state['thread_id'] = thread
        messages = restore_thread(thread)

        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role='ai'
            temp_messages.append({'role': role, 'content': message.content})
        st.session_state['message_history'] = temp_messages





# ****************** Main UI *************************************

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

chat_input = st.chat_input('Type Here')

if chat_input:
    st.session_state['message_history'].append({'role':'user', 'content': chat_input})
    with st.chat_message('user'):
        st.text(chat_input)

    CONFIG = {"configurable":{"thread_id":st.session_state['thread_id']}}

    with st.chat_message('ai'):
        ai_message = st.write_stream(
            message_chunk for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=chat_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role':'ai','content':ai_message})