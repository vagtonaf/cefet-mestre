# coding: utf8
# try something like
import random

class resultadoprova:
   # Atributos   
   def set_resultado(self, nome, nota):
     self.nome = nome
     self.nota = nota  
   # Metodos
   def get_nome(self):
     return self.nome 
   def get_nota(self):
     return self.nota 
   

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
    notabanco = db.executesql("""SELECT  e.first_name,  e.last_name, sum(i.valor) as nota, k.nome as turma, c.referencia, c.data_aplicacao, o.first_name,  o.last_name
                                           FROM item_prova_gerada as a  
                                           left join prova_gerada as b on a.prova_gerada==b.id 
                                           left join prova as c on b.prova==c.id 
                                           left join aluno as d on b.aluno==d.id 
                                           left join auth_user as e on d.usuario=e.id
                                           left join questao as f on a.questao==f.id
                                           left join plano_de_prova as g on c.plano_de_prova==g.id
                                           left join alternativa as h on a.alternativa_escolhida==h.id
                                           left join turma as k on c.turma==k.id
                                           left join professor as n on g.professor==n.id
                                           left join auth_user as o on n.usuario=o.id
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova) where h.correta=="T" group by c.referencia, g.referencia, e.first_name, e.last_name order by sum(i.valor) desc
                                     """)
                                     
    testebanco = db.executesql("""SELECT  e.first_name,  e.last_name, c.tipo as avaliacao, m.nome as taxionomia, sum(i.valor) as nota
                                           FROM item_prova_gerada as a  
                                           left join prova_gerada as b on a.prova_gerada==b.id 
                                           left join prova as c on b.prova==c.id 
                                           left join aluno as d on b.aluno==d.id 
                                           left join auth_user as e on d.usuario=e.id
                                           left join questao as f on a.questao==f.id
                                           left join plano_de_prova as g on c.plano_de_prova==g.id
                                           left join alternativa as h on a.alternativa_escolhida==h.id
                                           left join turma as k on c.turma==k.id
                                           left join taxionomia as m on f.taxionomia==m.id
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova) where h.correta=='T' group by e.first_name,  e.last_name, m.nome order by sum(i.valor) desc
                                     """)                                  
    
    
    
    resposta = []
    notar=[]
    #resultado = resultadoprova()
    for resp in notabanco:
        if resp[0]==None:
           nome='-'
        else:
           nome=resp[0] + " " + resp[1]
        if resp[2]==None:
           nota = 0
        else:
           nota = float(resp[2]) 
        if resp[3]==None:
           turma = "-"
        else:
           turma = resp[3]    
        if resp[4]==None:
           prova = "-"
        else:
           prova = resp[4] 
        if resp[5]==None:
           data = "-"
        else:
           data = str(resp[5])
        if resp[6]==None:
           professor = "-"
        else:
           professor = resp[6]+' ' + resp[7]   
                               
        #resultado.set_resultado(nome,nota)
        rr={}
        rr['name']= str(prova) + " - " + str(nome)
        rr['start']=nota
        resposta.append(rr)
        ss={}
        ss['professor']=professor
        ss['prova']=prova
        ss['turma']=turma
        ss['nome']=nome
        ss['nota']=nota
        ss['data']=data
        notar.append(ss)
        
  
    #dado = ["vagton", 8.0, "Jose Roberto", 9.0,"Zezaum", 10.0,]
    #dado = ["Zezaum", 10.0]
    #names = [x for i, x in enumerate(dado) if not i % 2]
    #starts = [x for i, x in enumerate(dado) if i % 2]
    #for name, start in zip(names, starts):
    #    resposta.append({'name': name, 'start': start})
    return dict(resposta=resposta, notar=notar, testebanco=testebanco)

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
