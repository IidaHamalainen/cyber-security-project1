
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', include('polls.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='register/login.html')),
	path('logout/', LogoutView.as_view(next_page='/')),
]
