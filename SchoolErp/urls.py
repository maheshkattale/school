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
    path('teacher_master/', include(('teacher.urls','teacher'),namespace='teacher')),
    path('student/', include(('student.urls','student'),namespace='student')),
    path('academic/', include(('academic.urls','academic'),namespace='academic')),
    path('time_table_master/', include(('time_table.urls','time_table'),namespace='time_table')),
    path('subject_master/', include(('subject.urls','subject'),namespace='subject')),
    path('exam/', include(('exam.urls','exam'),namespace='exam')),
    path('messages/', include(('message.urls','message'),namespace='message')),
    path('designation_master/', include(('designation.urls','designation'),namespace='designation')),
    path('class_master/', include(('class.urls','class'),namespace='class')),
    path('parent_student_master/', include(('parent_student.urls','parent_student'),namespace='parent_student')),
    path('academic_calender/', include(('academic_calender.urls','academic_calender'),namespace='academic_calender')),
    path('user/',include(('user.urls','user'),namespace='user')),
    path('fees/',include(('fees.urls','fees'),namespace='fees')),
    path('attendance/',include(('attendance.urls','attendance'),namespace='attendance')),

    path('',include(('school.urls', 'school'),namespace='school')),

    # backend
    path('api/User/', include('User.urls')),
    path('api/SchoolMaster/', include('SchoolMaster.urls')),
    path('api/FeesMaster/', include('FeesMaster.urls')),
    path('api/DesignationMaster/', include('DesignationMaster.urls')),
    path('api/SubjectMaster/', include('SubjectMaster.urls')),
    path('api/TeacherMaster/', include('TeacherMaster.urls')),
    path('api/Parent_StudentMaster/', include('Parent_StudentMaster.urls')),
    path('api/ClassMaster/', include('ClassMaster.urls')),
    path('api/TimeTableMaster/', include('TimeTableMaster.urls')),
    path('api/MarksheetMaster/', include('MarksheetMaster.urls')),
    path('api/MessageMaster/', include('MessageMaster.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


