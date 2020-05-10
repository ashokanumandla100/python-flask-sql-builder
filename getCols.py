import os

def getColumns(conn, cursor, dbType, tableName):
    conn = conn
    cursor = cursor
    dbType = dbType
    tableName = tableName
    if(dbType == 'db2'):
        query = "select name from SYSIBM.SYSCOLUMNS where tbname = '" + tableName + "'"
        cursor.execute(query)
        getColsResult = cursor.fetchall()
    elif(dbType == 'sqlServer' or dbType == 'mySql'):
        query = "select column_name from information_schema.columns where table_name='" + tableName + "' order by column_name"
        cursor.execute(query)
        getColsResult = cursor.fetchall()
    elif(dbType == 'oracle'):
        query = "select COLUMN_NAME from ALL_TAB_COLUMNS where lower(TABLE_NAME)=lower('" + tableName + "') order by COLUMN_NAME"
        cursor.execute(query)
        getColsResult = cursor.fetchall()
    return getColsResult    