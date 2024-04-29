import requests
from school.static_info import frontend_url


def getMenu(request):
    token = request.session.get('token')
    user_id = request.session.get('user_id')
    Menu = request.session.get('Menu')
    return {
        
            'user_id':user_id,
            'token':token,
            'frontend_url':frontend_url,
            'Menu':Menu,
            
            
            }