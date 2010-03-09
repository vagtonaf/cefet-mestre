# coding: utf8
# try something like

def url(f,args=[]): return URL(r=request,f=f,args=args)

def button(text,action,args=[]):
    return SPAN('[',A(text,_href=URL(r=request,f=action,args=args)),']')
    
@auth.requires_login()   
def cad_professor():
    professor = SQLFORM(db.professor)
    if professor.accepts(request.vars,session):
            redirect(URL(r=request,f='list_professores'))
    if professor.errors: response.flash='Erro em seu formulário'
    return dict(professor=professor)
    
def edit_professorteste():
    thisprofessor = db.professor[request.args(0)]
    if not thisprofessor:
        redirect(URL(r=request, f='index'))
    db.professor.codigo_funcional.widget = advanced_editor
    form = crud.update(db.professor, thisprofessor,
        next = URL(r=request, f='show', args=request.args))
    return dict(form=form)


@auth.requires_login()
def list_professores():
   form=crud.create(db.professor)
   professores=db(db.professor.id>0).select(db.professor.ALL,db.auth_user.ALL,left=db.auth_user.on(db.professor.usuario==db.auth_user.id))
   response.flash='Lista Professor'
   return dict(professores=professores,form=form)

@auth.requires_login()
def edit_professor():
   professor_id=request.args(0)
   professor=db.professor[professor_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.professor,professor,next=url('list_professores'))
   return dict(form=form)
