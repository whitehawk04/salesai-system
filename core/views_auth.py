"""
Authentication views - Login, Registration, and User Management
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json
from datetime import datetime

from core.models import User, Company, Subscription


@csrf_exempt
def register_company(request):
    """Register a new company with initial admin user"""
    if request.method == 'GET':
        return render(request, 'register_company.html')
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Company information
        company_name = data.get('company_name')
        company_email = data.get('company_email')
        company_phone = data.get('company_phone')
        company_address = data.get('company_address')
        tin = data.get('tin')  # Tax ID
        business_type = data.get('business_type')
        
        # Admin user information
        admin_name = data.get('admin_name')
        admin_email = data.get('admin_email')
        admin_password = data.get('admin_password')
        admin_phone = data.get('admin_phone')
        
        # Validation
        if not all([company_name, company_email, admin_name, admin_email, admin_password]):
            return JsonResponse({
                'error': 'Missing required fields',
                'required': ['company_name', 'company_email', 'admin_name', 'admin_email', 'admin_password']
            }, status=400)
        
        # Check if email already exists
        if User.email_exists(admin_email):
            return JsonResponse({
                'error': 'Email already registered',
                'message': 'This email address is already in use'
            }, status=400)
        
        # Generate IDs
        company_id = f"COMP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        user_id = f"USER-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        subscription_id = f"SUB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create company
        company = Company.create(
            company_id=company_id,
            name=company_name,
            email=company_email,
            phone=company_phone or '',
            address=company_address or '',
            tin=tin,
            business_type=business_type,
            contact_person=admin_name
        )
        
        # Create subscription with trial
        subscription = Subscription.create(
            subscription_id=subscription_id,
            company_id=company_id,
            billing_email=company_email,
            trial_enabled=True
        )
        
        # Create admin user
        user = User.create(
            user_id=user_id,
            email=admin_email,
            password=admin_password,
            role=User.ROLE_COMPANY_ADMIN,
            company_id=company_id,
            name=admin_name,
            phone=admin_phone
        )
        
        # Set session
        request.session['user_id'] = user_id
        
        return JsonResponse({
            'success': True,
            'message': 'Company registered successfully',
            'company_id': company_id,
            'user_id': user_id,
            'trial_days': Subscription.TRIAL_DAYS,
            'api_token': user.get('api_token')
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Registration failed',
            'message': str(e)
        }, status=400)


@csrf_exempt
def login(request):
    """User login"""
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({
                'error': 'Missing credentials',
                'required': ['email', 'password']
            }, status=400)
        
        # Authenticate user
        user = User.authenticate(email, password)
        
        if not user:
            return JsonResponse({
                'error': 'Invalid credentials',
                'message': 'Email or password is incorrect'
            }, status=401)
        
        # Set session
        request.session['user_id'] = user['_id']
        
        # Get company info
        company = None
        if user.get('company_id'):
            company = Company.get(user['company_id'])
        
        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['_id'],
                'email': user['email'],
                'name': user.get('name'),
                'role': user['role'],
                'company_id': user.get('company_id')
            },
            'company': {
                'id': company['_id'],
                'name': company['name']
            } if company else None,
            'api_token': user.get('api_token')
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Login failed',
            'message': str(e)
        }, status=400)


@csrf_exempt
def logout(request):
    """User logout"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Clear session
    request.session.flush()
    
    return JsonResponse({
        'success': True,
        'message': 'Logged out successfully'
    })


@csrf_exempt
def get_current_user(request):
    """Get current logged-in user information"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    user = request.user
    
    # Get company info
    company = None
    if user.get('company_id'):
        company = Company.get(user['company_id'])
    
    # Get subscription info
    subscription = None
    if user.get('company_id'):
        subscription = Subscription.get_by_company(user['company_id'])
    
    return JsonResponse({
        'user': {
            'id': user['_id'],
            'email': user['email'],
            'name': user.get('name'),
            'role': user['role'],
            'company_id': user.get('company_id'),
            'phone': user.get('phone')
        },
        'company': {
            'id': company['_id'],
            'name': company['name'],
            'email': company['email'],
            'status': company.get('status')
        } if company else None,
        'subscription': {
            'status': subscription.get('status'),
            'trial_end_date': subscription.get('trial_end_date').isoformat() if subscription.get('trial_end_date') else None,
            'agent_count': subscription.get('current_agent_count'),
            'price_per_agent': subscription.get('price_per_agent')
        } if subscription else None
    })


@csrf_exempt
def change_password(request):
    """Change user password"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return JsonResponse({
                'error': 'Missing required fields',
                'required': ['old_password', 'new_password']
            }, status=400)
        
        user_id = request.user['_id']
        success = User.change_password(user_id, old_password, new_password)
        
        if not success:
            return JsonResponse({
                'error': 'Password change failed',
                'message': 'Current password is incorrect'
            }, status=400)
        
        return JsonResponse({
            'success': True,
            'message': 'Password changed successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Password change failed',
            'message': str(e)
        }, status=400)


@csrf_exempt
def create_user(request):
    """Create a new user for the company (admin only)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    # Check if user is company admin
    if request.user.get('role') not in [User.ROLE_COMPANY_ADMIN, User.ROLE_SUPER_ADMIN]:
        return JsonResponse({
            'error': 'Insufficient permissions',
            'message': 'Only company admins can create users'
        }, status=403)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        name = data.get('name')
        phone = data.get('phone')
        related_id = data.get('related_id')  # agent_id, manager_id, etc.
        
        if not all([email, password, role, name]):
            return JsonResponse({
                'error': 'Missing required fields',
                'required': ['email', 'password', 'role', 'name']
            }, status=400)
        
        # Check if email already exists
        if User.email_exists(email):
            return JsonResponse({
                'error': 'Email already exists',
                'message': 'This email address is already in use'
            }, status=400)
        
        # Validate role
        valid_roles = [User.ROLE_AGENT, User.ROLE_AREA_MANAGER, User.ROLE_DIVISION_HEAD, User.ROLE_COMPANY_ADMIN]
        if role not in valid_roles:
            return JsonResponse({
                'error': 'Invalid role',
                'valid_roles': valid_roles
            }, status=400)
        
        company_id = request.user.get('company_id')
        user_id = f"USER-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        user = User.create(
            user_id=user_id,
            email=email,
            password=password,
            role=role,
            company_id=company_id,
            name=name,
            phone=phone,
            related_id=related_id
        )
        
        return JsonResponse({
            'success': True,
            'message': 'User created successfully',
            'user_id': user_id,
            'api_token': user.get('api_token')
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'error': 'User creation failed',
            'message': str(e)
        }, status=400)
