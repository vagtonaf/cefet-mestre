# coding: utf8
# try something like
    
def executesql(self, query): 
    self['_lastsql'] = query    
    self._execute(query)
    try:        
        return self._cursor.fetchall()
    except:
        return None

def executesql2(self, query, args):
    #make self['_lastsql'] tell us the args used too
    self['_lastsql'] = query + "      with ARGS >> " + str(args)  
    self._execute(query, args)
    try:       
        return self._cursor.fetchall()    
    except:        
        return None

def resultadoprova():
    results = db.executesql("""SELECT a.id, c.referencia as prova, g.referencia as plano_de_prova, e.first_name,  e.last_name, c.data_aplicacao, b.data as data_conclusao, b.gerada, f.enunciado, h.resposta, h.correta, i.valor
                                           FROM item_prova_gerada as a  
                                           left join prova_gerada as b on a.prova_gerada==b.id 
                                           left join prova as c on b.prova==c.id 
                                           left join aluno as d on b.aluno==d.id 
                                           left join auth_user as e on d.usuario=e.id
                                           left join questao as f on a.questao==f.id
                                           left join plano_de_prova as g on c.plano_de_prova==g.id
                                           left join alternativa as h on a.alternativa_escolhida==h.id
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova)                                           
                                           """)
                                           
    totaliza = db.executesql("""SELECT a.id, c.referencia as prova, g.referencia as plano_de_prova, e.first_name,  e.last_name, c.data_aplicacao, b.data as data_conclusao, b.gerada, f.enunciado, h.resposta, h.correta, sum(i.valor)
                                           FROM item_prova_gerada as a  
                                           left join prova_gerada as b on a.prova_gerada==b.id 
                                           left join prova as c on b.prova==c.id 
                                           left join aluno as d on b.aluno==d.id 
                                           left join auth_user as e on d.usuario=e.id
                                           left join questao as f on a.questao==f.id
                                           left join plano_de_prova as g on c.plano_de_prova==g.id
                                           left join alternativa as h on a.alternativa_escolhida==h.id
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova) where h.correta=="T"
                                           """)
    return dict(resposta=results, totaliza=totaliza)
