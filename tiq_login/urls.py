from django.conf.urls.defaults import *
from settings import *

urlpatterns = patterns(PATH_TO_THIS_MODULE + '.views',
   (r'login', 'login'),
   (r'authenticate', 'login', {'template_name':TIQ_LOGIN_TEMPLATE_AUTHENTICATE}),
   (r'logout', 'logout'),
   (r'signup', 'signup'),
   (r'password_change', 'password_change'),
   (r'password_change_done', 'password_change_done'),
   (r'', 'login')
)