from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Đảm bảo không có khoảng trắng thừa
        email = email.strip()
        
        # Thử đăng nhập
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Đăng nhập thành công!')
            
            # Chuyển hướng
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('/')
        else:
            # In ra thông báo cụ thể hơn để debug
            user_exists = Account.objects.filter(email=email).exists()
            if user_exists:
                messages.error(request, 'Mật khẩu không chính xác')
            else:
                messages.error(request, 'Email không tồn tại')
            return redirect('login')
    
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        
        # Lấy user hiện tại
        user = request.user
        
        # Cập nhật thông tin
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.email = email
        user.save()
        
        messages.success(request, 'Thông tin tài khoản đã được cập nhật thành công!')
        return redirect('edit_profile')
    
    return render(request, 'accounts/edit_profile.html')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = request.user
        
        if new_password == confirm_password:
            # Kiểm tra mật khẩu hiện tại
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # Cập nhật lại session sau khi đổi mật khẩu
                auth.login(request, user)
                messages.success(request, 'Mật khẩu đã được thay đổi thành công!')
                return redirect('change_password')
            else:
                messages.error(request, 'Mật khẩu hiện tại không chính xác')
                return redirect('change_password')
        else:
            messages.error(request, 'Mật khẩu mới không khớp!')
            return redirect('change_password')
    
    return render(request, 'accounts/change_password.html')

@login_required(login_url='login')
def my_orders(request):
    # Import Order model nếu chưa import
    from orders.models import Order
    
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
def order_detail(request, order_number):
    # Import các model cần thiết
    from orders.models import Order, OrderProduct
    
    order_detail = OrderProduct.objects.filter(order__order_number=order_number, order__user=request.user)
    order = Order.objects.get(order_number=order_number, user=request.user)
    
    context = {
        'order_detail': order_detail,
        'order': order,
    }
    return render(request, 'accounts/order_detail.html', context)

@login_required(login_url='login')
def address_book(request):
    return render(request, 'accounts/address_book.html')

@login_required(login_url='login')
def wishlist(request):
    return render(request, 'accounts/wishlist.html')
