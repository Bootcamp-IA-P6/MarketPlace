from django.shortcuts import render
from django.conf import settings


def handler400(request, exception):
    """Maneja errores 400 - Bad Request"""
    # Si estamos en modo de errores personalizados o en producción
    if getattr(settings, 'SHOW_CUSTOM_ERRORS', False) or not settings.DEBUG:
        return render(request, '400.html', status=400)
    # En desarrollo, dejar que Django maneje el error normalmente
    return None


def handler403(request, exception):
    """Maneja errores 403 - Forbidden"""
    if getattr(settings, 'SHOW_CUSTOM_ERRORS', False) or not settings.DEBUG:
        return render(request, '403.html', status=403)
    return None


def handler404(request, exception):
    """Maneja errores 404 - Not Found"""
    if getattr(settings, 'SHOW_CUSTOM_ERRORS', False) or not settings.DEBUG:
        return render(request, '404.html', status=404)
    return None


def handler500(request):
    """Maneja errores 500 - Internal Server Error"""
    if getattr(settings, 'SHOW_CUSTOM_ERRORS', False) or not settings.DEBUG:
        return render(request, '500.html', status=500)
    return None
