# coding: utf8
# try something like
import random

def geraProva(lista):
  s=[0] * 10
  for i in range(10):
   while s[i]==0:
    r = random.choice (lista)
    t=0
    if r in s:
       t=1
    if (t==0 and r<>0):
       s[i]=r
  s.sort()
  return s

def teste():
    #teste = db(db.questao.id==db.resposta.questao).select(db.questao.ALL,db.resposta.ALL)
    rows = db(db.questao.id==db.prova_gerada.questao).select(db.questao.ALL, db.prova_gerada.ALL)
    return dict(rows=rows)

def botao():
    form=FORM(INPUT(_type='hidden',_name='action',_id='action',_value='undefined'),INPUT(_type='button',_value='Gerar Prova',_onclick='''this.form.action.value=1;this.form.submit();
    ''',),INPUT(_type='button',_value='Criar turma',_onclick='''this.form.action.value=2;this.form.submit();''',),)
    if (request.vars):
       op = request.vars.action
       #response.flash='Vocé clicou o botão %s Gerar Prova'%op
       if op=='1':
          response.flash='Vocé clicou o botão %s Gerar Prova'%op
	  #aqui vamos pegar os dados do Banco de dados (id questoes) em um select 
	  #exemplo de lista para o teste
          lista=[2,3,55,57,9,11,13,15,28,33,44,90,18,10,100,133,22]  
          resp = geraProva(lista)
          #aqui vamos gerar o inserte no Banco de dados  da 10 (id questoes) selecionadas  
          response.flash='Indices Gerados - %s '%resp
       elif op=='2':
          response.flash='Vocé clicou o botão %s Criar Turma'%op
    return {'':form}
