def getDbTables(conn, cursor, envName, dbType):
    conn = conn
    cursor = cursor
    envName = envName
    dbType = dbType
    cursor = conn.cursor()
    if(dbType == 'db2'):
        query = "select table_name from SYSIBM.tables where table_type = 'BASE TABLE' order by table_name"
        cursor.execute(query)
        getDbTablesResult = cursor.fetchall()
    elif(dbType == 'sqlServer'):
        query = "select table_name from information_schema.tables where table_type='BASE TABLE' and table_catalog='" + envName + "' order by table_name"
        cursor.execute(query)
        getDbTablesResult = cursor.fetchall()
    elif(dbType == 'oracle'):
        query = "select object_name from user_objects where object_type = 'TABLE' order by object_name"
        cursor.execute(query)
        getDbTablesResult = cursor.fetchall()    
    elif(dbType == 'mySql'):
        query = "select table_name from information_schema.tables where table_type='BASE TABLE' and table_schema= '" + envName + "' order by table_name"
        cursor.execute(query)
        getDbTablesResult = cursor.fetchall()
    return getDbTablesResult
    