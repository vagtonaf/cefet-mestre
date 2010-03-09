# coding: utf8
# try something like

def cad_disciplina():
    disciplina = SQLFORM(db.disciplina)
    if disciplina.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_disciplina'))
    if disciplina.errors: response.flash='Erro em seu formulário'
    return dict(disciplina=disciplina)

def ver_disciplina():
    row_disciplina=db().select(db.disciplina.ALL)
    return dict(row_disciplina=row_disciplina)

 
@auth.requires_login()
def list_disciplinas():
   form=crud.create(db.disciplina)
   disciplinas=db(db.disciplina.id>0).select(db.disciplina.ALL,db.curso.ALL,left=db.curso.on(db.disciplina.curso==db.curso.id))
   response.flash='Lista de Disciplina'
   return dict(disciplinas=disciplinas,form=form)

@auth.requires_login()
def edit_disciplina():
   disciplina_id=request.args(0)
   disciplinas=db.disciplina[disciplina_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.disciplina,disciplinas,next=url('list_disciplinas'))
   return dict(form=form)
