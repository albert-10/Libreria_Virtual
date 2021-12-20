from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.conf import settings

# El siguiente middleware redirigira al usuario, cuando haya un error, hacia una pagina, donde
# se muestra un mensaje relacionado al error

class Middleware_Manejador_Errores:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        
        if not settings.DEBUG:            
            if isinstance(exception, PermissionDenied):
                return render(request,'permisosDenegados.html')
            return render(request,'errorInesperado.html', {'exception': exception})
        