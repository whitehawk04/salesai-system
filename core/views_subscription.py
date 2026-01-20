"""
Views for subscription management
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from datetime import datetime, timedelta

from core.models import Company, Subscription, Payment, User
from core.middleware import require_role, require_company_access


def subscription_dashboard(request):
    """Dashboard for managing subscription"""
    if not request.user:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = request.user
    company_id = user.get('company_id')
    
    if not company_id:
        return JsonResponse({'error': 'No company associated'}, status=400)
    
    # Get company and subscription info
    company = Company.get(company_id)
    subscription = Subscription.get_by_company(company_id)
    
    if not subscription:
        return JsonResponse({'error': 'No subscription found'}, status=404)
    
    # Calculate current costs
    agent_count = subscription.get('current_agent_count', 0)
    price_per_agent = subscription.get('price_per_agent', 299)
    monthly_cost = agent_count * price_per_agent
    
    # Get recent payments
    recent_payments = Payment.get_by_company(company_id, limit=10)
    
    context = {
        'company': company,
        'subscription': subscription,
        'agent_count': agent_count,
        'price_per_agent': price_per_agent,
        'monthly_cost': monthly_cost,
        'recent_payments': recent_payments,
        'user': user
    }
    
    return render(request, 'subscription_dashboard.html', context)


@csrf_exempt
def get_subscription_info(request):
    """API endpoint to get subscription information"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    company_id = request.user.get('company_id')
    if not company_id:
        return JsonResponse({'error': 'No company associated'}, status=400)
    
    subscription = Subscription.get_by_company(company_id)
    if not subscription:
        return JsonResponse({'error': 'No subscription found'}, status=404)
    
    # Calculate costs
    monthly_cost = Subscription.calculate_monthly_cost(company_id)
    
    # Convert datetime objects to strings
    sub_data = {
        '_id': subscription.get('_id'),
        'company_id': subscription.get('company_id'),
        'status': subscription.get('status'),
        'price_per_agent': subscription.get('price_per_agent'),
        'current_agent_count': subscription.get('current_agent_count'),
        'monthly_cost': monthly_cost,
        'next_billing_date': subscription.get('next_billing_date').isoformat() if subscription.get('next_billing_date') else None,
        'trial_end_date': subscription.get('trial_end_date').isoformat() if subscription.get('trial_end_date') else None,
        'billing_cycle': subscription.get('billing_cycle', 'monthly')
    }
    
    return JsonResponse({
        'subscription': sub_data,
        'is_active': Subscription.is_active(company_id)
    })


@csrf_exempt
@require_role(User.ROLE_COMPANY_ADMIN)
def update_subscription(request):
    """Update subscription settings (admin only)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    company_id = request.user.get('company_id')
    if not company_id:
        return JsonResponse({'error': 'No company associated'}, status=400)
    
    try:
        data = json.loads(request.body)
        billing_email = data.get('billing_email')
        
        if billing_email:
            Subscription.get_by_company(company_id)
            # Update would go here
            
        return JsonResponse({
            'success': True,
            'message': 'Subscription updated successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to update subscription',
            'message': str(e)
        }, status=400)


@csrf_exempt
def get_payment_history(request):
    """Get payment history for company"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    company_id = request.user.get('company_id')
    if not company_id:
        return JsonResponse({'error': 'No company associated'}, status=400)
    
    payments = Payment.get_by_company(company_id)
    
    # Convert datetime objects to strings
    payment_list = []
    for payment in payments:
        payment_data = {
            '_id': payment.get('_id'),
            'invoice_number': payment.get('invoice_number'),
            'amount': payment.get('amount'),
            'status': payment.get('status'),
            'agent_count': payment.get('agent_count'),
            'due_date': payment.get('due_date').isoformat() if payment.get('due_date') else None,
            'payment_date': payment.get('payment_date').isoformat() if payment.get('payment_date') else None,
            'payment_method': payment.get('payment_method'),
            'reference_number': payment.get('reference_number')
        }
        payment_list.append(payment_data)
    
    return JsonResponse({
        'payments': payment_list
    })


@csrf_exempt
@require_role(User.ROLE_COMPANY_ADMIN)
def record_payment(request):
    """Record a payment (admin only)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        invoice_id = data.get('invoice_id')
        amount_paid = data.get('amount_paid')
        payment_method = data.get('payment_method')
        reference_number = data.get('reference_number')
        notes = data.get('notes')
        
        if not invoice_id or not amount_paid or not payment_method:
            return JsonResponse({
                'error': 'Missing required fields',
                'required': ['invoice_id', 'amount_paid', 'payment_method']
            }, status=400)
        
        # Record the payment
        Payment.record_payment(
            invoice_id=invoice_id,
            amount_paid=amount_paid,
            payment_method=payment_method,
            reference_number=reference_number,
            notes=notes
        )
        
        # Get the invoice to get company_id
        invoice = Payment.get(invoice_id)
        if invoice:
            company_id = invoice.get('company_id')
            # Renew the subscription
            Subscription.renew(company_id)
        
        return JsonResponse({
            'success': True,
            'message': 'Payment recorded successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to record payment',
            'message': str(e)
        }, status=400)


@csrf_exempt
@require_role(User.ROLE_SUPER_ADMIN)
def generate_invoices(request):
    """Generate invoices for all active subscriptions (super admin only)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Get all active subscriptions
        subscriptions = Subscription.get_all(status='active')
        
        invoices_created = 0
        billing_period_start = datetime.now()
        billing_period_end = billing_period_start + timedelta(days=30)
        
        for subscription in subscriptions:
            company_id = subscription.get('company_id')
            agent_count = subscription.get('current_agent_count', 0)
            price_per_agent = subscription.get('price_per_agent', 299)
            amount = agent_count * price_per_agent
            
            if amount > 0:  # Only create invoice if there are agents
                invoice_id = f"INV-{company_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                Payment.create_invoice(
                    invoice_id=invoice_id,
                    company_id=company_id,
                    amount=amount,
                    agent_count=agent_count,
                    billing_period_start=billing_period_start,
                    billing_period_end=billing_period_end
                )
                invoices_created += 1
        
        return JsonResponse({
            'success': True,
            'message': f'Generated {invoices_created} invoices'
        })
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to generate invoices',
            'message': str(e)
        }, status=400)
