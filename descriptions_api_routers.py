api_description = "Esta API é uma solução RESTful projetada para facilitar a gestão de conteúdo e usuários em uma plataforma de publicação digital. Ela permite que aplicativos cliente realizem operações de CRUD (Create, Read, Update, Delete) em artigos, bem como gerenciem registros de usuários, incluindo autenticação e autorização."
api_title = 'API para Cadastro de Artigos e Usuários'
api_version = '0.0.1'

#artigo_post_description = "Este endpoint permite que um usuário autenticado crie um novo artigo fornecendo detalhes como título, descrição e URL fonte. O usuario_id é automaticamente derivado do token de acesso do usuário logado."
artigo_post_summary = "Cria um novo artigo"
artigo_response_description="Artigo gravado com sucesso!"

artigo_get_summary = 'Obtém um artigo específico'
artigo_get_response_description='Artigo recuperado com sucesso'

artigo_get_all_summary = 'Lista todos os artigos'
artigo_get_all_response_description='Artigos recuperados com sucesso'

artigo_put_summary = 'Atualiza um artigo existente'
artigo_put_response_description = 'Artigo atualizado com sucesso'

artigo_delete_summary = 'Deleta um artigo específico'
artigo_delete_response_description = 'Artigo deletado com sucesso'

usuario_post_sign_summary = 'Registra um novo usuário'
usuario_post_login_summary = 'Autentica um usuário'

usuario_get_logado_summary = 'Obtém detalhes do usuário logado'
usuario_put_summary = 'Atualiza um usuário existente'
usuario_delete_summary = 'Deleta um usuário específico'
usuario_get_all_summary = 'Lista todos os artigos'
usuario_get_summary = 'Obtém detalhes de um artigo específico'
