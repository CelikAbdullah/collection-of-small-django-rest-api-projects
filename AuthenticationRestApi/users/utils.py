from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError as DRFValidationError


def custom_exception_handler(exc, context):
    """
    A custom exception handler.
    Note that the exception handler will only be called for responses generated
    by raised exceptions. It will not be used for any responses returned directly by the view,
    such as the HTTP_400_BAD_REQUEST responses that are returned by the generic views when
    serializer validation fails.
    """

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        customized_response = {}
        customized_response_helper = {}
        # When we deal with a validation error, then customize the
        # result of the exception a little bit. The standard validation
        # error puts the values of the keys into a list. I do not want that.
        # Instead of mapping a string (key) to a list (value), we will map a
        # string (key) to a string (value).
        # So, for example: I turn this {"email": ["This field is required."] }
        # into this {"email": "This field is required."}
        if isinstance(exc, DRFValidationError):
            for key, value in response.data.items():
                customized_response_helper[key] = value[0]

            customized_response["error"] = customized_response_helper
            response.data = customized_response

    return response
