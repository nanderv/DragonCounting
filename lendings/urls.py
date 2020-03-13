from django.urls import path

from bellettrie_library_system.permissions import simple_path, PERM_ALL
from lendings.permissions import LENDING_VIEW, LENDING_LIST, LENDING_NEW_WORK, LENDING_FINALIZE, \
    LENDING_MY_LENDINGS

from members.views import MemberList
from . import views

urlpatterns = [
    path('', MemberList.as_view(), name=LENDING_LIST),
    path('work/<int:work_id>', views.work_based, name=LENDING_NEW_WORK),
    path('finalize/<int:work_id>/<int:member_id>', views.finalize, name=LENDING_FINALIZE),
    path('me/', views.me, name=LENDING_MY_LENDINGS),

]
