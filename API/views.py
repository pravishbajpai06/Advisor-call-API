from .models import Advisor, NewUser, Booking
from rest_framework import viewsets
from .serializers import AdvisorSerializer, RegisterSerializer, LoginSerializer, AdviseSerializer, BookSerializer, \
    BookViewSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class AdvisorView(viewsets.ModelViewSet):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer


@api_view(['GET'])
def advisorList(request, user_id):
    try:
        user = NewUser.objects.get(pk=user_id)
    except NewUser.DoesNotExist:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)
    adv = Advisor.objects.all()
    serializer = AdviseSerializer(adv, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def createBooking(request, user_id, adv_id):
    data = {}
    try:
        user = NewUser.objects.get(pk=user_id)
    except NewUser.DoesNotExist:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)
    try:
        adv = Advisor.objects.get(pk=adv_id)
    except Advisor.DoesNotExist:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)
    data['date'] = request.data.get('date')
    book = Booking.objects.create(user=user, advisor=adv, date=data['date'])
    book.save()
    serializer = BookSerializer(data=book)
    serializer.is_valid()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def viewBooking(request, user_id):
    try:
        user = NewUser.objects.get(pk=user_id)
    except NewUser.DoesNotExist:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)
    book = Booking.objects.filter(user=user)

    serializer = BookViewSerializer(book, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    queryset = NewUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, **kwargs):
        data = {'email': request.data.get('email', ''), 'name': request.data.get('name', ''),
                'password': request.data.get('password', '')}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = {'email': request.data.get('email', ""), 'password': request.data.get('password', "")}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
