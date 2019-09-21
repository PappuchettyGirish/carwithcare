from myapp import views as my_views
from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', my_views.index, name='index'),
    url('create/',TemplateView.as_view(template_name = 'myapp/signup.html')),
    url('mail/',my_views.mail,name='mail'),
    url('verifyotp/',my_views.verifyotp,name='verifyotp'),
    url('verifyotpdriver/',my_views.verifyotpdriver,name='verifyotpdriver'),
    url('forgotpwd/',my_views.forgotpwd,name='forgotpwd'),

    ]
