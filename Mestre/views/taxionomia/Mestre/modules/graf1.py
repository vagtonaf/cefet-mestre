import numpy as np
import matplotlib.pyplot as plt

def gera_grafico(aluno_nota,tit_grafico,tity,titx,nom_arq):
    pos = np.arange(len(aluno_nota))+.5 
    nomes=[aluno['nome'] for aluno in aluno_nota]
    notas=[aluno['nota'] for aluno in aluno_nota]
    plt.subplot(111).set_autoscale_on(False)
    plt.axis((0,10,0,len(aluno_nota)))
    plt.barh(pos,notas, align='center')
    plt.yticks(pos, nomes)
    plt.xlabel(titx)
    plt.ylabel(tity)
    plt.title(tit_grafico)
    plt.grid(True, alpha=0.3)
    plt.savefig(nom_arq)

#if __name__=='__main__':
#    ls_aluno=[{'nome':'ze','nota':8},{'nome':'augusto','nota':7.5},{'nome':'gustavo','nota':5},{'nome':'Dani','nota':8.5}]
#    gera_grafico(ls_aluno,'Turma 01 - Notas','Alunos','Notas','Turma01.png')
