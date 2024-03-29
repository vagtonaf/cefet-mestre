# coding: utf8
# try something like
from uml import uml
def url(f,args=[]): return URL(r=request,f=f,args=args)

def button(text,action,args=[]):
    return SPAN('[',A(text,_href=URL(r=request,f=action,args=args)),']')

@auth.requires_login()
# Cadastra e Lista tabela simples
def cadlist():
    refObj=[]
    try:
        tabela=request.args(0) or redirect(URL(r=request,f='../default/error'))
        crud.messages.submit_button = 'Cadastrar'
        #if tabela == 'questao':
            #db.questao.enunciado.widget = advanced_editor
        #if tabela == 'alternativa':
            #db.alternativa.resposta.widget = advanced_editor
            #db.alternativa.questao.writable=False    
        form=crud.create(db[tabela])
        if form.accepts(request.vars,session): 
            redirect(URL(r=request,f='cadlist/' + tabela))
        elif form.errors: response.flash='Erro em seu formulário'
        row_admins=db(db.administrador.usuario==auth.user.id).select(db.administrador.ALL)
        row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
        # aqui no if somente as tabelas que tem um select especial valeu
        if tabela == 'aluno':
            if row_professor:
                registros=db(db.aluno.matricula>0).select(
                    db.aluno.matricula,
                    db.aluno.usuario,
                    db.aluno.id,
                    db.auth_user.ALL,
                    left=db.auth_user.on(db.aluno.usuario==db.auth_user.id),
                orderby=db.aluno.matricula
                )
                if registros:
                     for reg in registros:
                        objAluno = uml.aluno()
                        objAluno.set_matricula(reg.aluno.matricula)
                        objAluno.set_nome(reg.auth_user.first_name)
                        objAluno.set_sobrenome(reg.auth_user.last_name)
                        objAluno.set_email(reg.auth_user.email)
                        refObj.append(objAluno)
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
        elif tabela == 'professor':
            registros=db(db.professor.id>0).select(
                db.professor.ALL,
                db.auth_user.ALL,
                left=db.auth_user.on(db.professor.usuario==db.auth_user.id)
            )
        elif tabela == 'alocacao':
            if row_professor:  
                list_alunosA=db()._select(db.alocacao.aluno)
                list_alunos=db(~db.aluno.id.belongs(list_alunosA)).select(
                    db.aluno.ALL,
                    db.auth_user.ALL,
                    left=db.auth_user.on(db.aluno.usuario==db.auth_user.id)
                )
                list_turmas=db(db.turma.id>0).select(
                    db.turma.ALL,
                    db.disciplina.ALL,
                    left=db.disciplina.on(db.turma.disciplina==db.disciplina.id))
                list_alocacao=db().select(db.alocacao.ALL)
                response.flash='Lista ' + tabela.replace('_',' ')
                return dict(registros=list_alocacao, form=form, tabela=tabela, list_turmas=list_turmas, list_alunos=list_alunos)
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
        elif tabela == 'disciplina':
            if row_professor:
                registros= disciplinas=db(db.disciplina.id>0).select(
                    db.disciplina.ALL,
                    db.curso.ALL,
                    left=db.curso.on(db.disciplina.curso==db.curso.id)
                )
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
        elif tabela == 'turma':
            if row_professor:
                registros=db(db.turma.id>0).select(db.turma.ALL,
                    db.disciplina.ALL,
                    orderby=db.turma.nome,
                    left=db.disciplina.on(db.turma.disciplina==db.disciplina.id)
                )
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
        elif tabela == 'plano_de_prova':
            if row_professor:
                registros=db(db.plano_de_prova.id>0).select(
                    db.plano_de_prova.ALL
                )
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
        elif tabela == 'item_plano_de_prova':
            if row_professor:
                if request.args(1):
                  registros=db(db.item_plano_de_prova.plano_de_prova==request.args(1)).select(
                      db.item_plano_de_prova.ALL,orderby=db.item_plano_de_prova.plano_de_prova
                  )
                else:
                  registros=db(db.item_plano_de_prova.id>0).select(
                      db.item_plano_de_prova.ALL,orderby=db.item_plano_de_prova.plano_de_prova
                  )
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
        elif tabela == 'prova':
            registros=db(db.prova.id>0).select(db.prova.ALL)
            turmas=db(db.turma.id>0).select(db.turma.ALL)
            if 'auth' in globals():
                if auth.is_logged_in(): 
                    planoprovas=db(db.plano_de_prova.id>0).select(db.plano_de_prova.ALL,
                        db.professor.ALL,
                        left=db.professor.on( (db.professor.id==db.plano_de_prova.professor ) & (db.professor.usuario==auth.user.id))
                    )
                    response.flash='Lista Prova'
                    return dict(registros=registros, turmas=turmas, planoprovas=planoprovas, form=form, tabela=tabela)
                else:
                    redirect(URL(r=request,f='../default/erro_acesso'))
            else:
                redirect(URL(r=request,f='../default/erro_acesso'))
        elif tabela == 'questao':
              registros=db(db.questao.id>0).select(
                     db.questao.ALL,
                     db.alternativa.ALL,
                     left=db.alternativa.on(db.questao.id==db.alternativa.questao)
               )
        else:
            # esse é um select genérico, serve para a maioria das tabelas
            if row_admins:
               registros=db(db[tabela].id>0).select(db[tabela].ALL)
            else:
               redirect(URL(r=request,f='../default/erro_admin'))
    except KeyError, NameError:
        tabela='error'
        response.flash='Tabela Inexistente!'
        form = ''
        return dict(form=form, registros='Não posso listar esta tabela!', tabela=tabela)
    if tabela == 'auth_user':
        response.flash='Lista Usuario'
    else:
        response.flash='Lista ' + tabela.replace('_',' ')
    return dict(registros=registros,form=form, tabela=tabela,refObj=refObj)

@auth.requires_login()
# Edita tabela simples
def edit():
  if auth.user:
    #só deixa editar se for professor
    row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
    if row_professor:
        tabela=request.args(0) or redirect(URL(r=request,f='../default/error'))
        registro_id=request.args(1) or redirect(URL(r=request,f='../default/error'))
        registros=db[tabela][registro_id] or redirect(URL(r=request,f='../default/error'))
    #if not registros: raise HTTP(404)
        crud.messages.submit_button = 'Alterar / Deletar'
        #if tabela == 'questao':
            #db.questao.enunciado.widget = advanced_editor
        #if tabela == 'alternativa':
            #db.alternativa.questao.writable = False  
            #db.alternativa.questao.widget = advanced_editor  
            #db.alternativa.resposta.widget = advanced_editor
        form=crud.update(db[tabela],registros,next=url('cadlist/'+ tabela))
        return dict(form=form, tabela=tabela)
    else:
        redirect(URL(r=request,f='../default/erro_acesso'))
  else:
   redirect(URL(r=request,f='../default/error'))

def edit2():
  if auth.user:
    #só deixa editar se for professor
    row_professor=db(db.professor.usuario==auth.user.id).select(db.professor.ALL)
    if row_professor:
        tabela=request.args(0) or redirect(URL(r=request,f='../default/error'))
        registro_id=request.args(1) or redirect(URL(r=request,f='../default/error'))
        if tabela=="aluno":
           ref=db(db.aluno.matricula==registro_id).select(db.aluno.id) or redirect(URL(r=request,f='../default/error')) 
        else:
           redirect(URL(r=request,f='../default/error')) 
        registros=db[tabela][ref[0].id] or redirect(URL(r=request,f='../default/error'))      
        crud.messages.submit_button = 'Alterar / Deletar'
        form=crud.update(db[tabela],registros,next=url('cadlist/'+ tabela))
        return dict(form=form, tabela=tabela)
    else:
        redirect(URL(r=request,f='../default/erro_acesso'))
  else:
   redirect(URL(r=request,f='../default/error'))
