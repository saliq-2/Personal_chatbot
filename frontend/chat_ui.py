import streamlit as st

from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage
import sys
import os


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


sys.path.insert(0, PROJECT_ROOT)
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

from backend.langraph_backend import mychat_bot
#session state

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

user_input=st.chat_input('Type')


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


if user_input:
    #first add the message to the list
    st.session_state['message_history'].append({'role':'user','content':user_input})


    with st.chat_message('user'):
        st.text(user_input)

    Output_llm=mychat_bot.invoke({'messages':[HumanMessage(content=user_input)]},config=CONFIG)
    message_ai=Output_llm['messages'][-1].content
    #firsr add the mesage to the conv history
    st.session_state['message_history'].append({'role':'assistant','content':message_ai})    
    with st.chat_message('assistant'):
        st.text(message_ai)    