# coding: utf8
# try something like

def url(f,args=[]): return URL(r=request,f=f,args=args)

def button(text,action,args=[]):
    return SPAN('[',A(text,_href=URL(r=request,f=action,args=args)),']')

@auth.requires_login()
# Cadastra e Lista tabela simples
def cadlist():
    try:
        tabela=request.args(0) or redirect(URL(r=request,f='../default/error'))
        form=crud.create(db[tabela])
        if form.accepts(request.vars,session): 
            redirect(URL(r=request,f='../default/error'))
        elif form.errors: response.flash='Erro em seu formulário'
        row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
	# aqui no if somente as tabelas que tem um select especial valeu
        if tabela=='aluno':
            if row_professor:
                registros=db(db.aluno.matricula>0).select(
                    db.aluno.matricula,
                    db.aluno.usuario,
                    db.aluno.id,
                    db.auth_user.ALL,
                    left=db.auth_user.on(db.aluno.usuario==db.auth_user.id),
                orderby=db.aluno.matricula
                )
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
        elif tabela=='professor':
            registros=db(db.professor.id>0).select(
                db.professor.ALL,
                db.auth_user.ALL,
                left=db.auth_user.on(db.professor.usuario==db.auth_user.id)
            )
        elif tabela=='alocacao':
            if row_professor:  
                list_alunosA=db()._select(db.alocacao.aluno)
                list_alunos=db(~db.aluno.id.belongs(list_alunosA)).select(
                    db.aluno.ALL,
                    db.auth_user.ALL,
                    left=db.auth_user.on(db.aluno.usuario==db.auth_user.id)
                )
                list_turmas=db(db.turma.id>0).select(
                    db.turma.ALL,
                    db.disciplina.ALL,
                    left=db.disciplina.on(db.turma.disciplina==db.disciplina.id))
                registros=db(db.aluno.id>0).select(
                    db.alocacao.ALL,
                    db.auth_user.ALL,
                    left=db.auth_user.on(db.alocacao.aluno==db.auth_user.id),distinct=True
                )
		return dict(registros=registros,form=form, tabela=tabela, list_turmas=list_turmas, ist_aluno=ist_aluno)
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
            response.flash='Cadastra e Lista ' + tabela
            return dict(registros=registros, form=form, list_turmas=list_turmas, list_alunos=list_alunos, tabela=tabela)
        elif tabela=='disciplina':
            if row_professor:
                registros= disciplinas=db(db.disciplina.id>0).select(
                    db.disciplina.ALL,
                    db.curso.ALL,
                    left=db.curso.on(db.disciplina.curso==db.curso.id)
                )  
	elif tabela=='plano_de_prova':
            if row_professor:
		form2=crud.create(db.item_plano_de_prova)
		professores=db(db.professor.id>0).select(db.professor.ALL)
		registros=db(db.plano_de_prova.id>0).select(
			db.plano_de_prova.ALL,
			db.item_plano_de_prova.ALL,
			left=db.item_plano_de_prova.on(db.item_plano_de_prova.plano_de_prova==db.plano_de_prova.id)
		)
		registros.db(db.plano_de_prova.taxionomia>0).select(db.taxionomia.ALL,left=db.plano_de_prova.on(db.plano_de_prova.taxionomia==db.taxionomia.id))
		response.flash='Lista Plano de Prova'
		return dict(registros=registros, professores=professores, form=form, form2=form2, tabela=tabela)
        elif tabela=='prova':
		registros=db(db.prova.id>0).select(db.prova.ALL)
		turmas=db(db.turma.id>0).select(db.turma.ALL)
		if 'auth' in globals():
			if auth.is_logged_in(): 
				planoprovas=db(db.plano_de_prova.id>0).select(db.plano_de_prova.ALL,db.professor.ALL,left=db.professor.on( (db.professor.id==db.plano_de_prova.professor )& (db.professor.usuario==auth.user.id)))
				response.flash='Lista Prova'
				return dict(registros=registros, turmas=turmas, planoprovas=planoprovas, form=form, tabela=tabela)
                        else:
				redirect(URL(r=request,f='../default/erro_acesso'))
                else:
			redirect(URL(r=request,f='../default/erro_acesso'))
	else:
		# esse é um select genérico, serve para a maioria das tabelas
		registros=db(db[tabela].id>0).select(db[tabela].ALL)
    except KeyError, NameError:
	tabela='error'
        response.flash='Tabela Inexistente!'
        form=''
        return dict(form=form, registros='Não posso listar esta tabela!', tabela=tabela)   
    response.flash='Cadastra e Lista ' + tabela
    return dict(registros=registros,form=form, tabela=tabela)

@auth.requires_login()
# Edita tabela simples
def edit():
    #só deixa editar se for professor
    row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
    if row_professor:
        tabela=request.args(0) or redirect(URL(r=request,f='../default/error'))
        registro_id=request.args(1) or redirect(URL(r=request,f='../default/error'))
        registros=db[tabela][registro_id] or redirect(URL(r=request,f='../default/error'))
	#if not registros: raise HTTP(404)
        form=crud.update(db[tabela],registros,next=url('Cadlist/'+ tabela))
        return dict(form=form, tabela=tabela)
    else:
        redirect(URL(r=request,f='../default/erro_acesso'))

