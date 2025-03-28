import os
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from scipy.sparse import hstack
import matplotlib.pyplot as plt
import re


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

    plt.title("Document Similarity Matrix\n(Red lines = Cluster Boundaries)")
    plt.xlabel("Document Index")
    plt.ylabel("Document Index")
    plt.xticks(np.arange(len(filenames)), fontsize=4, rotation=90)
    plt.yticks(np.arange(len(filenames)), filenames, fontsize=4)
    
    plt.tight_layout()
    plt.show()
def camel_to_kebab(name):
    # Convert camelCase to kebab-case.
    s = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
    return s

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract CSS from <style> tags 
    css_contents = []
    additional_css = []
    for style_tag in soup.find_all('style'):
        css = style_tag.get_text()
        css = ' '.join(css.split()).lower()
        css_contents.append(css)
        style_tag.decompose()  
    

    # Regex Patterns:

    # 1. Direct assignment: element.style.property = 'value';
    pattern_direct = re.compile(r"\.style\.([a-zA-Z]+)\s*=\s*['\"]([^'\"]+)['\"]")
    # 2. Using cssText assignment: element.style.cssText = `...` or "..."
    pattern_cssText = re.compile(r"\.style\.cssText\s*=\s*([`'\"])(.*?)\1", re.DOTALL)
    # 3. Using setProperty: element.style.setProperty('property', 'value'[, ...]);
    pattern_setProperty = re.compile(r"\.style\.setProperty\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]")
    # 4. Capture a template literal definition assigned to a variable.
    pattern_template_literal = re.compile(r"const\s+(\w+)\s*=\s*`([^`]+)`", re.DOTALL)
    
    # Store any template literals for later lookup.
    template_literals = {}

    for script_tag in soup.find_all('script'):
        script_text = script_tag.get_text()
        for var, content in re.findall(pattern_template_literal, script_text):
            # Clean up the extracted CSS content.
            cleaned = ' '.join(content.split()).lower()
            template_literals[var] = cleaned

    for script_tag in soup.find_all('script'):
        script_text = script_tag.get_text()

        # 1. Process direct inline style assignments.
        for match in re.finditer(pattern_direct, script_text):
            prop, value = match.groups()
            # Convert property from camelCase to kebab-case.
            prop_kebab = camel_to_kebab(prop)
            # Build a CSS declaration string.
            rule = f"{prop_kebab}: {value};"
            additional_css.append(rule)
        
        # 2. Process cssText assignments.
        for match in re.finditer(pattern_cssText, script_text):
            delimiter, content = match.groups()
            # Check if content is a reference to a template literal variable.
            if content.strip() in template_literals:
                rule = template_literals[content.strip()]
            else:
                rule = ' '.join(content.split()).lower()
            additional_css.append(rule)
        
        # 3. Process setProperty calls.
        for match in re.finditer(pattern_setProperty, script_text):
            prop, value = match.groups()
            rule = f"{prop}: {value};"
            additional_css.append(rule)
        
        # Remove the script tag after processing.
        script_tag.decompose()
    
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
    css_str = ' '.join(css_contents + inline_styles + additional_css)
    
    return text, tag_str, css_str

def compute_similarities(texts, tags, css, weights=(0.4, 0.3, 0.3)):
    # Vectorize each feature 
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

def main(directory, weights=(0.4, 0.3, 0.3), threshold=0.5, output_filename='groups.txt', multiple = 0):
    
    filenames, texts, tag_seqs, css_seqs = process_directory(directory)
    if not filenames:
        return []
    
    combined_sim = compute_similarities(texts, tag_seqs, css_seqs, weights)

    clusters = cluster_files(combined_sim, threshold)
    grouped = group_files(filenames, clusters)

    if multiple == 0:
        with open(output_filename, 'w') as out_file:
            for group in grouped:
                out_file.write("[" + ", ".join(group) + "]")
                if group != grouped[-1]:
                    out_file.write(", ")
    return grouped

def process_subdirectories(root_directory, output_filename='groups_all.txt'):
    with open(output_filename, 'w') as out_file:
        # Iterate over each item in the root_directory
        for folder in sorted(os.listdir(root_directory)):
            folder_path = os.path.join(root_directory, folder)
            if os.path.isdir(folder_path):
                groups = main(folder_path, multiple=1)
                out_file.write(f"Folder: {folder}\n")
                if groups:
                    for group in groups:
                        out_file.write("[" + ", ".join(group) + "]")
                        if group != groups[-1]:
                            out_file.write(", ")
                out_file.write("\n")
                print(f"Processed folder: {folder}")

if __name__ == "__main__":
    root_directory = r"clones"  
    
    print("Choose the processing mode:")
    print("1: Process all subdirectories")
    print("2: Process a specific subdirectory (e.g., tier1, tier2, tier3, tier4)")
    choice = input("Enter 1 or 2: ").strip()

    
    if choice == '1':
        process_subdirectories(root_directory)
    elif choice == '2':
        subdir_name = input("Enter the subdirectory name (e.g., tier1, tier2, tier3, tier4): ").strip()
        subdir_path = os.path.join(root_directory, subdir_name)
        if os.path.isdir(subdir_path):
            main(subdir_path)