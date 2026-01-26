from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    """Middleware para manejo global de errores"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return self.handle_error(request, e)

    def handle_error(self, request, exception):
        """Maneja errores no capturados"""
        if isinstance(exception, ValidationError):
            return render(request, 'error/error.html', {
                'error_code': 400,
                'message': 'Datos inválidos proporcionados.',
                'detail': str(exception)
            }, status=400)
        
        if isinstance(exception, PermissionDenied):
            return render(request, 'error/error.html', {
                'error_code': 403,
                'message': 'No tienes permisos para realizar esta acción.',
                'detail': str(exception)
            }, status=403)
        
        if isinstance(exception, IntegrityError):
            return render(request, 'error/error.html', {
                'error_code': 409,
                'message': 'Conflicto de datos. Esta acción no se puede completar.',
                'detail': 'Los datos proporcionados entran en conflicto con los existentes.'
            }, status=409)

        # Error genérico del servidor
        return render(request, 'error/error.html', {
            'error_code': 500,
            'message': 'Ha ocurrido un error interno del servidor.',
            'detail': 'Por favor, inténtalo de nuevo más tarde.'
        }, status=500)


def handle_exceptions(error_template='error/error.html'):
    """Decorador para manejar excepciones en vistas"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except ValidationError as e:
                logger.warning(f"ValidationError in {view_func.__name__}: {str(e)}")
                return render(request, error_template, {
                    'error_code': 400,
                    'message': 'Datos inválidos.',
                    'detail': str(e)
                }, status=400)
            
            except PermissionDenied as e:
                logger.warning(f"PermissionDenied in {view_func.__name__}: {str(e)}")
                return render(request, error_template, {
                    'error_code': 403,
                    'message': 'Permisos insuficientes.',
                    'detail': str(e)
                }, status=403)
            
            except IntegrityError as e:
                logger.error(f"IntegrityError in {view_func.__name__}: {str(e)}")
                return render(request, error_template, {
                    'error_code': 409,
                    'message': 'Conflicto de datos.',
                    'detail': 'La operación no se puede completar debido a un conflicto.'
                }, status=409)
            
            except Exception as e:
                logger.error(f"Unexpected error in {view_func.__name__}: {str(e)}", exc_info=True)
                return render(request, error_template, {
                    'error_code': 500,
                    'message': 'Error interno del servidor.',
                    'detail': 'Por favor, inténtalo de nuevo más tarde.'
                }, status=500)
        
        return wrapper
    return decorator


def require_premium(view_func):
    """Decorador para requerir usuario premium"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'error/error.html', {
                'error_code': 401,
                'message': 'Debes iniciar sesión.',
                'detail': 'Esta acción requiere autenticación.'
            }, status=401)
        
        if not hasattr(request.user, 'profile') or not request.user.profile.is_premium:
            return render(request, 'error/error.html', {
                'error_code': 403,
                'message': 'Funcionalidad premium requerida.',
                'detail': 'Necesitas una cuenta premium para acceder a esta funcionalidad.'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def api_error_response(error_code, message, detail=None):
    """Genera respuestas de error consistentes para API"""
    response_data = {
        'error': True,
        'code': error_code,
        'message': message
    }
    
    if detail:
        response_data['detail'] = detail
    
    return JsonResponse(response_data, status=error_code)


# Funciones auxiliares para manejo de errores específicos
def handle_product_not_found(request):
    """Maneja cuando un producto no existe"""
    return render(request, 'error/error.html', {
        'error_code': 404,
        'message': 'Producto no encontrado.',
        'detail': 'El producto que buscas no existe o ha sido eliminado.'
    }, status=404)


def handle_insufficient_permissions(request, required_permission=None):
    """Maneja permisos insuficientes"""
    detail = f'Se requiere: {required_permission}' if required_permission else None
    return render(request, 'error/error.html', {
        'error_code': 403,
        'message': 'Permisos insuficientes.',
        'detail': detail
    }, status=403)


def handle_already_sold_product(request):
    """Maneja cuando se intenta comprar un producto ya vendido"""
    return render(request, 'error/error.html', {
        'error_code': 409,
        'message': 'Producto no disponible.',
        'detail': 'Este producto ya ha sido vendido.'
    }, status=409)
