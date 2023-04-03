from django.shortcuts import render

# Create your views here.

# Define the home view
def home(request):
  return render(request, 'welcome.html')
