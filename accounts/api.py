from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.account.adapter import get_adapter

User = get_user_model()

class WsResendActivationEmailAPIView(APIView):

    def get(self, request):
        try:
            user = User.objects.get(email=request.query_params.get("email"))

            get_adapter(request).send_confirmation_mail(request, user)
        except:
            return Response("Unable to send activation email please ensure you entered a valid email",
                            status=status.HTTP_400_BAD_REQUEST)
        return Response("success")