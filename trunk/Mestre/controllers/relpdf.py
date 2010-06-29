# coding: utf8
# try something like

def executesql(self, query): 
    self['_lastsql'] = query    
    self._execute(query)
    try:        
        return self._cursor.fetchall()
    except:
        return None
        
    
def arqpdf():
    import datetime
    import time
    try:
      from reportlab.pdfgen import canvas
      from reportlab.lib.pagesizes import A4, landscape, letter
      from reportlab.lib.units import cm, mm, inch, pica
      from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
      from reportlab.lib.styles import getSampleStyleSheet
      from reportlab.graphics.shapes import Drawing
      from reportlab.graphics.charts.barcharts import VerticalBarChart
    except: 
      return dict(filename=None, msg='Falta a Bliblioteca para gerar o pdf, procure o administrador!')       
    import gluon.contenttype
    import StringIO
    resp = StringIO.StringIO()
    dataref = datetime.date.today()
     
    filename = 'applications/Mestre/static/relpdf'+str(dataref)+'.pdf'
    filename2 = 'relpdf'+str(dataref)+'.pdf'
    pdf = canvas.Canvas(filename, pagesize = letter) #Nome do arquivo e Tipo do papel
    pdf.setTitle("Relatorio de Alunos")
    pdf.setFont('Courier',6) #Seta a fonte para Courier tamanho 12
    pdf.setStrokeColorRGB(1, 0, 0)
    row_aluno=db().select(db.aluno.ALL)
    query = """SELECT c.referencia as prova, g.referencia as plano_de_prova, e.first_name,  e.last_name, c.data_aplicacao, b.data as data_conclusao, b.gerada, f.enunciado, h.resposta, h.correta, i.valor
                                           FROM item_prova_gerada as a  
                                           left join prova_gerada as b on a.prova_gerada==b.id 
                                           left join prova as c on b.prova==c.id 
                                           left join aluno as d on b.aluno==d.id 
                                           left join auth_user as e on d.usuario=e.id
                                           left join questao as f on a.questao==f.id
                                           left join plano_de_prova as g on c.plano_de_prova==g.id
                                           left join alternativa as h on a.alternativa_escolhida==h.id
                                           left join item_plano_de_prova as i on (f.taxionomia==i.taxionomia and f.dificuldade==i.dificuldade and f.topico==i.topico and c.plano_de_prova==i.plano_de_prova) """ 
                                           
    respQuery = db.executesql(query)
    lista = pdf.beginText(inch * 1, inch * 10)
    lista.textLine('Resultado da Prova dos Alunos')
    for item,reg in enumerate(respQuery):
         if reg[6]=='T':
            r1='Sim'
         else:
            r1='Não' 
         if reg[9]=='T':
            r2='Sim'
         else:
            r2='Não'   
         lista.textLine("#####################################################################################") 
         lista.textLine('Prova:[' + reg[0] + '] Plano de Prova:[ ' + reg[1] + ']')
         lista.textLine('Data da Aplicação:[ ' + str(reg[4]) + '] Data da Conclusão:[' + str(reg[5])+']')
         lista.textLine('Aluno:[' + reg[2] + ' ' + reg[3] + '] Prova foi Gerada:[' + r1 + ']')
         lista.textLine('Enunciado:[' + reg[7] + ']')
         lista.textLine('Resposta:[' + str(reg[8]) + '] Resposta estava Correta:[' + r2 + '] Valor da Questão:[' + str(reg[10])+']')
    pdf.drawText(lista)
    pdf.showPage()
    try:
      pdf.save()
    except: 
      return dict(filename=str(filename2), msg='Professor, o arquivo está aberto e não pode ser criado, por favor feche o Acrobat Read')
    #resp.seek(0)
    #response.headers['Content-Type'] = gluon.contenttype.contenttype('.pdf')
    #response.headers['Content-disposition'] = "attachment; filename='relpdf"+str(dataref)+".pdf"
    #return resp.read()
    #return response.stream(resp,chunk_size=64*1024)
    return dict(filename=str(filename2), msg=None)
