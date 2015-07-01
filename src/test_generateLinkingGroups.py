'''
Created on 1 Jul 2015

@author: Rombli
'''
import unittest
import os
import generateLinkingGroups as glg
from lxml import etree

xml_1 = """<?xml version="1.0" encoding="UTF-8" ?>
            <tei>
                <header><title>this is the title</title></header>
                <text><lb id="1"/><p id="1-1">par 1</p><lb id="2"/><p id="1-2">par 2</p><lb id="3"/><p id="1-3">par 3</p></text>
            </tei>
            """
            
xml_2 = """<?xml version="1.0" encoding="UTF-8" ?>
            <tei>
                <header><title>this is the title</title></header>
                <text><lb id="1"/><p id="2-1">par 1</p><lb id="2"/><p id="2-2">par 2</p><lb id="3"/><p id="2-3">par3</p></text>
            </tei>
            """
            
xslt_1 = """<?xml version="1.0" encoding="UTF-8"?>
            <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
            <xsl:template match="@*|node()">
                <xsl:copy>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:copy>
            </xsl:template>
            
            <xsl:template match="header">
            </xsl:template>
            
            </xsl:stylesheet>
        """

level_of_comparison = "//p"            
            
cur_dir = os.getcwd()

xml_file_1 = cur_dir + os.sep + "xml_test_1.xml"

xml_file_2 = cur_dir + os.sep + "xml_test_2.xml"

class Test(unittest.TestCase):


    def setUp(self):
        with open(xml_file_1, "w") as f:
            f.write(xml_1)
        with open(xml_file_2, "w") as f:
            f.write(xml_2)


    def tearDown(self):
        os.remove(xml_file_1)
        os.remove(xml_file_2)
        


    def test_xml_1_file_import(self):
        t1 = glg.open_xml_file(xml_file_1)
        self.assertTrue(isinstance(t1, etree._ElementTree), "The variable t should be a lxml _ElementTree element but is: {}".format(t1))


    def test_xml_2_file_import(self):
        t2 = glg.open_xml_file(xml_file_2)
        self.assertTrue(isinstance(t2, etree._ElementTree), "The variable t should be a lxml _ElementTree element but is: {}".format(t2))

    def test_get_elements_to_compare(self):
        t1 = glg.open_xml_file(xml_file_1)
        elements1 = glg.get_elements_to_compare(t1, level_of_comparison)
        self.assertTrue(isinstance(elements1, list), "The variable elements1 should be a list, but is: {}".format(elements1))
        for e in elements1:
            self.assertTrue(isinstance(e, etree._Element), "The variable elements1 should be a lxml _Element, but is: {}".format(e))

    def test_compare_two_elements(self):
        t1 = glg.open_xml_file(xml_file_1)
        elements1 = glg.get_elements_to_compare(t1, level_of_comparison)
        t2 = glg.open_xml_file(xml_file_2)
        elements2 = glg.get_elements_to_compare(t2, level_of_comparison)
        for idx, t in enumerate(zip(elements1, elements2)):
            x = t[0]
            y = t[1]
            r = glg.compare_two_elements(x, y)
            if idx < 2:
                self.assertTrue(r, "Error: function compare_two_elements should return True, but returned: {0}!".format(r))
            else:
                self.assertFalse(r, "Error: function compare_two_elements should return False, but returned: {0}!".format(r))
    
    def test_slice_strg(self):
        pat = """<lb id="\d"/>"""
        with open(xml_file_1, "r") as f:
            strgs = glg.slice_strg(f.read(), pat)
        self.assertTrue(isinstance(strgs, list), "The variable strgs should be a list, but is: {}".format(strgs))
        for s in strgs:
            self.assertTrue(isinstance(s, str), "The variable r should be a list, but is: {}".format(s))
            
        
        #the first element contains all the xml data before the first <lb/> element
        self.assertEqual(strgs[1], """<p id="1-1">par 1</p>""", """Error: the string {0} does not match <p id="1-1">par 1</p>!""".format(strgs[0]))
        
    def test_apply_xslt(self):
        t1 = glg.open_xml_file(xml_file_1)
        x = glg.apply_xslt(t1, xslt_1)
        print(type(x))
    

if __name__ == "__main__":
    unittest.main()