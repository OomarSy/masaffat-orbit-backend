from rest_framework.response import Response
from rest_framework import status


def api_response(errorno=0, message="", data=None, status_code=status.HTTP_200_OK):
    return Response({"errorno": errorno, "message": message, "data": data or {}}, status=status_code)