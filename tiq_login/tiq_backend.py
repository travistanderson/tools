from django.conf import settings
from django.contrib.auth.models import User, check_password
from models import TiqUserProfile
from tiqLibraries.tiqErrors.tiqError import TiqError, TiqPasswordExpiredError
from tiq_login import getSessionRpcClient

class TiqLoginBackend:
   """
   """
   def authenticate(self, username=None, password=None):

      try:
         sessionRpcClient = getSessionRpcClient() 
         loginResult = sessionRpcClient.login(username, password)
      except TiqError, e:
         if (e.message == "Security Error: Password Expired."):
            raise TiqPasswordExpiredError, e.message
         return None
      
      if (loginResult['login'] != 'success'):
         return None
         
      try:
         user = User.objects.get(username=username)

      except User.DoesNotExist:
         user = User(username=username, password='')
         user.set_unusable_password()
         user.is_staff = False
         user.is_superuser = False
         user.sessionId = "DFS SESSION ID STRING"
         user.save()
         
         profile = TiqUserProfile.objects.create(user=user)
            
      else:
         profile = user.get_profile()
      
      # Pull this info every time we authenticate...
      user_info = sessionRpcClient.execute('user.getMyUserInfo')
      user.first_name = user_info['screenname']
      user.email = user_info['email']

      contact_id = user_info['contact']
      
      if (contact_id == 0) or (contact_id == None):
         contact = {}
         contact['class_name'] = 'Contact'
         contact['name'] = user.first_name
         contact['owner'] = 0
         contact_id = sessionRpcClient.execute('entity.new', contact)
         sessionRpcClient.execute('user.editMyUserInfo', {'contact':contact_id})
         # set permissions !
         
         email = {}
         email['class_name'] = 'Email'
         email['description'] = 'SFC Primary'
         email['_link'] = {'token': 'CONTACT_INFO', 'entity2': contact_id}
         email['email'] = user.email
         email['owner'] = 0
         email_id = sessionRpcClient.execute('entity.new', email)
         # set permissions !
         
         links_between = sessionRpcClient.execute('linker.isLinked', {'id_1': contact_id, 'id_2': email_id})
         
         # add permissions for SFC Users, DFS Users to email, contact, and all links_between
         sfc_user_data_group = sessionRpcClient.execute('permission.findDataGroup', {'name':'SFC Users'})
         dfs_user_data_group = sessionRpcClient.execute('permission.findDataGroup', {'name':'DFS Users'})
         
         entity_ids = [contact_id, email_id]
         for l in links_between:
            entity_ids.append(l['id'])
         
         for e in entity_ids:
            sessionRpcClient.execute('permission.addDataGroupPermission', {'data_group_id':sfc_user_data_group, 'entity_id':e, 'permission':'r'})
            sessionRpcClient.execute('permission.addDataGroupPermission', {'data_group_id':dfs_user_data_group, 'entity_id':e, 'permission':'r'})
         
         #print sessionRpcClient.execute('entity.get', {'id':contact_id})
      
      profile.contact_id = contact_id
      profile.session_id = sessionRpcClient.sessionId
      profile.save()
      
      return user


   def get_user(self, user_id):
      try:
         return User.objects.get(pk=user_id)
      except User.DoesNotExist:
         return None
