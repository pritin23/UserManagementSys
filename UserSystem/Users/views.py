from django.urls import reverse
from Users.models import UserDerived
from Users.serializers import UserSerializer, UserUpdateSerializer
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from Users.permissions import CustomUserPermission
from dj_rest_auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout


# Create your views here.
class UserRegisterView(viewsets.ModelViewSet):
    queryset = UserDerived.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
            New user can register here, after register he can activate his account
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            email = serializer.data['email']
            uid = urlsafe_base64_encode(force_bytes(user.id))
            domain = get_current_site(request).domain
            token = Token.objects.create(user=user)
            link = reverse('activate', kwargs={'uid': uid, 'token': token})
            activate_url = "http://" + domain + link
            email_subject = "Activate Your Account"
            email_body = "Hello " + user.first_name + "\nPlease use this link to activate your account\n" + activate_url
            email_msg = EmailMessage(email_subject, email_body, 'noreply@semicolon.com', [email])
            email_msg.send(fail_silently=False)
            return Response({"result": serializer.data, "status": status.HTTP_200_OK, "message": "Now check your "
                                                                                                 "mail for "
                                                                                                 "activation"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def verify_account(request, uid, token):
    """
        This function is used to activate user account for login
    """
    try:
        id = force_str(urlsafe_base64_decode(uid))
        user = UserDerived.objects.get(pk=id)
        user.is_active = True
        user.save()
        return Response({"status": status.HTTP_201_CREATED, "message": "Thank You "
                                                                       "for "
                                                                       "activation.Now you can Login"})
    except Exception as e:
        print(e)


# CRUD API
class UserViewSet(viewsets.ModelViewSet):
    """
        CRUD api for User
    """
    permission_classes = [CustomUserPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = UserUpdateSerializer
    filterset_fields = ['username', 'email', 'id']
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return UserDerived.objects.all()
        else:
            return UserDerived.objects.filter(id=user.id)


# Custom LoginAPI
class LoginViewCustom(LoginView):
    """
        Custom Login API. registered user can log in to the system
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "user_id": user.pk})


# custom Logout API
class LogoutViewCustom(LogoutView):
    """
          Custom Logout API. User can out from the system
      """

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            logout(request)
            Response({'status': status.HTTP_200_OK, 'message': "You are Successfully logout"})
        except Exception as e:
            print(e)
