from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login,logout
from .forms import EventRegistrationForm  # Import your EventRegistrationForm if needed
from django.contrib.auth.models import User
from .models import Event
from django.contrib.auth.decorators import login_required
from .forms import EventEditForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.urls import reverse

def payment_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Your payment processing logic here
        # Assuming the payment is successful
        if event.payment_status != 'Paid':
            event.payment_status = 'Paid'
            event.save()
            messages.success(request, 'Payment successful!')
            return redirect('payment_success', event_id=event.id)
        else:
            messages.info(request, 'No pending payments')
            return render(request, 'event_app/no_pending.html', {'event': event})

    return render(request, 'event_app/payment.html', {'event': event})

def payment_success_view(request):
    # Process the payment and update the status (similar to your payment_view)
    # For demonstration purposes, assume payment is successful
    event_id = request.POST.get('event_id')
    event = get_object_or_404(Event, pk=event_id)
    event.payment_status = 'Paid'
    event.save()
    messages.success(request, 'Payment successful! Payment status updated to "Paid".')
    return redirect('plain')

def payment_success(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_app/payment_success.html', {'event': event})

def handle_payment(request, event_id):
    # Add your logic to handle the payment here
    # This is a placeholder response, replace it with actual payment processing code
    #return HttpResponse("Payment successful!")
    messages.success(request, 'Payment successful!')
    return redirect('event_app/plain.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the user is an admin
            if user.is_staff:
                # Redirect to display_events for admin users
                return redirect('display_events')
            else:
                # Redirect to plain view for regular users
                return redirect('plain')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'event_app/login.html')

def home(request):
    return render(request, 'event_app/home.html')



def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('plain')  # Redirect to the plain view after successful edit
    else:
        form = EventEditForm(instance=event)

    return render(request, 'event_app/edit_event.html', {'form': form})


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_name = event.name  # Save the event name before deleting

    # Perform additional checks if needed before deleting
    # For example, check if the user has permission to delete the event

    event.delete()
    messages.success(request, f'Event "{event_name}" deleted successfully.')

    return redirect('plain')

@login_required
def register_view(request):
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user  # Associate the event with the current user
            event.save()
            return redirect('plain')  # Redirect to the appropriate view
    else:
        form = EventRegistrationForm()

    return render(request, 'event_app/register.html', {'form': form})


@login_required
def plain_view(request):
    # Filter events for the current user
    events = Event.objects.filter(user=request.user)
    return render(request, 'event_app/plain.html', {'events': events})



@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Log in the user after signup
            login(request, user)

            # Redirect to the home page or any other desired page
            return redirect('login')  # Change 'home' to the actual name of your home view

    else:
        form = UserCreationForm()

    return render(request, 'event_app/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def display_events(request):
    events = Event.objects.all()
    return render(request, 'event_app/display_events.html', {'events': events})

def your_friends_view(request):
    return render(request, 'event_app/data.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('display_events')
        else:
            # Authentication failed, handle accordingly (e.g., show an error message)
            pass

    return render(request,'event_app/al.html')

def data_page(request):
    # Your logic to render the data.html page
    return render(request, 'event_app/data.html')


@login_required
def update_confirmation_status(request):
    response_data = {'message': 'Confirmation status and amounts updated successfully.'}

    if request.method == 'POST':
        for event in Event.objects.all():
            confirmation_status_key = f'confirmation_status_{event.id}'
            amount_key = f'amount_{event.id}'

            # Update confirmation status
            event.event_confirmation = confirmation_status_key in request.POST

            # Update amount if the key exists in the form data
            if amount_key in request.POST:
                event.amount = request.POST[amount_key]

            event.save()

    return JsonResponse(response_data)