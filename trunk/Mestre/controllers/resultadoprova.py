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
    if 'auth' in globals():
        if auth.is_logged_in():
          if request.args(0)=='imp':
             vimp='imp'
          else:
             vimp=None   
          row_prova = db().select(db.prova.ALL)
          if row_prova: 
            pergunta = FORM(TABLE(
                          TR('Qual a Prova?', SELECT([OPTION(pro.referencia,_value=pro.referencia) for pro in db().select(db.prova.referencia,distinct=True)],_name='prova',requires=IS_IN_DB(db,'prova.referencia')), INPUT(_type='submit', _value='Pesquisar')),
                       ))
            if pergunta.accepts(request.vars, session):
                #pega identificao da prova
                prova = pergunta.vars.prova
                query = """SELECT a.id, c.referencia as prova, g.referencia as plano_de_prova, e.first_name,  e.last_name, c.data_aplicacao, b.data as data_conclusao, b.gerada, f.enunciado, h.resposta, h.correta, i.valor, j.nome as taxonomia
                                           FROM item_prova_gerada as a  
                                           left join prova_gerada as b on a.prova_gerada==b.id 
                                           left join prova as c on b.prova==c.id 
                                           left join aluno as d on b.aluno==d.id 
                                           left join auth_user as e on d.usuario=e.id
                                           left join questao as f on a.questao==f.id
                                           left join plano_de_prova as g on c.plano_de_prova==g.id
                                           left join alternativa as h on a.alternativa_escolhida==h.id
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova) 
                                           left join taxionomia as j on f.taxionomia==j.id
                                           where c.referencia == %s """ % ("'" + str(prova) + "'")
                resposta = db.executesql(query)
                
                query = """SELECT c.referencia as prova, g.referencia as plano_de_prova, e.first_name,  e.last_name, c.data_aplicacao, b.data as data_conclusao, b.gerada, f.enunciado, h.resposta, h.correta, sum(i.valor), c.tipo
                                           FROM item_prova_gerada as a  
                                           left join prova_gerada as b on a.prova_gerada==b.id 
                                           left join prova as c on b.prova==c.id 
                                           left join aluno as d on b.aluno==d.id 
                                           left join auth_user as e on d.usuario=e.id
                                           left join questao as f on a.questao==f.id
                                           left join plano_de_prova as g on c.plano_de_prova==g.id
                                           left join alternativa as h on a.alternativa_escolhida==h.id
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova) where h.correta=="T" and c.referencia == %s group by c.referencia, g.referencia, e.first_name, e.last_name """ % ("'" + str(prova) + "'")
                                           
                totaliza = db.executesql(query)
                return dict(pergunta=None, resposta=resposta, totaliza=totaliza, vimp=vimp)
            elif pergunta.errors:
                response.flash = 'Formulario Invalido'
            else:
                response.flash = 'Por favor, Selecione uma prova!'
                return dict(pergunta=pergunta, resposta=None, totaliza=None, vimp=vimp)
          else:      
              return dict(pergunta="não possue prova cadastrada", resposta=None, totaliza=None, vimp=vimp)
        else:
            redirect(URL(r=request, f='../default/user/login'))
    else:
        redirect(URL(r=request, f='../default/user/login'))
