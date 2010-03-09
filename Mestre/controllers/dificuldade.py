# coding: utf8
# try something like
    
@auth.requires_login()
def cad_dificuldade():
    dificuldade = SQLFORM(db.dificuldade)
    if dificuldade.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_dificuldade'))
    if dificuldade.errors: response.flash='Erro em seu formulário'
    return dict(dificuldade=dificuldade)
  
@auth.requires_login()
def list_dificuldades():
   form=crud.create(db.dificuldade)
   dificuldades=db(db.dificuldade.id>0).select(db.dificuldade.ALL)
   response.flash='Lista de Dificuldades'
   return dict(dificuldades=dificuldades,form=form)

@auth.requires_login()
def edit_dificuldade():
   dificuldade_id=request.args(0)
   dificuldade=db.dificuldade[dificuldade_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.dificuldade,dificuldade,next=url('list_dificuldades'))
   return dict(form=form)
