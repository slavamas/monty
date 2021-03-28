import os
import sys
class Montyfile:
    """
    Class Montyfile records data to text file, thus providing stateful, persistent objects,
    whose data can be inspected/retrived either manually or by another program.
    Montyfile does not provide locking mechanism, so updating records outside of this module
    will create unpredictable results.
    Montyfile stores data as strings without encryption.
    """
    def __init__(self,fname=os.path.basename(__file__)):
        self.fname=fname
        self.sname=self.__process_fname__(self.fname)

##############
    def showAll(self,sname):
        """
        Return contents of attributes' records
        :param fn: file name (string)
        :return: a list containing all recorded attributes (list of strings separated by '\n')
                each line ends with ',' (before '\n')
                or 1 if file doesn't exist
        """
        assert (isinstance(self.sname, str)), f"First parameter must be a string. Provided: {self.sname}"
        assert (len(self.sname) > 0), f"First parameter cannot be empty. Provided: {self.sname}"
        all_data = self.__read_from_file__(self.sname)
        return list(all_data) if os.path.exists(self.sname) else 1
#################
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
#################
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
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                for ind in range(1,len(tup),2):
                    if tup[ind -1] == 's':
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
                        for v in tup[ind]:
                            icounter = 0
                            if v[0] == '-' or v[0] == '+':
                                #it's OK to be either positive or negative
                                pass
                            for vi in range(0,len(v)):
                                if v[vi] == '.':
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
                            if icounter != 0:
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
    def add(self,tup, sname):
        """
        Record new attribute to file. If file doesn't exist - new file with file name (fn) created
        and attributes are written to file
        If file exist - attributes are appended to existing file
        :param tup: tuple, consisting - tup[0] - attribute name type('s'),
                    tup[1] - attribute name (string),
                    tup[2] - attribute  value type ('s' or 'i' or 'f')
                    tup[3] - attribute value (string or integer or float)
        :param fn: file name (string)
        :return: list of integers indicating either success or failure (0 - on success, 1 - otherwise)
        """
        addstatus = []
        all_attr = []
        if sum(self.__verify_tuple__(tup)) > 0:
            addstatus.append(1)
            return addstatus
        else:
            addstatus.append(0)
            #tuple is OK
            all_attr = self.showAll(self.sname)
            if all_attr != 1:
                if self.__isexist__(tup, self.sname) == 0:
                    # 0 - string unique and file exists, so append
                    t2w = self.__tuple_to_string__(tup)
                    all_attr.append(t2w)
                    st2w = ''.join(all_attr)
                    t2f = self.__record_to_file__(self.sname, st2w)
                    addstatus.append(t2f)
                else:
                    #string is not unique and file exists - refuse
                    print(f"attribute: {tup} is already present")
                    addstatus.append(1)
                    return sum(addstatus)
            else:
                t2w = self.__tuple_to_string__(tup)
                t2f = self.__record_to_file__(self.sname, t2w)
                addstatus.append(t2f)
        return sum(addstatus)
#############
    def remove(self,tup,sname):
        """
        Delete attribute entry.
        :param tup: tuple 
        :param sname: file name (string)
        :return: for success - count of updated rows (1) 
                 '-1' - otherwise
        """
        rmstatus = []
        all_attr = []
        if sum(self.__verify_tuple__(tup)) > 0:
            rmstatus.append(1)
            return rmstatus
        else:
            rmstatus.append(0)
            # tuple is OK
            all_attr = self.showAll(self.sname)
            if all_attr != 1:
                t2r = self.__tuple_to_string__(tup)
                for line in all_attr:
                    if line.find(t2r) != -1:
                        index = all_attr.index(t2r)
                        updated_attr = all_attr.pop(index)
                        st2w = ''.join(all_attr)
                        t2f = self.__record_to_file__(self.sname, st2w)
                        rmstatus.append(0)
                        break
                    else:
                        continue
            else:
                print(f"file: {self.sname} is empty - nothing to remove")
                rmstatus.append(1)
        return rmstatus
############
    def update(self,tup,new_val,sname):
        """
        Updates attribute's value
        :param tup: tuple 
        :param new_val: new value to set (string)
        :param sname: file name (string)
        :return: for success - count of updated row (actually 1) 
                 '-1' -otherwise
        """
        upstatus=[]
        tup2add =(tup[0],tup[1],tup[2],new_val)
        if sum(self.remove(tup,self.sname)) !=1:
            if self.add(tup2add,self.sname) == 0:
                upstatus.append(0)
            else:
                upstatus.append(1)
                return upstatus
        else:
            upstatus.append(1)
            return upstatus
        return upstatus
############
    def __record_to_file__(self,fn,strdata):
        """
        Record attributes to file
        :param fn: file name (string)
        :param strdata: data to be written (string)
        :return: 0 on success - 1 otherwise
        """
        status = None
        try:
            fo = open(self.sname, mode='wt')
            fo.write(strdata)
            fo.close()
            status = 0
        except OSError as oser:
            print(f"Exception while writing to file: {self.sname} - {oser}")
            status = 1
        return status
##############
    def __read_from_file__(self,sname):
        """
        Read records from file
        :param fn: file name (string)
        :return: list of records or 1 otherwise
        """
        import errno
        all_data = []
        try:
            fa = open(self.fname, mode='rt')
            all_data = fa.readlines()
            fa.close()
        except IOError as e:
            if e.errno == errno.ENOENT:
                all_data = None
            elif e.errno == errno.EBADF:
                print(e.strerror)
        return list(all_data) if os.path.exists(self.sname) else 1
#############
    def __tuple_to_string__(self,tup):
        """
        Read tuple
        :param tup: tuple
        :return: for success - string
                 1 - otherwise
        """
        if sum(self.__verify_tuple__(tup)) != 1:
            t = ','.join(tup) + ',' + '\n'
        else:
            return 1
        return t if len(t) > 0 else 1
##############
    def __isexist__(self,tup,sname, /):
        """
        Test whether or not record exists.
        :param tup: tuple 
        :param sname: file name (string)
        :return: 0 if no such record found  
                 1 if record exists
        """
        cmpstatus = []
        if sum(self.__verify_tuple__(tup)) > 0:
            cmpstatus.append(1)
            return cmpstatus
        else:
            list_from_file = self.showAll(self.sname)
            if list_from_file == 1:
                cmpstatus.append(0)
                #no file == UNIQUENESS
                return cmpstatus
            else:
                t2st = self.__tuple_to_string__(tup)
                ifany = 0
                for line in list_from_file:
                    if line.find(t2st) != -1:
                        cmpstatus.append(1)
                        ifany += 1
                    else:
                        cmpstatus.append(0)
                        continue
                if ifany > 0:
                    print(f"there are {ifany} occurences of {t2st} in {self.sname}")
                    cmpstatus.append(ifany)
                else:
                    cmpstatus.append(0)
        return sum(cmpstatus)
#############
    def get_value(self,attr_name,sname,/):
        """
        Find the value for attribute name
        :param attr_name: attribute name (string)
        :param fn: file name (string)
        :return: Value (string)
                 1 - otherwise
        """
        gavstatus = None
        val = None
        list_from_file = self.showAll(self.sname)
        if list_from_file == 1:
            #empty file - nothing to search for
            print("empty file")
            gavstatus = 1
            return gavstatus
        else:
            if isinstance(attr_name,str):
                for line in (list_from_file):
                    lspt = line.split(',')
                    for i in range(0,len(lspt)):
                        if lspt[i]  == attr_name:
                            val = lspt[i + 2]
                            gavstatus = 0
                            break
                        else:
                            continue
                if val is None:
                    print(f"Not found")
                    gavstatus = 1
                    return gavstatus
                else:
                    return val
            else:
                print(f"attr name provided: {attr_name} is not a string")
                gavstatus = 1
                return gavstatus
#############

