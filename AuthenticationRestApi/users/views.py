from users.models import User
from users.serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken


class RegisterView(APIView):
    """
    The class-based view for registration.
    """

    def post(self, request, format=None):
        """
        REST framework introduces a Request object that extends the regular HttpRequest,
        and provides more flexible request parsing. The core functionality of the Request
        object is the request.data attribute, which is similar to request.POST, but more
        useful for working with Web APIs.
        """

        serializer = RegisterSerializer(data=request.data)  # pass incoming data to serializer

        # recall: the is_valid() call deserializes and validates incoming data
        if serializer.is_valid(raise_exception=True):
            # recall: the save() call on the serializer object persists the validated data
            #         into an object instance.
            #         since only the data keyword's argument is passed to the serializer above,
            #         save() will create a new User instance
            user = serializer.save()

            """
            REST framework also introduces a Response object, which is a type of TemplateResponse 
            that takes unrendered content and uses content negotiation to determine the correct 
            content type to return to the client.
            The Response we send back to the client contains a response message, 
            the user information of the user and the token. 
            
            Recall: The .data property of the serializer returns the outgoing 
                    primitive representation.
            """
            return Response({
                "response": "Registration is successful.",
                "user": UserSerializer(user, context={"request": request}).data,
                "token": AuthToken.objects.create(user)[1]
            })

        # if there is an error during validation, we return a HTTP_422_UNPROCESSABLE_ENTITY error
        # recall: the error() call on the serializer returns any errors during validation.
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    """
    The class-based view for login.
    """

    def post(self, request, format=None):
        # pass incoming data to corresponding serializer
        serializer = LoginSerializer(data=request.data)
        # deserialize and validate incoming data
        if serializer.is_valid(raise_exception=True):
            # validated_data: returns the validated incoming data.
            user = serializer.validated_data

            # The Response we send back to the client contains a response message,
            # the user information of the user and the token.
            return Response({
                "response": "Login is successful.",
                "user": UserSerializer(user, context={"request": request}).data,
                "token": AuthToken.objects.create(user)[1]
            })

        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ForgotPasswordView(APIView):
    """
    The class-based view for resetting the password.
    """
    def post(self, request, format=None):
        response = {}
        email = request.data.get('email')
        password = request.data.get('newPassword')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response['response'] = 'Your email does not exist.'
            return Response(response)

        if user:
            user.set_password(password)
            user.save()

            response['response'] = 'Your new password is saved successfully.'
            return Response(response)
