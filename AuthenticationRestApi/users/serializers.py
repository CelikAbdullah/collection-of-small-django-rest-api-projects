from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User


# Serializer for the serialization/deserialization of a User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'picture']


# Serializer for the registration
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # since we want a hashed version of our password,
    # we have to override the create() method. This method is used for creating a User instance.
    # To create a hash of a password, we use Django's built-in set_password() method.
    # That way, we have created a User object with a hashed password.
    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    # validates the user & username field
    # here, we check whether a User with the given email or username exists
    def validate(self, data):
        email = data['email']
        username = data['username']

        if validate_email(email) is not None:
            raise serializers.ValidationError({"response": "Error", "error_message": "That email is already in use."})
        if validate_username(username) is not None:
            raise serializers.ValidationError(
                {"response": "Error", "error_message": "That username is already in use."})

        return data


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # Use authenticate() to verify a set of credentials. It takes credentials
        # as keyword arguments, username and password for the default case, checks
        # them against each authentication backend, and returns a  object if the
        # credentials are valid for a backend. If the credentials aren’t valid for any
        # backend or if a backend raises PermissionDenied, it returns None.
        user = authenticate(**data)
        if user and user.is_active:
            return user

        if validate_username(data["username"]) is None:
            raise serializers.ValidationError({"response": "Error", "error_message": "Check your username. It might "
                                                                                     "be wrong."})
        else:
            raise serializers.ValidationError({"response": "Error", "error_message": "Check your password. It might "
                                                                                     "be wrong."})


# Serializer for changing password
class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    newPassword = serializers.CharField()

    def validate(self, data):
        if validate_email(data["email"]) is None:
            raise serializers.ValidationError({"response": "Your email does not exist."})

        return data


# helper method to validate the email of the user
def validate_email(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user is not None:
        return email


# helper method to validate the username of the user
def validate_username(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    if user is not None:
        return username
