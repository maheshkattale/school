"""SchoolErp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacher_master/', include('teacher.urls')),
    path('time_table_master/', include('time_table.urls')),
    path('subject_master/', include('subject.urls')),
    path('designation_master/', include('designation.urls')),
    path('class_master/', include('class.urls')),
    path('parent_student_master/', include('parent_student.urls')),
    path('academic_calender/', include('academic_calender.urls')),
    path('user/', include('user.urls')),
    path('',include(('school.urls', 'school'),namespace='school')),

    # backend
    path('api/User/', include('User.urls')),
    path('api/SchoolMaster/', include('SchoolMaster.urls')),
    path('api/DesignationMaster/', include('DesignationMaster.urls')),
    path('api/SubjectMaster/', include('SubjectMaster.urls')),
    path('api/TeacherMaster/', include('TeacherMaster.urls')),
    path('api/Parent_StudentMaster/', include('Parent_StudentMaster.urls')),
    path('api/ClassMaster/', include('ClassMaster.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


