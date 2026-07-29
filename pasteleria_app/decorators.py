from django.contrib.auth.decorators import user_passes_test

def role_required(roles):
    def check_role(user):
        return user.rol in roles
    return user_passes_test(check_role)