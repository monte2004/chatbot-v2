from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
import json

# ✅ Render chatbot page
def chatbot_page(request):
    return render(request, 'chatbot/chat.html')

# ✅ Handle incoming chat messages (still stores messages)
def chatbot_api(request):
    user_message = request.GET.get('message', '')
    if user_message:
        ChatMessage.objects.create(sender='user', message=user_message)
        return JsonResponse({'reply': 'Bot reply disabled for now.'})

    return JsonResponse({'reply': "No message received."})

# ✅ Handle complaint submissions
@csrf_exempt
def submit_complaint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            complaint = data.get('complaint')

            if not complaint:
                return JsonResponse({'success': False, 'message': 'Empty complaint'}, status=400)

            send_mail(
                subject='FreshMart Complaint Received',
                message=f"Complaint:\n\n{complaint}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['montebackuppp@gmail.com'],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'Complaint sent successfully'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
