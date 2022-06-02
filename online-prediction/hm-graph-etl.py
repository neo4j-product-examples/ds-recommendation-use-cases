# Databricks notebook source
from neo4j_dwh_connector import *

# COMMAND ----------

# note to create indexes in Neo4j
# CREATE CONSTRAINT article_id_unique IF NOT EXISTS ON (n:Article) ASSERT n.articleId IS UNIQUE
# CREATE CONSTRAINT customer_id_unique IF NOT EXISTS ON (n:Customer) ASSERT n.customerId  IS UNIQUE


# COMMAND ----------

default_source_options={
  "sfURL": dbutils.secrets.get(scope = "zachtesting", key = "sfURL"),
  "sfUser": dbutils.secrets.get(scope = "zachtesting", key = "sfUsername"),
  "sfPassword": dbutils.secrets.get(scope = "zachtesting", key = "sfPassword"),
  "sfDatabase": "HM",
  "sfSchema": "ML_DATA"
}

default_target_options={
  "url": dbutils.secrets.get(scope = "zachtesting", key = "auraURLdbml3"),
  "authentication.basic.username": "neo4j",
  "authentication.basic.password": dbutils.secrets.get(scope = "zachtesting", key = "auraPassworddbml3"),
}

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Customer Properties

# COMMAND ----------

customer_properties_source = Source(
    format="snowflake",
    options={**default_source_options, **{"dbtable":"CUSTOMERS"}},
    columns=[
        Column(name="CUSTOMER_ID", alias="customerId"),
        Column(name="FN", alias="fn"),
        Column(name="ACTIVE", alias="active"),
        Column(name="CLUB_MEMBER_STATUS", alias="clubMemberStatus"),
        Column(name="FASHION_NEWS_FREQUENCY", alias="fasionNewsFrequency"),
        Column(name="CAST(AGE AS LONG)", alias="age"),
        Column(name="POSTAL_CODE", alias="postalCode")
    ],
    printSchema=True
)

customer_properties_target =  Target(
    format="org.neo4j.spark.DataSource", 
    options={**default_target_options, **{"labels": "Customer", "node.keys": "customerId"}},
    mode="Overwrite"
)

# COMMAND ----------

customer_connector = Neo4jDWHConnector(spark, JobConfig(name="load-hm-customer-properties", conf={}, hadoopConfiguration={}, source=customer_properties_source, target=customer_properties_target))
# this will ingest the data from source to target database
customer_connector.run()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Article Properties

# COMMAND ----------

article_properties_source = Source(
    format="snowflake",
    options={**default_source_options, **{"dbtable":"ARTICLES"}},
    columns=[
      Column("ARTICLE_ID", alias="articleId"),
      Column("PRODUCT_CODE", alias="productCode"),
      Column("PROD_NAME", alias="productName"),
      Column("PRODUCT_TYPE_NO", alias="productTypeNo"),
      Column("PRODUCT_TYPE_NAME", alias="productTypeName"),
      Column("PRODUCT_GROUP_NAME", alias="productGroupName"),
      Column("GRAPHICAL_APPEARANCE_NO", alias="graphicalAppearanceNo"),
      Column("GRAPHICAL_APPEARANCE_NAME", alias="graphicalAppearanceName"),
      Column("COLOUR_GROUP_CODE", alias="colorGroupCode"),
      Column("COLOUR_GROUP_NAME", alias="colorGroupName"),
      Column("PERCEIVED_COLOUR_VALUE_ID", alias="percievedColorValueId"),
      Column("PERCEIVED_COLOUR_VALUE_NAM", alias="percievedColorValueName"),
      Column("PERCEIVED_COLOUR_MASTER_ID", alias="percievedColorMasterId"),
      Column("PERCEIVED_COLOUR_MASTER_NAME", alias="percievedColorMasterName"),
      Column("DEPARTMENT_NO", alias="departmentNo"),
      Column("DEPARTMENT_NAME", alias="departmentName"),
      Column("INDEX_CODE", alias="indexCode"),
      Column("INDEX_NAME", alias="indexName"),
      Column("INDEX_GROUP_NO", alias="indexGroupNo"),
      Column("INDEX_GROUP_NAME", alias="indexGroupName"),
      Column("SECTION_NO", alias="sectionNo"),
      Column("SECTION_NAME", alias="sectionName"),
      Column("GARMENT_GROUP_NO", alias="garmentGroupNo"),
      Column("GARMENT_GROUP_NAME", alias="garmentGroupName"),
      Column("DETAIL_DESC", alias="detailDesc")
    ],
    printSchema=True
)

article_properties_target =  Target(
    format="org.neo4j.spark.DataSource", 
    options={**default_target_options, **{"labels": "Article", "node.keys": "articleId"}},
    mode="Overwrite"
)

# COMMAND ----------

article_connector = Neo4jDWHConnector(spark, JobConfig(name="load-hm-article-properties", conf={}, hadoopConfiguration={}, source=article_properties_source, target=article_properties_target))
# this will ingest the data from source to target database
article_connector.run()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Purchase Transactions

# COMMAND ----------

transaction_source = Source(
    format="snowflake",
    options={**default_source_options, **{"dbtable":"TRANSACTIONS"}},
    columns=[
      Column("TRANSACTION_ID", alias="transactionId"),
      Column("CUSTOMER_ID", alias="customerId"),
      Column("ARTICLE_ID", alias="articleId"),
      Column("T_DAT", alias="transactionDate"),
      Column("PRICE", alias="price"),
      Column("SALES_CHANNEL_ID", alias="salesChannelId")
    ],
    printSchema=True, 
    partition=Partition(
        number=-1,
        by=""
    )
)

transaction_target =  Target(
    format="org.neo4j.spark.DataSource", 
    options={**default_target_options, **{
      "query" : '''
        MATCH(c:Customer {customerId: event.customerId})
        MATCH(a:Article {articleId: event.articleId})
        CREATE(c)-[r:PURCHASED {transactionId: event.transactionId, transactionDate: event.transactionDate, price: event.price}]->(a)
        '''
    }},
    mode="Append"
)

# COMMAND ----------

config = JobConfig(name="load-hm-transactions",conf={}, hadoopConfiguration={},source=transaction_source, target=transaction_target)
transaction_connector = Neo4jDWHConnector(spark, config)
# this will ingest the data from source to target database
transaction_connector.run()

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

