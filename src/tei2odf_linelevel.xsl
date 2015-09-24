<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" exclude-result-prefixes="tei xs" version="2.0">
    <xsl:strip-space elements="tei:*"/>
    <xsl:output method="xml" encoding="UTF-8"/>
    
    <xsl:template match="/">
        <text:span text:style-name="T7">
            <xsl:apply-templates></xsl:apply-templates>
        </text:span>
    </xsl:template>
    
    <xsl:template match="tei:line">
        <xsl:choose>
            <xsl:when test="child::node()[1]=tei:seg[@type='ws'] or child::node()[1]//tei:seg[@type='ws']">
                <xsl:text>|</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text> | </xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template match="tei:zone[@type='column']">
        <xsl:text>(</xsl:text>
        <xsl:value-of select="substring-after(@xml:id,'-')"></xsl:value-of>
        <xsl:text>)</xsl:text>
    </xsl:template>
    <xsl:template match="tei:surface[@type='page']">
        <xsl:text>(</xsl:text>
        <xsl:value-of select="substring-after(@xml:id,'-')"></xsl:value-of>
        <xsl:text>)</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:zone">
        
    </xsl:template>
    
    
    <!-- WORDS and SEGMENTS -->
    
    <xsl:template match="tei:w">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:seg[@type='ws']">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:seg">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <!-- PUNCTUATION and SPACES-->
    
    <xsl:template match="tei:pc">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:space">
        <!-- space is controlled via the python script -->
    </xsl:template>
    
    
    <xsl:template match="tei:subst">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    
    <xsl:template match="tei:choice">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:expan">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:ex">
        <text:span text:style-name="T1">
            <xsl:apply-templates></xsl:apply-templates>
        </text:span>
    </xsl:template>
    
    <xsl:template match="tei:abbr"/> 
    
    <xsl:template match="tei:am"/>
    
    <xsl:template match="tei:note"/> 
    
    
    <!-- ADDITION -->
    
    <xsl:template match="tei:add[@place='margin-left']/tei:lb">
        <xsl:text> | </xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:add[@place='margin-right']/tei:lb">
        <xsl:text> | </xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:add[@place='beginningOfText'] | tei:add[@place='line']">
        <!-- indicates usually a decorated initial or incipit -->
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
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
    
    
    
    <!-- METAMARKS -->
    <xsl:template match="tei:metamark[@rend='z-mark']">
        <xsl:if test="not(ancestor::tei:add)">
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
        </xsl:if>
    </xsl:template>
    
    
    
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
    
    <xsl:template match="tei:sic | tei:orig">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:choice/tei:corr |tei:w/tei:corr | tei:seg/tei:corr | tei:expan/tei:corr">
    </xsl:template>
    
    <xsl:template match="tei:choice/tei:reg | tei:w/tei:reg | tei:seg/tei:reg | tei:expan/tei:reg">
    </xsl:template>
    
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