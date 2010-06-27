# coding: utf8
# try something like
# coding: utf8
# try something like
    
def executesql(self, query): 
    self['_lastsql'] = query    
    self._execute(query)
    try:        
        return self._cursor.fetchall()
    except:
        return None


def rel():
 if 'auth' in globals():
  if auth.is_logged_in():
    if request.args(1)=='imp':
       vimp='imp'
    else:
       vimp=None   
    #pega o Professor  
    nome=auth.user.first_name
    sobrenome=auth.user.last_name
    nome = nome + ' ' + sobrenome
    idUsuario=auth.user.id
    referencia=request.args(0) or redirect(URL(r=request,f='../default/error')) 
    #testa se é um professor
    row_professor=db(db.professor.usuario==idUsuario).select(db.professor.ALL)
    if row_professor:
        if referencia=='Turma_Aluno':
            resultado = db.executesql("""SELECT a.nome, a.turno, c.matricula, d.first_name, d.last_name
                                     FROM turma as a  
                                     inner join alocacao as b on b.turma==a.id
                                     inner join aluno as c on b.aluno==c.id
                                     inner join auth_user as d on c.usuario==d.id
                                     """)
        
        elif referencia=='Turma_Aluno_Disciplina':
            resultado = db.executesql("""SELECT a.nome, a.turno,  c.matricula, d.first_name, d.last_name, e.nome
                                     FROM turma as a  
                                     inner join alocacao as b on b.turma==a.id
                                     inner join aluno as c on b.aluno==c.id
                                     inner join auth_user as d on c.usuario==d.id
                                     inner join disciplina as e on b.turma==e.id
                                      """)
        else:
            resultado = None 
    else:   
        resultado = FORM(TABLE(TR('Só Professor pode executar esse relatôrio!')))
    return dict(resultado=resultado, nome=nome, referencia=referencia, vimp=vimp)
