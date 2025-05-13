from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import joblib
from django.contrib import messages  # Import messages for success messages
from django.views import View

# Load your model
model = joblib.load('../InsurancePredictor/static/random_forest_regressor')


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def login(request):
    return render(request, 'login.html')


def registration(request):
    if request.method == "POST":
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate inputs
        errors = {}
        if len(username) < 3:
            errors['username'] = "Username must be at least 3 characters long."
        if '@' not in email:
            errors['email'] = "Please enter a valid email address."
        if len(password) < 6:
            errors['password'] = "Password must be at least 6 characters long."
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."

        # If there are errors, pass them to the template
        if errors:
            return render(request, 'registration.html', {'errors': errors, 'username': username, 'email': email})

        # Otherwise, if all validations pass
        messages.success(request, "Successfully registered!")
        return redirect('registration')

    return render(request, 'registration.html')


def prediction(request):
    if request.method == "POST":
        # Retrieve and convert the inputs
        age = int(request.POST.get('age'))
        sex = int(request.POST.get('sex'))
        bmi = float(request.POST.get('bmi'))  # Use float for BMI
        children = int(request.POST.get('children'))
        smoker = int(request.POST.get('smoker'))
        region = int(request.POST.get('region'))

        # Make prediction
        pred = model.predict([[age, sex, bmi, children, smoker, region]])

        # Prepare output
        output = {
            "output": round(pred[0], 2)  # Format the prediction result
        }

        return render(request, 'prediction.html', output)

    return render(request, 'prediction.html')
