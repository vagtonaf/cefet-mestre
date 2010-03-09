# coding: utf8
# try something like

def cad_questao():
    db.questao.enunciado.widget = advanced_editor
    questao = SQLFORM(db.questao)
    if questao.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_questao'))
    if questao.errors: response.flash='Erro em seu formulário'
    return dict(questao=questao)

def ver_questao():
    row_questao=db().select(db.questao.ALL)
    table = SQLTABLE(row_questao, orderby=True, _class='sortable', _width="100%")

    table[0][0].append(TH("Registro"))
    for i, value in enumerate(table[1]):
       table[1][i].append(TD("linha %d" % i, _align="center"))

    #row_questao.que_enu.widget = advanced_editor
    #rows=db(db.Questao.que_cod==db.resposta.res_que_cod).select()
    #for row in rows: print row.Questao.que_cod,row.Resposta.res_cod
    return dict(row_questao=table)

@auth.requires_login()
def list_questoes():
   db.questao.enunciado.widget = advanced_editor
   form=crud.create(db.questao)
   questoes=db(db.questao.id>0).select(
     db.questao.ALL,
     db.alternativa.ALL,
     left=db.alternativa.on(db.questao.id==db.alternativa.questao))
   response.flash='Lista Questões'
   return dict(questoes=questoes,form=form)

@auth.requires_login()
def edit_questao():
   questao_id=request.args(0)
   questao=db.questao[questao_id] or redirect(URL(r=request,f='../default/error'))
   form=crud.update(db.questao,questao,next=url('list_questoes'))
   return dict(form=form)
