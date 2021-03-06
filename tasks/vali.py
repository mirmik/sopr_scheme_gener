import common
import paintwdg

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import taskconf_menu
import tablewidget
import paintool

import items.arrow
from items.arrow import ArrowItem
from items.circmoment import CircMomentItem
from items.squaremoment import SquareMomentItem
from items.text import TextItem
import math

def deg(x): return x / 180.0 * math.pi

class ShemeType(common.SchemeType):
	def __init__(self):
		super().__init__("Валы и трубки")
		self.setwidgets(ConfWidget(self), PaintWidget(), common.TableWidget())

class ConfWidget(common.ConfWidget):
	def __init__(self, scheme):
		super().__init__(scheme, noinitbuttons=True)
		self.has_central = False
		
		self.shemetype.texteditor = QTextEdit()
		self.shemetype.texteditor.textChanged.connect(self.redraw)

		self.sett = taskconf_menu.TaskConfMenu()
		self.shemetype.has_central = self.sett.add("Центральная секция:", "bool", False)
		self.shemetype.external_camera = self.sett.add("Внешняя камера:", "bool", True)
		self.shemetype.socr = self.sett.add("Сокращённая длина:", "bool", False)
		self.shemetype.ztube = self.sett.add("Полая труба:", "bool", True)
		self.shemetype.razrez = self.sett.add("Тип торца:", "list", 0, variant=["труба", "камера", "разрез"])
		self.sett.add_delimiter()
		self.shemetype.uncentered_force = self.sett.add("Сила:", "list", 0, variant=["нет", "+", "-"])
		self.shemetype.is_uncentered_force = self.sett.add("Внецентренная сила:", "bool", True)
		self.shemetype.is_uncentered_force_alternate = self.sett.add("сверху / снизу:", "bool", False)
		self.shemetype.text_force = self.sett.add("Текст силы:", "str", "P")
		self.sett.add_delimiter()
		self.shemetype.invert_moment = self.sett.add("Направление момента:", "list", 0, variant=["нет", "+", "-"])
		self.shemetype.text_moment = self.sett.add("Текст момента:", "str", "M")
		self.shemetype.torc_moment = self.sett.add("Моменты на торцах:", "bool", False)
		self.sett.add_delimiter()
		self.shemetype.invert_izgmoment = self.sett.add("Направление изг. момента:", "list", 0, variant=["нет", "+", "-"])
		self.shemetype.text_izgmoment = self.sett.add("Текст изг. момента:", "str", "M")
		self.shemetype.var_izgmoment = self.sett.add("Вариант изображения:", "list", 0, variant=["круговой", "угловой"])
		self.sett.add_delimiter()
		self.shemetype.text_pressure = self.sett.add("Метка давления внешн.:", "str", "p")
		self.shemetype.text_pressure_in = self.sett.add("Метка давления внутр.:", "str", "")
		self.shemetype.htext = self.sett.add("Текст толщины трубы", "str", "h")
		self.shemetype.Ltext = self.sett.add("Размер расчётной секции", "str", "")
		self.sett.add_delimiter()
		self.shemetype.camera_w = self.sett.add("Толщина камеры:", "int", "25")
		self.shemetype.tubewidth = self.sett.add("Толщина трубы:", "int", "10")
		self.shemetype.wborder = self.sett.add("Поля по горизонтали:", "float", "10")
		self.shemetype.hborder = self.sett.add("Поля по вертикали:", "float", "20")
				
		self.sett.updated.connect(self.redraw)
		
		self.update_interface()

	def redraw(self):
		if self.shemetype.has_central.get() and len(self.shemetype.task["sections"]) != 2:
			self.shemetype.task["sections"].append(self.sect())
			self.clean_and_update_interface()

		if not self.shemetype.has_central.get() and len(self.shemetype.task["sections"]) != 1:
			del self.shemetype.task["sections"][1]	
			self.clean_and_update_interface()
		
		super().redraw()

	def update_interface(self):
		self.table = tablewidget.TableWidget(self.shemetype, "sections")
		self.table.addColumn("D", "float")
		self.table.addColumn("Dtext", "str")
		self.table.updateTable()
		self.table.updated.connect(self.redraw)
		self.vlayout.addWidget(self.table)

		self.vlayout.addWidget(self.sett)
		self.vlayout.addWidget(self.shemetype.texteditor)
		self.setLayout(self.vlayout)

	class sect:
		def __init__(self, D=30, Dtext="d"):
			self.D = D
			self.Dtext = Dtext

	def create_task_structure(self):
		self.shemetype.task = {
			"sections": 
			[
				self.sect(40)
			],
		}

	def inittask(self):
		return {}

class PaintWidget(paintwdg.PaintWidget):
	def __init__(self):
		super().__init__()
		self.no_text_render = True
		self.no_resize = True

	def draw_tube(self, wmin, wmax, R, z=False, text="", camera=False, notext=False, nobody=False, tpos=None):
		S = self.shemetype.tubewidth.get()

		if tpos is None:
			tpos=(wmax+wmin)/2

		if not nobody:
			if not z:
				self.scene.addRect(QRectF(wmin, -R, -wmin+wmax, 2*R), pen=self.pen)
			else:
	
				if camera:
					zbrush = QBrush(Qt.BDiagPattern)
					self.scene.addRect(QRectF(wmin, -R, -wmin+wmax, 2*R), pen=self.pen, brush=zbrush)
					self.scene.addRect(QRectF(wmin+S, -R+S, -wmin+wmax-S*2, 2*R-S*2), pen=self.pen, brush=Qt.white)
					
	
				else:
					zbrush = QBrush(Qt.BDiagPattern)
					self.scene.addRect(QRectF(wmin, -R, -wmin+wmax, S), pen=self.pen, brush=zbrush)
					self.scene.addRect(QRectF(wmin, -R+S, -wmin+wmax, 2*R-S*2), pen=self.pen)
					self.scene.addRect(QRectF(wmin, R, -wmin+wmax, -S), pen=self.pen)
			
			if z:
				self.scene.addLine(QLineF(
					QPointF(wmin, -R+S/2),
					QPointF(wmax, -R+S/2)
				), pen = self.axpen)
	
				self.scene.addLine(QLineF(
					QPointF(wmin, R-S/2),
					QPointF(wmax, R-S/2)
				), pen = self.axpen)
	


				if text != "":
					self.scene.addItem(
						items.arrow.ArrowItem(
							QPointF(tpos, R-S/2), 
							QPointF(tpos, -R+S/2),
							arrow_size=(10,3),
							pen=self.pen,
							brush=Qt.black,
							double=True
					)
				)
			else:
				if text != "":
					self.scene.addItem(
						items.arrow.ArrowItem(
							QPointF(tpos, R), 
							QPointF(tpos, -R),
							arrow_size=(10,3),
							pen=self.pen,
							brush=Qt.black,
							double=True
						)
				)

		if not notext:
			if text != "":
				self.scene.addItem(TextItem(
					text=paintool.greek(text),
					font=self.font,
					center=QPointF(tpos-15, 0),
					pen=self.pen,
					rotate=deg(90),
					clean=True
				))

	def scene_bound(self):
		return (self.scene.itemsBoundingRect().width(),
			self.scene.itemsBoundingRect().height())

	def set_crest_circle(self, point, r, invert):
		self.scene.addEllipse(QRectF(
			QPointF(point-QPointF(r,r)),
			QPointF(point+QPointF(r,r))
		), pen=self.pen, brush=Qt.white)

		if invert:
			self.scene.addLine(QLineF(
				point-QPointF(r/math.sqrt(2),r/math.sqrt(2)),
				point+QPointF(r/math.sqrt(2),r/math.sqrt(2)),
			), pen=self.pen)

			self.scene.addLine(QLineF(
				point-QPointF(-r/math.sqrt(2),r/math.sqrt(2)),
				point+QPointF(-r/math.sqrt(2),r/math.sqrt(2)),
			), pen=self.pen)
		else:
			self.scene.addEllipse(
				QRectF(
					QPointF(point-QPointF(r/4,r/4)),
					QPointF(point+QPointF(r/4,r/4))
				), pen=self.pen, brush=Qt.black
			)

	def draw_camera(self, wmax, wmin, hmax, hmin, hint):
		zbrush = QBrush(Qt.BDiagPattern)
		zbrush2 = QBrush(Qt.FDiagPattern)
		self.scene.addPolygon(QPolygonF([
			QPointF(wmax,hmax),
			QPointF(-wmax,hmax),
			QPointF(-wmax,hint),
			QPointF(-wmin,hint),
			QPointF(-wmin,hmin),
			QPointF(wmin,hmin),
			QPointF(wmin,hint),
			QPointF(wmax,hint),
		]), brush=zbrush, pen=self.pen)		

		self.scene.addPolygon(QPolygonF([
			QPointF(wmax,-hmax),
			QPointF(-wmax,-hmax),
			QPointF(-wmax,-hint),
			QPointF(-wmin,-hint),
			QPointF(-wmin,-hmin),
			QPointF(wmin,-hmin),
			QPointF(wmin,-hint),
			QPointF(wmax,-hint),
		]), brush=zbrush, pen=self.pen)		

		w = wmax - wmin
		self.scene.addPolygon(QPolygonF([
			QPointF(-wmin-w/4,-hint),
			QPointF(-wmin-w/3,-hint-15),
			QPointF(-wmax+w/3,-hint-15),
			QPointF(-wmax+w/4,-hint),
		]), brush=zbrush2, pen=self.pen)		

		self.scene.addPolygon(QPolygonF([
			QPointF(wmin+w/4,-hint),
			QPointF(wmin+w/3,-hint-15),
			QPointF(wmax-w/3,-hint-15),
			QPointF(wmax-w/4,-hint),
		]), brush=zbrush2, pen=self.pen)		

		self.scene.addPolygon(QPolygonF([
			QPointF(wmin+w/4,hint),
			QPointF(wmin+w/3,hint+15),
			QPointF(wmax-w/3,hint+15),
			QPointF(wmax-w/4,hint),
		]), brush=zbrush2, pen=self.pen)		

		self.scene.addPolygon(QPolygonF([
			QPointF(-wmin-w/4,hint),
			QPointF(-wmin-w/3,hint+15),
			QPointF(-wmax+w/3,hint+15),
			QPointF(-wmax+w/4,hint),
		]), brush=zbrush2, pen=self.pen)		


	def paintEventImplementation(self, ev):
		self.scene = QGraphicsScene()
		self.painter.setRenderHints(QPainter.Antialiasing)

		camera_w = self.shemetype.camera_w.get()

		WIDTH=500

		if self.shemetype.socr.get():
			wpoint1 = -WIDTH*0.45
			wpoint2 = -WIDTH*0.1
			wpoint3 = WIDTH*0.1
			wpoint4 = WIDTH*0.45

		else:
			wpoint1 = -WIDTH*0.45
			wpoint2 = -WIDTH*0.2
			wpoint3 = WIDTH*0.2
			wpoint4 = WIDTH*0.45


		wpoint2c = -WIDTH*0.2
		wpoint3c = WIDTH*0.2

		if len(self.shemetype.task["sections"]) == 2:
			ymax =self.shemetype.task["sections"][0].D if self.shemetype.task["sections"][0].D > self.shemetype.task["sections"][1].D else self.shemetype.task["sections"][1].D
			ymin =self.shemetype.task["sections"][0].D if self.shemetype.task["sections"][0].D < self.shemetype.task["sections"][1].D else self.shemetype.task["sections"][1].D
		else:
			ymax = self.shemetype.task["sections"][0].D 
			ymin = self.shemetype.task["sections"][0].D 

		R = self.shemetype.task["sections"][0].D
		# Метка давления:
		#if self.shemetype.external_camera.get():
		self.scene.addItem(TextItem(
			text=self.shemetype.text_pressure.get(),
			font=self.font,
			center=QPointF(-(wpoint3+3*wpoint2)/4 +15, -ymax-18),
			pen=self.pen,
		))

		# Рисуем моменты:
		if self.shemetype.invert_moment.get() != "нет":
			pos = (3*wpoint1+wpoint2)/4
			if self.shemetype.torc_moment.get():
				pos = wpoint1

			minr = self.shemetype.task["sections"][0].D
			maxr = self.shemetype.task["sections"][0].D+30
			self.scene.addLine(QLineF(QPointF(pos, minr), QPointF(pos, maxr)))
			self.scene.addLine(QLineF(QPointF(pos, -minr), QPointF(pos, -maxr)))
			self.scene.addLine(QLineF(QPointF(-pos, minr), QPointF(-pos, maxr)))
			self.scene.addLine(QLineF(QPointF(-pos, -minr), QPointF(-pos, -maxr)))

			point_or_crest = self.shemetype.invert_moment.get() == "-"
			self.set_crest_circle(QPointF(pos, -maxr), r=10, invert = point_or_crest)
			self.set_crest_circle(QPointF(-pos, -maxr), r=10, invert = not point_or_crest)
			self.set_crest_circle(QPointF(pos, maxr), r=10, invert = not point_or_crest)
			self.set_crest_circle(QPointF(-pos, maxr), r=10, invert = point_or_crest)

			self.scene.addItem(TextItem(
				text=self.shemetype.text_moment.get(),
				font=self.font,
				center=QPointF(pos -15, -maxr),
				pen=self.pen,
				offset="left"
				))

			self.scene.addItem(TextItem(
				text=self.shemetype.text_moment.get(),
				font=self.font,
				center=QPointF(-pos +15, -maxr),
				pen=self.pen,
				offset="right"
				))

		# изгиб.
		if self.shemetype.invert_izgmoment.get()!="нет":
			if self.shemetype.var_izgmoment.get() == "круговой":
				self.scene.addItem(CircMomentItem(
					center=QPointF(wpoint1,0),
					angle=deg(180),
					rad = 50,
					pen = self.pen,
					brush=Qt.black,
					inverse=self.shemetype.invert_izgmoment.get()=="-"
				))
	
				self.scene.addItem(CircMomentItem(
					center=QPointF(wpoint4,0),
					angle=deg(0),
					rad = 50,
					pen = self.pen,
					brush=Qt.black,
					inverse=self.shemetype.invert_izgmoment.get()=="+"
				))
	
				self.scene.addItem(TextItem(
					text=self.shemetype.text_izgmoment.get(),
					font=self.font,
					center=QPointF(wpoint1 - 56, 0),
					pen=self.pen,
					offset="left"
					))
	
				self.scene.addItem(TextItem(
					text=self.shemetype.text_izgmoment.get(),
					font=self.font,
					center=QPointF(wpoint4 + 56, 0),
					pen=self.pen,
					offset="right"
					))
			else:
				x = 35
				y = self.shemetype.task["sections"][0].D + 15

				self.scene.addItem(SquareMomentItem(
					center=QPointF(wpoint1,0),
					x = x,
					y = y,
					pen = self.pen,
					brush=Qt.black,
					inverse=self.shemetype.invert_izgmoment.get()=="-"
				))
	
				self.scene.addItem(SquareMomentItem(
					center=QPointF(wpoint4,0),
					x = x,
					y = y,
					pen = self.pen,
					brush=Qt.black,
					inverse=self.shemetype.invert_izgmoment.get()=="+"
				))
	
				y = y - 15
				inv = self.shemetype.invert_izgmoment.get()=="+"  
				self.scene.addItem(TextItem(
					text=self.shemetype.text_izgmoment.get(),
					font=self.font,
					center=QPointF(wpoint1 - 20, y if inv else -y),
					pen=self.pen,
					offset="left"
					))
	
				self.scene.addItem(TextItem(
					text=self.shemetype.text_izgmoment.get(),
					font=self.font,
					center=QPointF(wpoint4 + 20, y if inv else -y),
					pen=self.pen,
					offset="right"
					))

		# Рисуем силы
		if self.shemetype.uncentered_force.get() != "нет":
			RR = R if self.shemetype.is_uncentered_force.get() else 0

			if RR == R:
				if self.shemetype.ztube.get() and len(self.sections()) == 1:
					RR = R - self.shemetype.tubewidth.get() / 2

			if self.shemetype.is_uncentered_force_alternate.get():
				RR = - RR

			inverse = self.shemetype.uncentered_force.get() == "-"
			self.scene.addItem(
				ArrowItem(
					QPointF(wpoint4+5, -RR),
					QPointF(wpoint4+50, -RR),
					arrow_size=(15,5), 
					pen=self.pen, 
					brush=Qt.black,
					reverse = inverse,
					double=False
				)
			)
			
			self.scene.addItem(
				ArrowItem(
					QPointF(wpoint1-5, -RR),
					QPointF(wpoint1-50, -RR),
					arrow_size=(15,5), 
					pen=self.pen, 
					brush=Qt.black,
					reverse = inverse,
					double=False
				)
			)

			self.scene.addItem(TextItem(
				text=self.shemetype.text_force.get(),
				font = self.font,
				center=(QPointF(wpoint1-5, -RR-13) + QPointF(wpoint1-50, -RR-13)) / 2,
				pen = self.pen
			))

			self.scene.addItem(TextItem(
				text=self.shemetype.text_force.get(),
				font = self.font,
				center=(QPointF(wpoint4+5, -RR-13) + QPointF(wpoint4+50, -RR-13)) / 2,
				pen = self.pen
			))

		# Рисуем трубы
		tpos = None
		if self.shemetype.socr.get():
			tpos = (wpoint3*3+wpoint4)/4
		else:
			tpos = (wpoint3*2+wpoint4*2)/4
			

		if self.shemetype.has_central.get():
			self.draw_tube(wpoint1, wpoint2, self.shemetype.task["sections"][0].D, False, text=self.shemetype.task["sections"][0].Dtext, notext=True, tpos=-tpos)
			self.draw_tube(wpoint2, wpoint3, self.shemetype.task["sections"][1].D, self.shemetype.ztube.get(), text=self.shemetype.task["sections"][1].Dtext, notext=True)
			self.draw_tube(wpoint3, wpoint4, self.shemetype.task["sections"][0].D, False, text=self.shemetype.task["sections"][0].Dtext, notext=True, tpos = tpos)
		else:
			self.draw_tube(wpoint1, wpoint4, self.shemetype.task["sections"][0].D, self.shemetype.ztube.get(), text=self.shemetype.task["sections"][0].Dtext, camera=self.shemetype.razrez.get()=="камера", notext=True)

		# Рисуем ось:
		self.scene.addLine(QLineF(QPointF(wpoint1-20, 0), QPointF(wpoint4+20, 0)), pen=self.axpen)

		# Внутренняя метка давления:
		self.scene.addItem(TextItem(
			text=self.shemetype.text_pressure_in.get(),
			font=self.font,
			center=QPointF(-(wpoint3+3*wpoint2)/4 +15, -ymin+25),
			pen=self.pen,
			clean = True
		))

		# Текст диаметров:
		if self.shemetype.has_central.get():
			self.draw_tube(wpoint1, wpoint2, self.shemetype.task["sections"][0].D, False, text=self.shemetype.task["sections"][0].Dtext, nobody=True, tpos=-tpos)
			self.draw_tube(wpoint2, wpoint3, self.shemetype.task["sections"][1].D, self.shemetype.ztube.get(), text=self.shemetype.task["sections"][1].Dtext, nobody=True)
			self.draw_tube(wpoint3, wpoint4, self.shemetype.task["sections"][0].D, False, text=self.shemetype.task["sections"][0].Dtext, nobody=True, tpos = tpos)
		else:
			self.draw_tube(wpoint1, wpoint4, self.shemetype.task["sections"][0].D, self.shemetype.ztube.get(), text=self.shemetype.task["sections"][0].Dtext, camera=self.shemetype.razrez.get()=="камера", nobody=True)

		# Рисуем камеру.
		if self.shemetype.external_camera.get():
			self.draw_camera(
				wmax=wpoint3c + 20+camera_w,
				wmin=wpoint3c + 20,
				hmax=ymax + 30+camera_w,
				hmin=ymax + 30,
				hint = self.shemetype.task["sections"][0].D)

		# Толщина трубы:
		T = self.shemetype.tubewidth.get()
		if len(self.shemetype.task["sections"]) == 2:
			item = 1
		else:
			item = 0
		
		H = self.shemetype.task["sections"][item].D
		if self.shemetype.ztube.get():
			self.scene.addItem(TextItem(
				text=self.shemetype.htext.get(),
				font = self.font,
				center=QPointF(45, H+15),
				pen = self.pen,
				offset="right"
			))


			self.scene.addItem(ArrowItem(
				QPointF(40,H + 15),
				QPointF(40,H),
				arrow_size=(10, 3),
				pen=self.pen,
				brush = Qt.black
			))

			self.scene.addItem(ArrowItem(
				QPointF(40,H-T-15),
				QPointF(40,H-T),
				arrow_size=(10, 3),
				pen=self.pen,
				brush = Qt.black
			))
			
			self.scene.addLine(QLineF(
				QPointF(40,H+15),
				QPointF(40,H-T-15)),
				pen=self.halfpen
			)

		# Рисуем разрезы на концах трубы
		if self.shemetype.razrez.get() == "разрез":
			line = [
				QPointF(wpoint1+5, R), 
				QPointF(wpoint1+0, R/2), 
				QPointF(wpoint1+10, -R/2), 
				QPointF(wpoint1+5, -R),
			]

			R = self.shemetype.task["sections"][0].D
			self.scene.addPolygon(QPolygonF(
				line+
			[
				QPointF(wpoint1-20, -R-10), QPointF(wpoint1-20, R+10)  
			]), pen=Qt.white, brush=Qt.white)

			for i in range(len(line) - 1):
				self.scene.addLine(QLineF(line[i], line[i+1]))


			line = [
				QPointF(wpoint4-5, R), 
				QPointF(wpoint4-10, R/2), 
				QPointF(wpoint4-0, -R/2), 
				QPointF(wpoint4-5, -R),
			]

			R = self.shemetype.task["sections"][0].D
			self.scene.addPolygon(QPolygonF(
				line+
			[
				QPointF(wpoint4+20, -R-10), QPointF(wpoint4+20, R+10)  
			]), pen=Qt.white, brush=Qt.white)

			for i in range(len(line) - 1):
				self.scene.addLine(QLineF(line[i], line[i+1]))


		#Размер расчётной секции:
		if self.shemetype.Ltext.get() != "":
			if self.shemetype.external_camera.get():
				self.scene.addLine(QLineF(
					QPointF(wpoint2, 0),
					QPointF(wpoint2, ymax + 30 + camera_w + 33),
				))
	
				self.scene.addLine(QLineF(
					QPointF(wpoint3, 0),
					QPointF(wpoint3, ymax + 30 + camera_w + 33),
				))
	
				self.scene.addItem(ArrowItem(
					QPointF(wpoint2, ymax + 30 + camera_w + 30),
					QPointF(wpoint3, ymax + 30 + camera_w + 30),
					double = True,
					pen = self.halfpen,
					brush = Qt.black,
					arrow_size=(10,3)
				))
			else:
				z = self.shemetype.tubewidth.get() if self.shemetype.razrez.get() == "камера" else 0

				self.scene.addLine(QLineF(
					QPointF(wpoint1 + z, 0),
					QPointF(wpoint1 + z, ymax + 63),
				))
	
				self.scene.addLine(QLineF(
					QPointF(wpoint4 - z, 0),
					QPointF(wpoint4 - z, ymax + 63),
				))
	
				self.scene.addItem(ArrowItem(
					QPointF(wpoint1 + z, ymax + 60),
					QPointF(wpoint4 - z, ymax + 60),
					double = True,
					pen = self.halfpen,
					brush = Qt.black,
					arrow_size=(10,3)
				))

			self.scene.addItem(TextItem(
				text=self.shemetype.Ltext.get(),
				font=self.font,
				center = QPointF(0, ymax + 30 + camera_w + 20),
				pen=self.pen
			))

		br = QColor(0,0,0)
		br.setAlphaF(0)
		p = QPen()
		p.setColor(br)
		rect = self.scene.itemsBoundingRect()

		rect = self.scene.itemsBoundingRect()
		addtext = paintool.greek(self.shemetype.texteditor.toPlainText())
		n = len(addtext.splitlines())
		for i, l in enumerate(addtext.splitlines()):
			t = self.scene.addText(l, self.font)
			t.setPos(
				rect.x(), 
				rect.height() + rect.y() + QFontMetrics(self.font).height()*i
			)

		WBORDER = self.shemetype.wborder.get()
		HBORDER = self.shemetype.hborder.get()

		if self.shemetype.uncentered_force.get() != "нет":
			WBORDER += 25

		self.scene.addRect(QRectF(-rect.width()/2-WBORDER, -rect.height()/2-HBORDER, rect.width()+WBORDER*2, rect.height()+HBORDER), pen = p, brush=br)

		self.scene.render(self.painter, 
			target=QRectF(0,0, 
				self.scene.itemsBoundingRect().width(), 
				self.scene.itemsBoundingRect().height()), 
			source=self.scene.itemsBoundingRect())

		self.resize_after_render(*self.scene_bound())