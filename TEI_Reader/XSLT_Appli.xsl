<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xs" version="2.0">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <xsl:template match="tei:TEI">
        <html>
            <head>
                <meta charset="UTF-8"/>
                <title><xsl:apply-templates select=".//tei:titleStmt/tei:title"/></title>
                <link rel="stylesheet" href="/static/css/styles.css"/>
            </head>
            <body class="piece">

                <h1 class="titre_piece">
                    <xsl:apply-templates select=".//tei:titleStmt/tei:title"/>
                </h1>
                <p class="auteur">
                    <xsl:apply-templates select=".//tei:titleStmt/tei:author"/>
                </p>
                
                    <xsl:apply-templates select="//tei:div[@type='act']"/>

            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="//tei:div[@type='act']">
        <xsl:for-each select=".">
            <h2 class="titre_acte">
            <xsl:value-of select="./tei:head"/>
            </h2>
            <xsl:for-each select="./tei:div">
                <h3 class="titre_scene">
                <xsl:value-of select="./tei:head"/>
                </h3>
                <xsl:for-each select="./tei:sp">
                    <xsl:element name="p">
                        <xsl:attribute name="class">
                            <xsl:text>speaker</xsl:text>
                        </xsl:attribute>
                        <xsl:value-of select="./tei:speaker"/>
                    </xsl:element>
                    <p class="stage">
                        <xsl:value-of select="./tei:stage/tei:choice/tei:reg"/>
                    </p>
                    <xsl:for-each select="./tei:l">
                        <xsl:element name="p">
                            <xsl:attribute name="id">
                                <xsl:value-of select="./@n"/>
                            </xsl:attribute>
                            <xsl:attribute name="class">
                                <xsl:text>ligne</xsl:text>
                            </xsl:attribute>
                            <xsl:value-of select="./tei:choice/tei:reg"/>
                        </xsl:element>
                    </xsl:for-each>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>


