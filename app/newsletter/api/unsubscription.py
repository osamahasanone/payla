from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from newsletter.services.unsubscription import confirm as confirm_unsubscription
from newsletter.services.unsubscription import start as start_unsubscription


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def unsubscribe(request: Request) -> Response:
    start_unsubscription(request.user.client)
    return Response({}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view()
def confirm_user_unsubscription(request: Request, secret_code) -> Response:
    confirm_unsubscription(secret_code)
    return Response({}, status=status.HTTP_200_OK)
