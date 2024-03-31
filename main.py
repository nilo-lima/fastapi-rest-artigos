from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

import descriptions_api_routers as dar

#api_description = "Esta API é uma solução RESTful projetada para facilitar a gestão de conteúdo e usuários em uma plataforma de publicação digital. Ela permite que aplicativos cliente realizem operações de CRUD (Create, Read, Update, Delete) em artigos, bem como gerenciem registros de usuários, incluindo autenticação e autorização."

app = FastAPI(
    title = dar.api_title,
    version = dar.api_version,
    description = dar.api_description
    )


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level='info', reload=True)
    
"""
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzEyNTE2OTg0LCJpYXQiOjE3MTE5MTIxODQsInN1YiI6IjEyIn0.Od4hW7ujWpL7uHEza8YsmzeMkJUnuQ1nxUVyTP6JWq0
Tipo: bearer
"""    
