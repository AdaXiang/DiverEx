import os

class Settings:
    MEMGRAPH_HOST = os.getenv("MEMGRAPH_HOST", "localhost")
    MEMGRAPH_PORT = os.getenv("MEMGRAPH_PORT", "7687")
    MEMGRAPH_USER = os.getenv("MEMGRAPH_USER", "")
    MEMGRAPH_PASSWORD = os.getenv("MEMGRAPH_PASSWORD", "")

    MEMGRAPH_URL = os.getenv(
        "MEMGRAPH_URL",
        f"bolt://{MEMGRAPH_HOST}:{MEMGRAPH_PORT}"
    )


settings = Settings()