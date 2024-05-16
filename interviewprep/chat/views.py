from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import random
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login
from .forms import NewUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from PyPDF2 import PdfReader
import io
from .models import Message, Conversation

def index(request):
    return render(request, 'index.html')
@login_required
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        file = request.FILES.get('file')
        conversation_id = request.POST.get('conversation_id')

        if file:
            reader = PdfReader(io.BytesIO(file.read()))
            number_of_pages = len(reader.pages)
            pdf_text = ''
            for page in range(number_of_pages):
                pdf_text += reader.pages[page].extract_text()
            user_message += "the content of the pdf is:\n\n"
            user_message += pdf_text
            print(user_message)

            
        persona = ("Hello! I'm your dedicated interview preparation assistant. "
                   "My goal is to help you ace your upcoming interviews by providing valuable insights, "
                   "tips, and practice scenarios. Whether you're preparing for technical questions, "
                   "behavioral interviews, or just need general advice, I'm here to support you every step of the way. "
                   "Let's work together to boost your confidence and land that dream job!")


        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": persona},
                    {"role": "user", "content": user_message}
                ],
                model="gpt-3.5-turbo",
            )
            bot_message = response.choices[0].message['content']
        except Exception as e:
            random_responses = [
                "I'm sorry, I couldn't process your request at the moment.",
                "It seems there was an issue. Let's try again later.",
                "Hmm, something went wrong. Let me think...",
                "Apologies, my circuits seem to be a bit fuzzy right now.",
                "Looks like there's a glitch in the matrix. Please stand by."
            ]
            bot_message = random.choice(random_responses)

        # Create or get the conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        else:
            title = name_conversation(user_message)
            conversation = Conversation.objects.create(user=request.user, title=title)

        Message.objects.create(conversation=conversation, role='user', content=user_message)
        Message.objects.create(conversation=conversation, role='bot', content=bot_message)

        return JsonResponse({'message': bot_message, 'conversation_id': conversation.id})

    if request.method == 'GET':
        conversation_id = request.GET.get('conversation_id')
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            messages = conversation.messages.all().order_by('timestamp')
        else:
            conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
            return render(request, 'chat.html', {'conversations': conversations})

        return render(request, 'chat.html', {'messages': messages, 'conversation_id': conversation_id})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def name_conversation(first_message):
    persona = ("Hello! I'm your dedicated conversation namer. My goal is to come up with catchy and meaningful titles for our chats based on the content of your initial message. All the names I generate are related to an interview preperation theme.")


    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": first_message}
            ],
            model="gpt-3.5-turbo",
        )
    except Exception as e:
        return "Conversation"+ str(Conversation.objects.count() + 1)
    return response.choices[0].message['content']







def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if not User.objects.filter(username=request.POST.get("username")).exists():
            if not User.objects.filter(email=request.POST.get("email")).exists():
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    email = form.cleaned_data.get('email')
        
                    user = form.save()
                    messages.success(request, f'Account created for {username}!')
                                        
                    login(request, user)
                    messages.success(request, "Registration successful.")
                    return redirect("/api/chat/")
                else:
                    messages.error(request, "Password and confirm password do not match.")
                    return render(request, 'registration/register.html', {'register_form': form, 'uname': request.POST.get("username"), 'address': request.POST.get("email")})
            else:
                messages.error(request, "Email address already registered")
                return render(request, 'registration/register.html', {'register_form': form, 'uname': request.POST.get("username")})
        else:
            messages.error(request, "The username is occupied")
            return render(request, 'registration/register.html', {'register_form': form, 'address': request.POST.get("email")})
    else:
        form = NewUserForm()
    return render(request, template_name="registration/register.html", context={"register_form": form})
