from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    start: bool
    conversation: int
    question: str
    answer: str
    topic: bool
    documents: list
    recursion_limit: int #limit endless loops
    memory: list #conversation history
    continue_chat: bool 

# Connect to Pinecone
embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPEN_AI_KEY'],
    model='text-embedding-3-large')
vectorstore = PineconeVectorStore(index_name='mbochi-francais-dict', embedding=embeddings)

llm = ChatOpenAI(api_key=os.environ['OPEN_AI_KEY'], model='gpt-4o')

def check_question(state):
    question = state['question']

    system_prompt = """
        You are a Mbochi-French dictionary assistant.
        Your job is to assess if the user is asking for a translation
        or the meaning of a word or phrase related to the Mbochi or French language.
        If the question is about translating, finding a word, or its meaning — reply YES.
        If the question is completely unrelated to translation — reply NO.
        Reply with only one word: YES or NO.
    """


    TEMPLATE = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('human', '{question}'),])
    
    prompt = TEMPLATE.format(question = question)

    response_text = llm.invoke(prompt)

    print(f"LLM response: '{response_text.content}'") 

    state['topic'] = response_text.content.strip().upper() == 'YES'

    return state

def topic_router(state):
    topic = state['topic']
    print(f"topic value: '{topic}', type: {type(topic)}")

    if topic == True:
        return 'on_topic'
    else:
        return 'off_topic'

def off_topic(state):
    state['answer'] = 'I can only help with Mbochi-French translations.'
    print(state['answer'])
    return state

def retrieved_docs(state):
    conversation = "\n".join(state['memory'])

    #retrieve chunk from pinecone
    docs = vectorstore.similarity_search(conversation, k=10)

    #Store docs in state
    state['documents'] = [doc.page_content for doc in docs]

    return state

def generate_answer(state):
    question = state['question']
    documents = state['documents']
    memory = state['memory']

    system_prompt = """
        You are an translator tasked with translating customer questions.
        Answer the question, avoid being too verbose. And the questions
        will be in french.
    """

    TEMPLATE = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('human', "Context: {document}, \nConversation history: {memory},\nCustomer Question: {question}"),
        ])

    prompt = TEMPLATE.format(document=documents, memory=memory, question=question)

    response_text = llm.invoke(prompt)

    state['answer'] = response_text.content.strip()

    return state

def improve_answer(state):
    question = state['question']
    answer = state['answer']

    system_prompt = f"""
        based on the {question},
        Improve the answer.
        Make it clear and more concise. 
    """

    TEMPLATE = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('human', '{answer}'),])

    prompt = TEMPLATE.format(answer = answer)

    response_text = llm.invoke(prompt)

    state['answer'] = response_text.content.strip()
    state['memory'].append(response_text.content.strip())
    return state

workflow = StateGraph(AgentState)

workflow.add_node('check_question', check_question)
workflow.add_node('retrieved_docs', retrieved_docs)
workflow.add_node('off_topic_response', off_topic)
workflow.add_node('generate_answer', generate_answer)
workflow.add_node('improve_answer', improve_answer)

#Add an entry point
workflow.set_entry_point('check_question')

#Connecting the nodes (edges)
workflow.add_edge('retrieved_docs', 'generate_answer')
workflow.add_edge('generate_answer', 'improve_answer')
workflow.add_edge('improve_answer', END)
workflow.add_edge('off_topic_response', END)

#Conditional edge
workflow.add_conditional_edges(
    'check_question',
    topic_router,
    {
        'on_topic': 'retrieved_docs',
        'off_topic': 'off_topic_response'
    }
)

app = workflow.compile()
