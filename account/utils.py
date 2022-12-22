from django.core.mail import send_mail


def send_activation_mail(email, activation_code):
    activation_link = f'http://localhost:8000/account/activate/{activation_code}/'
    message = f'Activate your account with a link:\n{activation_link}'
    send_mail("Activate account", message, 'admin@admin.com', recipient_list=[email], fail_silently=False)


def send_activation_code(email, activation_code):
    activation_link = f'http://localhost:8000/account/accept/{activation_code}/'
    message = f'Reset your password with this link:\n{activation_link}'
    send_mail("Drop password", message, 'admin@admin.com', recipient_list=[email], fail_silently=False)
