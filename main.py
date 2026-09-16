from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importe seu router de chat aqui (exemplo)
from api.routes.chat import router as chat_router 

app = FastAPI()

# Configuração de CORS (importante para o React conseguir falar com o backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Certifique-se de que o prefixo bate com o que o frontend chama ('/chat/')
app.include_router(chat_router, prefix="/chat")