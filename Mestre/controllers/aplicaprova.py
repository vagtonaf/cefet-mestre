# coding: utf8
# try something like
import datetime
import time
def aplicar_prova():
 #somente para teste e estudo
 if 'auth' in globals():
  if auth.is_logged_in():
    #pega o Professor  
    nome=auth.user.first_name
    sobrenome=auth.user.last_name
    idUsuario=auth.user.id
    #testa se é um professor
    row_professor=db(db.professor.usuario==idUsuario).select(db.professor.ALL)
    if row_professor:
       for pr in row_professor:
          idProfessor=pr.id
          codigo_funcional=pr.codigo_funcional
    else:
       response.flash = 'O usuário não é um Professor cadastrado!'
       aplicar_prova = FORM(TABLE(TR('Professor não cadastrado, procure o Administrador!')))
       return dict(aplicar_prova=aplicar_prova)

    #testa se o professor possue plano_de_prova criado
    row_planodeprova = db(db.plano_de_prova.professor==idProfessor).select(db.plano_de_prova.ALL)
    if row_planodeprova:
       n=0
       for pla in row_planodeprova:
           idPlanodeprova=pla.id
           row_prova = db(db.prova.plano_de_prova==idPlanodeprova).select(db.prova.ALL)
           for prv in row_prova:
              idProva=prv.id
              refProva=prv.referencia
              n=n+1
       if n==0:
          response.flash = 'O Plano de prova não possui uma prova relacionada!'
          aplicar_prova = FORM(TABLE(TR('O Plano de prova não possui uma prova relacionada!')))
          return dict(aplicar_prova=aplicar_prova)
    else:
       response.flash = 'Professor não possue plano de prova associado!'
       aplicar_prova = FORM(TABLE(TR('Professor não possue plano de prova associado!')))
       return dict(aplicar_prova=aplicar_prova)
    hoje = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    aplicar_prova = FORM(TABLE(
       TR('Professor:', nome + ' '+ sobrenome),
       TR('Codigo Funcional:',codigo_funcional),
       TR('Qual a Prova?', SELECT([OPTION(pr.referencia,_value=pr.referencia) for pr in db().select(db.prova.referencia,distinct=True)],_name='Prova',requires=IS_IN_DB(db,'prova.referencia'))),
       TR('Aplicar Prova?', SELECT(['Não','Sim'],_name='opcao',requires=IS_IN_SET(['Não','Sim']))),
       TR(INPUT(_type='hidden', _name='idProfessor', _value=idProfessor)),
       TR(INPUT(_type='hidden', _name='data_aplicacao', _value=hoje)),
       TR(INPUT(_type='hidden', _name='total_prova', _value=n)),
       TR(INPUT(_type='submit', _value='Aplica')),
       ))
    if aplicar_prova.accepts(request.vars, session):
       sopcao=aplicar_prova.vars.opcao
       if (sopcao == 'Não'):
          #Escreve no banco a desistência do professor
          response.flash = 'O Professor Desistiu da ação, posso aqui retornar para o menu!'
          realizar_prova = FORM(TABLE(TR('Retorne ao menu e selecione outra atividade!')))
          return dict(aplicar_prova=aplicar_prova)        
       else:
          #recupera o Prova selecionado
          Prova =  aplicar_prova.vars.Prova
          row_prova = db(db.prova.referencia==Prova).select(
                              db.prova.ALL, 
                              db.plano_de_prova.ALL, 
                              left=db.plano_de_prova.on(db.prova.plano_de_prova==db.plano_de_prova.id))
          for plpr in row_prova:
             idProva = plpr.prova.id
             # criar o update do campo data_aplicada da tabela prova para o professor para cada idProva
          aplicar_prova = FORM(TABLE('Ainda não faz o Update, mas sabe em quem deve colocar ' + hoje + ' no campo data_aplicacao',TR(row_prova)))  
        
          response.flash = 'Prova aplicada pelo professor!'
    elif aplicar_prova.errors:
          response.flash = 'Formulário Inválido'
    else:
          response.flash = 'Professor por favor, Verifique se seus dados estão corretos, quando estiver pronto, selecionar se quer "Aplicar a Prova" e clique em "Continuar"!'
    return dict(aplicar_prova=aplicar_prova, vars = aplicar_prova.vars)    
  else:  
    #realizar_prova = FORM(TABLE(TR('Usuario não Logado')))        
    #response.flash = 'Usuário não Logado'
    redirect(URL(r=request, f='../default/user/login'))
 else:
   #realizar_prova = FORM(TABLE(TR('Usuario não Autenticado')))        
   #response.flash = 'Usuário não Autenticado'
   redirect(URL(r=request, f='../default/user/login'))
