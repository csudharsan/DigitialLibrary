from django.conf.urls import url

app_name = 'tutorials'

urlpatterns = [
        url(r'^$', views.index, name='index'),
    ] 