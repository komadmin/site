from django.http import HttpResponse
from movies.forms import SettingButton
from movies.models import UserSettings
# from django.contrib.auth.models import User

def settingbutton(request):
    if not request.user.is_authenticated():
        return HttpResponse('loggedout')
    if request.method == 'POST':
        b = SettingButton(request.POST)
    else:
        b = SettingButton(request.GET)

    u = request.user

    if not b.is_valid():
        return HttpResponse('invalid data')

    if not getattr(u, 'usersettings'):
        us = UserSettings(user=u)
        us.save()

    if getattr(u.usersettings, b.cleaned_data['type']) == True:
        val = setattr(u.usersettings, b.cleaned_data['type'], False)
    else:
        val = setattr(u.usersettings, b.cleaned_data['type'], True)

    u.usersettings.save()

    return HttpResponse('success')
