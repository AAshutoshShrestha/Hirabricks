from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import ContactForm
from .models import ContactMessage

def main(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            homepage_C_name = request.POST.get('name')
            homepage_C_email = request.POST.get('email')
            homepage_C_message = request.POST.get('message')
            Bform = ContactMessage.objects.create(
                name=homepage_C_name,
                email=homepage_C_email,
                message=homepage_C_message,
                created_at=timezone.now(),
            )
            Bform.save()
            messages.success(request, 'Your message has been sent successfully!')  # Sending success message
    else:
        form = ContactForm()
    context = {
    }
    return render(request, 'Main/home.html', context)