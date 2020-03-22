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
            </head>
            <body>

                <h1>
                    <xsl:apply-templates select=".//tei:titleStmt/tei:title"/>
                </h1>
                <ul>
                    <xsl:apply-templates select=".//tei:titleStmt/tei:author"/>
                </ul>

<p>
    <xsl:apply-templates select="//tei:l/tei:choice/tei:reg"/>
</p>
            </body>
        </html>
    </xsl:template>

        <xsl:template match="//tei:l/tei:choice/tei:reg">
        <xsl:element name="li">
            <xsl:attribute name="title">
                <xsl:number select="." format="1" level="any"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>


