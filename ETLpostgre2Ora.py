# -*- coding: utf-8 -*-

#connect parameters for ORACLE
#$user_ora$
#pass_ora$
#$host$
#$base_name$

#$NAME_PARTITION$ - name of partition for oracle tables

#connect parameters for Postgre
#$dbname$
#$user$
#$password$
#$host$

# 1. Oracle tables must be created Before running/ For example METASTORE_COLUMNS_V2_STG, with list partition. Partitioning a column by name "INSTANCE", in this case. 
# 2. Table columns in the source base (postgre) and destination base (ORACLE) must match.

import sys
import psycopg2
import cx_Oracle

sqlS = [
('SELECT "CD_ID","COMMENT" as "COLUMN_COMMENT","COLUMN_NAME","TYPE_NAME","INTEGER_IDX",:1 from public."COLUMNS_V2"','insert into METASTORE_COLUMNS_V2_STG(CD_ID,COLUMN_COMMENT,COLUMN_NAME,TYPE_NAME,INTEGER_IDX,INSTANCE) values (:1,:2,:3,:4,:5,:6)', 'METASTORE_COLUMNS_V2_STG'),
('SELECT "DB_ID","DESC" as "DB_DESC","DB_LOCATION_URI","NAME" as "DB_NAME","OWNER_NAME","OWNER_TYPE",:1 from public."DBS"','insert into METASTORE_DBS_STG(DB_ID,DB_DESC,DB_LOCATION_URI,DB_NAME,OWNER_NAME,OWNER_TYPE,INSTANCE) values (:1,:2,:3,:4,:5,:6,:7)', 'METASTORE_DBS_STG'),
('SELECT "TBL_ID","PKEY_COMMENT","PKEY_NAME","PKEY_TYPE","INTEGER_IDX",:1 from public."PARTITION_KEYS"','insert into METASTORE_PARTITION_KEYS_STG(TBL_ID,PKEY_COMMENT,PKEY_NAME,PKEY_TYPE,INTEGER_IDX,INSTANCE) values (:1,:2,:3,:4,:5,:6)', 'METASTORE_PARTITION_KEYS_STG'),
('SELECT "SD_ID","INPUT_FORMAT","IS_COMPRESSED","LOCATION" as "SDS_LOCATION","NUM_BUCKETS","OUTPUT_FORMAT","SERDE_ID","CD_ID","IS_STOREDASSUBDIRECTORIES",:1 from public."SDS"','insert into METASTORE_SDS_STG(SD_ID,INPUT_FORMAT,IS_COMPRESSED,SDS_LOCATION,NUM_BUCKETS,OUTPUT_FORMAT,SERDE_ID,CD_ID,IS_STOREDASSUBDIRECTORIES,INSTANCE) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)', 'METASTORE_SDS_STG'),
('SELECT "TBL_ID","PARAM_KEY","PARAM_VALUE",:1 from public."TABLE_PARAMS"','insert into METASTORE_TABLE_PARAMS_STG(TBL_ID,PARAM_KEY,PARAM_VALUE,INSTANCE) values (:1,:2,:3,:4)', 'METASTORE_TABLE_PARAMS_STG'),
('SELECT "TBL_ID","CREATE_TIME","DB_ID","LAST_ACCESS_TIME","OWNER","RETENTION" as "TBL_RETENTION","SD_ID","TBL_NAME","TBL_TYPE","VIEW_EXPANDED_TEXT","VIEW_ORIGINAL_TEXT",:1 from public."TBLS"','insert into METASTORE_TBLS_STG(TBL_ID,CREATE_TIME,DB_ID,LAST_ACCESS_TIME,OWNER,TBL_RETENTION,SD_ID,TBL_NAME,TBL_TYPE,VIEW_EXPANDED_TEXT,VIEW_ORIGINAL_TEXT,INSTANCE) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)', 'METASTORE_TBLS_STG')
]


conP = psycopg2.connect(dbname='$dbname$', user='$user$', password='$password$', host='$host$')
conP.set_client_encoding('UTF8')
cursorP = conP.cursor()

conOra = cx_Oracle.connect("$user_ora$/$pass_ora$@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=$host$)(PORT=$port$))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=$base_name$)))", encoding='UTF-8', nencoding='UTF-8')
cursorO = conOra.cursor()

nSize = 25000
sInstance = '$NAME_PARTITION$'
for sql,sql_ins, tab_name in sqlS:
    try:
        cursorO.execute(f'alter table {tab_name} truncate partition {sInstance}')
        sql = sql.replace(':1',"'"+sInstance+"' as INSTANCE")
        cursorP.execute(sql, sInstance)
        while True:
            buf_dict = cursorP.fetchmany(nSize)
            if len(buf_dict) == 0:
                break
            try:
                cursorO.executemany(sql_ins, buf_dict)
            except cx_Oracle.Error as e:
                print(e)
                print(sql_ins)
                raise
            buf_dict=[]
        conOra.commit()
    except psycopg2.Error as e:
        cursorP.close()
        print (e)
        print(sql)
        print(sInstance)
        raise


