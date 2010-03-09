# coding: utf8
# try something like

def url(f,args=[]): return URL(r=request,f=f,args=args)

def button(text,action,args=[]):
    return SPAN('[',A(text,_href=URL(r=request,f=action,args=args)),']')

@auth.requires_login()
def cad_instituicao():
    instituicoes = SQLFORM(db.instituicao)
    if instituicoes.accepts(request.vars,session):
            redirect(URL(r=request,f='list_instituicoes'))
    if instituicoes.errors: response.flash='Erro em seu formulário'
    return dict(instituicoes=instituicoes)
    
def dtl_instituicao():
    instituicao_id=request.args(0)
    p = db.instituicao[instituicao_id]
    if not p: raise HTTP(404) 
    return dict(instituicao=p)

@auth.requires_login()
def list_instituicoes():
   form=crud.create(db.instituicao)
   instituicoes=db(db.instituicao.id>0).select(db.instituicao.ALL)
   response.flash='Lista instituicoes'
   return dict(instituicoes=instituicoes,form=form)

@auth.requires_login()
def edit_instituicao():
   instituicao_id=request.args(0)
   instituicao=db.instituicao[instituicao_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.instituicao,instituicao,next=url('list_instituicoes'))
   return dict(form=form)
