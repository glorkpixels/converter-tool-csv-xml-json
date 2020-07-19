
import csv
import lxml.etree as etree
import lxml.builder as bt
import copy 
unis = []
from lxml import etree
import json
from lxml import etree
from io import StringIO
import pandas as pd

class University:
   
    def __init__(self,unikind,uniname):
        self.unikind = unikind
        self.uniname = uniname
        self.UniversityMajor = []
        
    def addxd(self,Major):
        self.UniversityMajor.append(Major)
        
class UniversityMajor:
    def __init__( self,faculty,majorcode, major, language, typeofeducation, scholarship, programlength, scoretype, quota , fosquota, minplacelastyear ,minscorelastyear ):
        self.faculty = faculty
        self.majorcode = majorcode
        self.major = major
        self.language = language
        self.typeofeducation = typeofeducation
        self.scholarship = scholarship
        self.programlength = programlength
        self.scoretype = scoretype
        self.quota = quota
        self.fosquota = fosquota
        self.minplacelastyear = minplacelastyear
        self.minscorelastyear = minscorelastyear
        
        

        
def csvread():
    with open('DEPARTMENTS.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file ,delimiter="\t")
        next(reader)
        for i, line in enumerate(reader):
           #print(i, line)
            Type = line[0].split(";")
            major =UniversityMajor(Type[2],Type[3], Type[4] ,  Type[5],  Type[6], Type[7], Type[8], Type[9] , Type[10],  Type[11], Type[12], Type[13])
            uni = University( Type[0] , Type[1])
            uni.UniversityMajor.append(major)
            
            unis.append(uni)
            attrs = vars(uni)
            attrts = vars(uni.UniversityMajor[0])

        
def csvduplicationclearing():
    for i in range(lens):
        if unis[i] != None:
            temp = unis[i].uniname
            for x in range(lens):
                if unis[x] != None:
                    temp2 = unis[x].uniname
                    if temp == temp2:
                    #temphold=unis[x].UniversityMajor[0]
                        if x!=i:
                            if unis[i] != None:
                                temphold = copy.deepcopy(unis[x].UniversityMajor[0])
                                unis[i].addxd(temphold)
                                unis[x] = None

                        
                
                
                                
csvread()

lens = len(unis)

csvduplicationclearing()   

unis = list(filter(None, unis)) 

#for x in range(len(unis)): 
 #   print(unis[x].unikind)
  #  print(unis[x].uniname)
   # print(unis[x].faculty)
    #print(len(unis[x].UniversityMajor))
    #for a in range(len(unis[x].UniversityMajor)):
     #   print (vars(unis[x].UniversityMajor[a]))   

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def xmlcon():
    root = etree.Element('DEPARTMENTS')
    for x in range(len(unis)): 
        uniname = unis[x].uniname
        utype = unis[x].unikind
        sub=etree.SubElement(root, 'University', name = uniname, utype= utype)
        for a in range(len(unis[x].UniversityMajor)):
            majc = unis[x].UniversityMajor[a].majorcode
            maj = unis[x].UniversityMajor[a].major
            fac = unis[x].UniversityMajor[a].faculty
            lan = unis[x].UniversityMajor[a].language
            ted = unis[x].UniversityMajor[a].typeofeducation
            sch = unis[x].UniversityMajor[a].scholarship
            pln = unis[x].UniversityMajor[a].programlength
            scr = unis[x].UniversityMajor[a].scoretype
            qt = unis[x].UniversityMajor[a].quota
            fqt = unis[x].UniversityMajor[a].fosquota
            mpl= unis[x].UniversityMajor[a].minplacelastyear
            msl = unis[x].UniversityMajor[a].minscorelastyear
            if not sch:
                sch="0"
            if not lan:
                lan="Türkçe"
            
            sub2=etree.SubElement(sub, 'item', id = majc, faculty= fac)
            sub2.text = maj
            chil1= etree.SubElement(sub2, 'name', lan = lan, second= ted)
            chil2=etree.SubElement(sub2, 'scholarship').text=sch
            chil3=etree.SubElement(sub2, 'period').text=pln
            chil4=etree.SubElement(sub2, 'quota', spec = fqt).text=qt
            chil5=etree.SubElement(sub2, 'field').text=scr
            chil6=etree.SubElement(sub2, 'last_min_score').text=msl
            chil7=etree.SubElement(sub2, 'last_min_place').text=mpl
           


    # prettystring
    #print(etree.tostring(root ,pretty_print=True,encoding='unicode'))
    tree = etree.ElementTree(root)

    indent(root)
    # writing xml
    tree.write("example.xml", encoding="utf-8", xml_declaration=True)


xmlcon()

def xsdvalid():
    doc = etree.parse('example.xml')
    root = doc.getroot()
    #print(etree.tostring(root))
    xmlschema_doc = etree.parse('valid.xsd')
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(etree.tostring(root))
    validation_result = xmlschema.validate(doc)
    print(validation_result)
    xmlschema.assert_(doc)


def csvtojson():

    data = {}
    data["of"] ={}
    for x in range(len(unis)): 
        items = {}
        uniname = unis[x].uniname
        data["of"][uniname] = {}
        utype = unis[x].unikind
        data["of"][uniname]['unikind'] = utype
        data["of"][uniname]['items'] = {}
        fac = unis[x].UniversityMajor[0].faculty

        items["faculty"] = fac
        items["department"] = []



        for a in range(len(unis[x].UniversityMajor)):

            majc = unis[x].UniversityMajor[a].majorcode
            maj = unis[x].UniversityMajor[a].major
            fac = unis[x].UniversityMajor[a].faculty
            lan = unis[x].UniversityMajor[a].language
            ted = unis[x].UniversityMajor[a].typeofeducation
            sch = unis[x].UniversityMajor[a].scholarship
            pln = unis[x].UniversityMajor[a].programlength
            scr = unis[x].UniversityMajor[a].scoretype
            qt = unis[x].UniversityMajor[a].quota
            fqt = unis[x].UniversityMajor[a].fosquota
            mpl= unis[x].UniversityMajor[a].minplacelastyear
            msl = unis[x].UniversityMajor[a].minscorelastyear


            items["department"].append({
            'majorcode': majc,
            'major': maj,
            'language': lan,
            'typeofeducation': ted,
            'scholarship': sch,
            'programlength': pln,
            'scoretype': scr,
            'quota': qt,
            'School first N quota': fqt,
            'minplacelastyear': mpl,
            'minscorelastyear': msl,

            })
            data["of"][uniname]['items'] = items


    with open('data.json', 'w',encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False,indent=4,)



def csonread():
    with open('data.json',encoding="utf-8") as f:
        data = json.load(f)
    #print(data)

bad_chars = ['{', "'", '}', "*"] 
emelents = []

emelents.append("üNİVERSİTE_TÜRÜÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN")

def xmlread():
    # parses an XML section into an element tree.
    tree = etree.parse('example.xml')
    # returns the root element for this tree.
    root = tree.getroot()

    for i in range(len(root)):
        for elem in root:
            of = str(root[i].attrib)
            emelents.append(of+",")
            for subelem in elem:
                emelents.append(subelem.text+",")
                for xd in subelem:
                     if xd is not None:
                            e = str(xd.text)
                            emelents.append(e+",")
                     
                     else:
                        xd=""
                        emelents.append(xd+",")
    emelents.append("/newline")      
        
    

def xmltocsv():
   
    with open('csvfromxml.csv', "w",encoding="utf-8") as outfile:
        for entries in emelents:
            outfile.write(entries)
            
    
def jsontocsv():
    xd ="üNİVERSİTE_TÜRÜÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN"
    
    with open('data.json',encoding="utf-8") as json_file: 
        data = json.load(json_file) 
    
    uni = data['of']
    
    data_file = open('data_file.csv', 'w',encoding="utf-8") 
  
    # create the csv writer object 
    csv_writer = csv.writer(data_file) 
  
    # Counter variable used for writing  
    # headers to the CSV file 
      
  
    with open('csvfromxjson.csv', "w",encoding="utf-8") as outfile:
        outfile.write(xd)
        for entries in uni:
            outfile.write(str(entries))
            assx= uni[entries] 
            outfile.write(str(assx))
            ass= uni[entries]["items"]["department"]
            outfile.write(str(ass))
      
    data_file.close() 

    
def jsontoxml():
    pass

def xmltojson():
    pass


xmlread()
csonread()
csvtojson()
xmltocsv()
jsontocsv()
xsdvalid()