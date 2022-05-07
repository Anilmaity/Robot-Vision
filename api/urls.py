from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static
from .apis import get_angles
from .apis import register_robot
from .apis import set_angles



urlpatterns = [
    path('', views.index, name='index'),
    path('get_angles/', get_angles.get_angles.as_view() , name='index'),
    path('register_robot/', register_robot.register_robot.as_view(), ),
    path('set_angles/', set_angles.set_angles.as_view(), ),

              ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
