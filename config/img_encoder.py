import base64 
import os 

def image_encoder(file_name: str):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    return image_base64