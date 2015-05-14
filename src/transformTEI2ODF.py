"""
Script to apply an XSLT transformation to TEI files
The script was written to as part of a research project at TCD
"""
from lxml import etree
import zipfile, datetime
import os, re, types
from StringIO import StringIO
from ezodf import newdoc, Paragraph, Heading, Sheet, text

file_path = "C:" + os.sep + "Users" + os.sep + "Rombli" + os.sep + "Dropbox" + os.sep + "XML" + os.sep + "Transcriptions" + os.sep + "Masterfiles"



xml_dirs = [
    "london_british_library_ms_cotton_nero_E1",
    "paris_BnF_ms_lat17626"


    ]

current_ms = 1

xslt_file = "tei2odf-Freeman.xsl"


xml_file = file_path + os.sep + xml_dirs[current_ms] + os.sep + xml_dirs[current_ms] + ".xml"


result_file = xml_dirs[current_ms] + ".odt"

picture_dir = file_path + os.sep + xml_dirs[current_ms]


def open_file(fl=xml_file):
    #do not encode in unicode when opening, e.g. with codecs module
    with open(fl, "r") as f:
        try:
            xml = StringIO(f.read())
            parser = etree.XMLParser(encoding="utf-8", resolve_entities=False)
            tree = etree.parse(xml, parser=parser)
            
        except etree.XMLSyntaxError as e:
            print e

    #xml = StringIO("<surface><l><w n='1'>exam<ex>ABBR</ex>ple</w><w n='2'>Word2</w></l></surface>")
    #tree = etree.parse(xml, parser=parser)
    return tree
       
def print_info(archive_name):
    zf = zipfile.ZipFile(archive_name)
    for info in zf.infolist():
        print info.filename
        print '\tComment:\t', info.comment
        print '\tModified:\t', datetime.datetime(*info.date_time)
        print '\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)'
        print '\tZIP version:\t', info.create_version
        print '\tCompressed:\t', info.compress_size, 'bytes'
        print '\tUncompressed:\t', info.file_size, 'bytes'
        print




if __name__ == "__main__":
    
    xslt_tree = open_file(xslt_file)
    
    transform = etree.XSLT(xslt_tree)

    #transform the TEI transcriptions with XSLT to odt XML format
    doc = open_file(xml_file)
    result_tree = transform(doc)

    #create new odt file
    odt = newdoc(doctype='odt', filename=result_file)
    #add styles to the odt file
    styles = result_tree.xpath("//style:style", namespaces={"style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0"})
    for s in styles:
        odt.inject_style(etree.tostring(s, pretty_print = True))

    #add the body/text to the odd file
    text = result_tree.xpath("//office:text/*", namespaces={"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0"})
    
    for idx, t in enumerate(text):
        odt.body.xmlnode.insert(idx,t)

    odt.save()

    
    #add images to the odt file
    z = zipfile.ZipFile(result_file, mode="a")
    print help(z)
    for root, dirs, files in os.walk(picture_dir):
        for file in files:
            z.write(os.path.join(root, file), os.path.join("Pictures", file) ,compress_type=zipfile.ZIP_DEFLATED)

    z.close()

    #print a report of the content of the odt file
    #print_info(result_file)
    
    print "Done!"
    print "File " + result_file
