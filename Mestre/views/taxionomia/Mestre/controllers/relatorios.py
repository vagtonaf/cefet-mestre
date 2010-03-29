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
    gera_grafico(aluno_nota,'Turma 01 - Notas','Alunos','Notas','applications\Mestre\static\turma01.png')
    return dict(imagem = 'turma01.png')
    
def rel_alunos_turma():
    q_where=(db.aluno.id==db.alocacao.aluno)&(db.alocacao.turma==db.turma.id)
    db_alunos=db(q_where).select(db.turma.nome,db.alocacao.turma,db.aluno.ALL,db.alocacao.data)
    print db(q_where)._select(db.aluno.ALL,db.alocacao.turma,db.alocacao.data,db.turma.nome)
    return { 'v_alunos' : db_alunos}
