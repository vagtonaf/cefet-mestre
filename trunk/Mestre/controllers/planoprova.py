# coding: utf8
# try something like
   
@auth.requires_login()
def cad_planoprova():
    planoprova = SQLFORM(db.plano_de_prova)
    if planoprova.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_planoprova'))
    if planoprova.errors: response.flash='Erro em seu formulário'
    return dict(planoprova=planoprova)

def ver_planoprova():
    row_planoprova=db().select(db.plano_de_prova.ALL)
    return dict(row_planoprova=row_planoprova)


@auth.requires_login()
def list_planodeprovas():
   form=crud.create(db.plano_de_prova)
   form2=crud.create(db.item_plano_de_prova)
   professores=db(db.professor.id>0).select(db.professor.ALL)
   planodeprovas=db(db.plano_de_prova.id>0).select(db.plano_de_prova.ALL,db.item_plano_de_prova.ALL, left=db.item_plano_de_prova.on(db.item_plano_de_prova.plano_de_prova==db.plano_de_prova.id))
   planodeprovas.db(db.plano_de_prova.taxionomia>0).select(db.taxionomia.ALL,left=db.plano_de_prova.on(db.plano_de_prova.taxionomia==db.taxionomia.id))
   response.flash='Lista Plano de Prova'
   return dict(professores=professores,planodeprovas=planodeprovas,form=form,form2=form2)

@auth.requires_login()
def edit_planodeprova():
   planodeprova_id=request.args(0)
   planodeprova=db.plano_de_prova[planodeprova_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.plano_de_prova,planodeprova,next=url('list_planodeprovas'))
   return dict(form=form)