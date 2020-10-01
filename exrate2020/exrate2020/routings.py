from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# import chat.routing
# import rentalhouse.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            # chat.routing.websocket_urlpatterns,
            # rentalhouse.routing.websocket_urlpatterns,
        )
    ),
})