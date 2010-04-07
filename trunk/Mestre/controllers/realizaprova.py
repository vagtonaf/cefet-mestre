# coding: utf8
# try something like
import random
import datetime

def geraProva(lista):
 if len(lista) >= 10: 
  s = [0] * 10
  for i in range(10):
   while s[i]==0:
    r = random.choice (lista)
    t=0
    if r in s:
       t=1
    if (t==0 and r<>0):
       s[i]=r
  s.sort()
 else:
  s="Menos de 10 questões" 
 return s



def realizar_prova():
 #somente para teste e estudo
 if 'auth' in globals():
  if auth.is_logged_in():
    #pega o Aluno  
    nome=auth.user.first_name
    lastname=auth.user.last_name
    idUsuario=auth.user.id
    #testa se é um aluno
    row_aluno=db(db.aluno.usuario==idUsuario).select(db.aluno.ALL)
    if row_aluno:
       for al in row_aluno:
          idAluno=al.id
          matricula=al.matricula
    else:
       response.flash = 'O usuário não é um aluno cadastrado!'
       realizar_prova = FORM(TABLE(TR('Aluno não cadastrado, procure seu professor!')))
       return dict(realizar_prova=realizar_prova)
    #testa se tem um email cadastrado para um possível contato
    row_email=db(db.auth_user.id==idAluno).select(db.auth_user.email)
    if row_email:
       for se in row_email:
          semail=se.email
    else:
       response.flash = 'Aluno não possui email cadastrado!'
       realizar_prova = FORM(TABLE(TR('Aluno não possui email cadastrado!')))
       return dict(realizar_prova=realizar_prova)
    #testa se o aluno está alocado a uma turma   
    row_alocacao = db(db.alocacao.aluno==idAluno).select(db.alocacao.turma)
    if row_alocacao:
            for alo in row_alocacao:
                idTurma=alo.turma
                row_turma = db(db.turma.id==idTurma).select(db.turma.nome)
                if row_turma:
                   for tu in row_turma:
                     nome_turma=tu.nome
    else:
            response.flash = 'Aluno não está alocado a uma turma!'
            realizar_prova = FORM(TABLE(TR('Aluno não alocado a turma!')))
            return dict(realizar_prova=realizar_prova)
    #testa se foi gerado uma prova para essa turma
    row_prova = db(db.prova.turma==idTurma and db.prova.data_aplicacao!='').select(db.prova.id,db.prova.referencia,db.prova.plano_de_prova)
    if row_prova:
            for pl in row_prova:
                idProva=pl.id
                prova=pl.referencia
                idPlanoProva=pl.plano_de_prova
    else:
            response.flash = 'A turma não possui uma prova relacionada!'
            realizar_prova = FORM(TABLE(TR('A turma não possui uma prova relacionada!')))
            return dict(realizar_prova=realizar_prova)
    #testa se foi gerado uma plano de prova
    row_planoprova = db(db.plano_de_prova.id==idPlanoProva).select(db.plano_de_prova.id,db.plano_de_prova.referencia)
    if row_planoprova:
            for plp in row_planoprova:
                PlanoProva=plp.referencia
    else:
            response.flash = 'A turma não possui um plano de prova elaborado!'
            realizar_prova = FORM(TABLE(TR('A turma não possui um plano de prova elaborado!')))
            return dict(realizar_prova=realizar_prova)        
    realizar_prova = FORM(TABLE(
        #certo é selecionar o aluno, sem combo
        TR('Email:',semail,'Aluno:', nome + ' '+ lastname),
        TR('Matricula:',matricula,'Turma:',nome_turma),
        TR('Prova:',prova, 'Plano de Prova:',PlanoProva),
        #TR('Qual o Plano de Prova?', SELECT([OPTION(pro.referencia,_value=pro.referencia) for pro in db().select(db.plano_de_prova.referencia,distinct=True)],_name='planoprova',requires=IS_IN_DB(db,'plano_de_prova.referencia'))),
        #TR('Qual a Turma?', SELECT([OPTION(tur.nome,_value=tur.nome) for tur in db().select(db.turma.nome,distinct=True)],_name='turma',requires=IS_IN_DB(db,'turma.nome'))),
        TR('Realizar a Prova?', SELECT(['Sim','Não'],_name='opcao',requires=IS_IN_SET(['Sim','Não']))),
        TR(INPUT(_type='hidden', _name='PlanoProva', _value=PlanoProva)),
        TR(INPUT(_type='hidden', _name='idProva', _value=idProva)),
        TR(INPUT(_type='hidden', _name='idAluno', _value=idAluno)),
        TR('Responder as Perguntas -> ', INPUT(_type='submit', _value='Continuar ou Iniciar a Prova')),
        ))
    if realizar_prova.accepts(request.vars, session):
        sopcao=realizar_prova.vars.opcao
        if(sopcao=='Não'):
              #Escreve no banco a desistência do aluno
              response.flash = 'O Aluno Desistiu da prova!'
              realizar_prova = FORM(TABLE(TR('Vai receber uma nota zero!')))
              return dict(realizar_prova=realizar_prova)        
        #recupera o Plano de Prova selecionado
        PlanoProva =  realizar_prova.vars.PlanoProva
        #buscar Taxionomia, Topico e Dificuldade do plano de prova
        row_planoprova = db(db.plano_de_prova.referencia==PlanoProva).select(
                              db.plano_de_prova.ALL, 
                              db.item_plano_de_prova.ALL,
                              left=db.item_plano_de_prova.on(db.plano_de_prova.id==db.item_plano_de_prova.id))
        for plpr in row_planoprova:
          idTax = plpr.item_plano_de_prova.taxionomia
          idTop = plpr.item_plano_de_prova.topico 
          idDif = plpr.item_plano_de_prova.dificuldade  
          #selecionar todas as questão que tenham como caracteristicas a Taxionomia, Topico e Dificuldade
          row_questao=db((db.questao.topico==idTop)&(db.questao.taxionomia==idTax)&(db.questao.dificuldade==idDif)).select(db.questao.id)
          lista_Questao = [0] *  len(row_questao)
          i=0
          for que in row_questao:
              lista_Questao[i] = int(que.id)
              i = i + 1
              
        realizar_prova = FORM(TABLE(TR(row_planoprova,row_questao)))  #Temporariamente aqui para mostrar os resultados 
        # Teste para não precissar gerar as questoes
        lista_Questao=[2,3,55,57,9,11,13,15,28,33,44,90,18,10,100,133,22]  #aqui vamos pegar os daos do Banco de dados em um select 
        #gerador da lista de questoes OK
        #QuestoesSelecionadas = geraProva(lista_Questao)
        if QuestoesSelecionadas:
           idProvaGerada=db.prova_gerada.insert(data=datetime.datetime.now(),aluno=idAluno,prova=realizar_prova.vars.idProva)
           row_prova_gerada = db(db.prova_gerada.id==idProvaGerada).select(db.prova_gerada.ALL)
           if row_prova_gerada:
              for n in QuestoesSelecionadas:
                  db.item_prova_gerada.insert(prova_gerada=idProvaGerada,questao=n)
        response.flash = 'Os 10 Indices de Questões Gerados - %s '%QuestoesSelecionadas
    elif realizar_prova.errors:
        response.flash = 'Formulário Inválido'
    else:
        response.flash = 'Por favor, Verifique se seus dados estão corretos, quando estiver pronto, selecionar se quer "Realizar a Prova" e clique em "Continuar ou Iniciar a Prova" para responder as perguntas ou Desistir!'
    return dict(realizar_prova=realizar_prova, vars = realizar_prova.vars)    
  else:  
    #realizar_prova = FORM(TABLE(TR('Usuario não Logado')))        
    #response.flash = 'Usuário não Logado'
    redirect(URL(r=request, f='../default/user/login'))
