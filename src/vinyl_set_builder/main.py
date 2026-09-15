from fastapi import FastAPI

from vinyl_set_builder.api.routes import router

app = FastAPI(title="Vinyl Set Builder")
app.include_router(router)
