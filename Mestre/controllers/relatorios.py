# coding: utf8
# try something like
import random

def executesql(self, query): 
    self['_lastsql'] = query    
    self._execute(query)
    try:        
        return self._cursor.fetchall()
    except:
        return None


def relnota():
 if 'auth' in globals():
    if auth.is_logged_in():
        resultado = db.executesql("""SELECT h.referencia, j.first_name as nome, sum(i.valor) as nota
                                     FROM item_prova_gerada as a  
                                     inner join prova_gerada as b on a.prova_gerada=b.id
                                     inner join aluno as c on b.aluno=c.id
                                     inner join questao as d on a.questao=d.id
                                     inner join alternativa as e on d.id=e.id
                                     inner join alternativa as f on a.alternativa_escolhida=f.id
                                     inner join prova_gerada as g on a.prova_gerada=g.id
                                     inner join prova as h on g.prova=h.id
                                     inner join item_plano_de_prova as i on h.plano_de_prova=i.plano_de_prova
                                     inner join auth_user as j on c.usuario==j.id
                                     where e.correta=f.correta and i.taxionomia=d.taxionomia and i.topico=d.topico and i.dificuldade=d.dificuldade
                                     """)
    else:   
        resultado = None
    return dict(resultado=resultado)
    
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
    #resposta = db.executesql("""SELECT j.first_name as name, sum(i.valor) as start
    #                                 FROM item_prova_gerada as a  
    #                                 inner join prova_gerada as b on a.prova_gerada=b.id
    #                                 inner join aluno as c on b.aluno=c.id
    #                                 inner join questao as d on a.questao=d.id
    #                                 inner join alternativa as e on d.id=e.id
    #                                 inner join alternativa as f on a.alternativa_escolhida=f.id
    #                                 inner join prova_gerada as g on a.prova_gerada=g.id
    #                                 inner join prova as h on g.prova=h.id
    #                                 inner join item_plano_de_prova as i on h.plano_de_prova=i.plano_de_prova
    #                                 inner join auth_user as j on c.usuario==j.id
    #                                where e.correta=f.correta and i.taxionomia=d.taxionomia and i.topico=d.topico and i.dificuldade=d.dificuldade
    #                                 """)
    dado = ["vagton", 8.0, "Jose Roberto", 9.0,"Zezaum", 10.0,]
    #dado = ["Zezaum", 10.0]
    names = [x for i, x in enumerate(dado) if not i % 2]
    starts = [x for i, x in enumerate(dado) if i % 2]
    resposta = []
    for name, start in zip(names, starts):
        resposta.append({'name': name, 'start': start})
    return dict(resposta=resposta)

@auth.requires_login()
def resultado_prova():
    total=0
    tot=''
    idAluno=request.args(0)
    usuario = db(db.aluno.id==idAluno).select(db.aluno.usuario)
    if usuario:
        for u in usuario:
            Aluno=u.usuario.first_name + ' ' + u.usuario.last_name
    else:
        response.flash = 'Nao e um aluno cadastrado!'
        msg = FORM(TABLE(TR('Nao e aluno!')))
        return dict(msg=msg)
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
    return dict(aluno=Aluno, total=str(total), Plano_de_Prova=PlanodeProva1, gerada=gerada, Data_Final=str(Data2), Data_Aplicacao=str(Data1), Resultado_Final=total,provarealizada=provarealizada)