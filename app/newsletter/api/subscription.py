from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from newsletter.serializers import ClientTransactionSerializer
from newsletter.services.subscription import confirm as confirm_subscription
from newsletter.services.subscription import start as start_subscription


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def subscribe(request: Request) -> Response:
    attempt = start_subscription(request.user.client)
    serializer = ClientTransactionSerializer(instance=attempt)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def confirm_user_subscription(request: Request, secret_code) -> Response:
    confirm_subscription(secret_code)
    return Response({})
