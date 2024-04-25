import requests
from school.static_info import frontend_url


def getMenu(request):
    token = request.session.get('token')
    return {
            'token':token,
            'frontend_url':frontend_url,
            }