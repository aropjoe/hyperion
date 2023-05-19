from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans

# Sample data with text and numerical features
data = [
    ["I love eating apples", 30, 5000],
    ["I prefer oranges over apples", 25, 3500],
    ["Bananas are delicious", 35, 8000],
    ["Oranges are juicy", 40, 6000],
    ["I enjoy eating fruits", 28, 4500],
]

# Separate the text and numerical features
text_data = [row[0] for row in data]
numerical_data = [[row[1], row[2]] for row in data]

# Preprocess the text data using TF-IDF
text_transformer = TfidfVectorizer()
text_features = text_transformer.fit_transform(text_data)

# Preprocess the numerical data using standardization
numerical_transformer = StandardScaler()
numerical_features = numerical_transformer.fit_transform(numerical_data)

# Combine the text and numerical features
combined_features = np.concatenate(
    (text_features.toarray(), numerical_features), axis=1
)

# Apply K-means clustering
num_clusters = 2
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(combined_features)

# Get the cluster labels
cluster_labels = kmeans.labels_

# Print the cluster labels for each data point
for i, label in enumerate(cluster_labels):
    print(f"Data point {i+1}: Cluster {label+1}")
