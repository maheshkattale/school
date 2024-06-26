import requests
from school.static_info import frontend_url


def getMenu(request):
    token = request.session.get('token')
    user_id = request.session.get('user_id')
    Menu = request.session.get('Menu')
    username = request.session.get('username')
    mobileNumber = request.session.get('mobileNumber')
    Address = request.session.get('Address')
    email = request.session.get('email')
    roleid = request.session.get('roleid')
    children_list = request.session.get('children_list')
    PrimaryStudentId = request.session.get('PrimaryStudentId')
    PrimaryStudentCode = request.session.get('PrimaryStudentCode')
    school_logo = request.session.get('school_logo')
    user_role_name = request.session.get('user_role_name')
    profile_image=request.session.get('profile_image')
    school_name=request.session.get('school_name')

    return {
        
            'user_id':user_id,
            'token':token,
            'frontend_url':frontend_url,
            'Menu':Menu,
            'email':email,
            'mobileNumber':mobileNumber,
            'Address':Address,
            'roleid':roleid,
            'children_list':children_list,
            'PrimaryStudentId':PrimaryStudentId,
            'PrimaryStudentCode':PrimaryStudentCode,
            'username':username,
            'school_logo':school_logo,
            'user_role_name':user_role_name,
            'school_name':school_name,
            'profile_image':profile_image,
            
            
            }