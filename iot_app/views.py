import random
import threading
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from paho.mqtt import client as mqtt_client

from .models import ReceivedMessage

broker = '43.205.50.167'
port = 1883
topic = "MQTT"
client_id = f'client-{random.randint(0, 100)}'

# MQTT Client setup
mqtt_client_instance = mqtt_client.Client(client_id=client_id)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    mqtt_client_instance.on_connect = on_connect
    mqtt_client_instance.connect(broker, port)
    mqtt_client_instance.loop_start()
    return mqtt_client_instance

def subscribe():
    client = connect_mqtt()

    def on_message(client, userdata, msg):
        message = msg.payload.decode().strip()  # Remove any line breaks or spaces
        print(f"Received `{message}` from `{msg.topic}` topic")
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        
        # Save to database
        ReceivedMessage.objects.create(topic=msg.topic, message=message)
        # Optionally, keep in-memory list (if still needed)
        received_messages.append((msg.topic, message, current_time))
        if len(received_messages) > 10:  # Keep only the last 10 messages
            received_messages.pop(0)
        sent_messages.append((msg.topic, message, current_time))

    client.subscribe(topic)
    client.on_message = on_message

    # Start the MQTT client loop in a separate thread
    client.loop_start()

# Start the subscriber thread once at the beginning
subscriber_thread = threading.Thread(target=subscribe)
subscriber_thread.start()

# Global variable to store received messages
received_messages = []
sent_messages = []

def user_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('home')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password for user login')
    return render(request, 'iot_app/user_login.html')

def admin_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('home')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password for admin login')
    return render(request, 'iot_app/admin_login.html')

@login_required
def home(request):
    return render(request, 'iot_app/home.html')

@login_required
def user_dashboard(request):
    return render(request, 'iot_app/user_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    users = User.objects.all()
    if request.method == 'POST':
        if 'add_user' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'User added successfully')
        elif 'delete_user' in request.POST:
            user_id = request.POST['user_id']
            User.objects.get(id=user_id).delete()
            messages.success(request, 'User deleted successfully')
        elif 'modify_user' in request.POST:
            user_id = request.POST['user_id']
            new_password = request.POST['new_password']
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password modified successfully')
    return render(request, 'iot_app/admin_dashboard.html', {'users': users})


def logout_view(request):
    logout(request)
    if request.user.is_staff:
        return redirect('admin_login')
    else:
        return redirect('user_login')
@login_required
def view_logs(request):
    if request.is_ajax():
        return JsonResponse({'received_messages': received_messages})
    return render(request, 'iot_app/logs.html', {'received_messages': received_messages})
@login_required
def debug(request):
    return render(request, 'iot_app/debug.html')

PARAMETER_CODES = {
    'crd_system_health': {'Good': 'a', 'Bad': 'b'},
    'control_supply': {'On': 'c', 'Off': 'd'},
    'crd_on_off': {'On': 'e', 'Off': 'f'},
    'manual_travel_length': 'tli',
    'crd_current_operations': {'Winding': 'g', 'Unwinding': 'h'},
    'overload_trip': {'Safe': 'i', 'Warning': 'j'},
    'cable_overtension': {'Safe': 'k', 'Warning': 'l'},
    'cable_slagness': {'Safe': 'm', 'Warning': 'n'},
    'chain_snap': {'Safe': 'o', 'Warning': 'p'},
    'motor_selection': {'q': 'VFD', 'r': 'Stall Torque'},
    'feed_selection': {'s': 'End', 't': 'Center'},
    'local_remote_mode_selection': {'u': 'Remote', 'v': 'Local'},
    'left_right_sensor': {'w': 'Proximity', 'x': 'Inclination', 'y': 'PLS'},
    'travel_sensor': {'z': 'Encoder', 'A': 'GLS', 'B': 'Proximity'},
}

@login_required
def update(request):
    if request.method == 'POST':
        data = request.POST
        encoded_parameters = []
        topic1 = "REC"

        for param, value in data.items():
            if param in PARAMETER_CODES:
                if isinstance(PARAMETER_CODES[param], dict):
                    encoded_value = PARAMETER_CODES[param].get(value, value)
                    encoded_parameters.append(encoded_value)
                else:
                    encoded_value = f"{value}"
                    encoded_parameters.append(encoded_value)
    
        # Publish each encoded parameter to MQTT
        client = mqtt_client_instance
        for value in encoded_parameters:
            client.publish(topic1, value)

    return render(request, 'iot_app/update.html')

@login_required
def status(request):
    context = get_decoded_params()
    return render(request, 'iot_app/update.html', context)

@login_required
def get_status(request):
    decoded_params = get_decoded_params()
    return JsonResponse(decoded_params)

def get_decoded_params():
    decoded_params = {
        'manual_travel_length': None,
        'motor_selection': None,
        'feed_selection': None,
        'local_remote_mode_selection': None,
        'left_right_sensor': None,
        'travel_sensor': None,
    }

    messages = ReceivedMessage.objects.order_by('-timestamp')[:6]

    for msg in messages:
        message = msg.message.strip()
        
        # Check if the message is a number (integer or float)
        if message.replace('.', '', 1).isdigit():
            decoded_params['manual_travel_length'] = message
        else:
            for param, codes in PARAMETER_CODES.items():
                if isinstance(codes, dict) and message in codes:
                    decoded_params[param] = codes[message]

    return decoded_params

@csrf_exempt
def toggle_debug_mode(request):
    topic1= "REC"
    if request.method == 'POST':
        debug_mode = request.POST.get('debug_mode') == 'true'
        message = '-' if debug_mode else '+'

        # Publish the message to MQTT
        mqtt_client_instance.publish(topic1, message)

        return JsonResponse({'message': f'Debug mode {"enabled" if debug_mode else "disabled"}'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def send_reload_message(request):
    if request.method == 'POST':
        topic1 = "REC"
        message = 'reload'
        mqtt_client_instance.publish(topic1, message)
        return JsonResponse({'message': 'Reload message sent to MQTT server'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
