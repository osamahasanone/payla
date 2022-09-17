from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from newsletter.serializers import ClientTransactionSerializer
from newsletter.services.unsubscription import confirm as confirm_unsubscription
from newsletter.services.unsubscription import start as start_unsubscription


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def unsubscribe(request: Request) -> Response:
    attempt = start_unsubscription(request.user.client)
    serializer = ClientTransactionSerializer(instance=attempt)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def confirm_user_unsubscription(request: Request, secret_code) -> Response:
    confirm_unsubscription(secret_code)
    return Response({})
