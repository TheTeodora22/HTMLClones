import os
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from scipy.sparse import hstack
import matplotlib.pyplot as plt


def visualize_similarity(similarity_matrix, filenames, threshold=0.5):
    plt.figure(figsize=(10, 8))
    
    # Create heatmap
    im = plt.imshow(similarity_matrix, cmap='viridis', 
                    origin='upper', aspect='auto')
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Similarity Score')

    # Add cluster separation lines
    n = similarity_matrix.shape[0]
    for i in range(n-1):
        if similarity_matrix[i,i+1] < threshold:
            plt.axvline(x=i+0.5, color='red', linestyle='--', linewidth=0.8)
            plt.axhline(y=i+0.5, color='red', linestyle='--', linewidth=0.8)

    # Configure plot
    plt.title("Document Similarity Matrix\n(Red lines = Cluster Boundaries)")
    plt.xlabel("Document Index")
    plt.ylabel("Document Index")
    plt.xticks(np.arange(len(filenames)), fontsize=4, rotation=90)
    plt.yticks(np.arange(len(filenames)), filenames, fontsize=4)
    
    plt.tight_layout()
    plt.show()

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract CSS from <style> tags before removal
    css_contents = []
    for style_tag in soup.find_all('style'):
        css = style_tag.get_text()
        css = ' '.join(css.split()).lower()
        css_contents.append(css)
        style_tag.decompose()  
    
    # Remove scripts
    for script in soup.find_all('script'):
        script.decompose()
    
    # Extract visible text
    text = soup.get_text()
    text = ' '.join(text.split()).lower()
    
    # Extract tag structure with classes/IDs
    body = soup.find('body')
    tags = []
    if body:
        for tag in body.find_all():
            tag_info = tag.name
            if tag.get('class'):
                tag_info += '.' + '.'.join(tag['class'])
            if tag.get('id'):
                tag_info += '#' + tag['id']
            tags.append(tag_info)
    tag_str = ' '.join(tags)
    
    # Extract inline styles
    inline_styles = [
        tag['style'].replace(' ', '').lower()
        for tag in soup.find_all(style=True)
        if tag.has_attr('style')
    ]
    css_str = ' '.join(css_contents + inline_styles)
    
    return text, tag_str, css_str

def compute_similarities(texts, tags, css, weights=(0.4, 0.3, 0.3)):
    # Vectorize each feature with dtype=np.float32
    text_vec = TfidfVectorizer(stop_words="english", dtype=np.float32).fit_transform(texts) * weights[0]
    tag_vec = TfidfVectorizer(ngram_range=(2, 2), dtype=np.float32).fit_transform(tags) * weights[1]
    css_vec = TfidfVectorizer(dtype=np.float32).fit_transform(css) * weights[2]
    
    # Combine features horizontally (sparse matrices)
    combined_features = hstack([text_vec, tag_vec, css_vec])
    
    # Single similarity calculation
    return cosine_similarity(combined_features)

def process_directory(directory):
    files = sorted([os.path.join(directory, f) 
                    for f in os.listdir(directory) if f.endswith('.html')])
    texts = []
    tag_seqs = []
    css_seqs = []  
    filenames = []
    
    for file_path in files:
        text, tag_str, css_str = parse_html(file_path)
        texts.append(text)
        tag_seqs.append(tag_str)
        css_seqs.append(css_str)
        filenames.append(os.path.basename(file_path))
        
    return filenames, texts, tag_seqs, css_seqs

def cluster_files(similarity_matrix, threshold=0.5):
    # Convert similarity to distance
    distance_matrix = 1 - similarity_matrix
    clustering = AgglomerativeClustering(
        n_clusters=None,
        metric='precomputed',
        linkage='average',
        distance_threshold=1 - threshold
    )
    clusters = clustering.fit_predict(distance_matrix)
    return clusters

def group_files(filenames, clusters):
    groups = {}
    for filename, cluster_id in zip(filenames, clusters):
        if cluster_id not in groups:
            groups[cluster_id] = []
        groups[cluster_id].append(filename)
    # Sort groups by cluster id and filenames
    sorted_groups = sorted(groups.values(), key=lambda x: (len(x), x))
    return sorted_groups

def clean_transformed_files(directory):
    for f in os.listdir(directory):
        if f.startswith('transformed_') and f.endswith('.html'):
            os.remove(os.path.join(directory, f))

def main(directory, weights=(0.4, 0.3, 0.3), threshold=0.5):
    # Clean up any existing transformed files first
    clean_transformed_files(directory)
    
    filenames, texts, tag_seqs, css_seqs = process_directory(directory)
    if not filenames:
        return []
    
    combined_sim = compute_similarities(texts, tag_seqs, css_seqs, weights)
    
    visualize_similarity(combined_sim, filenames, threshold)

    clusters = cluster_files(combined_sim, threshold)
    grouped = group_files(filenames, clusters)
    return grouped

def process_subdirectories(root_directory, output_filename='groups_all.txt'):
    with open(output_filename, 'w') as out_file:
        # Iterate over each item in the root_directory
        for folder in sorted(os.listdir(root_directory)):
            folder_path = os.path.join(root_directory, folder)
            if os.path.isdir(folder_path):
                # Clean up before processing
                clean_transformed_files(folder_path)
                
                groups = main(folder_path)
                out_file.write(f"Folder: {folder}\n")
                if groups:
                    for group in groups:
                        out_file.write("[" + ", ".join(group) + "]\n")
                else:
                    out_file.write("No HTML files found or no groups.\n")
                out_file.write("\n")
                print(f"Processed folder: {folder}")

# Example usage
if __name__ == "__main__":
    # Set the root directory that contains multiple folders with HTML files
    root_directory = r"D:\Projects\HTMLClones\clones"  # Replace with your actual directory
    process_subdirectories(root_directory)