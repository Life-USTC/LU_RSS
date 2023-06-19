from .tj_ustc import tj_ustc_RSS

__all__ = [
    "tj_ustc_RSS"
]

def generate_RSS_feeds(output_dir: str):
    tj_ustc_RSS(output_dir)