"""queued URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from queuedapi.views import login_user, register_user
from queuedapi.views import Trips
from queuedapi.views import RideReviews
from queuedapi.views import RideFavorites
from queuedapi.views import Itineraries
from queuedapi.views import RideItineraries
from queuedapi.views import Rides
from queuedapi.views import Profiles


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'trips', Trips, 'trips')
router.register(r'ridereviews', RideReviews, 'ridereviews')
router.register(r'ridefavorites', RideFavorites, 'ridefavorites')
router.register(r'itineraries', Itineraries, 'itineraries')
router.register(r'rideitineraries', RideItineraries, 'rideitineraries')
router.register(r'rides', Rides, 'rides')
router.register(r'profile', Profiles, 'profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]