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
    <xsl:variable name="numColumns">
        <xsl:value-of select="//tei:layout/@columns"/>
    </xsl:variable>


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
                
                
                <style:style style:name="Table1" style:family="table">
                    <style:table-properties style:width="16.999cm" table:align="margins" style:shadow="none"
                    />
                </style:style>
                <style:style style:name="Table1.A" style:family="table-column">
                    <style:table-column-properties style:column-width="8.5cm"
                        style:rel-column-width="32767*"/>
                </style:style>
                <style:style style:name="Table1.1" style:family="table-row">
                    <style:table-row-properties style:min-row-height="1.402cm"/>
                </style:style>
                <style:style style:name="Table1.A1" style:family="table-cell">
                    <style:table-cell-properties fo:padding="0.097cm" fo:border="none"/>
                </style:style>
                <style:style style:name="Table1.B1" style:family="table-cell">
                    <style:table-cell-properties style:vertical-align="middle"
                        fo:background-color="transparent" fo:padding="0.097cm" fo:border="none">
                        <style:background-image/>
                    </style:table-cell-properties>
                </style:style>
                
                <style:style style:name="fr1" style:family="graphic" style:parent-style-name="Graphics">
                    <style:graphic-properties style:vertical-pos="from-top" style:vertical-rel="paragraph"
                        style:horizontal-pos="from-left" style:horizontal-rel="paragraph"
                        style:mirror="none" fo:clip="rect(0cm, 0cm, 0cm, 0cm)" draw:luminance="0%"
                        draw:contrast="0%" draw:red="0%" draw:green="0%" draw:blue="0%" draw:gamma="100%"
                        draw:color-inversion="false" draw:image-opacity="100%" draw:color-mode="standard"
                        style:flow-with-text="false"/>
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
                <text:sequence-decls>
                    <text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>
                    <text:sequence-decl text:display-outline-level="0" text:name="Table"/>
                    <text:sequence-decl text:display-outline-level="0" text:name="Text"/>
                    <text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>
                </text:sequence-decls>
                
                <text:h text:outline-level="2" text:style-name="H1"><xsl:value-of select="//tei:teiHeader//tei:title"></xsl:value-of></text:h>
                
                <xsl:for-each select="//*[@ref]">
                    <xsl:variable name="ref" select="substring-after(@ref,'#')"></xsl:variable>
                    <xsl:if test="not(//tei:charDecl/tei:glyph[@xml:id=$ref])">
                        <text:p text:style-name="P4"><xsl:value-of select="$ref"/></text:p>
                    </xsl:if>
                </xsl:for-each>
                
                
                <table:table table:name="Table1" table:style-name="Table1">
                    <table:table-column table:style-name="Table1.A" table:number-columns-repeated="2"/>
                    <xsl:for-each select="//tei:charDecl/tei:glyph">
                        <table:table-row table:style-name="Table1.1">
                            <table:table-cell table:style-name="Table1.A1" office:value-type="string">
                                <text:p text:style-name="Table_20_Contents">
                                    <xsl:if test="tei:graphic/@url">
                                        <draw:frame draw:style-name="fr1" draw:name="graphics1"  svg:width="1.4cm" svg:height="2cm"
                                        text:anchor-type="paragraph" svg:x="0.009cm" svg:y="0.228cm" draw:z-index="0">
                                            <draw:image xlink:href="Pictures/"
                                            xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad">
                                            <xsl:attribute name="xlink:href">
                                                <xsl:text>Pictures/</xsl:text><xsl:value-of select="substring-after(tei:graphic/@url, 'characters/')"/>
                                            </xsl:attribute>
                                        </draw:image>
                                        </draw:frame>
                                    </xsl:if>
                                </text:p>
                            </table:table-cell>
                            <table:table-cell table:style-name="Table1.B1" office:value-type="string">
                                <text:p text:style-name="Table_20_Contents">
                                    <text:span text:style-name="T3"><xsl:value-of select="tei:mapping"/></text:span>
                                    <xsl:text>  </xsl:text>
                                    <xsl:value-of select="tei:glyphName"/>
                                </text:p>
                            </table:table-cell>
                        </table:table-row>
                    </xsl:for-each>
                </table:table>
                
                <xsl:for-each select="//tei:linkGrp/tei:link">
                    <text:p text:style-name="P2">
                        
                        <xsl:if test="@type='incipit'">
                            <!-- if incipit: write first folio name to result document - incipit not always present -->
                            <xsl:text>(</xsl:text>
                            <xsl:value-of select="substring-after(//tei:zone[@type='folio-page'][1]/@xml:id, '-')"/>
                            <xsl:text>) </xsl:text>                        
                        </xsl:if>
                        
                        <xsl:if test="@n and @type='chapter'">
                            <xsl:value-of select="@n"/><xsl:text>. </xsl:text>
                        </xsl:if>
                        <xsl:call-template name="startProcessing">
                            <xsl:with-param name="startID"
                                select="substring-after(substring-before(@target,' '), '#')"/>
                            <xsl:with-param name="endID"
                                select="substring-after(substring-after(@target,' '), '#')"/>
                        </xsl:call-template>
                    </text:p>
                </xsl:for-each>

            </office:text>
        </office:body>
    </xsl:template>


    <xsl:template name="startProcessing">
        <xsl:param name="startID"/>
        <xsl:param name="endID"/>

        <xsl:call-template name="processNextNode">
            <xsl:with-param name="Node" select="//tei:lb[@xml:id=$startID]"/>
            <xsl:with-param name="startID" select="$startID"/>
            <xsl:with-param name="endID" select="$endID"/>
        </xsl:call-template>

    </xsl:template>


    <xsl:template name="processNextNode">
        <xsl:param name="Node"/>
        <xsl:param name="startID"/>
        <xsl:param name="endID"/>
        
        <xsl:variable name="nextNode" select="$Node/following-sibling::node()[1]"/>
        
        <xsl:choose>
            <xsl:when test="$nextNode/descendant-or-self::tei:lb[@xml:id=$endID]">
                
                <!-- if next node has a lb with the endID go to foundEndID -->
                <xsl:call-template name="foundEndID">
                    <xsl:with-param name="endID" select="$endID"/>
                    <xsl:with-param name="Node" select="$nextNode"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:choose>
                    <!-- problem with last elements of last elements??? -->
                    <xsl:when test="not($nextNode)">
                        <!-- no next node - go to parent -->
                        <xsl:call-template name="processNextNode">
                            <xsl:with-param name="Node" select="$Node/parent::node()"/>
                            <xsl:with-param name="startID" select="$startID"/>
                            <xsl:with-param name="endID" select="$endID"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:otherwise>
                        <!--  apply templates of next node and pass next node to processNextNode-->
                        <xsl:apply-templates select="$nextNode"/>
                        <xsl:call-template name="processNextNode">
                             <xsl:with-param name="Node" select="$nextNode"/>
                             <xsl:with-param name="startID" select="$startID"/>
                             <xsl:with-param name="endID" select="$endID"/>
                        </xsl:call-template>
                    </xsl:otherwise>
                 </xsl:choose>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>

    <xsl:template name="foundEndID">
        <xsl:param name="endID"/>
        <xsl:param name="Node"/>

        <xsl:if test="$Node[@type='folio-page']">
            <xsl:text>&lt;</xsl:text>
            <xsl:value-of select="substring-after($Node/@xml:id,'-')"/>
            <xsl:text>&gt;</xsl:text>
        </xsl:if>
        
        <xsl:variable name="childNode" select="$Node/child::node()[1]"></xsl:variable>

        <xsl:choose>
            <!-- might need one more when statement to test if there are children -->
            <xsl:when test="$Node[@xml:id=$endID] or not($Node)"><!-- if the node has the endID processing ends --></xsl:when>
            <xsl:when test="$Node//tei:lb[@xml:id=$endID]">
                <xsl:apply-templates select="$Node" mode="lbfound"></xsl:apply-templates>
                <xsl:call-template name="foundEndID">
                    <xsl:with-param name="endID" select="$endID"/>
                    <xsl:with-param name="Node" select="$childNode"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="$Node"></xsl:apply-templates>
                <xsl:call-template name="processNextNode">
                    <xsl:with-param name="endID" select="$endID"/>
                    <xsl:with-param name="Node" select="$Node"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>


    </xsl:template>


    <xsl:template match="tei:teiHeader"> </xsl:template>

    <xsl:template match="tei:surface">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="tei:zone[@type='folio']">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="tei:zone[@type='folio-page']">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>



    <xsl:template match="tei:zone[@type='column']">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="tei:space">
        <xsl:text> </xsl:text>
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

    <xsl:template match="tei:note"/> 
    
    <xsl:template match="tei:add[@place='margin-left'] | tei:add[@place='margin-right']">
        <xsl:text> \\</xsl:text><xsl:apply-templates></xsl:apply-templates><xsl:text>// </xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:add[@place='margin-left']/tei:lb">
        <xsl:text> | </xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:add[@place='margin-right']/tei:lb">
        <xsl:text> | </xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:add[@place='above']">
        <xsl:text>\</xsl:text>
        <xsl:apply-templates></xsl:apply-templates>
        <xsl:text>/</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:add[@place='below']">
        <xsl:text>/</xsl:text>
        <xsl:apply-templates></xsl:apply-templates>
        <xsl:text>\</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:add[@type='insertion' and @place='margin']">
        
    </xsl:template>
    
    <xsl:template match="tei:metamark">
        <xsl:choose>
            <xsl:when test="@type='insertion'">
                <xsl:apply-templates select="//tei:*[@xml:id=substring-after(@target, '#')]"></xsl:apply-templates>
                
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    
    <xsl:template match="tei:choice[tei:add and tei:del]">
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
    
    <xsl:template match="tei:choice[tei:sic][tei:reg]">
        <xsl:apply-templates select="tei:reg"></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="tei:hi[@rend='bigger' or @rend='initial']">
        <text:span text:style-name="T3">
            <xsl:apply-templates></xsl:apply-templates>
        </text:span>
    </xsl:template>
    
    <xsl:template match="tei:corr">
        <text:span text:style-name="T3">
            <xsl:apply-templates></xsl:apply-templates>
        </text:span>
    </xsl:template>
    
    
    
    <xsl:template match="tei:g[@ref][text()]">
        <!-- if the g element contains text it represents a ligature -->
        <text:span text:style-name="T2">
            <xsl:apply-templates></xsl:apply-templates>
        </text:span>
    </xsl:template>
    
    <xsl:template match="tei:g[@ref][not(text())]">
        <xsl:variable name="ref" select="@ref"></xsl:variable>
        <text:span text:style-name="T2">
            <xsl:value-of select="//tei:charDecl/tei:glyph[@xml:id=substring-after($ref,'#')]/tei:mapping"/>
        </text:span>
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
    
    <xsl:template match="tei:line" mode="lbfound">
        <xsl:choose>
            <xsl:when test="child::node()[1]=tei:seg[@type='ws']">
                <xsl:text>|</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text> | </xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    <xsl:template match="tei:zone | tei:div" mode="lbfound">
        
    </xsl:template>
    
   
</xsl:stylesheet>
