from ollama import chat
from ollama import ChatResponse

def AIResponse(ClientName, ClientSupportPlan):
    response: ChatResponse = chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': 'You are a care provider. Your patient is ' + ClientName + '. They are on the ' + ClientSupportPlan + ' support plan. You are required to provide service based on the agency policy'
        }
    ])
    return response