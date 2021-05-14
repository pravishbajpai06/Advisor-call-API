from django.urls import path, include
from . import views
from rest_framework import routers
from .views import LoginAPIView,RegisterView

router=routers.DefaultRouter()
router.register('admin/advisor',views.AdvisorView)


urlpatterns = [
    path('',include(router.urls)),
    path('user/login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('user/register/', RegisterView.as_view(), name='auth_register'),
    path('user/<int:user_id>/advisor',views.advisorList),
    path('user/<int:user_id>/advisor/<int:adv_id>/',views.createBooking),
    path('user/<int:user_id>/advisor/booking/',views.viewBooking),

]
