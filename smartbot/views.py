from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .bot import LearningBot

bot = LearningBot()

@csrf_exempt
def chat_view(request):
    if request.method == "GET":
        return render(request, "chat.html")

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_input = data.get("message", "").strip()
            learning_response = data.get("learning_response", "").strip()

            if not user_input:
                return JsonResponse({"error": "No message provided"}, status=400)

            # If the user provides a learning response, save it
            if learning_response:
                response = bot.learn(user_input, learning_response)
                return JsonResponse({"response": response, "learn": False})

            # Otherwise, check if the bot knows the answer
            result = bot.ask(user_input)
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)
