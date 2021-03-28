# monty
Persistent data storage. Stores data either in plain text file or in sqlite DB.

from montydb import  Montydb as monty 

dbname = 'attributes'
mdb = monty(dbname)
print(f"mdb: {mdb}")
print(f"mdb.sname: {mdb.sname}")
tupl1 = ('s','attr1', 'i', '-23')
print(f"showAll (empty db): {mdb.showAll(dbname)}")
print(f"adding attr1: {mdb.add(tupl1,dbname)}")
print(f"get attr1 val: {mdb.get_value('attr1',dbname)}")
#ures = mdb.update(tupl1,'13.7',dbname)
print(f"showAll: {mdb.showAll(dbname)}")
print(f"get attr1 val: {mdb.get_value('attr1',dbname)}")
print(f"attr1 val:? {mdb.get_value('attr1',dbname)}")

#####how about to repeate it?
print(f"add already recorded tupl1?: {mdb.add(tupl1,dbname)}") #will generate sqlite3.IntegrityError:
tupl2 = ('s','attr2','i','55')
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
###########

sqlite3 attributes 
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.
sqlite> .header on
sqlite> .mode column
sqlite> select * from attributes;
id  attr_type  attr_name  attr_value_type  attr_value         
--  ---------  ---------  ---------------  -------------------
1   s          attr1      i                -23                
2   s          attr2      i                55                 
3   s          attr3      s                attr_val3          
4   s          attr4      s                https://whatever.io

#############

from montyfile import Montyfile as monty

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
print("-----------")
print(f"removing attr1: {mf.remove(tupl1,fi)}")
print(f"get all5: {mf.showAll(fi)}")

#########
cat attributes 

s,attr2,f,3.478,
s,attr1,i,97,
s,attr3,s,https://whatever.io,

