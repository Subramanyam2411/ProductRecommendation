from django.conf import settings
import pandas as pd
import numpy as np

path = settings.MEDIA_ROOT + "//" + 'amazon products.csv'

dataset = pd.read_csv(path)
# Dropping redundant columns
cols = [0, 2, 3, 5, 6, 8, 9, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
dataset.drop(dataset.columns[cols], axis=1, inplace=True)
# dropping null values to avoid errors
dataset.dropna(inplace=True)
# dataset.info()
# new data frame with split value columns. We use n = 3 to get a maximum of 3+1 columns
new = dataset["Category"].str.split("|", n=3, expand=True)

# making the first category called Main Category
dataset["Main Category"] = new[0]

# making the second category called sub_category
dataset["Sub-Category"] = new[1]

# making the third category called side_category
dataset["Side Category"] = new[2]

# making the last column consist of the remaining categories
dataset["Other Categories"] = new[3]

# Dropping old category columns and the remaining categories
dataset.drop(columns=["Category", "Other Categories"], inplace=True)


def pre_proccessed_data():
    df = dataset.head(100)
    return df.to_html


dataset.rename(
    columns={'Uniq Id': 'Id', 'Shipping Weight': 'Shipping Weight(Pounds)', 'Selling Price': 'Selling Price($)'},
    inplace=True)

dataset['Shipping Weight(Pounds)'] = dataset['Shipping Weight(Pounds)'].str.strip('ounces')
dataset['Shipping Weight(Pounds)'] = dataset['Shipping Weight(Pounds)'].str.strip('pounds').astype(float)
dataset['Selling Price($)'] = dataset['Selling Price($)'].str.replace('$', '').astype(float)

dataset.head()

# Start of EDA
import seaborn as sns
import matplotlib.pyplot as plt

# finding out the unique main categories
dataset["Main Category"].unique()
# data visualisation

# lets look at patterns in terms of Product Category popularity
# generate count for "Main Category"

# #Top 10 barplot of categories
# order = dataset['Main Category'].value_counts()[:10].index
# sns.countplot(y='Main Category', data=dataset, order=order)
# plt.title("Product count by category")
# plt.xlabel("Main category")
# plt.ylabel("Count of products")
# plt.show()

# generate boxplot to understand the distribution
toys = dataset[dataset["Main Category"] == 'Toys & Games ']
sns.boxplot(data=toys, x='Main Category', y='Selling Price($)', showfliers=False)
plt.title("Distribution of the Prices in Toys & Games Category")
# generate scatterplot to understand the relationship
sns.scatterplot(data=toys, x="Selling Price($)", y="Shipping Weight(Pounds)")
plt.title("Relationship between Price & Shipping Weight in Toys & Games category")

# generate boxplot to understand the distribution
home = dataset[dataset["Main Category"] == 'Home & Kitchen ']
sns.boxplot(data=home, x='Main Category', y='Selling Price($)', showfliers=False)
plt.title("Distribution of the Prices in Home & Kitchen Category")
# generate scatterplot to understand the relationship
sns.scatterplot(data=home, x="Selling Price($)", y="Shipping Weight(Pounds)")
plt.title("Relationship between Price & Shipping Weight in Home & Kitchen Category")

# generate boxplot to understand the distribution
sports = dataset[dataset["Main Category"] == 'Sports & Outdoors ']
sns.boxplot(data=sports, x='Main Category', y='Selling Price($)', showfliers=False)
plt.show()
plt.title("Distribution of the Prices in Sports & Outdoors Category")
# generate scatterplot to understand the relationship
sns.scatterplot(data=sports, x="Selling Price($)", y="Shipping Weight(Pounds)")
plt.show()
plt.title("Relationship between Price & Shipping Weight in Sports & Outdoors Category")
# generate boxplot to understand the distribution
csj = dataset[dataset["Main Category"] == 'Clothing, Shoes & Jewelry ']
sns.boxplot(data=csj, x='Main Category', y='Selling Price($)', showfliers=False)
plt.title("Distribution of the Prices in Clothing, Shoes & Jewelry Category")
# generate scatterplot to understand the relationship
sns.scatterplot(data=csj, x="Selling Price($)", y="Shipping Weight(Pounds)")
plt.title("Relationship between Price & Shipping Weight in Clothing, Shoes & Jewelry Category")
plt.show()
# generate boxplot to understand the distribution
artscraft = dataset[dataset["Main Category"] == 'Arts, Crafts & Sewing ']
sns.boxplot(data=artscraft, x='Main Category', y='Selling Price($)', showfliers=False)
plt.title("Distribution of the Prices in Arts, Crafts & Sewing Category")
plt.show()
# generate scatterplot to understand the relationship
sns.scatterplot(data=artscraft, x="Selling Price($)", y="Shipping Weight(Pounds)")
plt.title("Relationship between Price & Shipping Weight in Arts, Crafts & Sewing Category")

plt.show()
