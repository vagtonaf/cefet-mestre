# coding: utf8
# try something like
import random
import datetime
import time

def geraProva(lista, numQuestoes):
 #testa se o numero de questoes da lista é maior do que o numero de questões para retorno
 if len(lista) >= numQuestoes: 
  s = [0] * numQuestoes
  for i in range(numQuestoes):
   while s[i]==0:
    r = random.choice (lista)
    t=0
    if r in s:
       t=1
    if (t==0 and r<>0):
       s[i]=r
  s.sort()
 else:
  s=0
 return s


def realizar_prova():
    #somente para teste e estudo
    if 'auth' in globals():
        if auth.is_logged_in():
                #pega os dados do Aluno  
                nome=auth.user.first_name
                lastname=auth.user.last_name
                idUsuario=auth.user.id
                #testa se é um aluno
                row_aluno=db(db.aluno.usuario==idUsuario).select(db.aluno.ALL)
                row_prova=db().select(db.prova.ALL)
                if row_aluno:
                    for al in row_aluno:
                        idAluno=al.id
                        matricula=al.matricula
                else:
                    response.flash = 'O usuário não é um aluno cadastrado!'
                    realizar_prova = FORM(TABLE(TR('Aluno não cadastrado, procure seu professor!')))
                    return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')
                #testa se tem um email cadastrado para um possível contato
                row_email=db(db.auth_user.id==idUsuario).select(db.auth_user.email)
                if row_email:
                    for se in row_email:
                        semail=se.email
                else:
                    response.flash = 'Aluno não possui email cadastrado!'
                    realizar_prova = FORM(TABLE(TR('Aluno não possui email cadastrado!')))
                    return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')
                #testa se o aluno está alocado a uma turma   
                row_alocacao = db((db.alocacao.aluno==idAluno)&(db.prova.data_aplicacao!=None)).select(db.alocacao.turma,
                                                                     db.prova.ALL,
                                                                     left=db.prova.on(db.alocacao.turma==db.prova.turma)
                                                                    )
                if row_alocacao:
                    for alo in row_alocacao:
                        idTurma=alo.prova.turma
                        row_turma = db(db.turma.id==idTurma).select(db.turma.nome)
                        for tu in row_turma:
                            nome_turma=tu.nome
                            print 'Turma Vaf:' + nome_turma
                else:
                    response.flash = 'Aluno não está alocado a uma turma!'
                    realizar_prova = FORM(TABLE(TR('Aluno não alocado a turma!')))
                    return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')
                #testa se foi gerado uma prova para essa turma
                row_prova = db((db.prova.turma==idTurma)&(db.prova.data_aplicacao!=None)).select(
                        db.prova.id,db.prova.referencia,db.prova.plano_de_prova)
                if row_prova:
                    for pl in row_prova:
                        idProva=pl.id
                        prova=pl.referencia
                        idPlanoProva=pl.plano_de_prova
                else:
                    response.flash = 'Sua turma não possui uma prova relacionada ou aplicada pelo professor!'
                    realizar_prova = FORM(TABLE(TR('Sua turma não possui uma prova relacionada ou aplicada pelo professor!')))
                    return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')
                #testa se foi gerado uma plano de prova
                row_planoprova = db(db.plano_de_prova.id==idPlanoProva).select(db.plano_de_prova.id,db.plano_de_prova.referencia)
                if row_planoprova:
                    for plp in row_planoprova:
                        PlanoProva=plp.referencia
                else:
                    response.flash = 'A turma não possui um plano de prova elaborado!'
                    realizar_prova = FORM(TABLE(TR('A turma não possui um plano de prova elaborado!')))
                    return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')
                #Permite ao aluno iniciar a prova ou não 
                realizar_prova = FORM(TABLE(
                      TR('Email:',semail,'Aluno:', nome + ' '+ lastname),
                      TR('Matricula:',matricula,'Turma:',nome_turma),
                      TR('Prova:',prova, 'Plano de Prova:',PlanoProva),
                      #TR('idProva:',idProva, 'idAluno:',idAluno),
                      #TR('Qual o Plano de Prova?', SELECT([OPTION(pro.referencia,_value=pro.referencia) for pro in db().select(db.plano_de_prova.referencia,distinct=True)],_name='planoprova',requires=IS_IN_DB(db,'plano_de_prova.referencia'))),
                      #TR('Qual a Turma?', SELECT([OPTION(tur.nome,_value=tur.nome) for tur in db().select(db.turma.nome,distinct=True)],_name='turma',requires=IS_IN_DB(db,'turma.nome'))),
                      TR('Realizar a Prova?', SELECT(['Sim','Não'],_name='opcao',requires=IS_IN_SET(['Sim','Não']))),
                      TR(INPUT(_type='hidden', _name='PlanoProva', _value=PlanoProva)),
                      TR(INPUT(_type='hidden', _name='idProva', _value=idProva)),
                      TR(INPUT(_type='hidden', _name='idAluno', _value=idAluno)),
                      TR('Responder as Perguntas -> ', INPUT(_type='submit', _value='Continuar ou Iniciar a Prova')),
                      ))
                if realizar_prova.accepts(request.vars, session):
                    #pega identificação do aluno
                    idAluno=realizar_prova.vars.idAluno
                    #pega identificação da prova
                    idProva=realizar_prova.vars.idProva
                    row_aluno=db(db.aluno.id==idAluno).select(db.aluno.ALL)
                    row_prova=db(db.prova.id==idProva).select(db.prova.ALL)
                    #pega do sistema a data da prova para o armazenamento no prova gerada para caracterizar uma prova concluida
                    dataprova = datetime.datetime.now()
                    #verifica se o aluno quer fazer a prova
                    sopcao=realizar_prova.vars.opcao
                    if(sopcao=='Não'):
                        prova_aluno=db((db.prova_gerada.aluno==idAluno)&(db.prova_gerada.prova==idProva)).select(db.prova_gerada.ALL)
                        if prova_aluno:
                           response.flash = 'O Aluno já possui uma prova criada, favor finaliza-la na tela de realizar prova!'
                           realizar_prova = FORM(TABLE(TR('O Aluno já possui uma prova criada, favor finaliza-la na tela de realizar prova (Sim)!'),A('Realizar Prova',_href=url('realizar_prova',0))))
                           return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')
                        else:
                           idProvaGerada = db.prova_gerada.insert(aluno=idAluno, prova=idProva,data=datetime.datetime.now())
                           response.flash = 'O Aluno Desistiu da prova!'
                           realizar_prova = FORM(TABLE(TR('A prova foi finalizada, o Aluno desistiu da prova!')))
                           return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')
                    #recupera o Plano de Prova selecionado
                    PlanoProva =  realizar_prova.vars.PlanoProva
                    #buscar Taxionomia, Topico e Dificuldade do plano de prova
                    row_planoprova = db(db.plano_de_prova.referencia==PlanoProva).select(
                        db.plano_de_prova.ALL, 
                        db.item_plano_de_prova.ALL,
                        left=db.item_plano_de_prova.on(db.plano_de_prova.id==db.item_plano_de_prova.plano_de_prova))
                    #Seleciona pelo Plano de Prova a taxionomia, topico e dificuldade para listar no banco de questões
                    for plpr in row_planoprova:
                        nValor = plpr.item_plano_de_prova.valor
                        idTax = plpr.item_plano_de_prova.taxionomia
                        idTop = plpr.item_plano_de_prova.topico 
                        idDif = plpr.item_plano_de_prova.dificuldade  
                        print 'Valor:' + str(nValor)
                        #selecionar todas as questão que tenham como caracteristicas a Taxionomia, Topico e Dificuldade
                        row_questao=db((db.questao.topico==idTop)&(db.questao.taxionomia==idTax)&(db.questao.dificuldade==idDif)).select(db.questao.id)
                        #cria uma lista de questões
                        lista_Questao = [0] *  len(row_questao)
                        i=0
                        for que in row_questao:
                            lista_Questao[i] = int(que.id)
                            print 'lista:' + str(lista_Questao[i])
                            i = i + 1
                        # Escolhe randomicamente da lista de questoes a questao que vai atender ao plano de prova selecionado
                        #seleciona uma questão da lista selecionada
                        QuestaoSelecionada = geraProva(lista_Questao,1)
                        #Verifica se conseguiu achar uma questão que atenda a exigencia, 0 = não consegui
                        print 'Questoes Selecionadas:' + str(QuestaoSelecionada)
                        if QuestaoSelecionada==0:
                            response.flash = 'Não existe questão para (topico, dificuldade e taxionomia) para o plano de prova ' + PlanoProva + ' Valor: ' + str(nValor)
                            realizar_prova = FORM(TABLE(TR('Favor informar ao professor para verificar o cadastro de questões!')))
                            return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')
                        if QuestaoSelecionada>0:
                            #verifica se a prova gerada existe e se não foi finalizada pelo aluno
                            row_prova_gerada = db((db.prova_gerada.aluno==idAluno)&(db.prova_gerada.prova==idProva)).select(
                                db.prova_gerada.ALL
                            )
                            if row_prova_gerada:
                               for provger in row_prova_gerada:
                                  if provger.data!=None:
                                      response.flash = 'Prova finalizada'
                                      realizar_prova = FORM(TABLE(TR('Prova Finalizada pelo aluno')))
                                      return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, tabela='solicitacao')

                            #se haver prova gerada pega o id, se não inclui uma prova_gerada
                            if row_prova_gerada:
                                gerada = row_prova_gerada[0].gerada
                                idProvaGerada = row_prova_gerada[0].id
                            else: 
                                gerada=False
                                #busca objeto aluno
                                rAluno = db(db.aluno.id==idAluno).select(db.aluno.id)
                                #busca objeto Prova                    
                                rProva = db(db.prova.id==idProva).select(db.prova.id)
                                for rr in rAluno:
                                    for rrr in rProva: 
                                        idProvaGerada = db.prova_gerada.insert(aluno=rr.id, prova=rrr.id)
                            if gerada:
                                response.flash = 'Prova ja foi gerada, o aluno só pode realizar a prova no moneto da geração'
                                realizar_prova = FORM(TABLE(TR('Prova Gerada, se houve algum problema peça para o professor para gerar nova prova')))
                            else:
                                #se haver item de prova gerada pega o id, se não gera um
                                row_item_prova_gerada = db((db.item_prova_gerada.prova_gerada==idProvaGerada)&(db.item_prova_gerada.questao==QuestaoSelecionada[0])).select(
                                    db.item_prova_gerada.ALL
                                )
                                #busca objeto questao
                                rQuestao = db(db.questao.id==QuestaoSelecionada[0]).select(db.questao.id)
                                #busca objeto Prova Gerada
                                rProvaGerada = db(db.prova_gerada.id==idProvaGerada).select(db.prova_gerada.id)
                                for rr2 in rProvaGerada:
                                    for rrr2 in rQuestao: 
                                        idItemProvaGerada = db.item_prova_gerada.insert(
                                            prova_gerada=rr2.id, questao=rrr2.id
                                        )
                    #bloqueia a prova já gerada
                    db(db.prova_gerada.id==idProvaGerada).update(gerada=True)
                    #response.flash = 'As Questões foram Geradas aleatoriamente para você responder - %s '%QuestaoSelecionada
                    #Mostra as questões criadas para o aluno
                    aluno = db(db.aluno.id==idAluno).select(db.aluno.ALL)
                    prova = db(db.prova.id==idProva).select(db.prova.ALL)
                    row_prova = db(db.item_prova_gerada.prova_gerada==idProvaGerada).select(db.item_prova_gerada.ALL)
                    return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=aluno, rprova=prova, tabela='prova')
                elif realizar_prova.errors:
                    response.flash = 'Formulário Inválido'
                else:
                    response.flash = 'Por favor, Verifique se seus dados estão corretos, quando estiver pronto, selecionar se quer "Realizar a Prova" e clique em "Continuar ou Iniciar a Prova" para responder as perguntas ou Desistir!'
                    return dict(realizar_prova=realizar_prova, row_prova=row_prova, raluno=row_aluno, rprova=row_prova, vars = realizar_prova.vars, tabela='solicitacao')    
        else:
            #realizar_prova = FORM(TABLE(TR('Usuario não Logado')))        
            #response.flash = 'Usuário não Logado'
            redirect(URL(r=request, f='../default/user/login'))
    else:
        #realizar_prova = FORM(TABLE(TR('Usuario não Autenticado')))        
        #response.flash = 'Usuário não Autenticado'
        redirect(URL(r=request, f='../default/user/login'))

def concluir():
    #só deixa editar se for aluno
    row_aluno=db(db.aluno.usuario==auth.user.id).select(db.aluno.ALL)
    if row_aluno:
        idProvaGerada=request.args(0) or redirect(URL(r=request,f='../default/error'))
        hoje = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db(db.prova_gerada.id==idProvaGerada).update(data=datetime.datetime.now())
        return dict(realizar_prova=hoje, tabela='Prova concluida')
    else:
        redirect(URL(r=request,f='../default/erro_acesso'))
