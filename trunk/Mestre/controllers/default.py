# coding: utf8

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  


error_page=URL(r=request,f='error')

if not session.recent_companies: session.recent_companies=[]
if not session.recent_persons: session.recent_persons=[]

#response.menu=[
#  ['Companies',False,url('list_companies')],
#  ['Contacts',False,url('list_persons')],
#  ['Tasks',False,url('list_tasks')],
#]

def add(mylist,item):
    if not item.id in [x[0] for x in mylist]:
        return mylist[:9]+[(item.id,item.name)]
    else:
        return mylist
        
def erro_acesso():
  response.flash="Só acessado por professores valeu!"
  form = "Só acessado por professores valeu!"
  return dict(form=form)        

def erro_admin():
  response.flash="Só acessado por professores valeu!"
  form = "Só acessado por administradores valeu!"
  return dict(form=form)

def index():
    return dict()
        
@auth.requires_login()
def list_alunos_turma():
    turma_id=request.args(0)
    row_alocacao=db(db.alocacao.turma==turma_id).select(orderby=db.alocacao.aluno)
    for alo in row_alocacao:
        row_turmas=db(db.turma.id==alo.turma.id).select(orderby=db.turma.nome)
        row_alunos=db(db.aluno.id==alo.aluno.id).select(orderby=db.aluno.matricula)
        for alu in row_alunos:
              alunos=db.aluno[alu.id] or redirect(error)  
              db.aluno.id=alunos.id
              db.aluno.matricula.writable=False
              db.aluno.matricula.readable=False
              form=crud.create(db.aluno)
    else:
        form=None
        row_alunos=db(db.aluno.id>0).select(orderby=db.aluno.matricula)
        row_turmas=db(db.turma.id>0).select(orderby=db.turma.nome)
    return dict(alunos=row_alunos,turmas=row_turmas,form=form)

@auth.requires_login()
def view_person():
    person_id=request.args(0)
    person=db.person[person_id] or redirect(error_page)    
    session.recent_persons = add(session.recent_persons,person)
    return dict(person=person)

@auth.requires_login()
def list_docs():
    person_id=request.args(0)
    person=db.person[person_id] or redirect(error_page)    
    session.recent_persons = add(session.recent_persons,person)
    db.document.person.default=person.id
    db.document.person.writable=False
    db.document.person.readable=False
    form=crud.create(db.document)
    docs=db(db.document.person==person.id).select(orderby=db.document.name)
    return dict(person=person,docs=docs,form=form)

@auth.requires_login()
def list_logs():
    person_id=request.args(0)
    person=db.person[person_id] or redirect(error_page)    
    session.recent_persons = add(session.recent_persons,person)
    db.log.person.default=person.id
    db.log.person.writable=False
    db.log.person.readable=False
    form=crud.create(db.log)
    logs=db(db.log.person==person.id).select(orderby=~db.log.created_on)
    return dict(person=person,logs=logs,form=form)

@auth.requires_login()
def edit_person():
    person_id=request.args(0)
    person=db.person[person_id] or redirect(error_page)
    session.recent_persons = add(session.recent_persons,person)
    db.person.company.writable=False
    db.person.company.readable=False
    form=crud.update(db.person,person,next=url('view_person',person_id))
    return dict(form=form)
    

@auth.requires_login()
def edit_task():
    task_id=request.args(0)
    task=db.task[task_id] or redirect(error_page)
    person=db.person[task.person]
    db.task.person.writable=db.task.person.readable=False
    form=crud.update(db.task,task,next='view_task/[id]')
    return dict(form=form, person=person)   
    
@auth.requires_login()
def view_task():    
    task_id=request.args(0)
    task=db.task[task_id] or redirect(error_page)
    person=db.person[task.person]
    db.task.person.writable=db.task.person.readable=False
    form=crud.read(db.task,task)
    return dict(form=form, person=person, task=task)   
    
@auth.requires_login()
def list_tasks():    
    person_id=request.args(0)
    person=db.person[person_id]
    if person_id:
       tasks=db(db.task.person==person_id)\
               (db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select() 
    else:
       tasks=db(db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select() 
    db.task.person.default=person_id
    db.task.person.writable=db.task.person.readable=False
    form=crud.create(db.task,next='view_task/[id]')
    return dict(tasks=tasks,person=person,form=form)
    
@auth.requires_login()
def calendar():
    person_id=request.args(0)
    person=db.person[person_id]
    if person_id:
       tasks=db(db.task.person==person_id)\
               (db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select() 
    else:
       tasks=db(db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select() 
    return dict(tasks=tasks,person=person)    
           
def error():
    return dict(message="Algo está errado, analise a sua solicitação!")

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
