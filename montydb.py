import sqlite3
import os
class Montydb:
    """
    Class Montydb records data to sqlite DB, thus providing stateful, persistent objects,
    whose data can be inspected/retrived either manually or by another program.
    Montydb does not provide locking mechanism, so updating records outside of this module
    will create unpredictable results.
    Montydb stores data as strings without encryption.
    """
    def __init__(self,fname=os.path.basename(__file__)):
        self.fname=fname
        self.sname = self.__process_fname__(self.fname)
#########
    def __process_fname__(self,fname):
        """
        Extract file name out of full file name
        :param fname: full version of file name (string)
        :return: short version of file name (string)
        """
        assert (isinstance(self.fname, str)), f"First parameter must be a string. Provided: {self.fname}"
        assert (len(self.fname) > 0), f"First parameter cannot be empty. Provided: {self.fname}"
        split_name = self.fname.split('.')
        self.sname = split_name[0]
        return str(self.sname)
############
    def __init_db__(self,fname):
        """
        Initialize  db. Meaning if db does NOT exist - it will be created
        - otherwise - opens existing one
        :param fname: file name (string)
        :return: tuple (db connection, db cursor)
        """
        if os.path.exists(self.sname):
            self.dbconn = sqlite3.connect(self.sname, uri=True)
            self.dbcur = self.dbconn.cursor()
            return (self.dbconn,self.dbcur)
        else:
            self.dbcn = self.__create_new_db__(self.sname)
            return self.dbcn
##########
    def __create_new_db__(self,sname):
        """
        Creates brand new sqlite3 db to hold attributes, where id is a primary key
        attribute name is unique and attribute value can hold any type of value
        :param sname: file name (string)
        :return: tuple containing db connection and db cursor - '-1' - otherwise
        """
        cn = sqlite3.connect(self.sname)
        cr = cn.cursor()
        createstr = 'CREATE TABLE IF NOT EXISTS ' + self.sname + \
                    ' (id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, \
                    attr_type text DEFAULT NULL, \
                    attr_name text DEFAULT NULL UNIQUE, \
                    attr_value_type text DEFAULT NULL, \
                    attr_value blob DEFAULT NULL )'
        cr.execute(createstr)
        cn.commit()
        return (cn,cr) or -1
#############
    def showAll(self,sfname):
        """
        Display contents of attribute table
        :param sfname: file name (string)
        :return: list of attributes (as strings) - '-1' - otherwise
        """
        if os.path.exists(self.sname):
            cn_tup = self.__init_db__(self.sname)
            sqlst = 'select * from ' + self.sname
            lst=[]
            cn_tup[1].execute(sqlst)
            cn_tup[0].commit()
            lst = list(cn_tup[1].fetchall())
            cn_tup[0].close()
            return lst
        else:
            print("Database is empty")
            return -1
#############
    def get_value(self,attr_name,sname,/):
        """
        Get value of attribute for given attribute name.
        :param attr_name: attribute name (string)
        :param sname: file name (string)
        :return: value (strings) 
                 1 - otherwise
        """
        if os.path.exists(self.sname):
            cn_tup = self.__init_db__(self.sname)
            if self.showAll(self.sname) != []:
                sqlst = 'select attr_value from ' + self.sname + ' where attr_name =' + '\'' + attr_name + '\'' + ';'
                er = cn_tup[1].execute(sqlst)
                cn_tup[0].commit() 
                try:
                    val = cn_tup[1].fetchone()
                    cn_tup[0].close()
                    return val[0]
                except TypeError as te:
                    print(f"no such attribute name:  {attr_name}")
                    cn_tup[0].close()
                    return 1 
            else:
                print(f"db {self.sname} is empty")
                cn_tup[0].close()
                return 1 
        else:
            print(f"db: {self.sname} does not exist")
            return 1 
############
    def __isexist__(self,tup,sname,dbconn,/):
        """
        Test whether or not record exists.
        :param tup: tuple 
        :param sname: file name (string)
        :param dbconn: DB handle, Cursor handle (tuple)
        :return: 0 if no such record found  
                 1 if record exists
                 -1 if DB Could not be initialized
        """
        cn_tup = self.__init_db__(self.sname)
        if len(cn_tup) != 0:
            sqlst='select * from ' + sname + ' where attr_name = ' + '\'' + tup[1] + '\'' + ';'
            cn_tup[1].execute(sqlst)
            cn_tup[0].commit()
            try:
                lst = list(cn_tup[1].fetchone())
                cn_tup[0].close()
            except TypeError as te:
                return 0 #no record
            except sqlite3.IntegrityError as sie:
                cn_tup[0].close()
                return 1 #record exists
        else:
            print("Could initialize database: {self.sname}")
            return -1

############
    def remove(self,tup,sname,/):
        """
        Delete attribute entry.
        :param tup: tuple 
        :param sname: file name (string)
        :return: for success - count of updated rows (1) 
                 '-1' - otherwise
        """
        if os.path.exists(self.sname):
            cn_tup = self.__init_db__(self.sname)
            if self.__isexist__(tup,self.sname,self.dbconn) == 1:
                sqlst = 'delete from ' + self.sname + ' where attr_name = ' + '\'' + tup[1] + '\'' + ';'
                rcount=0
                cn_tup[1].execute(sqlst)
                cn_tup[0].commit()
                rcount = cn_tup[1].rowcount
                cn_tup[0].close()
                print(f"Record: {tup} has been deleted")
                return rcount
            else:
                print(f"No such record: {tup} in the database: {self.sname}")
                return -1
        else:
            print(f"Database: {self.sname} does not exist")
            return -1
#############
    def update(self,tup,new_val,sname,/):
        """
        Updates attribute's value
        :param tup: tuple 
        :param new_val: new value to set (string)
        :param sname: file name (string)
        :return: for success - count of updated row (actually 1) 
                 '-1' -otherwise
        """
        if sum(self.__verify_tuple__(tup)) == 0:
            if os.path.exists(self.sname):
                cn_tup = self.__init_db__(self.sname)
                if self.get_value(tup[1], self.sname) != -1:
                    sqlst = 'update ' + self.sname + ' set attr_value = ' + '\'' + new_val + '\'' + ' where attr_name = ' + '\'' + tup[1] + '\'' + ';'
                    rcount = 0
                    cn_tup[1].execute(sqlst)
                    cn_tup[0].commit()
                    rcount = cn_tup[1].rowcount
                    print(f"rcount: {rcount}")
                    cn_tup[0].close()
                    print(f"Record: {tup} has been updated with: {new_val}")
                    return rcount
                else:
                    print(f"attr name: {tup[1]} was not found")
                    return -1
            else:
                print(f"db: {self.sname} does not exist")
                return -1
        else:
            return -1
############
    def add(self,tup,sname,/):
        """
        Add new record to the DB.
        :param tup: tuple
        :param sname: file name (string)
        :return: for success - count of rows (1)
                 -1 - if record already exists/connection to DB could not be established
        """
        if os.path.exists(self.sname):
            cn_tup = self.__init_db__(self.sname)
            if len(cn_tup) != 0:
                if  self.__isexist__(tup,self.sname,self.dbconn) == 0:
                    rcount = 0
                    executestr1='INSERT INTO ' + self.sname + ' ( attr_type,attr_name,attr_value_type,attr_value ) VALUES('
                    executestr2 = '\'' + tup[0] + '\'' + ',' + '\'' + tup[1] + '\'' + ',' + '\'' + tup[2] + '\'' + ',' + '\'' + tup[3] + '\''
                    fullexecstr= executestr1 + executestr2 + ');'
                    cn_tup[1].execute(fullexecstr)
                    cn_tup[0].commit()
                    rcount = cn_tup[1].rowcount
                    cn_tup[0].close()
                    print(f"Record: {tup} has been added")
                    return rcount
                else:
                    print(f"record: {tup} already exists")
                    return -1
            else: #no db connection
                print(f"Could not establish connection to db: {self.sname}")
                return -1
        else:   #no db file yet
            cn_tup = self.__init_db__(self.sname)
            rcount = 0
            executestr1='INSERT INTO ' + self.sname + ' ( attr_type,attr_name,attr_value_type,attr_value ) VALUES('
            executestr2 = '\'' + tup[0] + '\'' + ',' + '\'' + tup[1] + '\'' + ',' + '\'' + tup[2] + '\'' + ',' + '\'' + tup[3] + '\''
            fullexecstr= executestr1 + executestr2 + ');'
            cn_tup[1].execute(fullexecstr)
            cn_tup[0].commit()
            rcount = cn_tup[1].rowcount
            cn_tup[0].close()
            print(f"Record: {tup} has been added")
            return rcount
###########
    def __tuple_to_string_db__(self,tup):
        """
        Make tuple suitable for insertion.
        :param tup: tuple
        :return: for success - string
                 1 - otherwise
        """
        st=[]
        if sum(__verify_tuple__(tup)) != 1:
            for el in tup:
                stt = '\'' + el
                st.append(stt)
        else:
            return 1
        return ('\'' + ''.join(st)) if len(st) > 0 else 1
#############
    def __verify_tuple__(self,tup):
        """
        Trust, but verify. Check the tuple and its elements provided by user
        :param tup: tuple
        :return list of int, containing 0 for success - 1 otherwise.
        """
        tstatus = []
        if not isinstance(tup,tuple):
            print(f"Provided parameter: {tup} is not a tuple")
            tstatus.append(1)
            return tstatus
        else:
            counter=0
            tstatus.append(0)
            if len(tup) == 0:
                print(f"Provided tuple: {tup} is empty")
                tstatus.append(1)
                return tstatus
            else:
                #let's check each element of tuple
                import re
                #though it doesn't check for EVERYTHING in url but most of it.
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                for ind in range(1,len(tup),2):
                    if tup[ind -1] == 's':
                        #uh... first let's see if tup[ind] is url
                        cu = re.findall(regex, tup[ind])
                        vu = [x[0] for x in cu]
                        if vu:
                            #valid url
                            tstatus.append(0)
                        elif tup[ind].isalpha() or tup[ind].isalnum():
                            tstatus.append(0)
                        else:
                            print(f"Provided parameter: {tup[ind]} is not a proper string")
                            tstatus.append(1)
                            return tstatus
                    elif tup[ind -1] == 'i':
                        #because it is quite difficult in python
                        # to find out simple thing if there is a number inside the string
                        #and if so, what kind of number it is.
                        #Python could really learn from Erlang... :(
                        for v in tup[ind]:
                            icounter = 0
                            for vi in range(0,len(v)):
                                if v[vi] == '-' or v[vi] == '+':
                                    #it's OK to be either positive or negative
                                    tstatus.append(0)
                                    icounter +=1
                                elif v[vi].isdigit():
                                    #it is most likely an integer
                                    tstatus.append(0)
                                else:
                                    print(f"Provided parameter: {tup[ind]} claimed to be an integer, but it is not")
                                    tstatus.append(1)
                                    return tstatus
                            if icounter > 1:
                                print(f"Provided element: {tup[ind]} is not proper integer")
                                tstatus.append(1)
                                return tstatus
                    elif tup[ind -1] == 'f':
                        dotcounter=0
                        for v in tup[ind]:
                            if v == '-' or v == '+' or v.isdigit():
                                #it's OK to be negative or positive
                                tstatus.append(0)
                            elif v == '.':
                                if dotcounter > 1:
                                    print(f"Improper float encountered: {tup[ind]}")
                                    tstatus.append(1)
                                    return tstatus
                                else:
                                    tstatus.append(0)
                                    dotcounter += 1
                            elif v.isalnum() or v.isalpha():
                                #we cannot tolerate complex numbers yet.
                                print(f"Improper float detected: {tup[ind]}")
                                tstatus.append(1)
                                return tstatus
                        if dotcounter == 0:
                            print(f"Number provided: {tup[ind]} is not a float")
                            tstatus.append(1)
                            return tstatus
                    else:
                        print(f"Unsupported type of parameter: {tup[ind - 1]}")
                        tstatus.append(1)
                        return tstatus
        return tstatus
#################




