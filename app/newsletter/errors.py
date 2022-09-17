from rest_framework import status
from rest_framework.exceptions import APIException


class NewsletterException(Exception):
    pass


class AlreadySubscriber(APIException, NewsletterException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "AlreadySubscriber"
    default_detail = "You are already a subscriber"


class SubscriptionConfirmationFailed(APIException, NewsletterException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "SubscriptionConfirmationFailed"
    default_detail = "This link is either expired, not existed or already visited"
