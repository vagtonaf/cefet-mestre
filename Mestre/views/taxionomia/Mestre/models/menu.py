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
           [T('Login'), False, auth.settings.login_url,
                [
                   [T('Register'), False,
                    URL(request.application,'default','user/register')],
                   [T('Lost Password'), False,
                    URL(request.application,'default','user/retrieve_password')]]
            ],
       ]
       response.menu = [
          [T('Index'), 
           False, 
           URL(request.application,'default','index'), []
          ],
          [T('Creditos'), 
           False, 
           URL(request.application,'default','index'), []
          ],
       ]
    else:
       response.menu_auth = [
            ['user: '+auth.user.first_name,False,None,
                 [
                    [T('Logout'), False, 
                     URL(request.application,'default','user/logout')],
                    [T('Edit Profile'), False, 
                     URL(request.application,'default','user/profile')],
                    [T('Change Password'), False,
                     URL(request.application,'default','user/change_password')],
                    [T('Administration'), False,
                     URL('admin','default','index')]           
                 ]
             ],
       ]
       row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
       if row_professor:
         response.menu = [
            [T('Index'), 
             False, 
             URL(request.application,'default','index'), []
            ],
                ['Cadastros', 
                 False, 
                 URL(request.application,'appcadastro','index'), 
                      [
                       ['Usuario', 
                            False, 
                            URL(request.application,'mcrud','cadlist/usuario'), [
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
                       ['Instituicao', 
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
                            		URL(request.application,'turma','cad_turma'), [
                       				['Alocacao', 
                            				False, 
                            				URL(request.application,'alocacao','cad_alocacao'), []
                       				],						
						
						]
                       		],				    
				    
			]
                       ],


                       ['Plano de Prova', 
                            False, 
                            URL(request.application,'planoprova','cad_planoprova'), [
                       		['Prova', 
                            		False, 
                            		URL(request.application,'prova','cad_prova'), [
						
						['Topico', 
                            				False, 
                            				URL(request.application,'topico','cad_topico'), []
                       				],
                       				['Questao', 
                            				False, 
                            				URL(request.application,'questao','cad_questao'), []
                       				],     
                       				['Alternativa', 
                            				False, 
                            				URL(request.application,'alternativa','cad_alternativa'), []
                       				],
						
						
					]
                       		],				    
				
                       		['Aplicar Prova', 
                            		False, 
                            		URL(request.application,'aplicaprova','aplicar_prova'), []
                       		],
                       		['Realiza Prova', 
                            		False, 
                            		URL(request.application,'realizaprova','realizar_prova'), []
                       		],

				    ]
                       ],


                      ]

               ],
               ['Relatorios', 
                 False, 
                 URL(request.application,'appcadastro','index'), [
                       ['Usuario', 
                            False, 
                            URL(request.application,'usuario','list_usuarios'), []
                       ],
                       ['Professor', 
                            False, 
                            URL(request.application,'professor','list_professores'), []
                       ],
                       ['Aluno', 
                            False, 
                            URL(request.application,'aluno','list_alunos'), []
                       ],
                       ['Instituicao', 
                            False, 
                            URL(request.application,'instituicao','list_instituicoes'), []
                       ],
                       ['Curso', 
                            False, 
                            URL(request.application,'curso','list_cursos'), []
                       ],
                       ['Disciplina', 
                            False, 
                            URL(request.application,'disciplina','list_disciplinas'), []
                       ],
                       ['Turma', 
                            False, 
                            URL(request.application,'turma','list_turmas'), []
                       ],
                       ['Alocacao', 
                            False, 
                            URL(request.application,'alocacao','list_alocacoes'), []
                       ],
                       ['Topico', 
                            False, 
                            URL(request.application,'topico','list_topicos'), []
                       ],
                       ['Questao', 
                            False, 
                            URL(request.application,'questao','list_questoes'), []
                       ],
                       ['Plano de Prova', 
                            False, 
                            URL(request.application,'planoprova','list_planodeprovas'), []
                       ],
                       ['Prova', 
                            False, 
                            URL(request.application,'prova','list_provas'), []
                       ],
                       ['Gerar Relatorio por Aluno', 
                            False, 
                            URL(request.application,'aluno','ver_relAluno'), []
                       ],
                       ['Gerar Relatorio por Aluno', 
                            False, 
                            URL(request.application,'aluno','ver_relAluno'), []
                       ],
                       ['Gerar Relatorio por Professor', 
                            False, 
                            URL(request.application,'professor','ver_relProfessor'), []
                       ],
                       ['Gerar Relatorio de Resultados Por Turma', 
                            False, 
                            URL(request.application,'turma','ver_relTurma'), []
                       ],
                  ]
               ],
        [T('Creditos'), 
         False, 
         URL(request.application,'default','index'), []
        ],
       ]
       else:
        response.menu = [
            [T('Index'), 
             False, 
             URL(request.application,'default','index'), []
            ],
                ['Cadastros', 
                 False, 
                 URL(request.application,'uteis','index'), [
                       ['Realiza Prova', 
                            False, 
                            URL(request.application,'realizaprova','realizar_prova'), []
                       ],
                      ]

               ],
               ['Relatorios', 
                 False, 
                 URL(request.application,'appcadastro','index'), [
                       ['Gerar Relatorio por Aluno', 
                            False, 
                            URL(request.application,'aluno','ver_relAluno'), []
                       ],
                       ['Gerar Relatorio por Aluno', 
                            False, 
                            URL(request.application,'aluno','ver_relAluno'), []
                       ],
                       ['Gerar Relatorio por Professor', 
                            False, 
                            URL(request.application,'professor','ver_relProfessor'), []
                       ],
                       ['Gerar Relatorio de Resultados Por Turma', 
                            False, 
                            URL(request.application,'turma','ver_relTurma'), []
                       ],
                  ]
               ],
        [T('Creditos'), 
         False, 
         URL(request.application,'default','creditos'), []
        ],
       ]
##########################################
## this is here to provide shortcuts
## during development. remove in production 
##########################################

response.menu_edit=[
  [T('Edit'), False, URL('admin', 'default', 'design/%s' % request.application),
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
