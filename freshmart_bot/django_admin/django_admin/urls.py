from django.contrib import admin
from django.urls import path, include
import sys
print("DEBUG: chatbot.urls included", file=sys.stderr)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chatbot/', include('chatbot.urls')),  # ✅ this is perfect
]
