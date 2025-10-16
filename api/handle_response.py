from typing import Any
from django.http import JsonResponse


class HandleResponseUtils(object):

    """ A service class for handling function responses.

        This class have the following methods for handling reponses:

        Methods
        _______
        handle_response(status_code, message) -> JsonResponse
            Static method to handle response without denormalizing them - .data

        handle_response_with_data(status_code, message) -> JsonResponse
            Static method to handle response while normalizing them - appending .data
    """
    @staticmethod
    def handle_response(message: Any, status_code: int) -> JsonResponse:
        """ Returns proper response data.

        :param status_code: Http status code.
        :type status_code: int.
        :param message: Function that contains response.
        :return: JsonResponse.
        :rType: JsonResponse.
        """
        # If the obj is type set return list(obj)
        if isinstance(message, set):
            return JsonResponse(data=list(message), status=status_code, safe=False)
        else:
            return JsonResponse(data=message, status=status_code, safe=False)

    @staticmethod
    def handle_response_with_data(message: Any, status_code: int) -> JsonResponse:
        """ Returns proper response data.

        :param status_code: Http status code.
        :type status_code: int.
        :param message: Function that contains response.
        :rType: JsonResponse.
        :return: JsonResponse.
        """
        if isinstance(message, set):
            return JsonResponse(data=list(message).data, status=status_code, safe=False)
        else:
            return JsonResponse(data=message.data, status=status_code, safe=False)
