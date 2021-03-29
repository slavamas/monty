# monty
Monty is python module. It provides mechanism for persistent data storage saving data either in plain text file or in sqlite DB.
####
below are test files for montydb and montyfile modules:  
testing db module:  
testmontydb.py  
#####  
from montydb import  Montydb as monty 

dbname = 'attributes'  
mdb = monty(dbname)  
print(f"mdb: {mdb}")  
print(f"mdb.sname: {mdb.sname}")  
tupl1 = ('s','attr1', 'i', '-23')  
print(f"showAll (empty db): {mdb.showAll(dbname)}")  
print(f"adding attr1: {mdb.add(tupl1,dbname)}")  
print(f"get attr1 val: {mdb.get_value('attr1',dbname)}")  
print(f"attemting to update value of wrong type:  {mdb.update(tupl1,'13.7',dbname)}")  
print(f"showAll: {mdb.showAll(dbname)}")  
print(f"get attr1 val: {mdb.get_value('attr1',dbname)}")  
print(f"now updating correctly: {mdb.update(tupl1,'55',dbname)}")  
print(f"attr1 val:? {mdb.get_value('attr1',dbname)}")  

#####how about to repeate it?  
print(f"add already recorded tupl1?: {mdb.add(tupl1,dbname)}")   
tupl2 = ('s','attr2','f','33.77')  
print(f"adding attr2: {mdb.add(tupl2,dbname)}")  
print(f"showAll: {mdb.showAll(dbname)}")  
print(f"get attr2: {mdb.get_value('attr2',dbname)}")  
tupl3 = ('s','attr3','s','attr_val3')  
print(f"adding attr3: {mdb.add(tupl3,dbname)}")  
print(f"showAll: {mdb.showAll(dbname)}")  
print(f"get attr3: {mdb.get_value('attr3',dbname)}")  
tupl4 = ('s','attr4','s','https://whatever.io')  
print(f"adding attr4: {mdb.add(tupl4,dbname)}")  
print(f"get attr4: {mdb.get_value('attr4',dbname)}")  
print(f"removing attr3: {mdb.remove(tupl3,dbname)}")  
print(f"showAll: {mdb.showAll(dbname)}")  
print(f"all_attributes: {mdb.showAll(dbname)}")  
tupl5 = ('s','attr5','f','345.567')  
print(f"removing non existing attribute: {mdb.remove(tupl5,dbname)}")  
#####  
running testmontydb.py:

python testmontydb.py   
mdb: <montydb.Montydb object at 0x10116f9a0>  
mdb.sname: attributes  
Database is empty  
showAll (empty db): -1  
Record: ('s', 'attr1', 'i', '-23') has been added  
adding attr1: 1  
get attr1 val: -23  
Provided parameter: -23 claimed to be an integer, but it is not  
attemting to update value of wrong type:  -1  
showAll: [(1, 's', 'attr1', 'i', '-23')]  
get attr1 val: -23  
Provided parameter: -23 claimed to be an integer, but it is not  
now updating correctly: -1  
attr1 val:? -23  
record: ('s', 'attr1', 'i', '-23') already exists  
add already recorded tupl1?: -1  
Record: ('s', 'attr2', 'f', '33.77') has been added  
adding attr2: 1  
showAll: [(1, 's', 'attr1', 'i', '-23'), (2, 's', 'attr2', 'f', '33.77')]  
get attr2: 33.77  
Record: ('s', 'attr3', 's', 'attr_val3') has been added  
adding attr3: 1  
showAll: [(1, 's', 'attr1', 'i', '-23'), (2, 's', 'attr2', 'f', '33.77'), (3, 's', 'attr3', 's', 'attr_val3')]  
get attr3: attr_val3  
Record: ('s', 'attr4', 's', 'https://whatever.io') has been added  
adding attr4: 1  
get attr4: https://whatever.io  
No such record: ('s', 'attr3', 's', 'attr_val3') in the database: attributes  
removing attr3: -1  
showAll: [(1, 's', 'attr1', 'i', '-23'), (2, 's', 'attr2', 'f', '33.77'), (3, 's', 'attr3', 's', 'attr_val3'), (4, 's', 'attr4', 's', 'https://whatever.io')]  
all_attributes: [(1, 's', 'attr1', 'i', '-23'), (2, 's', 'attr2', 'f', '33.77'), (3, 's', 'attr3', 's', 'attr_val3'), (4, 's', 'attr4', 's', 'https://whatever.io')]  
No such record: ('s', 'attr5', 'f', '345.567') in the database: attributes  
removing non existing attribute: -1  
  
###############  
sqlite3 attributes  
SQLite version 3.34.1 2021-01-20 14:10:07  
Enter ".help" for usage hints.  
sqlite> .header on  
sqlite> .mode column  
sqlite> select * from attributes;  
id | attr_type | attr_name | attr_value_type | attr_value|       
---|-----------|-----------|-----------------|-----------|  
1  | s         | attr1     | i               |  -23                 
2  | s         | attr2     | f               | 33.77                
3  | s         | attr3     | s               | attr_val3          
4  | s         | attr4     | s               | https://whatever.io  

sqlite> .quit  
  
#############   
testing file module:  
testmontyfile.py  
#####  
from montyfile import  Montyfile as monty  
  
fi = 'attributes'  
emptytupl=()  
tupl1 = ('s','attr1', 'i', '-23')  
mf = monty(fi)  
print(f"mf: {mf}")  
print(f"mf.sname: {mf.sname}")  
print(f"get all: {mf.showAll(fi)}")  
print(f"adding attr1: {mf.add(tupl1,fi)}")  
print(f"get all2: {mf.showAll(fi)}")  
print(f"get attr1 value: {mf.get_value('attr1',fi)}")  
tupl2 = ('s','attr2', 'f','3.478',)  
print(f"adding attr2: {mf.add(tupl2,fi)}")  
print(f"get all3: {mf.showAll(fi)}")  
print(f"update attr1: {mf.update(tupl1,'97',fi)}")  
tupl3=('s','attr3','s','https://whatever.io')  
print(f"adding attr3: {mf.add(tupl3,fi)}")  
print(f"get all4: {mf.showAll(fi)}")  
print(f"removing attr1: {mf.remove(tupl1,fi)}")  
print(f"get all5: {mf.showAll(fi)}")  
  
#############  
python testmontyfile.py  
mf: <montyfile.Montyfile object at 0x106c40b80>  
mf.sname: attributes  
get all: 1  
Provided parameter: -23 claimed to be an integer, but it is not  
adding attr1: [1]  
get all2: 1  
empty file  
get attr1 value: 1  
adding attr2: 0  
get all3: ['s,attr2,f,3.478,\n']  
Provided parameter: -23 claimed to be an integer, but it is not  
update attr1: [1]  
adding attr3: 0  
get all4: ['s,attr2,f,3.478,\n', 's,attr3,s,https://whatever.io,\n']  
Provided parameter: -23 claimed to be an integer, but it is not  
removing attr1: [1]  
get all5: ['s,attr2,f,3.478,\n', 's,attr3,s,https://whatever.io,\n']  
############  
  
cat attributes   
s,attr2,f,3.478,  
s,attr3,s,https://whatever.io,  


