import uvicorn
from cryptobalance.api.routers.history_router import History_Router
from cryptobalance.api.uvicorn import UvicornServer

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class Server:
    def __init__(self, config, logger, loop, history_handler):
        self.config = config
        self.logger = logger
        self.loop = loop
        app = FastAPI(
            redoc_url=None,
            docs_url="/",
            title="CryptoBalance",
            description="CryptoBalance backend API",
            log_level="trace"
        )
        @app.get("/api/ping")
        async def pong():
            return("pong")
        
        self.app = app
        deps = {}
        deps["config"] = config
        deps["logger"] = logger
        deps["history_handler"] = history_handler
        
        self.app.state.dependencies = deps

        self.app.include_router(
            History_Router, prefix="/api/history", tags=["Historic Data"]
        )

        origins = ["*"]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        uvi_conf = uvicorn.Config(
            app=self.app,
            loop="asyncio",
            host=self.config["API_ADDRESS"],  # nosec
            port=self.config["API_PORT"],
            reload=True,
            debug=True,
        )

        self.server = UvicornServer(uvi_conf)

    def start(self):
        """
        Start the server
        """
        self.loop.create_task(self.server.serve())