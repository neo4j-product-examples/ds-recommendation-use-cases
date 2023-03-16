# Collaborative Filtering Example with News Content

In [Neo4j Graph Data Science (GDS)](https://neo4j.com/docs/graph-data-science/current/) we can leverage graph feature engineering and similarity algorithms to produce outcomes similar to Collaborative Filtering (CF) but at a much larger scale. This methodology in Neo4j and GDS overcomes traditional CF scale limitations related to sparse/missing data and large in-memory matrix computations. 


## This Example
Using Embeddings like Fast Random Projections (FastRP) and K-Nearest Neighbor (KNN) we can draw relationships between similar items based on user activity.  This is a highly scalable implementation of an _item-item memory-based_ recommender system.  The similarity relationships can drastically speed up the real-time query performance for recommenders in production while also improving the quality of personalized results.

While the dataset used is focused on news recommendation, the same methodology is highly transferable to retail, marketing, financial services, and other industry verticals. 

## Dataset
The source dataset is not being re-hosted due to licensing restrictions, but you can find directions for loading thew dataset into Neo4j [here](https://github.com/neo4j-product-examples/demo-news-recommendation/blob/main/mind-large-collab-filtering/prepare-and-load-data.ipynb)

If you are a Neo4j employee interested in internal experimentation please reach out to [zach.blumenfeld@neo4j.com](zach.blumenfeld@neo4j.com). 

## Usage
Once you have the data in Neo4j you can use `stage.ipynb` to stage the demo and `demo.ipynb` to run the demo.