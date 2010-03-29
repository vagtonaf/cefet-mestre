# coding: utf8
# try something like

def cad_taxionomia():
    taxionomia = SQLFORM(db.taxionomia)
    if taxionomia.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_taxionomia'))
    if taxionomia.errors: response.flash='Erro em seu formulário'
    tax=LISTA_TAXIONOMIA
    return dict(taxionomia=taxionomia,tax=tax)

@auth.requires_login()
def list_taxionomias():
   form=crud.create(db.taxionomia)
   taxionomias=db(db.taxionomia.id>0).select(db.taxionomia.ALL)
   response.flash='Lista Taxionomia'
   return dict(taxionomias=taxionomias,form=form)

@auth.requires_login()
def edit_taxionomia():
   taxionomia_id=request.args(0)
   taxionomia=db.taxionomia[taxionomia_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.taxionomia,taxionomia,next=url('list_taxionomias'))
   return dict(form=form)
