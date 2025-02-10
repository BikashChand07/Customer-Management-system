from django.urls import  path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home, name="home" ),
    # path('login/',views.login_user,name="login" ),
    path('logout/',views.logout_user, name="logout" ),
    path('register/',views.register_user, name="register" ),
    path('record/<int:pk>',views.customer_record, name="record" ), #  eg : record/<int:pk or id> = localhost:8000/record/2 , 2 = id of the record
    path('delete/<int:pk>',views.delete_record, name="delete-record" ),
    path('add_record/',views.add_record, name="add-record" ),
    path('update/<int:pk>',views.update_record, name="update-record" ),
    path('search_record',views.search_record, name="search-record" ),
]

