from User.models import User



def createschooladmin(adminemail,adminname,schoolcode,roleobject):
    User.objects.create(
            email=adminemail,
            Username = adminname,
            school_code = schoolcode,
            role = roleobject
        )