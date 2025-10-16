from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from .handle_response import HandleResponseUtils
from .handle_exception_response import CustomExceptionHandler
from .search_sort_filter_v3 import ManualSQLQueryEngine


class SearchView(APIView):
    """Search function"""
    permission_classes = (AllowAny,)
    def get(self, request):
        try:
            message = ManualSQLQueryEngine.search_data(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(message, status_code)
        except Exception as error:
            return CustomExceptionHandler.exception_handler(error)
