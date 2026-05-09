from fastapi import APIRouter
from services.agent import app as agent_app
from uuid import uuid4

router = APIRouter()

sessions = {}

@router.post('/translate/start')
def start():
    session_id = str(uuid4())
    sessions[session_id] = {
        'start': True,
        'conversation': 0,
        'question': '',
        'answer': '',
        'topic': False,
        'documents': [],
        'memory': [],
        'continue_chat': True,
        'recursion_limit': 10
    }
    return {'session_id': session_id, 'message': 'Hello! Welcome to Mbochi-Francais dictionary. I will be your translator!'}

@router.post('/translate/{session_id}')
def translate(session_id: str, question: str):
    if session_id not in sessions:
        return {'error': 'Session not found. Start a new conversation at /translate/start'}
    
    state = sessions[session_id]
    state['question'] = question
    state['memory'].append(question)
    state['conversation'] += 1

    result = agent_app.invoke(state, config={'recursion_limit': 10})

    sessions[session_id] = result

    return {'answer': result['answer']}
