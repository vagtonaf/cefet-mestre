# coding: utf8
# try something like

def executesql(self, query): 
    self['_lastsql'] = query    
    self._execute(query)
    try:        
        return self._cursor.fetchall()
    except:
        return None
        
def grafico():
    selecao = db.executesql("""SELECT  k.nome as turma, m.nome as taxonomia, sum(i.valor) as nota
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
    turmax = []
    for resp in selecao:
        if resp[0]==None:
           turma='-'
        else:
           turma=resp[0] 
        if resp[1]==None:
           taxonomia='-'
        else:
           taxonomia=resp[1] 
        if resp[2]==None:
           nota = 0
        else:
           nota = float(resp[2]) 
  
        rr={}
        rr['taxonomia']= str(taxonomia) 
        rr['A']=nota
        resposta.append(rr)
        
        ss={}
        ss['turma']= str(turma)
        turmax.append(ss) 
        
    return dict(resposta=resposta, turma=turmax)
