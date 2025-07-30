from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .responses import RESPONSES, DEFAULT_RESPONSE

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "").lower()

        matched_responses = []
        for keyword, response in RESPONSES.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', user_input):
                if response not in matched_responses:
                    matched_responses.append(response)

        if matched_responses:
            return JsonResponse({"response": " ".join(matched_responses)})
        return JsonResponse({"response": DEFAULT_RESPONSE})
    
    return JsonResponse({"error": "Invalid request"}, status=400)
