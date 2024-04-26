import requests
from school.static_info import frontend_url


def getMenu(request):
    token = request.session.get('token')
    user_id = request.session.get('user_id')
    return {
            'user_id':user_id,
            'token':token,
            'frontend_url':frontend_url,
            }