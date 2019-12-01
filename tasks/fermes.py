import common
import paintwdg
import math

import tablewidget
import util
import paintool
import taskconf_menu

from paintool import deg

import sections
import elements

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ShemeTypeT4(common.SchemeType):
	def __init__(self):
		super().__init__("Рамы")
		self.setwidgets(ConfWidget_T4(self), PaintWidget_T4(), common.TableWidget())

class ConfWidget_T4(common.ConfWidget):
	class sect:
		def __init__(self, direct=1, strt=("",""), fini=(1,1), lsharn="нет", rsharn="нет", txt="", alttxt=False):
			self.xstrt=str(strt[0])
			self.ystrt=str(strt[1])
			self.xfini=str(fini[0])
			self.yfini=str(fini[1])
			self.lsharn = lsharn
			self.rsharn = rsharn
			self.txt = txt
			self.alttxt = alttxt

	class label:
		def __init__(self, smaker="", fmaker="", smaker_pos="сверху", fmaker_pos="сверху"):
			self.smaker = smaker
			self.fmaker = fmaker
			self.smaker_pos = smaker_pos
			self.fmaker_pos = fmaker_pos


	class sectforce:
		def __init__(self, distrib="clean", txt=""):
			self.distrib = distrib
			self.txt = txt

	class betsect:
		def __init__(self, 
					fenl="нет", fenr="нет", 
					menl="нет", menr="нет",
					fl_txt="", fr_txt="", ml_txt="", mr_txt="",
					fl_txt_alt=False, fr_txt_alt=False):
			self.fenl = fenl
			self.fenr = fenr
			self.menl = menl
			self.menr = menr
			self.fl_txt, self.fr_txt = fl_txt, fr_txt
			self.ml_txt, self.mr_txt = ml_txt, mr_txt
			self.fl_txt_alt, self.fr_txt_alt = fl_txt_alt, fr_txt_alt
			
	def create_task_structure(self):
		self.shemetype.task = {
			"sections": 
			[
				self.sect(strt=(0,0), fini=(1,1), lsharn="слева шарн2"),
				self.sect(strt=("",""), fini=(2,1)),
				self.sect(strt=("",""), fini=(3,0))
			],

			"sectforce": 
			[
				self.sectforce(distrib="clean"),
				self.sectforce(distrib="clean"),
				self.sectforce(distrib="-"),
			],

			"betsect": 
			[
				self.betsect(menr="слева +"),
				self.betsect(),
				self.betsect()
			],

			"label": 
			[
				self.label(),
				self.label(),
				self.label()
			],
		}

	def __init__(self, sheme):
		super().__init__(sheme)

		self.sett = taskconf_menu.TaskConfMenu()
		self.shemetype.base_length = self.sett.add("Базовая длина:", "int", "100")
		#self.shemetype.base_d = self.sett.add("Базовая длина:", "int", "40")
		#self.shemetype.base_h = self.sett.add("Базовая толщина:", "int", "20")
		#self.shemetype.zadelka = self.sett.add("Заделка:", "bool", True)
		#self.shemetype.axis = self.sett.add("Центральная ось:", "bool", True)
		#self.shemetype.zadelka_len = self.sett.add("Длина заделки:", "float", "30")
		#self.shemetype.dimlines_start_step = self.sett.add("Отступ размерных линий:", "float", "20")
		#self.shemetype.dimlines_step = self.sett.add("Шаг размерных линий:", "float", "40")
		#self.shemetype.base_height = self.sett.add("Базовая высота стержня:", "int", "10")
		self.sett.updated.connect(self.redraw)

		self.shemetype.font_size = common.CONFVIEW.font_size_getter
		self.shemetype.line_width = common.CONFVIEW.lwidth_getter

		men_arr= elements.men_arr
		fen_arr= elements.fen_arr
		sharnir_arr = elements.sharn_arr

		self.table = tablewidget.TableWidget(self.shemetype, "sections")
		self.table.addColumn("xstrt", "str", "X0")
		self.table.addColumn("ystrt", "str", "Y0")
		self.table.addColumn("xfini", "str", "X1")
		self.table.addColumn("yfini", "str", "Y1")
		self.table.addColumn("lsharn", "list", "ШарнирЛ", variant=sharnir_arr)
		self.table.addColumn("rsharn", "list", "ШарнирП", variant=sharnir_arr)
		self.table.addColumn("txt", "str", "Текст")
		self.table.addColumn("alttxt", "bool", "alt")
		self.table.updateTable()

		self.table1 = tablewidget.TableWidget(self.shemetype, "sectforce")
		self.table1.addColumn("distrib", "list", "Распр.", variant=["clean", "+", "-"])
		self.table1.addColumn("txt", "str", "Распр.")
		self.table1.updateTable()


		self.table2 = tablewidget.TableWidget(self.shemetype, "betsect")
		self.table2.addColumn("fenl", "list", "F", variant=fen_arr)
		self.table2.addColumn("fl_txt", "str", "F")
		self.table2.addColumn("fenr", "list", "F", variant=fen_arr)
		self.table2.addColumn("fr_txt", "str", "F")
		self.table2.addColumn("menl", "list", "M", variant=men_arr)
		self.table2.addColumn("ml_txt", "str", "M")
		self.table2.addColumn("menr", "list", "M", variant=men_arr)
		self.table2.addColumn("mr_txt", "str", "M")
		self.table2.addColumn("fr_txt_alt", "bool", "Falt")
		self.table2.addColumn("fr_txt_alt", "bool", "Falt")
		self.table2.updateTable()

		self.table3 = tablewidget.TableWidget(self.shemetype, "label")
		self.table3.addColumn("smaker", "str", "Метка")
		self.table3.addColumn("fmaker", "str", "Метка")
		self.table3.addColumn("smaker_pos", "list", "Метка", variant=elements.storoni)
		self.table3.addColumn("fmaker_pos", "list", "Метка", variant=elements.storoni)
		self.table3.updateTable()

		self.vlayout.addWidget(QLabel("Геометрия:"))
		self.vlayout.addWidget(self.table)
		
		self.vlayout.addWidget(QLabel("Распределённые силы:"))
		self.vlayout.addWidget(self.table1)
		
		self.vlayout.addWidget(QLabel("Локальные силы:"))
		self.vlayout.addWidget(self.table2)

		self.vlayout.addWidget(QLabel("Метки:"))
		self.vlayout.addWidget(self.table3)
		
		self.vlayout.addWidget(self.sett)

		self.table.updated.connect(self.redraw)
		self.table1.updated.connect(self.redraw)
		self.table2.updated.connect(self.redraw)
		self.table3.updated.connect(self.redraw)

		self.shemetype.arrow_size = self.sett.add("Размер стрелки:", "int", "12")

		self.shemetype.section_enable = self.sett.add("Отображение сечения:", "bool", False)
		self.shemetype.section_type = self.sett.add("Тип сечения:", "list", 
			defval=4,
			variant=sections.section_variant)

		self.shemetype.section_txt0 = self.sett.add("Сечение.Текст1:", "str", "D")
		self.shemetype.section_txt1 = self.sett.add("Сечение.Текст2:", "str", "d")
		self.shemetype.section_txt2 = self.sett.add("Сечение.Текст3:", "str", "d")

		self.shemetype.section_arg0 = self.sett.add("Сечение.Аргумент1:", "int", "60")
		self.shemetype.section_arg1 = self.sett.add("Сечение.Аргумент2:", "int", "50")
		self.shemetype.section_arg2 = self.sett.add("Сечение.Аргумент3:", "int", "10")

		self.shemetype.postfix = self.sett.add("Постфикс:", "str", ",EIx")

		self.shemetype.texteditor = QTextEdit()
		self.shemetype.texteditor.textChanged.connect(self.redraw)
		self.vlayout.addWidget(self.shemetype.texteditor)
		
		self.setLayout(self.vlayout)

	def add_action(self):
		self.shemetype.task["sections"].append(self.sect())
		self.shemetype.task["betsect"].append(self.betsect())
		self.shemetype.task["sectforce"].append(self.sectforce())
		self.redraw()
		self.updateTables()

	def del_action(self):
		if len(self.shemetype.task["sections"]) == 1: return
		del self.shemetype.task["sections"][-1]
		del self.shemetype.task["betsect"][-1]
		del self.shemetype.task["sectforce"][-1]
		self.redraw()
		self.updateTables()

	def inittask(self):
		#compat
		return {}

	def updateTables(self):
		self.table.updateTable()
		self.table1.updateTable()
		self.table2.updateTable()
		self.table3.updateTable()

class PaintWidget_T4(paintwdg.PaintWidget):

	def __init__(self):
		super().__init__()

	def paintEventImplementation(self, ev):
		assert len(self.sections()) == len(self.bsections())

		width = self.width()
		height = self.height()

		center = QPoint(width/2, self.hcenter)

		font_size = self.shemetype.font_size.get()
		lwidth = self.shemetype.line_width.get()

		fini_width = width
		hpostfix = 0

		base_length = self.shemetype.base_length.get()
		distrib_step = 10
		distrib_alen = 20
		#base_h = self.shemetype.base_h.get()
		#zadelka = self.shemetype.zadelka.get()
		#axis = self.shemetype.axis.get()
		#zadelka_len = self.shemetype.zadelka_len.get()
		#dimlines_step = self.shemetype.dimlines_step.get()
		#dimlines_start_step = self.shemetype.dimlines_start_step.get()
		arrow_size = self.shemetype.arrow_size.get()

		painter = self.painter
		painter.setPen(self.pen)
		painter.setBrush(Qt.white)
		section_width = self.draw_section(hcenter=(self.height() - hpostfix) / 2) - 10
		#section_width= 0

		painter.setPen(self.pen)
		painter.setBrush(Qt.white)


		# Расчитываем смещения
		coordes = []
		raw_coordes = []
		xmin=0
		ymin=0
		xmax=0
		ymax=0

		last = None
		for s in self.sections():
			xstrt = float(s.xstrt) if s.xstrt != "" else float(last.xfini)
			ystrt = float(s.ystrt) if s.ystrt != "" else float(last.yfini)
			xfini = float(s.xfini)
			yfini = float(s.yfini)

			xmin = min(xmin, xstrt, xfini)
			xmax = max(xmax, xstrt, xfini)
			ymin = min(ymin, ystrt, yfini)
			ymax = max(ymin, ystrt, yfini)

			last = s

		xshift = - (xmin + xmax) / 2 * base_length - section_width /2
		yshift = (ymin + ymax) / 2 * base_length
		
		last = None
		for s in self.sections():
			xstrt = float(s.xstrt) if s.xstrt != "" else float(last.xfini)
			ystrt = float(s.ystrt) if s.ystrt != "" else float(last.yfini)
			xfini = float(s.xfini)
			yfini = float(s.yfini)

			raw_coordes.append(((xstrt,ystrt), (xfini,yfini)))

			coordes.append((
				QPoint(
					xstrt * base_length + center.x() + xshift, 
					- ystrt * base_length + center.y() + yshift), 
				QPoint(
					xfini * base_length + center.x() + xshift, 
					- yfini * base_length + center.y() + yshift)))

			last = s

		
		# Начинаем рисовать
		for i in range(len(self.sections())):
			strt, fini = coordes[i]
			rstrt, rfini = raw_coordes[i]
			painter.setPen(self.doublepen)
			painter.drawLine(strt, fini)
			sect = self.sections()[i]

			txt = self.sections()[i].txt
			alttxt = self.sections()[i].alttxt

			if txt == "":
				dist = math.sqrt((rfini[0] - rstrt[0])**2 + (rfini[1] - rstrt[1])**2) 
				txt = util.text_prepare_ltext(dist) + self.shemetype.postfix.get()

			elements.draw_text_by_points(self, strt, fini, txt, alttxt)

			elements.draw_element_label(self, pnt=strt, txt=self.shemetype.task["label"][i].smaker, type=self.shemetype.task["label"][i].smaker_pos)
			elements.draw_element_label(self, pnt=fini, txt=self.shemetype.task["label"][i].fmaker, type=self.shemetype.task["label"][i].fmaker_pos)
		
		# Распределённая нагрузка
		for i in range(len(self.sections())):
			strt, fini = coordes[i]
			sect = self.sections()[i]
			bsect = self.sectforce()[i]
			angle = common.angle(strt, fini) 

			elements.draw_element_distribload(self, bsect.distrib, 
				strt, fini, distrib_step, 
				arrow_size/3*2, 20, txt=bsect.txt)

			
		# Шарниры и заделки
		for i in range(len(self.sections())):
			strt, fini = coordes[i]
			sect = self.sections()[i]
			bsect = self.sectforce()[i]
			angle = common.angle(strt, fini) 



			if sect.lsharn != "clean":
				termrad = 15 if not "шарн1" in sect.lsharn else 25
				elements.draw_element_sharn(self, strt, sect.lsharn, inangle=angle+deg(180), termrad=termrad)

			if sect.rsharn != "clean":
				termrad = 15 if not "шарн1" in sect.lsharn else 25
				elements.draw_element_sharn(self, fini, sect.rsharn, inangle=angle, termrad=termrad)


		# Силы и моменты
		for i in range(len(self.sections())):
			rad = 40
			strt, fini = coordes[i]
			sect = self.sections()[i]
			sectforce = self.sectforce()[i]
			bsect = self.bsections()[i]
			angle = common.angle(strt, fini) 

			painter.setPen(self.pen)

			elements.draw_element_torque(self, strt, bsect.menl, rad, arrow_size, txt=bsect.ml_txt)
			elements.draw_element_torque(self, fini, bsect.menr, rad, arrow_size, txt=bsect.mr_txt)
			elements.draw_element_force(self, strt, bsect.fenl, rad, arrow_size, txt=bsect.fl_txt, alt=bsect.fl_txt_alt)
			elements.draw_element_force(self, fini, bsect.fenr, rad, arrow_size, txt=bsect.fr_txt, alt=bsect.fr_txt_alt)
				
	def draw_section(self, hcenter):
		if self.shemetype.section_enable.get():
			section_width = sections.draw_section(
				wdg = self,
				section_type = self.shemetype.section_type.get(),
				arg0 = int(self.shemetype.section_arg0.get()),
				arg1 = int(self.shemetype.section_arg1.get()),
				arg2 = int(self.shemetype.section_arg2.get()),
	
				txt0 = paintool.greek(self.shemetype.section_txt0.get()),
				txt1 = paintool.greek(self.shemetype.section_txt1.get()),
				txt2 = paintool.greek(self.shemetype.section_txt2.get()),
				arrow_size = self.shemetype.arrow_size.get(),
				right = self.width() - 10,
				hcenter=hcenter
			)

			return section_width
		return 0
