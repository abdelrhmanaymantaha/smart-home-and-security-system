from app import app
from asgiref.wsgi import WsgiToAsgi

asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host="127.0.0.1", port=8000, log_level="info")