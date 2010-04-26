# coding: utf8
# try something like
import random


def index():
    c_turmas=db().select(db.turma.ALL)
    return { 'v_turmas' : c_turmas}

def rel_aluno_nota():
    aluno_nota=[]
    from applications.Mestre.modules.graf1 import gera_grafico   
    turma_id = request.args[0]
    query=(db.aluno.id == db.alocacao.aluno)&(db.turma.id==db.alocacao.turma)&(db.turma.id==turma_id)
    alocacao = db(query).select(db.aluno.matricula)
    print db(query)._select(db.aluno.matricula)
    for aluno in alocacao:
        novo_aluno = {'nome':aluno.matricula,'nota':random.random()*10}
        aluno_nota.append(novo_aluno)
        print novo_aluno 
    gera_grafico(aluno_nota,'Turma 01 - Notas','Alunos','Notas','applications/Mestre/static/turma01.png')
    return dict(imagem = 'turma01.png')
    
def graf_bar():
    return dict()

@auth.requires_login()
def resultado_prova():
	idAluno=request.args(0)
	usuario = db(db.aluno.id==idAluno).select(db.aluno.usuario)
	if usuario:
		for u in usuario:
			Aluno=u.usuario.first_name + ' ' + u.usuario.last_name
	else:
		response.flash = 'Nao e um aluno cadastrado!'
		msg = FORM(TABLE(TR('Nao e aluno!')))
		return dict(msg=msg)
	total=0
	provarealizada = db(db.prova_gerada.aluno==idAluno).select(db.prova_gerada.ALL, db.item_prova_gerada.ALL,
		left=db.item_prova_gerada.on(db.item_prova_gerada.prova_gerada==db.prova_gerada.id))
	for ipr in provarealizada:
		gerada = ipr.item_prova_gerada.prova_gerada.gerada
		Prova1=ipr.item_prova_gerada.prova_gerada.prova.referencia
		Data1 = ipr.item_prova_gerada.prova_gerada.prova.data_aplicacao
		Data2 = ipr.item_prova_gerada.prova_gerada.data
		PlanodeProva1=ipr.item_prova_gerada.prova_gerada.prova.plano_de_prova.referencia
		alternativa=db(db.alternativa.questao==ipr.item_prova_gerada.questao and db.alternativa.id==ipr.item_prova_gerada.alternativa_escolhida).select(db.questao.ALL, db.alternativa.ALL, 
			left=db.alternativa.on(db.alternativa.questao==db.questao.id))
		for ssa in alternativa:
			itemplanoprova=db(db.item_plano_de_prova.plano_de_prova==ipr.prova_gerada.prova.plano_de_prova).select(db.item_plano_de_prova.ALL)
			for resp in itemplanoprova:
				if resp.topico==ssa.questao.topico:
					if resp.dificuldade==ssa.questao.dificuldade:
						if resp.taxionomia==ssa.questao.taxionomia:
							if ssa.alternativa.correta==True:
								total = total + resp.valor
	return dict(aluno=Aluno, prova=Prova1, Plano_de_Prova=PlanodeProva1, gerada=gerada, Data_Final=str(Data2), Data_Aplicacao=str(Data1), Resultado_Final=str(total),provarealizada=provarealizada)
