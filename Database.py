import psycopg2

class DBHandler:
    def __init__(self, hostname: str, port: str, databaseName: str, databaseUser: str, databasePassword: str) -> None:
        conn = psycopg2.connect(
            host=hostname,
            port=port,
            database=databaseName,
            user=databaseUser,
            password=databasePassword
        )

        cur = conn.cursor()

        self.conn = conn
        self.cursor = cur
    
    def executeQuery(self, query: str, columns: list) -> list:
        self.cursor.execute(query=query)
        rows = self.cursor.fetchall()

        resultList = []

        for row in rows:
            rowDict = {}
            for i in range(len(columns)):
                if row[i] is None or row[i] == '':
                    rowDict[columns[i]] = None
                else:
                    rowDict[columns[i]] = row[i]
            resultList.append(rowDict)

        return resultList
    
    @staticmethod
    def contructQuery(queryType: str, columns: list, tableName: str, whereClause: str = None) -> str:
        if queryType == "SELECT":
            queryString = "SELECT {} FROM {}".format(", ".join(columns), tableName)
            return queryString
        return None
