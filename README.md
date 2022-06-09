# Graph Connect 2022 Data Science Ecosystem Integration Demo

This demo leverages the [H&M Personalized Fashion Recommendations Dataset](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data) to show:
1. using the [Neo4j Data Warehouse (DWH) Connector](https://github.com/neo4j-contrib/neo4j-dwh-connector) on a spark cluster to load tens of millions of records from Snowflake into a Neo4j graph database
2. using unsupervised graph machine learning to enrich a knowledge graph with item similarity relationships that enable faster and more focused real-time personalized recommendation queries. Specifically, we use [FastRP node embeddings](https://neo4j.com/docs/graph-data-science/current/machine-learning/node-embeddings/fastrp/) with [K-Nearest-Neighbor (KNN)](https://neo4j.com/docs/graph-data-science/current/algorithms/knn/) to infer similar articles of clothing based on common customer interactions and product types. 

## Prerequisites:
 - Snowflake - https://www.snowflake.com/. A free trial will work.
 - Spark 3.x with Scala 2.12 or 2.13.  You will also need the following libraries installed on your spark cluster
   - `org.neo4j:neo4j-dwh-connector_<scala version>:1.0.0_for_spark_3`
   - `org.neo4j:neo4j-connector-apache-spark_<scala version>:4.1.2_for_spark_3`
 - Python>=3.6  and Jupyter Notebook
 - Neo4j >= 4.3 and GDS >= 2.0.
   - This demo was tested with GDS Enterprise Edition (EE) which offers higher concurrency settings in algorithm execution and thus improved performance.
   - As a quick start, [AuraDS](https://neo4j.com/cloud/platform/aura-graph-data-science/) is a fully managed service that includes both the Neo4j graph database and enterprise GDS. With AuraDS you can create an instance for this demo through a guided user interface in a few clicks.  
   - I recommend a Neo4j instance with >=64 GB Memory given that we are handling tens of millions of purchase transactions.
   
## Demo Directions
 - Load the [H&M Personalized Fashion Recommendations Dataset](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data) into Snowflake.
   - I found it easiest to upload the data into cloud storage first then copy to Snowflake using the `COPY INTO` command.  I have an example using GCP in `step1-load-data-into-snowflake.sql`.  This pattern is also possible for AWS S3 and Azure Blob storage.
   - Regardless of how you get the data into Snowflake, please take note of the field names used in `step1-load-data-into-snowflake.sql` and ensure you are aligned
 - Create the following Uniqueness constraints in your target Neo4j Database.
   - `CREATE CONSTRAINT article_id_unique IF NOT EXISTS ON (n:Article) ASSERT n.articleId IS UNIQUE`
   - `CREATE CONSTRAINT customer_id_unique IF NOT EXISTS ON (n:Customer) ASSERT n.customerId  IS UNIQUE`
   - `CREATE CONSTRAINT product_code_unique IF NOT EXISTS ON (n:Product) ASSERT n.productCode  IS UNIQUE`

 - Use The Neo4j Data Warehouse (DWH) Connector to load the data from Snowflake into Neo4j as shown in `step2-hm-graph-etl.py`.  This takes approximately 20-30 minutes and can likely be sped up with more tuning.
 - (Optionally) You can run the `step3-knn-similarity-evaluation.ipynb` to evaluate FastRP and KNN performance on historic purchases using Mean Average Precision (MAP). Current performance can be improved with further hyperparameter tuning. 
 - Run `step4-run-knn-similarity.ipynb` to estimate article similarities via FastRP and KNN across the entire graph for use in product recommendation queries.
 - Run `step5-real-time-inference.ipynb` to compare query performance and results of using the the KNN similarity inference for real-time recommendation. 

