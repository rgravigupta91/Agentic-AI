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
    
    response = chatbot.invoke({'messages':[HumanMessage(content=chat_input)]}, config=CONFIG)
    ai_message = response['messages'][-1].content
    st.session_state['message_history'].append({'role':'ai', 'content': ai_message})
    with st.chat_message('ai'):
        st.text(ai_message)

