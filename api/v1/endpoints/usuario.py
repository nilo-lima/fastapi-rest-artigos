from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaArtigos, UsuarioSchemaUp
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

import descriptions_api_routers as dar


router = APIRouter()

# GET Logado
@router.get('/logado', response_model=UsuarioSchemaBase,summary=dar.usuario_get_logado_summary)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    """
    Retorna os detalhes do usuário atualmente logado.

    Requer que o usuário esteja autenticado e inclua o token JWT no cabeçalho de autorização da requisição.
    """    
    return usuario_logado


# POST SignUp
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase, summary=dar.usuario_post_sign_summary)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    """
    Cria um novo usuário na plataforma com as informações fornecidas.

    - **nome**: Nome do usuário.
    - **sobrenome**: Sobrenome do usuário.
    - **email**: Email do usuário, que será usado como login.
    - **senha**: Senha do usuário para autenticação.
    - **eh_admin** (opcional): Indica se o usuário possui privilégios administrativos (padrão: `False`).

    Retorna os detalhes básicos do usuário registrado, excluindo a senha por motivos de segurança.
    """    
    novo_usuario: UsuarioModel = UsuarioModel(nome=usuario.nome, sobrenome=usuario.sobrenome,
                                              email=usuario.email, senha=gerar_hash_senha(usuario.senha), eh_admin=usuario.eh_admin)
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
        
            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com este email cadastrado.')
    

# GET Usuarios
@router.get('/', response_model=List[UsuarioSchemaBase], summary="Lista todos os artigos")
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    """
    Lista todos os artigos disponíveis na plataforma. Este endpoint é acessível publicamente.
    """    
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        
        return usuarios
    

# GET Usuario
@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK, summary=dar.artigo_get_summary)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    """
    Retorna os detalhes de um artigo específico pelo ID fornecido.

    - **artigo_id** (int): O ID único do artigo a ser obtido.
    """    
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        
        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)
            
            
# PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED, summary=dar.usuario_put_summary)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    """
    Atualiza os detalhes de um usuário específico com base no `usuario_id` fornecido.

    - **nome** (opcional): Novo nome do usuário.
    - **sobrenome** (opcional): Novo sobrenome do usuário.
    - **email** (opcional): Novo email do usuário.
    - **senha** (opcional): Nova senha do usuário.
    - **eh_admin** (opcional): Indica se o usuário deve ter privilégios administrativos.

    Requer autenticação e que o usuário seja o próprio ou um administrador.
    """
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)

            await session.commit()

            return usuario_up
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)   
            
            
# DELETE Usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT, summary=dar.usuario_delete_summary)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    """
    Remove um usuário específico da plataforma com base no `usuario_id` fornecido.

    Requer autenticação e que o usuário seja o próprio ou um administrador.
    """    
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        
        print(f"Delete usuario {usuario_del}")

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)   
            
            
@router.post('/login', summary=dar.usuario_post_login_summary)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    """
    Autentica um usuário na plataforma utilizando email e senha.

    O endpoint espera um formulário com os campos `username` (que deve ser o email do usuário) e `password`.
    Em caso de sucesso, retorna um token JWT para ser usado em requisições subsequentes que requerem autenticação.
    """    
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')
        
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)