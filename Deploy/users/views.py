from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .models import AirQualityData
from .forms import AirQualityData_Form



def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


Model = joblib.load('users/XGB.pkl')
def Deploy_8(request):
    if request.method == 'POST':
        form = AirQualityData_Form(request.POST)
        if form.is_valid():
            
                pm25 = form.cleaned_data['pm25']
                pm10 = form.cleaned_data['pm10']
                no = form.cleaned_data['no']
                no2 = form.cleaned_data['no2']
                nox = form.cleaned_data['nox']
                nh3 = form.cleaned_data['nh3']
                co = form.cleaned_data['co']
                so2 = form.cleaned_data['so2']
                o3 = form.cleaned_data['o3']
                benzene = form.cleaned_data['benzene']
                toluene = form.cleaned_data['toluene']
                xylene = form.cleaned_data['xylene']
                aqi = form.cleaned_data['aqi']
                # Prepare features for prediction
                features = np.array([[pm25, pm10, no, no2, nox, nh3, co, so2, o3, benzene, toluene,xylene, aqi]])
                # Predict using the loaded model
                features=features.reshape(1,-1)
                prediction = Model.predict(features)
                prediction = prediction[0]
                print(prediction)
                # Determine the result based on prediction
                attack = ['Good','Moderate','Poor','Satisfactory','Severe','Very Poor']
                result = attack[prediction]
                
                # Save data to database
                instance = form.save(commit=False)
                instance.label = result
                instance.save()
                
                # Render output page with prediction result
                return render(request, 'app/output.html', {'predict': result})
        else:
            print('hi')
    else:
        form = AirQualityData_Form()
    
    return render(request, 'app/deploy_8.html', {'form': form})




import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
from django.shortcuts import render





def Basic_report(request):
    return render(request,'app/Basic_report.html')

def Metrics_report(request):
    return render(request,'app/Metrics_report.html')


def Air_db(request):
    data = AirQualityData.objects.all()
    return render(request, 'app/Air_db.html', {'data': data})




def logout_view(request):  
    auth_logout(request)
    return redirect('/')


