#!/usr/bin/python

import xlwt

Class write:
	def __init__(self);
		self.heading =  xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
		self.small_heading = xlwt.easyxf('font: name Times New Roman, color-index blue, bold on')
		self.wb =  xlwt.Workbook()
		self.ws = self.wb.add_sheet('Live POP report')

	def write_to_cell(column, row, text, type=""):
		if type == "HEAD":
			type = self.heading
		elif type = "SUB":
			type = self.small_heading
		if type:		
			ws.write(row, column, text, type)
		else:
			ws.write(row, column, text)

	

