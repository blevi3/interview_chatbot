from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import openai
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def chat_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        persona = "Hello! I'm your dedicated interview preparation assistant. My goal is to help you ace your upcoming interviews by providing valuable insights, tips, and practice scenarios. Whether you're preparing for technical questions, behavioral interviews, or just need general advice, I'm here to support you every step of the way. Let's work together to boost your confidence and land that dream job!"

        initial_context = f"{persona}\nUser: {user_message}\nAssistant:"
        
        client = OpenAI(
        api_key='sk-proj-1SIbGYYqAs0OORkrF30zT3BlbkFJTfZGVacC1SCpMmkyxFZB',  
        )        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": [{
                        "type": "text",
                        "text": persona
                }]
                },
                {
                    "role": "user",
                    "content":  [{
                        "type": "text",
                        "text": user_message
                }]
                }
            ],
            model="gpt-3.5-turbo",
)
        bot_message = response.choices[0].message['content']
        
        return JsonResponse({'message': bot_message})
    if request.method == 'GET':
        return render(request, 'chat.html')
    return JsonResponse({'error': 'Invalid request'}, status=400)
