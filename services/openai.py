from openai import OpenAI
from dotenv import load_dotenv
from config.img_encoder import image_encoder
import os 

load_dotenv()

client = OpenAI(api_key=os.environ['OPEN_AI_KEY'])

MODEL = 'gpt-5.2'
TOPIC = "Few shot prompting and include the data of the image"
INPUT = """
Your task is to write a linkedin post to showcase to the networks
the efforts you have been taking to improve your skills in AI

write a linkedin post about the latest course I am taking
on RAG by Diogo Resende. 

Highlight the awesome Prompt Engineering techniques where I am 
10x my outputs. 

Start with a provocative hook. 

Paragraph are 1 sentence only and short. 
"""
INSTRUCTIONS = """
    You are a Founder
    Your persona is friendly, funny with an acid humor

    Your goal is to engage with the Linkedin audience.
"""
def generate_post():
    response = client.responses.create(
        model = MODEL,
        input=INPUT,
        reasoning={
            'effort': 'xhigh'
        },
        text = {
            'verbosity': 'high'
        },
        instructions = INSTRUCTIONS
    )

    return response.output_text

def describe_image_gpt(url):
    response = client.responses.create(
        model = MODEL,
        input = [
            {
                'role': 'user', 
                'content': [
                    {
                        'type': 'input_text', 'text': 'Describe the image'
                    },
                    {
                        'type': 'input_image', 'image_url': url
                    }
                ]
            }
        ]
    )

    return response.output_text

def describe_image_b64(file_name: str):
    encoded = image_encoder(file_name)
    response = client.responses.create(
        model = MODEL,
        input = [
            {
                'role': 'user', 
                'content': [
                    {
                        'type': 'input_text', 'text': INPUT
                    },
                    {
                        'type': 'input_image', 'image_url': f"data:image/jpeg;base64,{encoded}"
                    }
                ]
            }
        ],
        instructions = INSTRUCTIONS
    )

    return response.output_text