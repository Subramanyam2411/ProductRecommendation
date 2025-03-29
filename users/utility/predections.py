from django.conf import settings
import pandas as pd
import numpy as np

path = settings.MEDIA_ROOT + "//" + 'amazon products.csv'

dataset = pd.read_csv(path)
#Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer

#Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

#Replace NaN with an empty string
dataset["Category"] = dataset["Category"].fillna("")

#Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(dataset["Category"])

#Output the shape of tfidf_matrix
tfidf_matrix.shape
# We can look at some of the features.
feature_names = tfidf.get_feature_names_out()

# Import linear_kernel, cosine_similarity, and sigmoid_kernel
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import sigmoid_kernel
linear = linear_kernel(tfidf_matrix, tfidf_matrix)
def ml_scores():
    # Create the matrix
    linear = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    sig_score = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
    print(linear.shape)
    print(cosine_sim.shape)
    print(sig_score.shape)
    print(linear[1])
    print(cosine_sim[1])
    print(sig_score[1])
    return linear[1],cosine_sim[1], sig_score[1]

#Construct a reverse map of indices and product names
indices = pd.Series(dataset.index, index=dataset["Product Name"])
# Function that takes in product name as input and outputs most similar product
def rec_lin(product_name, linear=linear):
    # Get the index of the product that matches the product name
    idx = indices[product_name]

    # Get the pairwise similarity scores
    # Enumerate adds a counter to the iterable and lets it be converted into a list of tuples
    sim_scores = list(enumerate(linear[idx]))

    # Sort the products based on the similarity scores
    # Reverse gives us the similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar products
    sim_scores = sim_scores[1:11]

    # Get the product indices
    product_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar products
    # iloc allows us to retrieve rows from a data frame
    return dataset[["Product Name", "Selling Price"]].iloc[product_indices]