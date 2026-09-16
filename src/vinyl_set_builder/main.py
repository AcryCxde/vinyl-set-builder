import os

from fastapi import FastAPI

from vinyl_set_builder.api import repository, router
from vinyl_set_builder.seed import seed_mock_tracks

app = FastAPI(title="Vinyl Set Builder")
app.include_router(router)

if os.getenv("VINYL_SEED_MOCKS"):
    seed_mock_tracks(repository)
