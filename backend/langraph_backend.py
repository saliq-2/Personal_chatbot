from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal,Annotated
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver,InMemorySaver


#state for the bot
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages] #basemessage ek superclasss hai system,human,tool ka jisne andr kuch bhi askata hai inme se ,addmessage zyda optimized hai then operator.add se


llm=ChatOllama(model='llama3.2')



def chat_node(state:ChatState):
    #take user query
    message=state['messages']
    #model invoke
    response=llm.invoke(message)
    #print(response)
    #resposnse ko store krna hai
    return {'messages':[response]}


checkpointer=InMemorySaver()

graph=StateGraph(ChatState)


#adding nodes to the graph

graph.add_node('chat_node',chat_node)

#connecting the graph

graph.add_edge(START,'chat_node')

graph.add_edge('chat_node',END)

mychat_bot=graph.compile(checkpointer=checkpointer)

