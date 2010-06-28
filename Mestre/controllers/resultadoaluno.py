# coding: utf8
# try something like
class resultadoAluno:
   # Atributos   
   prova = None
   plano = None
   nome = None
   aplicacao = None
   conclusao = None
   nota = None
   def set_resultado(self, prova, plano, nome, aplicacao, conclusao, nota):
     self.prova = prova
     self.plano = plano
     self.nome = nome
     self.aplicacao = aplicacao
     self.conclusao = conclusao
     self.nota = nota  
   # Metodos
   def get_prova(self):
     return self.prova
   def get_plano(self):
     return self.plano
   def get_nome(self):
     return self.nome 
   def get_aplicacao(self):
     return self.aplicacao 
   def get_conclusao(self):
     return self.conclusao 
   def get_nota(self):
     return self.nota     
   def minha_nota(self):  
     if self.prova=='-':
        self.nota="-"
        return "O aluno nao possue resultado"   
     if ((self.nota > 1) & (self.nota <= 6)):
        return "A nota do aluno: " + self.nome + " e " + str(self.nota) + ", prova:" + self.prova + ", ela foi baixa, o aluno deve melhorar!"
     elif (self.nota >= 10):               
        return "A nota do aluno: " + self.nome + " e " + str(self.nota) + ", prova:" + self.prova + ", ela foi otima continue assim!"
     elif ((self.nota > 6) & (self.nota < 10)):
        return "A nota do aluno: " + self.nome + " e " + str(self.nota) + ", prova:" + self.prova + ", muito bem!"
     elif self.nota=='-':
        return "O Aluno não possue nota!"
     else:
        return "O Aluno levou Zero!"

def executesql(self, query): 
    self['_lastsql'] = query    
    self._execute(query)
    try:        
        return self._cursor.fetchall()
    except:
        return None


def nota_aluno():
    # aluno Algusto Silva id=5 possue resultado
    usuario_id=request.args(0) or redirect(URL(r=request,f='../default/error'))
    query = """SELECT c.referencia as prova, g.referencia as plano_de_prova, e.first_name,  e.last_name, c.data_aplicacao, b.data as data_conclusao, sum(i.valor) as nota  
                                           FROM item_prova_gerada as a  
                                           left join prova_gerada as b on a.prova_gerada==b.id 
                                           left join prova as c on b.prova==c.id 
                                           left join aluno as d on b.aluno==d.id 
                                           left join auth_user as e on d.usuario=e.id
                                           left join questao as f on a.questao==f.id
                                           left join plano_de_prova as g on c.plano_de_prova==g.id
                                           left join alternativa as h on a.alternativa_escolhida==h.id
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova) where h.correta == 'T' and d.usuario == %s  group by c.referencia,  g.referencia, e.first_name, e.last_name, c.data_aplicacao,  b.data order by b.data""" % (str(usuario_id))
    nota = db.executesql(query)
    refObj=[]
    for resp in nota:
        resultado = resultadoAluno()
        if resp[0]==None:
           prova='-'
        else:
           prova=resp[0]
        if resp[1]==None:
           plano='-'
        else:
           plano=resp[1]
        if resp[2]==None:
           nome='-'
        else:
           nome=resp[2] + " " + resp[3]
        if resp[4]==None:
           aplicacao='-'
        else:
           aplicacao=resp[4]
        if resp[5]==None:
           conclusao='-'
        else:
           conclusao=resp[5]
        if resp[6]==None:
           nota = '-'
        else:
           nota = float(resp[6]) 
        if conclusao=='-':
           nota = 'Prova sendo realizada!'                                 
        if (conclusao=='-') & (prova=='-'):
           nota = 'Prova a ser realizada!'                                 
        resultado.set_resultado(prova,plano,nome,aplicacao,conclusao,nota)
        refObj.append(resultado)
    return dict(resultado=refObj)
