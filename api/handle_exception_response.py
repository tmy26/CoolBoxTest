from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from api.custom_exceptions import *


class CustomExceptionHandler(object):
    """ This class holds methods for custom exceptions.

    This class have the following method for handling exceptions.

    Methods
    _______
    exception_handler(exception_message) -> JsonResponse
        Static method to handle the error.
    """
    @staticmethod
    def exception_handler(exception_message: Exception) -> JsonResponse:
        """ Handles custom exceptions raised from user functions.

        :param exception_message: The custom exception that is passed.
        :type exception_message: Exception.
        :return: The status code and exception as error message.
        :rType: JsonResponse.
        """
        match exception_message:
            case Exception():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case _:
                response = JsonResponse({'Error': 'Internal Server Error'}, status=500)
        return response
