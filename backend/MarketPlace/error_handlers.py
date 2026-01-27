# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import render
# from django.core.exceptions import ValidationError, PermissionDenied
# from django.db import IntegrityError
# from functools import wraps
# import logging

# logger = logging.getLogger(__name__)


# class ErrorHandlingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             response = self.get_response(request)
#             return response
#         except Exception as e:
#             logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
#             return self.handle_error(request, e)

#     def handle_error(self, request, exception):
#         if isinstance(exception, ValidationError):
#             return render(request, 'error/error.html', {
#                 'error_code': 400,
#                 'message': 'Invalid data provided.',
#                 'detail': str(exception)
#             }, status=400)
        
#         if isinstance(exception, PermissionDenied):
#             return render(request, 'error/error.html', {
#                 'error_code': 403,
#                 'message': 'You do not have permission to perform this action.',
#                 'detail': str(exception)
#             }, status=403)
        
#         if isinstance(exception, IntegrityError):
#             return render(request, 'error/error.html', {
#                 'error_code': 409,
#                 'message': 'Data conflict. This action cannot be completed.',
#                 'detail': 'The provided data conflicts with existing data.'
#             }, status=409)

#         return render(request, 'error/error.html', {
#             'error_code': 500,
#             'message': 'An internal server error occurred.',
#             'detail': 'Please try again later.'
#         }, status=500)


# def handle_exceptions(error_template='error/error.html'):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request, *args, **kwargs):
#             try:
#                 return view_func(request, *args, **kwargs)
#             except ValidationError as e:
#                 logger.warning(f"ValidationError in {view_func.__name__}: {str(e)}")
#                 return render(request, error_template, {
#                     'error_code': 400,
#                     'message': 'Invalid data provided.',
#                     'detail': str(e)
#                 }, status=400)
            
#             except PermissionDenied as e:
#                 logger.warning(f"PermissionDenied in {view_func.__name__}: {str(e)}")
#                 return render(request, error_template, {
#                     'error_code': 403,
#                     'message': 'Insufficient permissions.',
#                     'detail': str(e)
#                 }, status=403)
            
#             except IntegrityError as e:
#                 logger.error(f"IntegrityError in {view_func.__name__}: {str(e)}")
#                 return render(request, error_template, {
#                     'error_code': 409,
#                     'message': 'Data conflict.',
#                     'detail': 'The operation cannot be completed due to a conflict.'
#                 }, status=409)
            
#             except Exception as e:
#                 logger.error(f"Unexpected error in {view_func.__name__}: {str(e)}", exc_info=True)
#                 return render(request, error_template, {
#                     'error_code': 500,
#                     'message': 'Internal server error.',
#                     'detail': 'Please try again later.'
#                 }, status=500)
        
#         return wrapper
#     return decorator


# def require_premium(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return render(request, 'error/error.html', {
#                 'error_code': 401,
#                 'message': 'You must be logged in.',
#                 'detail': 'This action requires authentication.'
#             }, status=401)
        
#         if not hasattr(request.user, 'profile') or not request.user.profile.is_premium:
#             return render(request, 'error/error.html', {
#                 'error_code': 403,
#                 'message': 'Premium functionality required.',
#                 'detail': 'You need a premium account to access this functionality.'
#             }, status=403)
        
#         return view_func(request, *args, **kwargs)
    
#     return wrapper


# def api_error_response(error_code, message, detail=None):
#     response_data = {
#         'error': True,
#         'code': error_code,
#         'message': message
#     }
    
#     if detail:
#         response_data['detail'] = detail
    
#     return JsonResponse(response_data, status=error_code)


# def handle_product_not_found(request):
#     return render(request, 'error/error.html', {
#         'error_code': 404,
#         'message': 'Product not found.',
#         'detail': 'The product you are looking for does not exist or has been deleted.'
#     }, status=404)


# def handle_insufficient_permissions(request, required_permission=None):
#     detail = f'Se requiere: {required_permission}' if required_permission else None
#     return render(request, 'error/error.html', {
#         'error_code': 403,
#         'message': 'Insufficient permissions.',
#         'detail': detail
#     }, status=403)


# def handle_already_sold_product(request):
#     return render(request, 'error/error.html', {
#         'error_code': 409,
#         'message': 'Product not available.',
#         'detail': 'This product has already been sold.'
#     }, status=409)
