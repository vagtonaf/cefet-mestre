# coding: utf8
# try something like
plot_helper=SQLDB("sqlite://plot_helper.db")

class PLOT:
   def __init__(self,**attributes):
       self.attributes=attributes
       if not attributes.has_key('_width'): attributes['_width']=400
       if not attributes.has_key('_height'): attributes['_height']=200
       self.id=attributes['_id']
       self.options=attributes['options'] if attributes.has_key('options') else {}
       self.type=attributes['type'] if attributes.has_key('type') else 'line'
       self.data=attributes['data'] if attributes.has_key('data') else 'data'
   def xml(self):
       attr=' '.join(['%s="%s"' %(k[1:],v) for k,v in self.attributes.items() if k[0]=='_'])
       txt='<div %s></div>\n<script type="text/javascript"><!--\nvar plot_%s=EasyPlot("%s", %s, $("%s"),%s);\n//--></script>' %(attr,self.id,self.type,repr(self.options),self.id,repr(self.data))
       return txt
