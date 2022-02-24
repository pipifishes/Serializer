from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 指向内置Admin后台系统的路由文件sites.py
    # admin代表127.0.0.1:8000/admin
    path('admin/', admin.site.urls),
    # 指向应用程序的路由文件urls.py
    path('', include('temp_app.urls'))

]

# 设置404，500错误状态码
from temp_app import views
handler404 = views.page_not_found
handler500 = views.page_error