from django.conf import settings
from django.shortcuts import redirect, render
from google import genai

from .models import ChatMessage

client = genai.Client(api_key=settings.GEMINI_API_KEY)
MODEL_NAME = "gemini-3.8-flash"

def clear_messages(request):
    if request.method == "POST":
        ChatMessage.objects.all().delete()
    return redirect("list_messages")

def send_message(request):
    if request.method == "POST":
        user_message = request.POST.get("user_message", "").strip()
        if user_message:
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=user_message,
                )
                bot_text = response.text
            except Exception as e:
                bot_text = f"Sorry, something went wrong: {e}"

            ChatMessage.objects.create(
                user_message=user_message,
                bot_response=bot_text,
            )
    return redirect("list_messages")


def list_messages(request):
    chat_messages = ChatMessage.objects.all().order_by("created_at")
    return render(request, "chatbot/list_messages.html", {"chat_messages": chat_messages})
