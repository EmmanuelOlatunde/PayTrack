from django.shortcuts import render, redirect
from .models import Payment, Member, MonthlyCollector
from django.db.models import Sum
from django.contrib import messages 
from django.db.models.functions import TruncMonth
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import MemberRegistrationForm



def logout_view(request):
    logout(request)
    return redirect('login')

@receiver(post_save, sender=User)
def create_member( instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance, name=instance.username)

@login_required
def dashboard(request):
    members = Member.objects.all()
    member_debts = [
        {'member': member, 'debt': member.calculate_debt()}
        for member in members
    ]
    payments = Payment.objects.all()
    total = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'dashboard.html', {'payments': payments, 'total': total, 'member_debts': member_debts})

@login_required
def add_payment(request):
    if request.method == 'POST':
        try:
            member_id = request.POST['member']
            amount = float(request.POST['amount'])
            receipt = request.FILES.get('receipt')

            Payment.objects.create(
                member_id=member_id,
                amount=amount,
                receipt=receipt
            )
            #messages.success(request, "Payment added successfully!")
            return redirect('dashboard')

        except ValueError as e:
            messages.error(request, f"Invalid input: {e}")

    # Get the current month's collector and exclude them from members
    current_month = date.today().replace(day=1)
    collector = MonthlyCollector.objects.filter(month=current_month).first()
    members = Member.objects.exclude(id=collector.collector.id) if collector else Member.objects.all()

    return render(request, 'add_payment.html', {'members': members})


@login_required
def monthly_records(request):
    payments = Payment.objects.annotate(
    month=TruncMonth('date')
    ).values('month').annotate(total=Sum('amount'))

    return render(request, 'monthly_records.html', {'payments': payments})

@login_required
def edit_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    if request.method == 'POST':
        try:
            payment.amount = float(request.POST['amount'])
            receipt = request.FILES.get('receipt')
            if receipt:
                payment.receipt = receipt
            payment.save()
            #messages.success(request, "Payment updated successfully!")
            return redirect('dashboard')

        except ValueError as e:
            messages.error(request, f"Invalid input: {e}")

    return render(request, 'edit_payment.html', {'payment': payment})


def register_view(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = MemberRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Change 'home' to your desired redirect URL
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
