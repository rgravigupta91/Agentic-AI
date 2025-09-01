import streamlit as st
from Chatbot_Backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable":{"thread_id":"thread-1"}}
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

chat_input = st.chat_input('Type Here')

if chat_input:
    st.session_state['message_history'].append({'role':'user', 'content': chat_input})
    with st.chat_message('user'):
        st.text(chat_input)

    with st.chat_message('ai'):
        ai_message = st.write_stream(
            message_chunk for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=chat_input)]},
                config= {'configurable': {'thread_id':'thread-1'}},
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role':'ai','content':ai_message})