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
                <h2>
                    <xsl:apply-templates select=".//tei:titleStmt/tei:author"/>
                </h2>

            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>


