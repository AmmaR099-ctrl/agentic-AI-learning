import json
import os
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

print("API key loaded:", "YES" if os.environ.get("GEMINI_API_KEY") else "NO")

_client = None

def get_client():
    global _client
    if _client is None:
        _client = genai.Client()
    return _client


def chat_view(request):
    return render(request, "chat.html")


@csrf_exempt
@require_POST
def ask_question(request):
    try:
        body = json.loads(request.body)
        message = body.get("message", "").strip()
        if not message:
            return JsonResponse({"error": "Message required"}, status=400)

        # --- History from Django session ---
        history = request.session.get("chat_history", [])

        # Build contents: full history + new user message
        contents = []
        for entry in history:
            contents.append({
                "role": entry["role"],          # 'user' or 'model'
                "parts": [{"text": entry["text"]}],
            })
        contents.append({
            "role": "user",
            "parts": [{"text": message}],
        })

        client = get_client()
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
        )

        reply_text = response.text

        # --- Save both turns to session ---
        history.append({"role": "user",  "text": message})
        history.append({"role": "model", "text": reply_text})
        request.session["chat_history"] = history
        request.session.modified = True

        return JsonResponse({
            "reply": reply_text,
            "history_turns": len(history),
        })

    except Exception as e:
        print(f"Gemini error: {e}")
        return JsonResponse({"error": str(e)}, status=500)