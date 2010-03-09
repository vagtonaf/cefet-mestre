# coding: utf8
# try something like

@auth.requires_login() 
def list_alocacoes():
  row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
  if row_professor:  
    form = SQLFORM(db.alocacao)
    if form.accepts(request.vars,session): 
            redirect(URL(r=request,f='list_alocacoes'))
    elif form.errors: response.flash='Erro em seu formulário'
    list_alunosA=db()._select(db.alocacao.aluno)
    list_alunos=db(~db.aluno.id.belongs(list_alunosA)).select(
          db.aluno.ALL,
          db.auth_user.ALL,
          left=db.auth_user.on(db.aluno.usuario==db.auth_user.id)
          )
    list_turmas=db(db.turma.id>0).select(db.turma.ALL,db.disciplina.ALL,left=db.disciplina.on(db.turma.disciplina==db.disciplina.id))
    list_alocados=db(db.aluno.id>0).select(
          db.alocacao.ALL,
          db.auth_user.ALL,
          left=db.auth_user.on(db.alocacao.aluno==db.auth_user.id),distinct=True
          )
    return dict(form=form,list_alunos=list_alunos,list_turmas=list_turmas,list_alocados=list_alocados)
  else:
    redirect(URL(r=request,f='../default/erro_acesso'))

@auth.requires_login()   
def ver_alocacao():
    row_alocacao=db().select(db.alocacao.ALL)
    return dict(row_alocacao=row_alocacao)

@auth.requires_login()   
def cad_alocacao():
  row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
  if row_professor:  
    alocacao = SQLFORM(db.alocacao)
    if alocacao.accepts(request.vars,session):
            redirect(URL(r=request,f='list_alocacoes'))
    if alocacao.errors: response.flash='Erro em seu formulário'
    return dict(alocacao=alocacao)
  else:
    redirect(URL(r=request,f='../default/erro_acesso'))
    
@auth.requires_login()
def edit_alocacao():
   alocacao_id=request.args(0)
   alocacao=db.alocacao[alocacao_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.alocacao,alocacao,next=url('list_alocacoes'))
   return dict(form=form)
