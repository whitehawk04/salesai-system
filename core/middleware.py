"""
Middleware for authentication and multi-tenancy
"""
from django.http import JsonResponse
from django.shortcuts import redirect
from core.models import User, Subscription


class AuthenticationMiddleware:
    """Middleware to authenticate users via session or API token"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Public paths that don't require authentication
        public_paths = [
            '/',  # Landing page
            '/register/',
            '/login/',
            '/api/register/',
            '/api/login/',
            '/static/',
            '/setup-database/',
            '/check-data/',
        ]
        
        # Check if path is public
        is_public = any(request.path.startswith(path) for path in public_paths)
        
        if not is_public:
            # Try to authenticate via session
            user_id = request.session.get('user_id')
            if user_id:
                user = User.get(user_id)
                if user and user.get('is_active'):
                    request.user = user
                else:
                    request.user = None
            else:
                # Try to authenticate via API token
                auth_header = request.headers.get('Authorization')
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    user = User.authenticate_by_token(token)
                    request.user = user
                else:
                    request.user = None
            
            # If not authenticated, redirect to login or return 401
            if not request.user:
                # For API requests, return JSON 401
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'error': 'Authentication required',
                        'message': 'Please login to access this resource'
                    }, status=401)
                # For regular pages, redirect to login
                else:
                    return redirect('/login/')
        else:
            request.user = None
        
        response = self.get_response(request)
        return response


class SubscriptionMiddleware:
    """Middleware to check subscription status"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip for public paths and super admins
        public_paths = [
            '/',  # Landing page
            '/register/',
            '/login/',
            '/api/register/',
            '/api/login/',
            '/static/',
            '/admin/',
            '/subscription/manage/',
            '/subscription/payment/',
            '/setup-database/',
            '/check-data/',
        ]
        
        is_public = any(request.path.startswith(path) for path in public_paths)
        
        if not is_public and hasattr(request, 'user') and request.user:
            user = request.user
            
            # Super admin bypass
            if user.get('role') == User.ROLE_SUPER_ADMIN:
                response = self.get_response(request)
                return response
            
            # Check company subscription
            company_id = user.get('company_id')
            if company_id:
                if not Subscription.is_active(company_id):
                    return JsonResponse({
                        'error': 'Subscription inactive',
                        'message': 'Your company subscription is not active. Please contact your administrator.',
                        'subscription_url': '/subscription/manage/'
                    }, status=403)
        
        response = self.get_response(request)
        return response


class MultiTenantMiddleware:
    """Middleware to enforce multi-tenant data isolation"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add company_id to request if user is authenticated
        if hasattr(request, 'user') and request.user:
            company_id = request.user.get('company_id')
            request.company_id = company_id
        else:
            request.company_id = None
        
        response = self.get_response(request)
        return response


def require_role(required_role):
    """Decorator to require a specific role"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'user') or not request.user:
                return JsonResponse({
                    'error': 'Authentication required'
                }, status=401)
            
            if not User.has_permission(request.user, required_role):
                return JsonResponse({
                    'error': 'Insufficient permissions',
                    'message': f'This action requires {required_role} role or higher'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_company_access(view_func):
    """Decorator to ensure user can access company data"""
    def wrapper(request, company_id=None, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user:
            return JsonResponse({
                'error': 'Authentication required'
            }, status=401)
        
        # If company_id is in URL params
        if company_id and not User.can_access_company(request.user, company_id):
            return JsonResponse({
                'error': 'Access denied',
                'message': 'You do not have access to this company data'
            }, status=403)
        
        return view_func(request, company_id=company_id, *args, **kwargs)
    return wrapper
