import os
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
import numpy as np

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
        style_tag.decompose()  # Remove from DOM but keep content
    
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
    # Text similarity
    text_vec = TfidfVectorizer(stop_words='english').fit_transform(texts)
    text_sim = cosine_similarity(text_vec)
    
    # Tag structure similarity
    tag_vec = TfidfVectorizer(ngram_range=(2, 2)).fit_transform(tags)
    tag_sim = cosine_similarity(tag_vec)
    
    # CSS similarity
    css_vec = TfidfVectorizer().fit_transform(css)
    css_sim = cosine_similarity(css_vec)
    
    # Weighted combination
    return (weights[0]*text_sim + weights[1]*tag_sim + weights[2]*css_sim) / sum(weights)

def process_directory(directory):
    files = sorted([os.path.join(directory, f) 
                    for f in os.listdir(directory) if f.endswith('.html')])
    texts = []
    tag_seqs = []
    css_seqs = []  # NEW: CSS container
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

def main(directory, weights=(0.4, 0.3, 0.3), threshold=0.5):
    filenames, texts, tag_seqs, css_seqs = process_directory(directory)
    if not filenames:
        return []
    
    combined_sim = compute_similarities(texts, tag_seqs, css_seqs, weights)
    clusters = cluster_files(combined_sim, threshold)
    grouped = group_files(filenames, clusters)
    return grouped

def process_subdirectories(root_directory, output_filename='groups_all.txt'):
    """
    Iterates through each subfolder in the root_directory.
    For each subfolder, it applies the clustering algorithm and writes the groupings to the output file.
    """
    with open(output_filename, 'w') as out_file:
        # Iterate over each item in the root_directory
        for folder in sorted(os.listdir(root_directory)):
            folder_path = os.path.join(root_directory, folder)
            if os.path.isdir(folder_path):
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
    root_directory = r"D:\Projects\HTMLCLONES\clones"  # Replace with your actual directory
    process_subdirectories(root_directory)
