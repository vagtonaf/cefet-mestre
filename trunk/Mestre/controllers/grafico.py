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
    if 'auth' in globals():
        if auth.is_logged_in():
          if request.args(0)=='imp':
             vimp='imp'
          else:
             vimp=None   
          row_turma = db().select(db.turma.ALL)
          if row_turma: 
            pergunta = FORM(TABLE(TR('Qual a Turma?', SELECT([OPTION(tur.nome,_value=tur.nome) for tur in db().select(db.turma.nome,distinct=True)],_name='turma',requires=IS_IN_DB(db,'turma.nome')), INPUT(_type='submit', _value='Pesquisar')),))
            if pergunta.accepts(request.vars, session):
               turma = pergunta.vars.turma
               selecao = db.executesql("""SELECT k.nome as turma,  m.nome as taxonomia, count(m.nome) as nota
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
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova) where h.correta=='T' and k.nome == %s group by  k.nome,  m.nome order by sum(i.valor) desc """ % ("'" + str(turma) + "'"))                                  
    
    
               resposta = []
               turmax = []
               if selecao:
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
                      nota = str(float(resp[2])) 
                   rr={}
                   rr['taxonomia']= str(taxonomia) 
                   rr['A']=nota
                   resposta.append(rr)
                   ss={}
                   ss['turma']= str(turma)
                   ss['taxonomia']= str(taxonomia)
                   ss['nota']= nota
                   turmax.append(ss) 
                 return dict(pergunta=pergunta, resposta=resposta, turma=turmax, vimp=vimp)
               else:
                 return dict(pergunta="Não possue resultado para essa turma", resposta=None,  turma=None, vimp=vimp)    
            elif pergunta.errors:
               response.flash = 'Formulario Invalido'
            else:
                response.flash = 'Por favor, Selecione uma turma!'
                return dict(pergunta=pergunta, resposta=None, turma=None, vimp=vimp)
          else:      
              return dict(pergunta="não possue turma cadastrada", resposta=None, turma=None, vimp=vimp)
        else:
            redirect(URL(r=request, f='../default/user/login'))
    else:
        redirect(URL(r=request, f='../default/user/login'))
