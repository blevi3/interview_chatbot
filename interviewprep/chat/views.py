from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import openai
from django.conf import settings
import random

def index(request):
    return render(request, 'index.html')

def chat_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        persona = "Hello! I'm your dedicated interview preparation assistant. My goal is to help you ace your upcoming interviews by providing valuable insights, tips, and practice scenarios. Whether you're preparing for technical questions, behavioral interviews, or just need general advice, I'm here to support you every step of the way. Let's work together to boost your confidence and land that dream job!"

        initial_context = f"{persona}\nUser: {user_message}\nAssistant:"
        
        client = OpenAI(
            api_key='sk-proj-1SIbGYYqAs0OORkrF30zT3BlbkFJTfZGVacC1SCpMmkyxFZB'
        )        
        
        try:
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
        except Exception as e:
            # If API call fails, generate a random response
            random_responses = [
                "I'm sorry, I couldn't process your request at the moment.",
                "It seems there was an issue. Let's try again later.",
                "Hmm, something went wrong. Let me think...",
                "Apologies, my circuits seem to be a bit fuzzy right now.",
                "Looks like there's a glitch in the matrix. Please stand by."
            ]
            bot_message = random.choice(random_responses)
        
        return JsonResponse({'message': bot_message})
    
    if request.method == 'GET':
        return render(request, 'chat.html')
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
