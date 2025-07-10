import os
import torch
import logging
import hashlib

# ========== Hashing ========== #
def hash_file(filepath, chunk_size=65536):
    """Efficiently compute SHA256 hash for large files."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb', buffering=0) as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.warning(f"[WARNING] Could not hash file: {filepath} - {e}")
        return None

# ========== Load Saved Embeddings ========== #
def load_saved_embeddings(features_mapping):
    """
    Load .pt embeddings from disk into memory.
    Returns dictionary of {name: list_of_embeddings}.
    """
    saved_embeddings = {}
    for name, paths in features_mapping.items():
        embeddings = []
        for path in paths:
            if not os.path.exists(path):
                logging.warning(f"[MISSING] {path}")
                continue
            try:
                emb = torch.load(path)
                embeddings.append(emb)
            except Exception as e:
                logging.warning(f"[LOAD ERROR] {path}: {e}")
        if embeddings:
            saved_embeddings[name] = embeddings
        else:
            logging.warning(f"[EMPTY] No embeddings found for {name}")
    return saved_embeddings

# ========== Update Database from Embeddings ========== #
def update_database_from_folders(embeddings_root, features_mapping):
    """
    Scan 'user_embeddings' directory and update features_mapping in-place.
    Avoids duplicated .pt files using SHA256 hashes.
    """
    if not os.path.isdir(embeddings_root):
        logging.warning(f"[WARNING] Embeddings directory not found: {embeddings_root}")
        return

    seen_hashes = set()
    features_mapping.clear()

    for folder in sorted(os.listdir(embeddings_root)):
        folder_path = os.path.join(embeddings_root, folder)
        if not folder.endswith('_pt') or not os.path.isdir(folder_path):
            continue

        person = folder.replace('_pt', '')
        pt_files = sorted([
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path) if f.endswith('.pt')
        ])

        unique_files = []
        for file in pt_files:
            h = hash_file(file)
            if h and h not in seen_hashes:
                seen_hashes.add(h)
                unique_files.append(file)

        if unique_files:
            features_mapping[person] = unique_files
            logging.info(f"[OK] {person}: {len(unique_files)} unique embeddings loaded")
        else:
            logging.warning(f"[SKIP] {person} has no valid or unique embeddings")

# ========== Manual Test ========== #
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    base_path = os.getcwd()
    embeddings_dir = os.path.join(base_path, "user_embeddings")
    features = {}

    update_database_from_folders(embeddings_dir, features)
    saved = load_saved_embeddings(features)

    for name, embeds in saved.items():
        logging.info(f"[SUMMARY] {name}: {len(embeds)} embeddings")
