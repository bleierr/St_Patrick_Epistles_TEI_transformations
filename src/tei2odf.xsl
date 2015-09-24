<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" exclude-result-prefixes="tei">
    <xsl:strip-space elements="tei:*"/>
    <xsl:output method="xml" encoding="UTF-8"/>
    <xsl:variable name="lineHeight">25pt</xsl:variable>
    <xsl:variable name="bigger">18pt</xsl:variable>

    <xsl:template match="/">
        <office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
            xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
            xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
            xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
            xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
            xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
            xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
            xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
            xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
            xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
            xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
            xmlns:math="http://www.w3.org/1998/Math/MathML"
            xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
            xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
            xmlns:ooo="http://openoffice.org/2004/office"
            xmlns:ooow="http://openoffice.org/2004/writer"
            xmlns:oooc="http://openoffice.org/2004/calc"
            xmlns:dom="http://www.w3.org/2001/xml-events"
            xmlns:xforms="http://www.w3.org/2002/xforms"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:rpt="http://openoffice.org/2005/report"
            xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
            xmlns:rdfa="http://docs.oasis-open.org/opendocument/meta/rdfa#"
            xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0"
            office:version="1.2">
            <office:scripts/>
            <office:font-face-decls>
                <style:font-face style:name="Tahoma1" svg:font-family="Tahoma"/>
                <style:font-face style:name="Times New Roman"
                    svg:font-family="&apos;Times New Roman&apos;" style:font-family-generic="roman"
                    style:font-pitch="variable"/>
                <style:font-face style:name="Arial" svg:font-family="Arial"
                    style:font-family-generic="swiss" style:font-pitch="variable"/>
                <style:font-face style:name="Andale Sans UI"
                    svg:font-family="&apos;Andale Sans UI&apos;" style:font-family-generic="system"
                    style:font-pitch="variable"/>
                <style:font-face style:name="Tahoma" svg:font-family="Tahoma"
                    style:font-family-generic="system" style:font-pitch="variable"/>
            </office:font-face-decls>
            <office:automatic-styles>
                <style:style style:name="P1" style:family="paragraph" style:parent-style-name="Footer">
                    <style:paragraph-properties fo:text-align="center" style:justify-single-word="false"/>
                </style:style>
                <style:style style:name="P2" style:family="paragraph" style:parent-style-name="Standard">
                    <style:paragraph-properties fo:line-height="150%"/>
                    <style:text-properties fo:font-size="12pt"/>
                </style:style>
                <style:style style:name="P3" style:family="paragraph"
                    style:parent-style-name="Table_20_Contents">
                    <style:paragraph-properties fo:line-height="150%"/>
                </style:style>
                <style:style style:name="P4" style:family="paragraph" style:parent-style-name="Heading">
                    <style:paragraph-properties fo:line-height="150%"/>
                    <style:text-properties fo:font-weight="bold"/>
                </style:style>
                <style:style style:name="T1" style:family="text">
                    <style:text-properties fo:font-style="italic"/>
                </style:style>
                <style:style style:name="T2" style:family="text">
                    <style:text-properties fo:font-weight="bold"/>
                </style:style>
                <style:style style:name="T3" style:family="text">
                    <style:text-properties fo:font-size="{$bigger}" fo:font-weight="bold" />
                </style:style>
                
                <style:style style:name="H1" style:family="paragraph"
                    style:parent-style-name="Heading" style:class="text">
                    <style:text-properties fo:font-size="85%" fo:font-weight="bold"/>
                </style:style>
            </office:automatic-styles>
            
            <xsl:call-template name="body"/>

        </office:document-content>
    </xsl:template>

    <xsl:template name="body">
        <office:body>
            <office:text>
                
                <text:h text:outline-level="2" text:style-name="H1"><xsl:value-of select="//tei:teiHeader//tei:title"></xsl:value-of></text:h>
                
                    <xsl:apply-templates></xsl:apply-templates>

            </office:text>
        </office:body>
    </xsl:template>

    <xsl:template match="tei:teiHeader"> </xsl:template>
    
    <xsl:template match="tei:sourceDoc">
        <text:p>
            <xsl:apply-templates/>
        </text:p>
    </xsl:template>

    <xsl:template match="tei:surface">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="tei:surfaceGrp[@type='folio']">
        
        <xsl:apply-templates></xsl:apply-templates>
        
    </xsl:template>

    <xsl:template match="tei:surface[@type='folio-page']">
        <xsl:if test="not(descendant::tei:zone[@type='column'])">
            <xsl:text>(</xsl:text><xsl:value-of select="substring-after(@xml:id, '-')"/><xsl:text>)</xsl:text>
        </xsl:if>
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="tei:zone[@type='column']">
        <xsl:text>(</xsl:text><xsl:value-of select="substring-after(@xml:id, '-')"/><xsl:text>)</xsl:text>
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="tei:line">
        <xsl:choose>
            <xsl:when test="child::node()[1]=tei:seg[@type='ws']">
                <xsl:text>|</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text> | </xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:w">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:pc">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:lb">
        <xsl:choose>
            <xsl:when test="ancestor::tei:add/@place='margin-left' or ancestor::tei:add/@place='margin-right'">
                <xsl:text> | </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <!-- the python script will pick up on the double curly brackets -->
                <xsl:text>{{</xsl:text><xsl:value-of select="@xml:id"/><xsl:text>}}</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:space">
        <xsl:choose>
            <xsl:when test="following-sibling::*[1][self::tei:pc]">
                <!-- don't print a space -->
            </xsl:when>
            <xsl:otherwise><xsl:text> </xsl:text></xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>

    <xsl:template match="tei:expan">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="tei:ex">
        <text:span text:style-name="T1">
            <xsl:apply-templates/>
        </text:span>
    </xsl:template>

    <xsl:template match="tei:abbr"/> 

    <xsl:template match="tei:am"/>

   
    
    <!-- METAMARKS -->
    <xsl:template match="tei:metamark[@rend='z-like']">
                <xsl:choose>
                    <xsl:when test="@place='above'">
                        \z/
                    </xsl:when>
                    <xsl:when test="@place='below'">
                        /z\
                    </xsl:when>
                    <xsl:when test="@place='margin'">
                        \\z//
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates></xsl:apply-templates>
                    </xsl:otherwise>
                </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:add[@place='margin-right']/tei:metamark[@rend='z-like'] | tei:add[@place='margin-left']/tei:metamark[@rend='z-like']">
        <xsl:text>z</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:metamark">
       
    </xsl:template>
    
    <!-- ADDITION -->
    
    <xsl:template match="tei:add">
        <xsl:choose>
            <xsl:when test="@place='above'">
                \<xsl:apply-templates></xsl:apply-templates>/
            </xsl:when>
            <xsl:when test="@place='below'">
                /<xsl:apply-templates></xsl:apply-templates>\
            </xsl:when>
            <xsl:otherwise>
                ERROR
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:add[@place='beginningOfText'] | tei:add[@place='line']">
        <!-- indicates usually a decorated initial or incipit -->
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    

    <xsl:template match="tei:add[@place='margin-left'] | tei:add[@place='margin-right']">
        <xsl:choose>
            <xsl:when test="ancestor::tei:w">
                <xsl:text>\\</xsl:text><xsl:apply-templates></xsl:apply-templates><xsl:text>//</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text> \\</xsl:text><xsl:apply-templates></xsl:apply-templates><xsl:text>// </xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- DELETION -->
    
    <xsl:template match="tei:subst[tei:add and tei:del]">
        <xsl:text>[</xsl:text>
        <xsl:value-of select="tei:del"/>
        <xsl:text> &gt; </xsl:text>
        <xsl:if test="tei:add[@place='above']">
            <xsl:text>\</xsl:text>
        </xsl:if>
        <xsl:value-of select="tei:add"/>
        <xsl:if test="tei:add[@place='above']">
            <xsl:text>/</xsl:text>
        </xsl:if>
        <xsl:text>]</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:del">
        <xsl:text>[</xsl:text>
        <xsl:apply-templates></xsl:apply-templates>
        <xsl:text>]</xsl:text>
    </xsl:template>
    
    <!-- CORRECTION and REG -->
    
    <xsl:template match="tei:choice[tei:orig][tei:reg]">
        <xsl:apply-templates select="tei:orig"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:choice[tei:sic][tei:corr]">
        <xsl:apply-templates select="tei:sic"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:corr | tei:reg">
        
    </xsl:template>
    
    <xsl:template match="tei:sic | tei:orig">
        <text:span text:style-name="T3">
            <xsl:apply-templates></xsl:apply-templates>
        </text:span>
    </xsl:template>
    
    
    <!-- HIGHLIGHTING -->

    <xsl:template match="tei:hi[@rend='bigger' or @rend='initial' or @rend='maj']">
        <text:span text:style-name="T3">
            <xsl:apply-templates></xsl:apply-templates>
        </text:span>
    </xsl:template>
    
    <xsl:template match="tei:seg[@rend='amp']">
        <text:span text:style-name="T1">
            <xsl:apply-templates></xsl:apply-templates>
        </text:span>
    </xsl:template>
    
    <xsl:template match="tei:seg[@type='ligature']">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:seg[@rend='uncial']">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    
    <xsl:template match="tei:g">
            <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    


    <!-- FOOTNOTE -->
    <xsl:template match="tei:note[@type='editorial']">
        <text:note text:id="ftn1"
            text:note-class="footnote">
            <text:note-citation><xsl:value-of select="count(preceding::tei:note[@type='editorial'])"></xsl:value-of></text:note-citation>
            <text:note-body>
                <text:p text:style-name="Footnote">
                    <xsl:apply-templates></xsl:apply-templates>
                </text:p>
            </text:note-body>
        </text:note>
    </xsl:template>
    
    <xsl:template match="tei:note"/> 
    
    
    
    
    <!-- SUPPLIED, DAMAGE, GAPS -->
    <xsl:template match="tei:supplied">
        <xsl:text>&lt;</xsl:text><xsl:apply-templates></xsl:apply-templates><xsl:text>&gt;</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:gap">
        <xsl:text>[[±</xsl:text><xsl:value-of select="@quantity"></xsl:value-of><xsl:text>]]</xsl:text>
    </xsl:template>
    
    
    <xsl:template match="tei:damage">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    
    
   
</xsl:stylesheet>
