# coding: utf8
# try something like

@auth.requires_login()
def cad_alternativa():
    alternativa = SQLFORM(db.alternativa)
    if alternativa.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_alternativa'))
    if alternativa.errors: response.flash='Erro em seu formulário'
    return dict(alternativa=alternativa)

def ver_alternativa():
    row_alternativa=db().select(db.alternativa.ALL)
    return dict(row_alternativa=row_alternativa)
    
@auth.requires_login()
def list_alternativas():
   form=crud.create(db.alternativa)
   alternativas=db(db.alternativa.id>0).select(db.alternativa.ALL)
   response.flash='Lista Alternativa'
   return dict(alternativas=alternativas,form=form)

@auth.requires_login()
def edit_alternativa():
   alternativa_id=request.args(0)
   alternativa=db.alternativa[alternativa_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.alternativa,alternativa,next=url('list_alternativas'))
   return dict(form=form)
