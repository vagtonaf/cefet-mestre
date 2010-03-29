# coding: utf8
# try something like
    

@auth.requires_login()
def cad_topico():
    topico = SQLFORM(db.topico)
    if topico.accepts(request.vars,session):
            redirect(URL(r=request,f='list_topicos'))
    if topico.errors: response.flash='Erro em seu formulário'
    return dict(topico=topico)
    
def ver_topico():
    row_topico=db().select(db.topico.ALL)
    return dict(row_topico=row_topico)

   
@auth.requires_login()
def list_topicos():
   form=crud.create(db.topico)
   topicos=db(db.topico.id>0).select(db.topico.ALL)
   response.flash='Lista Tópico'
   return dict(topicos=topicos,form=form)

@auth.requires_login()
def edit_topico():
   topico_id=request.args(0)
   topico=db.topico[topico_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.topico,topico,next=url('list_topicos'))
   return dict(form=form)
