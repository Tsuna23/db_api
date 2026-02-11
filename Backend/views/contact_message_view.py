import threading
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email

def send_email_thread(mail):
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(mail)
    except Exception as e:
        print("Erreur envoi email SendGrid:", e)

@csrf_exempt
def send_contact_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"status": False, "message": "JSON invalide"}, status=400)

        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if not all([name, email, subject, message]):
            return JsonResponse({"status": False, "message": "Tous les champs sont obligatoires"}, status=400)

        full_message = f"De: {name} <{email}>\n\n{message}"

        mail = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=settings.DEFAULT_FROM_EMAIL,
            subject=f"Contact: {subject}",
            plain_text_content=full_message,
        )
        mail.reply_to = Email(email)

        # On envoie l'email dans un thread pour ne pas bloquer Gunicorn
        threading.Thread(target=send_email_thread, args=(mail,)).start()

        return JsonResponse({"status": True, "message": "Email en cours d’envoi."})

    return JsonResponse({"status": False, "message": "Méthode non autorisée"}, status=405)
