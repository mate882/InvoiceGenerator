from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.core.mail import EmailMessage

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from invoice.models import Invoice, CompanyProfile


User = get_user_model()

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                if existing_user.is_active:
                    messages.error(request, "Email already registered and activated. Try logging in.")
                    return render(request, 'main/register.html', {'form': form})
                else:
                    existing_user.delete()
                    messages.info(request, "Previous inactive account deleted. Proceeding with registration.")

            password1 = form.cleaned_data.get('password1') 
            password2 = form.cleaned_data.get('password2')

            if not password1 or not password2:
                messages.error(request, "Password is required.")
                return render(request, 'main/register.html', {'form': form})

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request, 'main/register.html', {'form': form})

            user = form.save(commit=False)
            user.set_password(password1)  
            user.is_active = False  
            user.save()  

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            message = render_to_string('main/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            email_message = EmailMessage(mail_subject, message, to=[email])
            email_message.content_subtype = 'html'  
            email_message.send()

            messages.success(request, "Please check your email to complete registration.")
            return redirect('register')
            
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "✅ Account activated successfully!")
        return redirect('profile')  
    else:
        messages.error(request, "❌ Activation link is invalid or expired.")
        return redirect('register')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    
    company_profile = CompanyProfile.objects.filter(user=request.user).first()  

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            request.user.profile_pic = profile_pic
            request.user.save()

    context = {
        'user': request.user,
        'company_profile': company_profile,
    }

    return render(request, 'main/profile.html', context)


def home(request):
    if request.user.is_authenticated:
        invoices = Invoice.objects.filter(author=request.user).order_by('-invoice_number')
        company_profile = CompanyProfile.objects.filter(user=request.user).first()

        context = {
            'invoice': invoices,
            'company_profile': company_profile,
        }
        return render(request, 'main/home.html', context)
    else:
        invoice = None
    return render(request, 'main/home.html', {"invoice": invoice})


@login_required
def delete_profile_pic(request):
    user = request.user
    if user.profile_pic:
        user.profile_pic.delete(save=False)
        user.profile_pic = None
        user.save()
    return redirect('profile')


def resend_activation(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, "Please enter your email address.")
            return render(request, 'main/resend_activation.html')
        
        try:
            user = User.objects.get(email=email)
            
            if user.is_active:
                messages.info(request, "Account is already activated. You can log in.")
                return redirect('login')
            
            send_activation_email(request, user)
            messages.success(request, "✅ Activation email sent! Check your inbox.")
            return render(request, 'main/resend_activation.html')
            
        except User.DoesNotExist:
            messages.error(request, "No account found with this email address.")
            return render(request, 'main/resend_activation.html')
    
    return render(request, 'main/resend_activation.html')


def send_activation_email(request, user):
    """Helper function to send activation email"""
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

    message = render_to_string('main/activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })

    email_message = EmailMessage(mail_subject, message, to=[user.email])
    email_message.content_subtype = 'html'
    email_message.send()
