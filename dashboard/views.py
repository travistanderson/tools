from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from tools.dashboard.models import MenuItem

def index (request):
	
	menus = MenuItem.objects.filter(toplevel=True)
	
	return render_to_response('dashboard/index.html', {
		'user':request.user,
		})