# coding: utf8
# try something like

def cad_turma():
    turma = SQLFORM(db.turma)
    if turma.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_turma'))
    if turma.errors: response.flash='Erro em seu formulário'
    return dict(turma=turma)

def ver_turma():
    row_turma=db().select(db.turma.ALL)
    return dict(row_turma=row_turma)
    
def teste_turma():
    row_alocacao = db(db.alocacao.aluno==auth.user.id).select(db.alocacao.ALL)
    id = row_alocacao.alocacao.turma
    row_turma = db().select(db.turma.ALL)
    return dict(row_turma=row_turma)
    
@auth.requires_login()
def list_turmas():
   form=crud.create(db.turma)
   turmas=db(db.turma.id>0).select(db.turma.ALL,db.disciplina.ALL,orderby=db.turma.nome,left=db.disciplina.on(db.turma.disciplina==db.disciplina.id))
   response.flash='Lista Turma'
   return dict(turmas=turmas,form=form)

@auth.requires_login()
def edit_turma():
   turma_id=request.args(0)
   turma=db.turma[turma_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.turma,turma,next=url('list_turmas'))
   return dict(form=form)
