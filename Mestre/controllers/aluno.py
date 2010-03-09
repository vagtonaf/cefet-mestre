# coding: utf8
# try something like

@auth.requires_login()
def cad_aluno():
    aluno = SQLFORM(db.aluno)
    if aluno.accepts(request.vars,session):
            redirect(URL(r=request,f='list_alunos'))
    if aluno.errors: response.flash='Erro em seu formulário'
    return dict(aluno=aluno)

@auth.requires_login()
def list_alunos():
   form=crud.create(db.aluno)
   alunos=db(db.aluno.matricula>0).select(
          db.aluno.matricula,
          db.aluno.usuario,
          db.aluno.id,
          db.auth_user.ALL,
          left=db.auth_user.on(db.aluno.usuario==db.auth_user.id),
          orderby=db.aluno.matricula
          )
   response.flash='Lista Alunos'
   return dict(alunos=alunos,form=form)

@auth.requires_login()
def edit_aluno():
   aluno_id=request.args(0)
   aluno=db.aluno[aluno_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.aluno,aluno,next=url('list_alunos'))
   return dict(form=form)
