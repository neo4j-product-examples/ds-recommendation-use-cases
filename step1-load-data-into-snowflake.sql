-- create storage integration so you can copy data in to tables
CREATE STORAGE INTEGRATION hmStorageIntegration
    type = external_stage
    storage_provider = gcs
    enabled = true
    storage_allowed_locations = ('gcs://<GCP storage bucket name>');

-- create database and schema
CREATE DATABASE HM;
CREATE SCHEMA HM.ML_DATA;

-- create and load article data
CREATE OR REPLACE TABLE HM.ML_DATA.ARTICLES (
	ARTICLE_ID STRING NOT NULL,
	PRODUCT_CODE STRING,
	PROD_NAME STRING,
	PRODUCT_TYPE_NO STRING,
	PRODUCT_TYPE_NAME STRING,
	PRODUCT_GROUP_NAME STRING,
	GRAPHICAL_APPEARANCE_NO STRING,
	GRAPHICAL_APPEARANCE_NAME STRING,
	COLOUR_GROUP_CODE STRING,
	COLOUR_GROUP_NAME STRING,
	PERCEIVED_COLOUR_VALUE_ID STRING,
	PERCEIVED_COLOUR_VALUE_NAM STRING,
	PERCEIVED_COLOUR_MASTER_ID STRING,
	PERCEIVED_COLOUR_MASTER_NAME STRING,
	DEPARTMENT_NO STRING,
	DEPARTMENT_NAME STRING,
	INDEX_CODE STRING,
	INDEX_NAME STRING,
	INDEX_GROUP_NO STRING,
	INDEX_GROUP_NAME STRING,
	SECTION_NO STRING,
	SECTION_NAME STRING,
	GARMENT_GROUP_NO STRING,
	GARMENT_GROUP_NAME STRING,
	DETAIL_DESC STRING
);
COPY INTO HM.ML_DATA.ARTICLES
    FROM 'gcs://<GCP storage bucket name>/articles.csv'
    FILE_FORMAT = (TYPE=CSV, SKIP_HEADER=1, FIELD_OPTIONALLY_ENCLOSED_BY='"')
    storage_integration = hmStorageIntegration;

-- create and load customer data
CREATE OR REPLACE TABLE HM.ML_DATA.CUSTOMERS (
    CUSTOMER_ID STRING NOT NULL,
    FN FLOAT,
    ACTIVE FLOAT,
    CLUB_MEMBER_STATUS STRING,
    FASHION_NEWS_FREQUENCY STRING,
    AGE NUMBER,
    POSTAL_CODE STRING
);
COPY INTO HM.ML_DATA.CUSTOMERS
    FROM 'gcs://<GCP storage bucket name>/transactions_train.csv'
    FILE_FORMAT = (TYPE=CSV, SKIP_HEADER=1, FIELD_OPTIONALLY_ENCLOSED_BY='"')
    storage_integration = hmStorageIntegration;

-- create and load transactions
CREATE OR REPLACE TABLE HM.ML_DATA.TRANSACTIONS(
    T_DAT DATE NOT NULL,
    CUSTOMER_ID STRING NOT NULL,
    ARTICLE_ID STRING NOT NULL,
    PRICE FLOAT NOT NULL,
    SALES_CHANNEL_ID STRING NOT NULL
);
COPY INTO HM.ML_DATA.TRANSACTIONS
    FROM 'gcs://<GCP storage bucket name>/transactions_train.csv'
    FILE_FORMAT = (TYPE=CSV, SKIP_HEADER=1, FIELD_OPTIONALLY_ENCLOSED_BY='"')
    storage_integration = hmStorageIntegration;

/*
Generate unique purchase transaction ids.
In this case every transaction in the source data is implied to be unique for machine learning purposes. However, in most real-world scenarios we will want a unique id for each transaction so they can be tracked and modeled in the database appropriately.  The below command simply assigns random unique ids to each transaction.
 */
ALTER TABLE HM.ML_DATA.TRANSACTIONS
    ADD TRANSACTION_ID VARCHAR(36) AS uuid_string();