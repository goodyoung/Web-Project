from pymysql import cursors, connect
import requests
import re
import os

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

    def connect(self):
        self.db = connect(host='localhost', user='root', password = 'rjsdud', database='ProjectTest', cursorclass=cursors.DictCursor)

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
                print(problem)
                if(len(problem)!=9):
                    continue

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
        cursor = self.db.cursor()
        problem_list = parse_problems(get_problems())

        cursor.execute("TRUNCATE problem")
        cursor.execute("TRUNCATE objective")
        cursor.execute("TRUNCATE subjective")
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'problem'")
        get_column = cursor.fetchall()

        for problem_dict in problem_list:
            field_list = []
            value_list = []

            for column in get_column:
                if(column["COLUMN_NAME"] in problem_dict.keys()):
                    field_list.append(column["COLUMN_NAME"])
                    value = problem_dict[column["COLUMN_NAME"]]
                    value = value.replace("\'", "\'\'").replace("\"", "\"\"")

                    if(column["COLUMN_NAME"]=="id"):
                        value_list.append(value)
                    else:
                        value_list.append("\""+value+"\"")
            
            sql = 'INSERT INTO problem({0}) VALUES ({1})'.format(", ".join(field_list), ", ".join(value_list))
            cursor.execute(sql)

            if(problem_dict["type"]=="객관식"):
                field_list = []
                value_list = []

                cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'objective'")
                obj_column = cursor.fetchall()

                for column in obj_column:
                    if(column["COLUMN_NAME"] in problem_dict.keys()):
                        field_list.append(column["COLUMN_NAME"])
                        value = problem_dict[column["COLUMN_NAME"]]
                        value = value.replace("\'", "\'\'").replace("\"", "\"\"")

                        if(column["COLUMN_NAME"]=="id"):
                            value_list.append(value)
                        else:
                            value_list.append("\""+value+"\"")
                sql = 'INSERT INTO objective({0}) VALUES ({1})'.format(", ".join(field_list), ", ".join(value_list))
                cursor.execute(sql)
            else:
                field_list = []
                value_list = []

                cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'subjective'")
                obj_column = cursor.fetchall()
                for column in obj_column:
                    print(column)
                    if(column["COLUMN_NAME"] in problem_dict.keys()):
                        field_list.append(column["COLUMN_NAME"])
                        value = problem_dict[column["COLUMN_NAME"]]
                        value = value.replace("\'", "\'\'").replace("\"", "\"\"")

                        if(column["COLUMN_NAME"]=="id"):
                            value_list.append(value)
                        else:
                            value_list.append("\""+value+"\"")
                sql = 'INSERT INTO subjective({0}) VALUES ({1})'.format(", ".join(field_list), ", ".join(value_list))
                cursor.execute(sql)

        self.db.commit()
        sql = "SELECT * FROM problem"
        cursor.execute(sql)
        rows = cursor.fetchall()

        self.close()
        return rows

    def connect_form(self):

        def get_imginfos():
            req = requests.get("https://sheets.googleapis.com/v4/spreadsheets/1bYamrb9UUwvOTWmoYMXU1YF_nfBgABVDJG6CJ5lbu08/values/form_sheet?key=AIzaSyC4jcCAJgQAurX7-oZLa7KQTelx8AmVXFU")
            print(req.status_code)
            imginfos = req.json()['values'][1:]
            return imginfos

        img_list = get_imginfos()

        for img_info in img_list:
            drive_url = img_info[1]
            print(drive_url)
            img_id = re.findall("id=(.*)", drive_url)[0]
            img_name = img_info[2]
            print(img_id, img_name)

            req = requests.get("https://www.googleapis.com/drive/v3/files/{}?alt=media&key=AIzaSyC4jcCAJgQAurX7-oZLa7KQTelx8AmVXFU".format(img_id))
            print(req.status_code)
            img_content = req.content

            base_path = os.path.dirname(os.path.abspath(__file__))
            with open(base_path+"/static/problem_img/"+img_name, "wb") as f:
                f.write(req.content)

        return img_list


    def send_query(self, sql, commit=False):

        self.connect()

        cursor = self.db.cursor()

        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)

        if(commit):
            self.db.commit()

        self.close()
        
        return result