# coding: utf8
# try something like

def index(): 
    return dict(message="Usuario Benvindo ao Mestre")

def cad_usuario():
    usuario = SQLFORM(db.auth_user)
    if usuario.accepts(request.vars,session):
            redirect(URL(r=request,f='list_usuarios'))
    if usuario.errors: response.flash='Erro em seu formulário'
    return dict(usuario=usuario)

@auth.requires_login()
def list_usuarios():
   form=crud.create(db.auth_user)
   usuarios=db(db.auth_user.id>0).select(db.auth_user.ALL)
   response.flash='Lista Usuarios'
   return dict(usuarios=usuarios,form=form)

@auth.requires_login()
def edit_usuario():
   usuario_id=request.args(0)
   usuario=db.auth_user[usuario_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.auth_user,usuario,next=url('list_usuarios'))
   return dict(form=form)
