import datetime
import urllib2
import xlrd
import random
from xlrd import open_workbook

from parse_rest.connection import register
register("To6ZjPMq8BUtsCyUDGHSG8BtwVfSpNJ3XjpxdMOh", "g90vPDRIVQZp1Pc8VlaC8ekEH3rTDvY4vXHuFbGF", master_key = "PD2mJf48vAaItVo5NdCWYeuCArAPgOsoOHWY4s6V")

from parse_rest.datatypes import Object
from parse_rest.connection import ParseBatcher

class Crop(Object):
    pass

category = "ROOT CROPS"
categories = ["root crops","condiments and spices","leafy vegetables","vegetables", "fruits","citrus"]

def retrieveMonthly(base_url,  month, year):
	filename = "monthly "+"-"+str(month)+"-"+str(year)+".xls"
	months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

	if (str(month).isdigit()):
		mStr = months[month - 1]
	else:
		mStr = month
		month = months.index(month) + 1

	url = "http://www.namistt.com/DocumentLibrary/Market%20Reports/Monthly/"+str(mStr)+"%20"+str(year)+"%20NWM%20Monthly%20Report.xls"

	print "time: "+str(month)+"-"+str(year)

	# mInt = months.index(month) + 1
	result = traverseWorkbook(url, {}, "monthly")
	if result:
		for x in result:
			if x:
				x.update({"date": datetime.datetime(int(year), int(month), 1)})
		return result
	else:
		return

def processRow(sheet, row, type):
	global category
	global categories

	dic = {}

	#ensure that the row is not empty
	if sheet.cell_type(row, 0) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
		return None
	else:
		#Check if the second column is empty then usually for the category listing
		if not sheet.cell(row, 1).value:
			val = sheet.cell(row, 0).value
			#Check if in the valid list of categories
			if val.lower() in categories:
				category = val.upper()
		else:
			return processMonthly(sheet, row, category)

def processMonthly(sheet, row, category):
	dic = {}
	dic['commodity'] = sheet.cell_value(row, 0).encode('ascii').lower()
	dic['category'] = category.encode('ascii')
	dic['unit'] = str(sheet.cell_value(row, 1)).encode('ascii')

	if sheet.cell(row, 2) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
		dic['min'] = 0.0
	else:
		dic['min'] = sheet.cell_value(row, 2)

	if sheet.cell(row, 3) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
		dic['max'] = 0.0
	else:
		dic['max'] = sheet.cell_value(row, 3)

	if sheet.cell(row, 4) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
		dic['mode'] = 0.0
	else:
		dic['mode'] = sheet.cell_value(row, 4)

	if sheet.cell(row, 5) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
		dic['mean'] = 0.0
	else:
		dic['mean'] = sheet.cell_value(row, 5)

	if sheet.cell(row, 6) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
		dic['volume'] = 0.0
	else:
		dic['volume'] = sheet.cell_value(row, 6)

	return dic

def traverseWorkbook(url, params = {}, workbook_type = "daily"):
	values = []
	try:
		# print "Trying to read ", url
		data = urllib2.urlopen(url).read()
		wb = open_workbook(url, file_contents=data)
		for s in wb.sheets():
			for row in range(s.nrows):
				if (workbook_type == "daily" and row > 10) or (workbook_type == "monthly" and row > 15) :
					rowData = processRow(s, row, workbook_type)
					if rowData:
						values.append(rowData)
		return values;
	except Exception, e:
		# print "Error in reading workbook at ", url, e
		print "Error traversing workbook", e
		return None

def storeMonthlyPrices():
    all_scores = Crop.Query.all()
    data = retrieveMonthly("", 12, 2014)
	#length = 0
    crops = []
    #batches = []
    #batches.append(batcher)
    if data and len(data) > 0:
        for x in range(0, 49):
            crop = Crop(name=data[x]['commodity'], price=data[x]['mean'], size=random.randint(1, 5))
            crops.append(crop)
    batcher = ParseBatcher()
    batcher.batch_save(crops)

    #if data and len(data) > 49:
    #    for x in range(49, len(data)):
    #        crop = Crop(name=data[x]['commodity'], price=data[x]['mean'], size=random.randint(1, 5))
    #        crops.append(crop)

    #batcher2 = ParseBatcher()
    #batcher2.batch_save(crops)
    	#db.drop_collection("dailyRecent")
		#recent_daily = db.dailyRecent
		#recent_daily.insert(dData)
		#length = recent_daily.count()
	#return length

storeMonthlyPrices()