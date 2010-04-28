from settings import *
import sys
sys.path.insert(0, SYS_PATH_TO_TIQ_LIBRARIES)
from tiqLibraries.interface.sessionRpcClient import SessionRpcClient
from tiqLibraries.tiqErrors.tiqError import TiqError, TiqPasswordExpiredError
from django.http import HttpResponseRedirect

def getSessionRpcClient(request=None):

   sessionRpcClient = SessionRpcClient(TIQ_SERVER, TIQ_URL)      
   
   if request:
      profile = request.user.get_profile()
      sessionRpcClient.resume(profile.session_id, request.user.username)
   else:
      sessionRpcClient.start() 
   
   return sessionRpcClient

def authenticateRedirect(request):
   return HttpResponseRedirect(LOGIN_AUTHENTICATE_URL+ '?next=' + request.path)
   
