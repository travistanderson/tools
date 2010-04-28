from django.conf.urls.defaults import *
from settings import *

urlpatterns = patterns('tools.tags.views',
    (r'(?P<tag_id>\d+)', 'tags'),
   (r'', 'tagsets'),
)