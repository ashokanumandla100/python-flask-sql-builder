from flask import Flask, render_template, request, jsonify
from getTables import getDbTables
from getCols import getColumns
from logging.config import dictConfig
import ibm_db_dbi as db
import pyodbc, MySQLdb, cx_Oracle, logging

# flask application creation
app = Flask(__name__)

# application homepage
@app.route('/home')
def queryInput():
    with open('savedQueries.sql', 'r') as file:
        savedQueriesFromFile = file.read()
    logger.info('Application homepage is opened')
    return render_template('queryInput.html', savedQueries = savedQueriesFromFile)

# db connection after selecting the database
@app.route('/dbConnect',methods = ['POST'])
def dbConnect():
    
    # declaring the global variables
    global conn, cursor, getDbTablesResult, envName, dbType
    envName = request.form['myData']
    
    # creating the actual connection based on the selected environment
    if(envName == 'MSSQL DB'):
        dbType = 'sqlServer'
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=' + envName + ';UID=admin;PWD=password')
    elif(envName == 'Oracle DB'):
        dbType = 'oracle'
        conn = cx_Oracle.connect("admin/password@localhost:1521/" + envName)
    elif(envName == 'DB2 DB'):
        dbType = 'db2'
        conn = db.connect("DATABASE=" + envName + ";HOSTNAME=localhost;PORT=50000;PROTOCOL=TCPIP;UID=admin;PWD=password;", "", "")
    elif(envName == 'MySQL DB'):
        dbType = 'mySql'
        conn = MySQLdb.connect("localhost","admin","password", envName)
    cursor = conn.cursor()
    getDbTablesResult = getDbTables(conn, cursor, envName, dbType)
    logger.info('DB connection is created for DB: ' + envName)
    return "success"      

# get tables list for the selected database
@app.route('/getTable',methods = ['GET'])
def getTable():
    if request.method == 'GET':
        getDbTables = []
        for item in getDbTablesResult:
            getDbTables.append(item[0])
        data = {'data': getDbTables}
        logger.info('Table information retrieved for selected DB')
        return jsonify(data)

# get the columns from the selected table, database
@app.route('/getColumn/<tableName>',methods = ['GET'])
def getColumn(tableName):
    if request.method == 'GET':
        getCols = []
        logger.info('tableName: ' + tableName)
        getColsResult = getColumns(conn, cursor, dbType, tableName)
        for item in getColsResult:
            getCols.append(item[0])
        data = {'data': getCols}
        logger.info('Columns retrieved successfully')
        return jsonify(data) 

# closing the db connection
@app.route('/getConnDel',methods = ['GET'])
def getConnDel():
    try:
        if(envName):
            cursor.close()
            conn.close()
            logger.info('DB connection is closed')
            return "connection closed successfully"
    except:
        logger.info('Connection is not opened yet')
        return "connection is not opened yet"
    
@app.route('/outputResult',methods = ['POST'])
def outputResult():
    if request.method == 'POST':
        req_data = request.get_json(force=True)
        try: 
            if req_data['selectAll']:
                colValue = req_data['colValue']
                tableName = req_data['tableName']
                columnName = req_data['columnName']
                operator = req_data['operator']
                if req_data['conditional']:              
                    if(operator == 'is equal to'):
                        query = "select * from " + tableName + " where " + columnName + " = '" + colValue + "'"
                    elif(operator == 'like'):
                        query = "select * from " + tableName + " where " + columnName + " like '%" + colValue + "%'"
                else:
                    query = "select * from " + tableName   
            else:
                queryRaw = req_data['query']
                with open('savedQueries.sql', 'w') as file:
                    file.write(queryRaw)
                queryList = queryRaw.split('\n')
                n = len(queryList)
                i = 0
                while(i < n):
                    line = queryList[i]
                    if(line.strip() != ''):
                        if(line.startswith('--')):
                            pass
                        else:
                            if(line.strip().upper().startswith(('SELECT', 'UPDATE', 'INSERT', 'DELETE'))):
                                query = line.strip()
                                if(line.strip().endswith(';')):
                                    break
                                else:
                                    for j in range(1, 20):
                                        buildQuery = queryList[i + j]
                                        if not (buildQuery.strip().endswith(';')):
                                            query = query + '\n' + buildQuery
                                        else:
                                            query = query + '\n' + buildQuery
                                            break
                                    break
                    i += 1
            logger.info('Query: ' + query)
            if(query.upper().startswith('SELECT')):
                cursor.execute(query)
                queryResult = cursor.fetchall()
                recordCount = len(queryResult)
                colNames = [field[0] for field in cursor.description]
                if(recordCount > 0):
                    colCount = list(range(0,len(queryResult[0])))
                else:
                    colCount = 0
                return render_template("queryOutput.html",result = [queryResult, colCount, colNames, recordCount, query])
            elif(query.upper().startswith('INSERT')):
                cursor.execute(query)
                conn.commit()
                logger.info('Inserted Successfully')
                return "Inserted Successfully"
            elif(query.upper().startswith('UPDATE')):
                cursor.execute(query)
                conn.commit()
                logger.info('Updated Successfully')
                return "Updated Successfully"
            elif(query.upper().startswith('DELETE')):
                cursor.execute(query)
                conn.commit()
                logger.info('Deleted Successfully')
                return "Deleted Successfully"                    
        except (cx_Oracle.DatabaseError, pyodbc.Error) as e:
            logger.info('Databse connection error' + e)
            return "DB Error Occurred"
        else:
            logger.info('Unhandled Exception')
            return "Unhandled Exception"
    

if __name__ == '__main__':
    
    # logger functionality
    logging_config = dict(
        version = 1,
        formatters = {
            'frmt': {'format': '%(asctime)s - %(levelname)s - %(message)s'},
            },
        handlers = {
                'hndlr': {'class': 'logging.FileHandler',
                      'filename':'appServer.log',
                      'formatter': 'frmt',
                      'level': logging.DEBUG,
                      },
                  },
        root = {
            'handlers': ['hndlr'],
            'level': logging.DEBUG,
            },
    )
    dictConfig(logging_config)    
    logger = logging.getLogger()
    
    # running the application
    app.run(host="127.0.0.1", port=5000)