# This is the location where you store your local copy of tiqLibraries. It should be an absolute path, use forward slashes, and end with a trailing slash
SYS_PATH_TO_TIQ_LIBRARIES = '/Users/rjett/django-projects/'

# This is the path to this module. Usually, you'll replace 'django_tiq_login' with the name of this project.
PATH_TO_THIS_MODULE = "tools.tiq_login"

# The directory inside templates where you store your login templates
TIQ_LOGIN_TEMPLATE_DIR = 'tiq_login/'

# And the names of your login templates. 
TIQ_LOGIN_TEMPLATE_LOGIN = TIQ_LOGIN_TEMPLATE_DIR + 'login.html'
TIQ_LOGIN_TEMPLATE_AUTHENTICATE = TIQ_LOGIN_TEMPLATE_DIR + 'authenticate.html'
TIQ_LOGIN_TEMPLATE_LOGGED_OUT = TIQ_LOGIN_TEMPLATE_DIR + 'logged_out.html'
TIQ_LOGIN_TEMPLATE_PASSWORD_CHANGE = TIQ_LOGIN_TEMPLATE_DIR + 'password_change.html'
TIQ_LOGIN_TEMPLATE_PASSWORD_CHANGE_DONE = TIQ_LOGIN_TEMPLATE_DIR + 'password_change_done.html'
TIQ_LOGIN_TEMPLATE_SIGNUP = TIQ_LOGIN_TEMPLATE_DIR + 'signup.html'

REDIRECT_FIELD_NAME = 'next'

# The page to redirect to after a successful login or password change.
LOGIN_REDIRECT_URL = '/'

# The url where the login view is displayed
LOGIN_URL = '/user/login'

# The Hostname and Path of the SessionRPC Server
TIQ_SERVER = 'dfs.hisg-it.net' # hostname
TIQ_URL = '/.dfs' # path

LOGIN_AUTHENTICATE_URL =  '/user/authenticate'

SFC_GRANTOR_USERNAME = 'sfc_grantor'
SFC_GRANTOR_PASSWORD = 'DxymwCbdQZXDbtpiO2c'

MODERATE_NEW_USER_POSTS = False

try:
    from local_settings import *
except ImportError, exp:
    pass
