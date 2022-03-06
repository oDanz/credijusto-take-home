from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import authentication, generics, permissions
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from . import services
from .serializers import UserSerializer


class RatesListView(APIView):
    """
    View to list exchange rates from three different sources.

    * Requires token authentication.
    * Each user has a limit of 10 request per day.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        """
        Returns a json object with exchange rates.
        """
        banxico = cache.get('banxico')
        if not banxico:
            banxico = services.retrieve_banxico()
            cache.set('banxico', banxico)
        dof = cache.get('dof')
        if not dof:
            dof = services.retrieve_dof()
            cache.set('dof', dof)
        fixer = cache.get('fixer')
        if not fixer:
            fixer = services.retrieve_fixer()
            cache.set('fixer', fixer)
        response = {
            "rates": {
                'provider_1': fixer,
                'provider_2_variant_1': banxico,
                'provider_2_variant_2': dof,
                }
        }
        return Response(response)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
