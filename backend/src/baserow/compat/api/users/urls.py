from django.urls import re_path

from .views import GroupUserCompatView, GroupUsersCompatView

app_name = "baserow.api.groups.users"

urlpatterns = [
    re_path(
        r"group/(?P<group_id>[0-9]+)/$", GroupUsersCompatView.as_view(), name="list"
    ),
    re_path(r"(?P<group_user_id>[0-9]+)/$", GroupUserCompatView.as_view(), name="item"),
]
