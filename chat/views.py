from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .nlp_engine import ai_response
from .models import Message
from reportlab.pdfgen import canvas   # PDF export


# --- Load chat page + chat history ---
def chat_page(request):
    history = Message.objects.all()
    return render(request, 'chat/chat.html', {"history": history})


# --- Chat API handler ---
@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        # Save user message
        Message.objects.create(sender="user", text=user_message)

        # Bot reply
        bot_reply = ai_response(user_message)

        # Save bot reply
        Message.objects.create(sender="bot", text=bot_reply)

        return JsonResponse({"bot_reply": bot_reply})

    return JsonResponse({"error": "Invalid request"}, status=400)


# --- Clear chat history ---
@csrf_exempt   # <-- you missed this, required for JS POST
def clear_chat(request):
    if request.method == "POST":
        Message.objects.all().delete()
        return JsonResponse({"status": "cleared"})
    return JsonResponse({"error": "Only POST allowed"}, status=400)


# --- Export chat as .txt file ---
def export_txt(request):
    messages = Message.objects.all()
    content = ""

    for m in messages:
        content += f"{m.sender.upper()} ({m.timestamp.strftime('%I:%M %p')}): {m.text}\n"

    response = HttpResponse(content, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="chat_history.txt"'
    return response

# ----------- Export PDF (with wrapping)-----------
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def export_pdf(request):
    messages = Message.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="chat_history.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 50  # starting position

    max_width = 500  # text wrap width

    for m in messages:
        text = f"{m.sender.upper()} ({m.timestamp.strftime('%I:%M %p')}): {m.text}"

        # ⬇ wrap message automatically
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        style = getSampleStyleSheet()["Normal"]
        style.fontSize = 11

        para = Paragraph(text, style)
        w, h = para.wrap(max_width, y)

        if y - h < 50:  # next page if no space
            p.showPage()
            y = height - 50

        para.drawOn(p, 40, y - h)
        y -= (h + 12)

    p.save()
    return response
