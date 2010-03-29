# coding: utf8
# try something like

@auth.requires_login()
def cad_prova():
    prova = SQLFORM(db.prova)
    if prova.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_prova'))
    if prova.errors: response.flash='Erro em seu formulário'
    return dict(prova=prova)

def ver_prova():
    row_prova=db().select(db.prova.ALL)
    return dict(row_prova=row_prova)

@auth.requires_login()
def list_provas():
   form=crud.create(db.prova)
   provas=db(db.prova.id>0).select(db.prova.ALL)
   turmas=db(db.turma.id>0).select(db.turma.ALL)
   if 'auth' in globals():
       if auth.is_logged_in(): planoprovas=db(db.plano_de_prova.id>0).select(db.plano_de_prova.ALL,db.professor.ALL,left=db.professor.on( (db.professor.id==db.plano_de_prova.professor )& (db.professor.usuario==auth.user.id)))
   response.flash='Lista Prova'
   return dict(provas=provas,turmas=turmas,planoprovas=planoprovas, form=form)

@auth.requires_login()
def edit_prova():
   prova_id=request.args(0)
   prova=db.prova[prova_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.prova,prova,next=url('list_provas'))
   return dict(form=form)
