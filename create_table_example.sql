-- In Postgree
CREATE TABLE public."COLUMNS_V2"
(
    "CD_ID" bigint NOT NULL,
    "COMMENT" character varying(4000) COLLATE pg_catalog."default",
    "COLUMN_NAME" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    "TYPE_NAME" text COLLATE pg_catalog."default",
    "INTEGER_IDX" integer NOT NULL,
    CONSTRAINT "COLUMNS_V2_pkey" PRIMARY KEY ("CD_ID", "COLUMN_NAME"),
    CONSTRAINT "COLUMNS_V2_CD_ID_fkey" FOREIGN KEY ("CD_ID")
        REFERENCES public."CDS" ("CD_ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE
        NOT VALID
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- In ORACLE
CREATE TABLE metastore_columns_v2_stg
    (cd_id                          NUMBER,
    column_comment                 VARCHAR2(4000 BYTE),
    column_name                    VARCHAR2(500 BYTE),
    type_name                      CLOB,
    integer_idx                    NUMBER,
    instance                       VARCHAR2(30 BYTE))
  TABLESPACE  users
  PARTITION BY LIST (INSTANCE)
  (PARTITION sklod VALUES ('$NAME_PARTITION$'));
