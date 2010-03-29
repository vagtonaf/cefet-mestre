# coding: utf8
# try something like

def cad_resposta():
    resposta = SQLFORM(db.resposta)
    if resposta.accepts(request.vars,session):
            redirect(URL(r=request,f='ver_resposta'))
    if resposta.errors: response.flash='Erro em seu formulário'
    return dict(resposta=resposta)

def ver_resposta():
    row_resposta=db().select(db.resposta.ALL)
    #rows=db(db.Questao.que_cod==db.resposta.res_que_cod).select()
    #for row in rows: print row.Questao.que_cod,row.Resposta.res_cod
    return dict(row_resposta=row_resposta)