import json

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from django.template import RequestContext

from oppia.deviceadmin.forms import AdminMessageForm
from oppia.deviceadmin.models import UserDevice


def user_devices_list(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    ordering = request.GET.get('order_by', None)
    if ordering is None:
        ordering = '-modified_date'

    devices = UserDevice.objects.all().order_by(ordering)
    paginator = Paginator(devices, 10) # Show 25 per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        devices = paginator.page(page)
    except (EmptyPage, InvalidPage):
        devices = paginator.page(paginator.num_pages)

    print devices
    return render(request, 'oppia/deviceadmin/list.html',
                              { 'page': devices, 'page_ordering':ordering })

def send_message_to_device(request):

    if request.method != 'POST':
        return HttpResponse(status=405)

    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    form = AdminMessageForm(request.POST)
    if form.is_valid():
        action = form.cleaned_data.get("action")
        device_id = form.cleaned_data.get("device")

        message_data = {'type': 'admin', 'action': action}

        if 'password' in request.POST:
            password = request.POST.get('password')
            message_data['password'] = password

        device = UserDevice.objects.get(dev_id=device_id)
        messageID, response = device.send_message(message_data)
        success = response['failure'] == 0
        if success:
            return JsonResponse(response, status=200)
        else:
            return JsonResponse(response, status=400)
        #return the response object as json

    else:
        return HttpResponse(status=400)