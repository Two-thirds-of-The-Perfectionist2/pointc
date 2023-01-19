from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import RegisterUserSerializer, NewPasswordSerializer, UserSerializer
from .models import User
from .tasks import send_code_for_reset
from review.serializers import UserRating, UserRatingSerializer


class RegisterUserView(APIView):

    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        ser = RegisterUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response('Successfully registration')


@api_view(['DELETE'])
def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    if user.id != request.user.id:
        return Response('You cant delete this user', status=403)

    user.delete()

    return Response("User successfully deleted", status=204)


@api_view(['GET'])
def activate_view(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = None
    user.save()

    return Response('Congratulations!', status=200)


@swagger_auto_schema(manual_parameters=[
        openapi.Parameter('email', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ], method='GET')
@api_view(['GET'])
def forgot_password(request):
    email = request.query_params.get('email')
    user = get_object_or_404(User, email=email)
    user.is_active = False
    user.create_activation_code()
    user.save()
    send_code_for_reset.delay(user.email, user.activation_code)

    return Response('send_mail' ,status=200)


@swagger_auto_schema(request_body=NewPasswordSerializer(), method='POST')
@api_view(['POST'])
def new_password_post(request):
    ser = NewPasswordSerializer(data=request.data, context={'request': request})
    ser.is_valid(raise_exception=True)

    return Response('Your password successfully update', status=200)


@api_view(['GET'])  
def details_user(request, id):
    user = get_object_or_404(User, id=id)
    serializer = UserSerializer(user)

    return Response(serializer.data, status=200)


@swagger_auto_schema(request_body=UserRatingSerializer(), method='POST')
@api_view(['POST'])
def rating(request, id=None):
    if not request.user.is_authenticated:
        raise NotAuthenticated()

    if type(request.data) == QueryDict:
        request.data._mutable = True

    request.data.update({'deliveryman': id})
    user = request.user
    ser = UserRatingSerializer(data=request.data, context={'request':request})
    ser.is_valid(raise_exception=True)

    if UserRating.objects.filter(customer=user, deliveryman__id=id).exists():
        rating = UserRating.objects.get(customer=user, deliveryman__id=id)
        rating.value = request.data.get('value')
        rating.save()
    else:
        ser.save()

    return Response(status=201)
    
