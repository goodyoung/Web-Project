from pymysql import cursors, connect
import requests

class SingletonInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class WebProject(SingletonInstance):

    def __init__(self):
        self.db = connect(host='localhost', user='root', password = '1111', database='ProjectTest', cursorclass=cursors.DictCursor)
        self.cursor = self.db.cursor()
    
    def connect(self) :
        self.db = connect(host='localhost', user='root', password = '1111', database='ProjectTest', cursorclass=cursors.DictCursor)
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()

    def connect_sheet(self):

        def get_problems():
            req = requests.get("https://sheets.googleapis.com/v4/spreadsheets/1A-O6JNWZ4k0naVdsto69cuWe9o18EVpnY6ljdBxIqTQ/values/problem_sheet?key=AIzaSyC4jcCAJgQAurX7-oZLa7KQTelx8AmVXFU")
            print(req.status_code)
            problems = req.json()['values'][1:]
            return problems

        def parse_problems(problems):
            problems_list = []
            for problem in problems:
                problem_dict = {}

                problem_dict["id"] = problem[0]
                problem_dict["type"] = problem[1]
                problem_dict["category"] = problem[2]
                problem_dict["imgurl"] = problem[3]
                problem_dict["content"] = problem[4]
                problem_dict["choices"] = problem[5]
                problem_dict["answer"] = problem[6]
                problem_dict["explanation"] = problem[7]
                problem_dict["writer"] = problem[8]

                problems_list.append(problem_dict)

            print(problems_list)
            return problems_list

        self.connect()
        problem_list = parse_problems(get_problems())

        self.cursor.execute("TRUNCATE problem")
        self.cursor.execute("TRUNCATE objective")
        self.cursor.execute("TRUNCATE subjective")
        self.cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'problem'")
        get_column = self.cursor.fetchall()

        for problem_dict in problem_list:
            field_list = []
            value_list = []

            for column in get_column:
                if(column["COLUMN_NAME"] in problem_dict.keys()):
                    field_list.append(column["COLUMN_NAME"])
                    value = problem_dict[column["COLUMN_NAME"]]
                    value = value.replace("\'", "\'\'").replace("\"", "\'\'")

                    if(column["COLUMN_NAME"]=="id"):
                        value_list.append(value)
                    else:
                        value_list.append("\""+value+"\"")
            
            sql = 'INSERT INTO problem({0}) VALUES ({1})'.format(", ".join(field_list), ", ".join(value_list))
            self.cursor.execute(sql)

            if(problem_dict["type"]=="객관식"):
                field_list = []
                value_list = []

                self.cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'objective'")
                obj_column = self.cursor.fetchall()

                for column in obj_column:
                    if(column["COLUMN_NAME"] in problem_dict.keys()):
                        field_list.append(column["COLUMN_NAME"])
                        value = problem_dict[column["COLUMN_NAME"]]
                        value = value.replace("\'", "\'\'").replace("\"", "\'\'")

                        if(column["COLUMN_NAME"]=="id"):
                            value_list.append(value)
                        else:
                            value_list.append("\""+value+"\"")
                sql = 'INSERT INTO objective({0}) VALUES ({1})'.format(", ".join(field_list), ", ".join(value_list))
                self.cursor.execute(sql)
            else:
                field_list = []
                value_list = []

                self.cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'subjective'")
                obj_column = self.cursor.fetchall()
                for column in obj_column:
                    print(column)
                    if(column["COLUMN_NAME"] in problem_dict.keys()):
                        field_list.append(column["COLUMN_NAME"])
                        value = problem_dict[column["COLUMN_NAME"]]
                        value = value.replace("\'", "\'\'").replace("\"", "\'\'")

                        if(column["COLUMN_NAME"]=="id"):
                            value_list.append(value)
                        else:
                            value_list.append("\""+value+"\"")
                sql = 'INSERT INTO subjective({0}) VALUES ({1})'.format(", ".join(field_list), ", ".join(value_list))
                self.cursor.execute(sql)

        self.db.commit()
        sql = "SELECT * FROM problem"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        self.close()
        return rows

    def send_query(self, sql, commit=False):
        self.connect()

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)

        if(commit):
            self.db.commit()

        self.close()
        return result