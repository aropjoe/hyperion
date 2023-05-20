# Data import
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# from matplotlib.chord import Chord
from nxviz import circos as CircosPlot
from wordcloud import WordCloud
import base64
from io import BytesIO
import nltk
from nltk import ngrams


def read_text_data(file_path):
    with open(file_path, "r") as file:
        reviews = file.readlines()

    return reviews


def generate_bigram_wordcloud_images(reviews_negative, reviews_positive):
    # Generate a word cloud - negative sentiment
    wordcloud_neg = WordCloud(
        collocation_threshold=2,
        collocations=True,
        background_color="white",
        colormap="afmhot",
    ).generate(reviews_negative)

    # Generate a word cloud - positive sentiment
    wordcloud_pos = WordCloud(
        collocation_threshold=2,
        collocations=True,
        background_color="white",
        colormap="Set1",
    ).generate(reviews_positive)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18.5, 10.5, forward=True)
    ax1.imshow(wordcloud_neg, interpolation="bilinear")
    ax2.imshow(wordcloud_pos, interpolation="bilinear")
    ax1.title.set_text("Negative sentiment")
    ax2.title.set_text("Positive sentiment")
    ax1.axes.xaxis.set_visible(False)
    ax1.axes.yaxis.set_visible(False)
    ax2.axes.xaxis.set_visible(False)
    ax2.axes.yaxis.set_visible(False)

    # Save the figure to a byte buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=500, bbox_inches="tight")
    buffer.seek(0)

    # Encode the byte buffer as a base64 string
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # Close the figure to free up resources
    plt.close(fig)

    return image_base64


# Wordcloud - trigrams
def generate_wordcloud_images(pos_text, neg_text):
    neg_trigrams = ngrams(neg_text.split(), 3)
    neg_freq_dist = nltk.FreqDist(neg_trigrams)
    trigrams_neg_dict = {" ".join(tri): freq for tri, freq in neg_freq_dist.items()}

    pos_trigrams = ngrams(pos_text.split(), 3)
    pos_freq_dist = nltk.FreqDist(pos_trigrams)
    trigrams_pos_dict = {" ".join(tri): freq for tri, freq in pos_freq_dist.items()}

    trigrams_neg = pd.read_excel("core/datafile/trigrams_neg.xlsx")
    trigrams_pos = pd.read_excel("core/datafile/trigrams_pos.xlsx")

    trigrams_neg_dict = trigrams_neg.set_index("word")["frequency"].to_dict()
    trigrams_pos_dict = trigrams_pos.set_index("word")["frequency"].to_dict()

    # Generate a word cloud - negative sentiment
    wordcloud_trigrams_neg = WordCloud(
        background_color="white", colormap="twilight_shifted"
    ).generate_from_frequencies(trigrams_neg_dict)

    # Generate a word cloud - positive sentiment
    wordcloud_trigrams_pos = WordCloud(
        background_color="white", colormap="hsv"
    ).generate_from_frequencies(trigrams_pos_dict)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18.5, 10.5, forward=True)
    ax1.imshow(wordcloud_trigrams_neg, interpolation="bilinear")
    ax2.imshow(wordcloud_trigrams_pos, interpolation="bilinear")
    ax1.title.set_text("Negative sentiment")
    ax2.title.set_text("Positive sentiment")
    ax1.axes.xaxis.set_visible(False)
    ax1.axes.yaxis.set_visible(False)
    ax2.axes.xaxis.set_visible(False)
    ax2.axes.yaxis.set_visible(False)

    # Save the figure to a byte buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=500, bbox_inches="tight")
    buffer.seek(0)

    # Encode the byte buffer as a base64 string
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # Close the figure to free up resources
    plt.close(fig)

    return image_base64


def generate_network_image():
    data = pd.read_csv("core/datafile/co_occurence.csv")
    G = nx.from_pandas_edgelist(data, "node1", "node2")

    fig = plt.figure(figsize=(8, 6))
    nx.draw_shell(G, with_labels=True)

    # Save the figure to a byte buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=600, bbox_inches="tight")
    buffer.seek(0)

    # Encode the byte buffer as a base64 string
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # Close the figure to free up resources
    plt.close(fig)

    return image_base64


# calculate the degree of nodes, formalize edges
# Prepare a chord graph
def generate_chord_graph_image():
    data = pd.read_csv("core/datafile/co_occurence.csv")
    G = nx.from_pandas_edgelist(data, "node1", "node2")
    for v in G:
        G.nodes[v]["class"] = G.degree(v)
    weights = list(data["co_occurence"])

    c = CircosPlot(
        G,
        # figsize=(10, 10),
        # node_labels=True,
        # edge_width=weights,
        # node_grouping="class",
        # node_color="class",
    )
    c.draw()

    # Save the figure to a byte buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=600, bbox_inches="tight")
    buffer.seek(0)

    # Encode the byte buffer as a base64 string
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # Close the figure to free up resources
    plt.close()

    return image_base64
