# coding: utf8
# try something like

def cad_curso():
    curso = SQLFORM(db.curso)
    if curso.accepts(request.vars,session):
            redirect(URL(r=request,f='list_cursos'))
    if curso.errors: response.flash='Erro em seu formulário'
    return dict(curso=curso)

def ver_curso():
    row_curso=db().select(db.curso.ALL)
    return dict(row_curso=row_curso)


def dtl_curso():     
    p = db.Instituicao[request.args(0)]
    if not p: raise HTTP(404)
    
    selected_curso = db.curso[request.vars.curso_id]
    if not selected_curso or selected_curso.instituicao!=p.id:
        session.flash="Por favor selecione um curso válido"
        redirect(URL(r=request,f='dtl_instituicao',args=p.id))
    else:
        selected_curso.select(db.curso.id==request.vars.curso_id)
        redirect(URL(r=request,f='ver_curso',args=p.id))

@auth.requires_login()
def list_cursos():
   form=crud.create(db.curso)
   cursos=db(db.curso.id>0).select(db.curso.ALL)
   response.flash='Lista Cursos'
   return dict(cursos=cursos,form=form)

@auth.requires_login()
def edit_curso():
   curso_id=request.args(0)
   curso=db.curso[curso_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.curso,curso,next=url('list_cursos'))
   return dict(form=form)
