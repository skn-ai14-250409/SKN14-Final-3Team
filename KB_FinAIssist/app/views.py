from django.shortcuts import render

# Create your views here.
def kb_finaissist(request) : 
    return render(request, 'html/main.html')