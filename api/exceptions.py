from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        data = {
            'details': {key: value for key, value in response.data.items()},
            'code': response.status_code
        }
        print("custom_exception_handler")
        print(response.data)
        response.data = data

    return response
