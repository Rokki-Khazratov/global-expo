from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

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
        return response 