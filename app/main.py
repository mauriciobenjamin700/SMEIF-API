
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


from database.models import create_tables
from routes.classes import router as classes_router
from routes.disciplines import router as disciplines_router
from routes.user import router as user_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)


app.include_router(classes_router)
app.include_router(disciplines_router)
app.include_router(user_router)


@app.get('/')
def main():
    return {"detail": "API rodando!"}

# Executando o servidor
if __name__ == "__main__":

    create_tables()

    config = uvicorn.Config("main:app", 
                            port=5000,
                            host='0.0.0.0', 
                            log_level="info", 
                            reload=True)
    server = uvicorn.Server(config)
    server.run()