from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that don't require authentication
        public_urls = [reverse('login')]
        
        # Check if user is authenticated
        if not request.user.is_authenticated and request.path not in public_urls:
            return redirect('login')
            
        response = self.get_response(request)
        return response 