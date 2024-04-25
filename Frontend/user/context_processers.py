import requests

frontendURL = 'http://127.0.0.1:8000/'


def getMenu(request):
    token = request.session.get('token')
    return {
            'token':token,
            'frontendURL':frontendURL,
            }