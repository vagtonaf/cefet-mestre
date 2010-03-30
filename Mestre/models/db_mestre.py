is_phone = IS_MATCH('^(\+\d{2}\-)?[\d\-]*(\#\d+)?$')

TASK_TYPES = ('Phone', 'Fax', 'Mail', 'Meet')
LISTA_TAXIONOMIA = ('Analizar','Compreender','Lembrar','Aplicar','Avaliar','Criar')
LISTA_DIFICULDADE = ('Fácil','Médio','Difícil')


if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

def advanced_editor(field, value):
    return TEXTAREA(_id = str(field).replace('.','_'), _name=field.name, _class='text ckeditor', value=value, _cols=80, _rows=10)
    
import datetime; now=datetime.datetime.now()

        
db.define_table('administrador',
        Field('usuario',db.auth_user)
        )
db.administrador.usuario.requires=IS_IN_DB(db,'auth_user.id','%(first_name)s %(last_name)s - %(email)s')       
db.define_table('professor',
        Field('usuario',db.auth_user),
        Field('codigo_funcional',length=10,notnull=True)
        )
db.professor.usuario.requires=IS_IN_DB(db,'auth_user.id','%(first_name)s %(last_name)s - %(email)s')
db.professor.codigo_funcional.requires=IS_NOT_IN_DB(db, 'professor.codigo_funcional') 

db.define_table('aluno',
        Field('usuario',db.auth_user),
        Field('matricula',length=10,notnull=True)
        )
db.aluno.usuario.requires=IS_IN_DB(db,'auth_user.id','%(first_name)s %(last_name)s - %(email)s')
db.aluno.matricula.requires=IS_NOT_IN_DB(db, 'aluno.matricula') 

db.define_table('instituicao',
        Field('nome',length=50,notnull=True)
        )
db.instituicao.nome.requires=IS_NOT_IN_DB(db, 'instituicao.nome') 
        
db.define_table('curso',
        Field('nome',length=50,notnull=True),
        Field('instituicao',db.instituicao)
        )
db.curso.instituicao.requires=IS_IN_DB(db,'instituicao.id','instituicao.nome')
db.curso.nome.requires=IS_NOT_IN_DB(db(db.curso.instituicao==request.vars.instituicao),db.curso.nome)


db.define_table('disciplina',
        Field('nome',length=50,notnull=True),
        Field('curso',db.curso)
        )
db.disciplina.curso.requires=IS_IN_DB(db,'curso.id','curso.nome')
db.disciplina.nome.requires=IS_NOT_IN_DB(db(db.disciplina.curso==request.vars.curso),db.disciplina.nome)


db.define_table('turma',
        Field('nome',length=50,notnull=True),
        Field('turno','string',requires=IS_IN_SET(["MANHÃ","TARDE","NOITE"])),
        Field('disciplina',db.disciplina)
        )
db.turma.disciplina.requires=IS_IN_DB(db,'disciplina.id','disciplina.nome')
db.turma.nome.requires=[IS_NOT_IN_DB(db(db.turma.disciplina==request.vars.disciplina),db.turma.nome),IS_NOT_IN_DB(db(db.turma.turno==request.vars.turno),db.turma.nome)]


db.define_table('alocacao',
        Field('aluno',db.aluno),
        Field('turma',db.turma),
        Field('data','datetime',default=request.now, writable=False)
        )
db.alocacao.aluno.requires=IS_IN_DB(db,'aluno.id','aluno.matricula') #db(db.auth_user.id==aluno.id).select(db.auth_user.first_name)})
db.alocacao.turma.requires=IS_IN_DB(db,'turma.id','turma.nome')

db.define_table('taxionomia',
        Field('nome','string',requires=IS_IN_SET(["Analizar","Compreender","Lembrar","Aplicar","Avaliar","Criar"]))
        )
db.taxionomia.nome.requires=[IS_NOT_IN_DB(db,'taxionomia.nome'),IS_IN_SET(LISTA_TAXIONOMIA)]    
if not len(db().select(db.taxionomia.ALL)):
    for taxonomia in LISTA_TAXIONOMIA:
        db.taxionomia.insert(nome = taxonomia)

db.define_table('dificuldade',
        Field('nivel','string',requires=IS_IN_SET(["Fácil","Médio","Difícil"]))
        )
db.dificuldade.nivel.requires=IS_NOT_IN_DB(db,'dificuldade.nivel')  
if not len(db().select(db.dificuldade.ALL)):
    for dificuldade in LISTA_DIFICULDADE:
        db.dificuldade.insert(nivel = dificuldade)

db.define_table('topico',
        Field('nome',length=50,notnull=True)
        )
db.topico.nome.requires=IS_NOT_IN_DB(db, 'topico.nome')     

db.define_table('questao',
        Field('enunciado','text',notnull=True),
        Field('taxionomia',db.taxionomia),
        Field('dificuldade',db.dificuldade),
        Field('topico',db.topico)
        )
db.questao.taxionomia.requires=IS_IN_DB(db,'taxionomia.id','taxionomia.nome')
db.questao.dificuldade.requires=IS_IN_DB(db,'dificuldade.id','dificuldade.nivel')
db.questao.topico.requires=IS_IN_DB(db,'topico.id','topico.nome')
db.questao.enunciado.requires=IS_NOT_IN_DB(db, 'questao.enunciado') 

db.define_table('alternativa',
        Field('questao',db.questao),
        Field('resposta','text',notnull=True),
        Field('correta','boolean') 
        )
db.alternativa.questao.requires=IS_IN_DB(db,'questao.id','questao.enunciado')
db.alternativa.resposta.requires=IS_NOT_IN_DB(db, 'alternativa.resposta')

db.define_table('plano_de_prova',
        Field('referencia',length=50,notnull=True),
        Field('professor',db.professor)
        )
db.plano_de_prova.referencia.requires=IS_NOT_IN_DB(db,'plano_de_prova.referencia')
#db.plano_de_prova.professor.requires=IS_IN_DB(db,'professor.id','professor.codigo_funcional')   
db.plano_de_prova.professor.requires=IS_IN_DB(db,'professor.id','Codigo Funcional: %(codigo_funcional)s')

db.define_table('item_plano_de_prova',
        Field('valor','double',default=10.0,requires=IS_FLOAT_IN_RANGE(0,10.0)),
        Field('plano_de_prova',db.plano_de_prova),
        Field('taxionomia',db.taxionomia),
        Field('dificuldade',db.dificuldade),
        Field('topico',db.topico) 
        )
       
db.item_plano_de_prova.plano_de_prova.requires=IS_IN_DB(db,'plano_de_prova.id','plano_de_prova.referencia')
db.item_plano_de_prova.taxionomia.requires=IS_IN_DB(db,'taxionomia.id','taxionomia.nome')
db.item_plano_de_prova.dificuldade.requires=IS_IN_DB(db,'dificuldade.id','dificuldade.nivel')
db.item_plano_de_prova.topico.requires=IS_IN_DB(db,'topico.id','topico.nome')
      

db.define_table('prova',
        Field('referencia',length=50,notnull=True),
        Field('turma',db.turma),
        Field('plano_de_prova',db.plano_de_prova),
        Field('tipo','string',requires=IS_IN_SET(["P1","SCHP1","P2","SCHP2","P3","SCHP3","PF","SCHPF","PR",]))
        )
db.prova.referencia.requires=IS_NOT_IN_DB(db,'prova.referencia') 
db.prova.turma.requires=IS_IN_DB(db,'turma.id','turma.nome')
db.prova.plano_de_prova.requires=IS_IN_DB(db,'plano_de_prova.id','plano_de_prova.referencia') 


db.define_table('prova_gerada',
        Field('data','datetime',default=request.now, writable=False),
        Field('aluno',db.aluno),
        Field('prova',db.prova)
        )

db.prova_gerada.aluno.requires=IS_IN_DB(db,'aluno.id','aluno.matricula')
db.prova_gerada.prova.requires=IS_IN_DB(db,'prova.id','prova.referencia')

db.define_table('item_prova_gerada',
        Field('prova_gerada',db.prova_gerada),
        Field('questao',db.questao),
        Field('alternativa_correta',db.alternativa)
        )

db.item_prova_gerada.questao.requires=IS_IN_DB(db,'questao.id','questao.enunciado')
db.item_prova_gerada.alternativa_correta.requires=IS_IN_DB(db,'alternativa.id','alternativa.resposta',db(db.alternativa.id==db.item_prova_gerada.questao))
