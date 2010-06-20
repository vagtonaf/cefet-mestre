# coding: utf8

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('Mecanismo Sinergico de Treinamento')

##########################################
## this is the authentication menu
## remove if not necessary
##########################################

if 'auth' in globals():
    if not auth.is_logged_in():
       response.menu_auth = [
           ['Logar', False, auth.settings.login_url,
                [
                   ['Registrar', False,
                    URL(request.application,'default','user/register')],
                   ['Esqueci a Senha', False,
                    URL(request.application,'default','user/retrieve_password')]]
            ],
       ]
       response.menu = [
          [T('Principal'), 
           False, 
           URL(request.application,'default','index'), []
          ],
          [T('Créditos'), 
           False, 
           URL(request.application,'default','index'), []
          ],
       ]
    else:
       row_admins=db(db.administrador.usuario==auth.user.id).select(db.administrador.ALL)
       if row_admins:
          response.menu_auth = [
            ['Admin: '+auth.user.first_name,False,None,
                 [
                    ['Deslogar', False, 
                     URL(request.application,'default','user/logout')],
                    ['Alterar Perfil', False, 
                     URL(request.application,'default','user/profile')],
                    ['Mudar a Senha', False,
                     URL(request.application,'default','user/change_password')],
                    ['Menu de Administração', False,
                     URL('admin','default','index')],
                    ['Tabelas', False, 
                     URL(request.application,'appadmin','index')],
                    ['Administrador', False, URL(request.application,'mcrud','cadlist/administrador')]
                ]
             ],
           ]
       else:
          response.menu_auth = [
            ['Usuario: '+auth.user.first_name,False,None,
                 [
                    [T('Deslogar'), False, 
                     URL(request.application,'default','user/logout')],
                    [T('Alterar Perfil'), False, 
                     URL(request.application,'default','user/profile')],
                 ]
             ],
           ]
       row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
       if row_professor:
         response.menu = [
                ['Cadastros', 
                 False, 
                 URL(request.application,'default','index'), 
                      [
                       ['Usuário', 
                            False, 
                            URL(request.application,'mcrud','cadlist/auth_user'), [
                            ['Professor', 
                                    False, 
                                    URL(request.application,'mcrud','cadlist/professor'), []
                            ],
                            ['Aluno', 
                                    False, 
                                    URL(request.application,'mcrud','cadlist/aluno'), []
                            ],          
                           ]
                       ],
                       ['Instituição', 
                            False, 
                            URL(request.application,'mcrud','cadlist/instituicao'), [
                            ['Curso', 
                                    False, 
                                    URL(request.application,'mcrud','cadlist/curso'), []
                            ],          
                            ['Disciplina', 
                                    False, 
                                    URL(request.application,'mcrud','cadlist/disciplina'), []
                            ],                  
                            ['Turma', 
                                    False, 
                                    URL(request.application,'mcrud','cadlist/turma'), []
                            ],      
                            ['Alocação', 
                                    False, 
                                    URL(request.application,'mcrud','cadlist/alocacao'), []
                            ],             
                           ]
                       ],
                       ['Plano de Prova', 
                            False, 
                            URL(request.application,'mcrud','cadlist/plano_de_prova'), [
                                   ['Item Plano de Prova', 
                                            False, 
                                            URL(request.application,'mcrud','cadlist/item_plano_de_prova'), []
                                   ], 
                            ]
                       ],                  
                       ['Prova', 
                            False, 
                            URL(request.application,'mcrud','cadlist/prova'), [
                                    ['Tópico', 
                                            False, 
                                            URL(request.application,'mcrud','cadlist/topico'), []
                                    ],
                                    ['Questão', 
                                            False, 
                                            URL(request.application,'mcrud','cadlist/questao'), []
                                    ],     
                                    ['Alternativa', 
                                            False, 
                                            URL(request.application,'mcrud','cadlist/alternativa'), []
                                    ],
                            ]
                       ],  
                      ]             
               ],
               ['Aplicações', 
                    False, 
                    URL(request.application,'aplicaprova','aplicar_prova'), [
                                   ['Aplicar Prova', 
                                            False, 
                                            URL(request.application,'aplicaprova','aplicar_prova'), []
                                   ],
                    ]
               ],
               ['Relatórios', 
                 False, 
                 URL(request.application,'default','index'), [
                       ['Cadastros', 
                            False, 
                            URL(request.application,'default','index'), [
                           ['Lista Usuário', 
                            False, 
                            URL(request.application,'mcrud','cadlist/auth_user/list'), []
                           ],
                           ['Lista Professor', 
                            False, 
                            URL(request.application,'mcrud','cadlist/professor/list'), []
                           ],
                           ['Lista Aluno', 
                            False, 
                            URL(request.application,'mcrud','cadlist/aluno/list'), []
                           ],
                           ['Lista Instituição', 
                            False, 
                            URL(request.application,'mcrud','cadlist/instituicao/list'), []
                           ],
                           ['Lista Curso', 
                            False, 
                            URL(request.application,'mcrud','cadlist/curso/list'), []
                           ],
                           ['Lista Disciplina', 
                            False, 
                            URL(request.application,'mcrud','cadlist/disciplina/list'), []
                               ],
                           ['Lista Turma', 
                            False, 
                            URL(request.application,'mcrud','cadlist/turma/list'), []
                           ],
                           ['Lista Alocação', 
                            False, 
                            URL(request.application,'mcrud','cadlist/alocacao/list'), []
                           ],
                           ['Lista Tópico', 
                            False, 
                            URL(request.application,'mcrud','cadlist/topico/list'), []
                           ],
                           ['Lista Questão', 
                            False, 
                            URL(request.application,'mcrud','cadlist/questao/list'), []
                           ],
                           ['Lista Plano de Prova', 
                            False, 
                            URL(request.application,'mcrud','cadlist/plano_de_prova/list'), []
                           ],
                           ['Lista Prova', 
                            False, 
                            URL(request.application,'mcrud','cadlist/prova/list'), []
                           ],
                           ['Lista Prova Gerada', 
                            False, 
                            URL(request.application,'mcrud','cadlist/prova_gerada/list'), []
                           ],
                         ]  
                       ],    
                       ['Resultado Prova', 
                            False, 
                            URL(request.application,'resultadoprova','resultadoprova'), []
                       ],
                       ['Turma por Aluno', 
                            False, 
                            URL(request.application,'relatorio','rel/Turma_Aluno'), []
                       ],
                       ['Turma por Aluno e Disciplina', 
                            False, 
                            URL(request.application,'relatorio','rel/Turma_Aluno_Disciplina'), []
                       ],
                       ['Gráfico Notas Alunos', 
                            False, 
                            URL(request.application,'relatorios','graf_bar'), []
                       ],
                       ['Gráfico Taxonomias', 
                            False, 
                            URL(request.application,'grafico','grafico'), []
                       ],
                       ['Professor (Em Construção)', 
                            False, 
                            URL(request.application,'util','construcao'), []
                       ],
                       ['Turma (Em Construção)', 
                            False, 
                            URL(request.application,'util','construcao'), []
                       ],
                  ]
               ],
        [T('Créditos'), 
         False, 
         URL(request.application,'util','creditos'), []
        ],
       ]
       else:
        response.menu = [
               ['Realiza Prova', 
                     False, 
                     URL(request.application,'realizaprova','realizar_prova'), []
               ],
               ['Relatorios', 
                 False, 
                 URL(request.application,'default','index'), [
                       ['Resultado da Prova', 
                            False, 
                            URL(request.application,'resultadoaluno','nota_aluno/' + str(auth.user.id)), []
                       ],
                       ['Gabarito da Prova (Em Construção)', 
                            False, 
                            URL(request.application,'util','construcao'), []
                       ],
                  ]
               ],
        [T('Créditos'), 
         False, 
         URL(request.application,'util','creditos'), []
        ],
       ]
##########################################
## this is here to provide shortcuts
## during development. remove in production 
##########################################

response.menu_edit=[
  [T('Alterar'), False, URL('admin', 'default', 'design/%s' % request.application),
   [
            [T('Controller'), False, 
             URL('admin', 'default', 'edit/%s/controllers/default.py' \
                     % request.application)],
            [T('View'), False, 
             URL('admin', 'default', 'edit/%s/views/%s' \
                     % (request.application,response.view))],
            [T('Layout'), False, 
             URL('admin', 'default', 'edit/%s/views/layout.html' \
                     % request.application)],
            [T('Stylesheet'), False, 
             URL('admin', 'default', 'edit/%s/static/base.css' \
                     % request.application)],
            [T('DB Model'), False, 
             URL('admin', 'default', 'edit/%s/models/db.py' \
                     % request.application)],
            [T('Menu Model'), False, 
             URL('admin', 'default', 'edit/%s/models/menu.py' \
                     % request.application)],
            [T('Database'), False, 
             URL(request.application, 'appadmin', 'index')],
            ]
   ],
  ]
