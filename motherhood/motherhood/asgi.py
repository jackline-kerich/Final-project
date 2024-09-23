"""
ASGI config for motherhood project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from nurturewell import routing  # Update this line to reflect your app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motherhood.settings')  # Update to your project name

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Use the routing from your app
        )
    ),
})
