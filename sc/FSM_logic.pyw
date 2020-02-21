#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FSM_logic.py
#  
#  Copyright 2020 badanni <dannyvasconeze@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import os, sys, re
#from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QColorDialog, QFileDialog, QDialogButtonBox
from PyQt5 import uic

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

import graphviz_standalone as gv #graphviz modified for run dot.exe precompilate
#import graphviz as gv
##########UI################
class Ventana(QMainWindow):
 #Método constructor de la clase
 def __init__(self):
  self.first_if=False
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("gui/main.ui", self)
  
  self.setWindowTitle("Logika Wizard")
  self.archivo_trabajo_LN=""
  self.image = QImage()
  scene = QGraphicsScene()
  scene.addText("FlowChart")
  self.graphicsView.setScene(scene)
  self.rpy_class1='''init -1 python hide:
    config.log = "debuglog.txt"

init python:

    import math
    import pickle

    class FSM_logic(object):
        def __init__(self, label_0="'''
  self.rpy_class1b='''",logger=False):
            self.state=label_0
            self.logika = logger
            self.log_FSM=[]
        def logger(self,data):
            f=open("debug.img","wb")
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
            f.close()
            return 0
        def read_logger(self):
            s=file("debug.img","rb")
            value=pickle.load(s)
            s.close()
            return value
        def logic(self,command):
            old_state=self.state
'''
  self.rpy_class2='''            self.log_FSM.append(self.state)
            if self.logika:
                self.logger(self.log_FSM)
            if renpy.has_label(self.state):
                return self.state
            else:
                renpy.log("Warning: Something happened there is no label: {} / Class FSM_logic".format(self.state))
                renpy.notify("Something happened there is no label: {}".format(self.state))
                #puedo configurar para que retroceda un paso
                return old_state
  '''
  self.buttonBox.button(QDialogButtonBox.Open).clicked.connect(self.abrir_proyecto)
  self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.guardar_proyecto)
  self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.cerrar_proyecto)
  self.pushButton.clicked.connect(self.translate_LN)
  self.label_3.mousePressEvent = self.abrir_acerca_de
 
 def abrir_acerca_de(self,event):
  _acerca_de = Acerca_de()
  _acerca_de.acerca_de_etiqueta.setText("""
  Author: BaDanNi
  Site: badanni.itch.io
  Licence: CC-By 4.0
  
  Project derived from Tagon, aplication alpha
  """)
  _acerca_de.exec_()

 def abrir_proyecto(self):
  self.first_if=False
  if len(self.plainTextEdit.toPlainText())!=0:
   resultado = QMessageBox.question(self, "Are you sure?", "At the moment you have a file in edition, surely you want to open a new one?", QMessageBox.Yes | QMessageBox.No)
   if resultado == QMessageBox.Yes:
    self.leer_proyecto()
   else:
    pass
  else:
   self.leer_proyecto()

 def guardar_proyecto(self):
  self.first_if=False
  if len(self.plainTextEdit.toPlainText())==0:
   QMessageBox.information(self, "Document is empty", "Document is empty", QMessageBox.Close)
  elif len(self.plainTextEdit.toPlainText())!=0 and self.archivo_trabajo_LN!="":
   mensaje=self.plainTextEdit.toPlainText()
   res = open(self.archivo_trabajo_LN, "w")
   for line in mensaje:
    res.write(line)
   res.close()
   QMessageBox.information(self, "Project saved", "Project saved", QMessageBox.Ok)
  elif len(self.plainTextEdit.toPlainText())!=0 and self.archivo_trabajo_LN=="":
   options = QFileDialog.Options()
   options |= QFileDialog.DontUseNativeDialog
   files, _ = QFileDialog.getSaveFileName(self,"Save project", "","Logika Project (*.proj)", options=options)
   if len(files)>0:
    f=open(os.path.normpath(files),"w")
    for line in self.plainTextEdit.toPlainText():
     f.write(line)
    f.close()
    QMessageBox.information(self, "Project saved", "Project saved", QMessageBox.Ok)
 
 def cerrar_proyecto(self):
  self.first_if=False
  if len(self.plainTextEdit.toPlainText())!=0:
   resultado = QMessageBox.question(self, "Are you sure?", "At the moment you have a file in edition, surely you want to close it?", QMessageBox.Yes | QMessageBox.No)
   if resultado == QMessageBox.Yes:
     self.plainTextEdit.setPlainText("")
     self.plainTextEdit_2.setPlainText("")
     self.plainTextEdit_3.setPlainText("")
     self.setWindowTitle("Logika Wizard")
     self.archivo_trabajo_LN=""
     scene = QGraphicsScene()
     scene.addText("FlowChart")
     self.graphicsView.setScene(scene)
   else:
    pass
  else:
   QMessageBox.information(self, "Document is empty", "Document is empty", QMessageBox.Close)
 def leer_proyecto(self):
  options = QFileDialog.Options()
  options |= QFileDialog.DontUseNativeDialog
  files, _ = QFileDialog.getOpenFileNames(self,"Open project", "","Logika Project (*.proj)", options=options) ## "Tagon Project (base.db);;All Files (*)"
  if files!=[]:
   self.setWindowTitle("Logika Wizard - OPEN FILE")
   self.plainTextEdit.setPlainText("")
   self.plainTextEdit_2.setPlainText("")
   self.plainTextEdit_3.setPlainText("")
   self.archivo_trabajo_LN=os.path.normpath(files[0])
   f=open(os.path.normpath(files[0]),"r")
   for text in f:
    self.plainTextEdit.insertPlainText(text)
   f.close()

 def translate_LN(self):
  self.first_if=False
  data={"start":None,"conditions":[]}
  if os.path.isdir("output")==False:
   os.mkdir("output")
  #
  scene = QGraphicsScene()
  scene.addText("FlowChart")
  self.graphicsView.setScene(scene)
  #
  
  error_general=False
  datos=data_translate()
  self.plainTextEdit_2.setPlainText("")
  self.plainTextEdit_3.setPlainText("")
  res = open("output/logic_renpy.txt", "w")
  rpy = open("output/logic_renpy.rpy", "w")
  document=self.plainTextEdit.toPlainText().split("\n")
  if document[-1]=="":
   document.pop(-1)
  for i,text in enumerate(document):
   interpreter = Interpreter(text.rstrip())
   result = interpreter.expr()
   if result!="ERROR" and len(self.plainTextEdit.toPlainText())>0:
    #ren'Py Logic FSM 
    text=result[0]+"\n"
    if text[:2]=="if" and self.first_if==True:
      text="el"+text
    elif text[:2]=="if" and self.first_if==False:
      self.first_if=True
    res.write(text)
    self.plainTextEdit_2.insertPlainText(text)
    #guardar data
    if result[1]!=None and len(result[1])<2:
      data["start"]=result[1][0]
    else:
      data["conditions"].append(result[1])
   else:
    QMessageBox.warning(self, "ERROR", "Check line", QMessageBox.Ok)
  res.close()
  
  if data["start"]!=None and len(data["conditions"])>0:
    
    f=gv.Digraph("FSM",filename="logic")
    f.attr('graph',rankdir='LR',size='8,5')
    f.attr('node',shape='doublecircle')
    f.node(str(data["start"]))
    f.attr('node',shape='point')
    f.node('qi')
    f.edge('qi',str(data["start"]))
    f.attr('node',shape='circle')
    for i,linea in enumerate(data["conditions"]):
      f.edge(str(linea[0]),str(linea[2]),label=str(linea[1]))
    f.directory="output"
    f.format='png'
    f.render()
    f.format='svg'
    f.render()
    
    rpy.write(self.rpy_class1)
    rpy.write(data["start"])
    rpy.write(self.rpy_class1b)
    self.plainTextEdit_3.insertPlainText(self.rpy_class1)
    self.plainTextEdit_3.insertPlainText(data["start"])
    self.plainTextEdit_3.insertPlainText(self.rpy_class1b)
    for i,linea in enumerate(data["conditions"]):
      if i==0:
        text="if self.state=='"+str(linea[0])+"' and command in "+str(linea[1])+": self.state='"+str(linea[2])+"'"+"\n"
        rpy.write("            "+text)
        self.plainTextEdit_3.insertPlainText("            "+text)
      else:
        text="elif self.state=='"+str(linea[0])+"' and command in "+str(linea[1])+": self.state='"+str(linea[2])+"'"+"\n"
        rpy.write("            "+text)
        self.plainTextEdit_3.insertPlainText("            "+text)
    rpy.write(self.rpy_class2)
    self.plainTextEdit_3.insertPlainText(self.rpy_class2)
    #
    QMessageBox.information(self, "File created", "output/FSM_logic_renpy.txt")
    QMessageBox.information(self, "File created", "output/FSM_logic_renpy.rpy")
    filename="output/logic.png"
    self.image = QImage(filename)
    if self.image.isNull():
        QMessageBox.information(self, "Image Viewer", "Cannot load %s." % filename)
    if type(self.image) is QPixmap:
        pixmap = self.image
    elif type(self.image) is QImage:
        pixmap = QPixmap.fromImage(self.image)
    else:
        raise RuntimeError("ImageViewer.setImage: Argument must be a QImage or QPixmap.")
    scene = QGraphicsScene()
    #scene.addText("Hello, world!")
    scene.addPixmap(pixmap)
    self.graphicsView.setScene(scene)
    #
  rpy.close()

class data_translate(object):
  def __init__(self):
   self.start=""
   self.states=[]
   self.error1=0
   self.error2=0

class Acerca_de(QDialog):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("gui/about.ui", self)
  self.setWindowTitle("About of Logika Wizard")
  self.acerca_de_bt_cerrar.clicked.connect(self.cerrar_ventana)
 def cerrar_ventana(self):
  self.close()

#############LOGIC##########
START,IF, SEND, OR, GOTO,STRING, INTEGER, EOF= ('START','IF', 'SEND', 'OR', 'GOTO','STRING','INTEGER','EOF')


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(IF, 3)
            Token(IF, 'hola')
            Token(GET, 'next')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "IF a SEND b OR c GOTO d"
        self.text = text
        self.pos=0
        self.comands = self.text.split(" ")
        self.current_comand=self.comands[self.pos]

    def error(self):
        print("Invalid character\nCheck FSM_logic_log.txt\n")
        raise Exception('Invalid character\nCheck FSM_logic_log.txt\n')
        #return Token(ERROR, str(self.current_comand))

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.comands) - 1:
            self.current_comand = None  # Indicates end of input
        else:
            self.current_comand = self.comands[self.pos]

    def skip_whitespace(self):
        while self.current_comand is not None and self.current_comand.isspace():
            self.advance()

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_comand is not None:
            if self.current_comand.isspace():
                self.skip_whitespace()
                continue
            if self.current_comand in ['START','start']:
                value = Token(START, str("label_0="))
            elif self.current_comand in ['IF','if']:
                value = Token(IF, str("if self.state=='"))
            elif self.current_comand in ['OR','or']:
                value = Token(OR, str(self.current_comand))
            elif self.current_comand in ['SEND','send']:
                value = Token(SEND, str("' and command in "))
            elif self.current_comand in ['GOTO','goto']:
                value = Token(GOTO, str(": self.state='"))
            elif self.current_comand.isdigit():
                value = Token(INTEGER,int(self.current_comand))
            else:
                value = Token(STRING,str(self.current_comand))
            self.advance()
            return value

        return Token(EOF, None)

class Interpreter():
    def __init__(self, text):
        self.text = text
        self.lexer=Lexer(text)
        self.pos = 0
        self.current_token = None
    def error(self):
        raise Exception('Error parsing input')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.lexer.get_next_token()
        token = self.current_token
        result="ERROR"
        data=None
        if token.type == START:
         left = self.current_token
         self.eat(START)
         op = self.current_token
         self.eat(STRING)
         result = left.value+op.value
         data = [op.value]
        elif token.type == IF:
         left = self.current_token
         self.eat(IF)
         state_actual=self.current_token
         self.eat(STRING)
         condition=self.current_token
         self.eat(SEND)
         condition_value=self.current_token
         self.eat(STRING)
         condition_message=[condition_value.value]
         while self.current_token.type == OR:
          self.eat(OR)
          condition_value_next=self.current_token
          self.eat(STRING)
          condition_message.append(condition_value_next.value)
         state_new=self.current_token
         self.eat(GOTO)
         state_new_value=self.current_token
         self.eat(STRING)
         result=left.value+state_actual.value+condition.value+str(condition_message)+state_new.value+state_new_value.value+"'"
         data=[state_actual.value,condition_message,state_new_value.value]
        return (result,data)

# read this https://www.programcreek.com/python/example/108106/PyQt5.QtWidgets.QGraphicsView
#watch this https://www.youtube.com/watch?v=IKqkOI_o6_A
if __name__ == '__main__':
	app = QApplication(sys.argv)
	#Crear un objeto de la clase
	_ventana = Ventana()
	#Mostra la ventana
	_ventana.show()
	#Ejecutar la aplicación
	app.exec_()
