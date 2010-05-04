from tools.tags.settings import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import simplejson
from django.contrib.admin.views.decorators import staff_member_required
import MySQLdb
from tools.tiq_login import getSessionRpcClient, authenticateRedirect



def tagsets(request):
	#need to get all the tagsets from the DFS.
	
	db = MySQLdb.connect(DFS_HOSTNAME, DFS_USERNAME, DFS_PASSWORD, DFS_DATABASE)
	dfs = db.cursor()
	
	dfs.execute("""SELECT id, name from tagset	where id > 5""")
	
	retval = []
	
	while (1):
		row = dfs.fetchone()
		if row == None:
			break
		retval.append({'id':row[0], 'name':row[1] })
	
	return render_to_response('tags/tagsets.html', {
		'tagsets':retval,
		'user':request.user,
		})
tagsets = login_required(tagsets)

		
def tags(request, tag_id):
	
	db = MySQLdb.connect(DFS_HOSTNAME, DFS_USERNAME, DFS_PASSWORD, DFS_DATABASE)
	dfs = db.cursor()
	
	client = getSessionRpcClient(request)
	
	if request.method == 'POST':
		
		
		if request.POST.has_key('this_is_the_newtag_form'):
			#need to get data from the parent tag to fill out the data for the new tag.
			dfs.execute("SELECT id, name from tagset where id = " + tag_id)
			row = dfs.fetchone()
			
			if row == None:
				dfs.execute("SELECT max(tagset), max(ord) from Tag where parent = " + str(tag_id) )
				row = dfs.fetchone()
				if row[0] == None:
					dfs.execute("SELECT tagset from Tag where id = " + str(tag_id) )
					tset = dfs.fetchone()[0]
					tord = 1
				else:
					tset = row[0]
					tord = row[1] + 1
				try:
					client.execute('entity.new', { 'class_name':'Tag', 'name':request.POST['newtag'], 'parent':tag_id, 'ord':tord, 'tagset':tset, 'oldId':0 } )
				except Exception, err:
					if "Invalid Session" in str(err):
						#if were here, session expired, so lets fix that issue
						request.user.message_set.create(message='Your DFS Session has expired, please log in again to continue.')
						return HttpResponseRedirect('/user/login?next=/tags/' + str(tag_id) )
			else:
				tset = row[0]
				dfs.execute("SELECT max(ord) from Tag where tagset = " + tag_id)
				tord = dfs.fetchone()[0] + 1
				try:
					client.execute('entity.new', { 'class_name':'Tag', 'name':request.POST['newtag'], 'parent':0, 'ord':tord, 'tagset':tset, 'oldId':0 } )
				except Exception, err:
					if "Invalid Session" in str(err):
						request.user.message_set.create(message='Your DFS Session has expired, please log in again to continue.')
						return HttpResponseRedirect('/user/login?next=/tags/' + str(tag_id))
		elif request.POST.has_key('this_is_the_removetag_form'):
			#first, we need to see if there are any tags under this tag.  If it has children, we dont allow deleting it!
			dfs.execute("SELECT count(*) from Tag where parent = " + str(tag_id) )
			row = dfs.fetchone()[0]
			
			if row == 0:
				#this tag has no children, lets remove it.
				dfs.execute("SELECT rev_id from Tag where id = " + str(tag_id) )
				row = dfs.fetchone()[0]
				try:
					client.execute('entity.delete', { 'id':tag_id, 'rev_id':row } )
				except Exception, err:
					if "Invalid Session" in str(err):
						#if were here, session expired, so lets fix that issue
						request.user.message_set.create(message='Your DFS Session has expired, please log in again to continue.')
						return HttpResponseRedirect('/user/login?next=/tags/' + str(tag_id) )
				return HttpResponseRedirect('/tags/')
				
				
		elif request.POST.has_key('this_is_the_edittag_form'):
			#put edit tag stuff here
			dfs.execute("select rev_id from Tag where id = " + str(tag_id) )
			row = dfs.fetchone()[0]
			try:
				client.execute('entity.update', { 'id':tag_id, 'rev_id':row, 'name':request.POST['edittag'] } )
			except Exception, err:
				if "Invalid Session" in str(err):
					#if were here, session expired, so lets fix that issue
					request.user.message_set.create(message='Your DFS Session has expired, please log in again to continue.')
					return HttpResponseRedirect('/user/login?next=/tags/' + str(tag_id) )
			
	#lets see if this is a tagset or a tag
	dfs.execute("SELECT name from tagset where id = " + str(tag_id) )
	
	tag_name = ""
	while(1):
		row = dfs.fetchone()
		if row == None:
			break
		tag_name = row[0]
	
	if tag_name == "":
		#if were here, no name was found in tagset, so its not a tagset
		tags = _getTags(request, tag_id)
		dfs.execute("SELECT name from Tag where id = " + tag_id)
		row = dfs.fetchone()
		tag_name = row[0]
	else:
		try:
			tags = client.execute('tag.getTagTree', {'tagsets':[tag_name]} )
		except Exception, err:
			if "Invalid Session" in str(err):
				#if were here, session expired, so lets fix that issue
				request.user.message_set.create(message='Your DFS Session has expired, please log in again to continue.')
				return HttpResponseRedirect('/user/login?next=/tags/' + str(tag_id) )
			else:
				request.user.message_set.create(message=err)
				return HttpResponseRedirect('/user/login?next=/tags/' + str(tag_id) )
	
	hasTags = True
	if len(tags) == 0:
		hasTags = False
	
	return render_to_response('tags/tags.html', {
		'user':request.user,
		'tags':tags,
		'tag_name':tag_name,
		'tag_id':tag_id,
		'hasTags':hasTags,
		})
tags = login_required(tags)

def _getTags(request, tag_id):
	#this function should be in the DFS tag API, of course its not and I'm not doing a DFS push for this.  This should be moved to the DFS API.  Actually, the DFS API should be fixed since its unusable and horribly damaged.
	retval = []
	children = []
	
	db = MySQLdb.connect(DFS_HOSTNAME, DFS_USERNAME, DFS_PASSWORD, DFS_DATABASE)
	dfs = db.cursor()
	dfs.execute("SELECT id, name, ord from Tag where parent = " + tag_id + " order by ord" )
	
	while(1):
		row = dfs.fetchone()
		if row == None:
			break
		
		children.append({ 'tagId':row[0],
								  'tagName':row[1],
								  'ord':row[2],
								  'children':_getTags(request, str(row[0])) })
	
	return children