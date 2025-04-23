from django.shortcuts import redirect, render
from django.urls import reverse, resolve, Resolver404
from django.conf import settings
from django.http import Http404

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that don't require authentication
        public_urls = [
            reverse('login'),
            '/admin/login/',  # Для доступа к админке
            '/static/',       # Для статических файлов
            '/media/',        # Для медиа файлов
        ]
        
        # Проверяем, является ли текущий URL публичным
        current_path = request.path_info
        is_public = any(current_path.startswith(url) for url in public_urls)
        
        # Если пользователь не аутентифицирован и URL не публичный
        if not request.user.is_authenticated and not is_public:
            return redirect('login')
            
        response = self.get_response(request)
        
        # Handle 404 errors
        if response.status_code == 404:
            try:
                # Try to resolve the URL to check if it's a valid path
                resolve(request.path_info)
            except Resolver404:
                # If URL can't be resolved, render custom 404 page
                return render(request, '404.html', status=404)
                
        return response 