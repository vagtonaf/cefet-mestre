# coding: utf8
# try something like


@auth.requires_login()
# Cadastra e Lista tabela simples
def cadlist():
    try:
        tabela=request.args(0) or redirect(URL(r=request,f='../default/error'))
        form=crud.create(db[tabela])
        if form.accepts(request.vars,session): 
            redirect(URL(r=request,f='../default/error'))
        elif form.errors: response.flash='Erro em seu formulário'
        if tabela=='aluno':
            row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
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
            row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
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
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
            response.flash='Cadastra e Lista ' + tabela
            return dict(registros=registros, form=form, tabela=tabela, list_turmas=list_turmas, list_alunos=list_alunos)
        else:
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
    row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
    if row_professor:
        tabela=request.args(0) or redirect(URL(r=request,f='../default/error'))
        registro_id=request.args(1) or redirect(URL(r=request,f='../default/error'))
        registros=db[tabela][registro_id] or redirect(URL(r=request,f='../default/error'))
        form=crud.update(db[tabela],registros,next=url('Cadlist/'+ tabela))
        return dict(form=form, tabela=tabela)
    else:
        redirect(URL(r=request,f='../default/erro_acesso'))
