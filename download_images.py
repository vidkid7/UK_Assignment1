"""
Download free product images from Pexels and Pixabay for StyleVault.
Uses direct URLs to royalty-free images (Pexels license / Pixabay license).
"""

import os
import urllib.request
import ssl

IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'website', 'static', 'images')
HERO_DIR = os.path.join(IMAGE_DIR, 'hero')

# SSL context for downloads
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download(url, filepath):
    """Download a file from URL."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.exists(filepath):
        print(f"  [EXISTS] {os.path.basename(filepath)}")
        return True
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = resp.read()
        with open(filepath, 'wb') as f:
            f.write(data)
        print(f"  [OK] {os.path.basename(filepath)} ({len(data)//1024}KB)")
        return True
    except Exception as e:
        print(f"  [FAIL] {os.path.basename(filepath)}: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
# IMAGE URLS - All from Pexels (free to use, no attribution required)
# Using Pexels photo CDN with specific sizes for fast loading
# ═══════════════════════════════════════════════════════════════

PRODUCT_IMAGES = {
    # Women's products (w1-w6)
    'w1.jpg': 'https://images.pexels.com/photos/985635/pexels-photo-985635.jpeg?auto=compress&cs=tinysrgb&w=600',      # Silk dress / woman in dress
    'w2.jpg': 'https://images.pexels.com/photos/1036623/pexels-photo-1036623.jpeg?auto=compress&cs=tinysrgb&w=600',     # Blazer / woman in blazer
    'w3.jpg': 'https://images.pexels.com/photos/1755428/pexels-photo-1755428.jpeg?auto=compress&cs=tinysrgb&w=600',     # Maxi skirt / floral
    'w4.jpg': 'https://images.pexels.com/photos/1021693/pexels-photo-1021693.jpeg?auto=compress&cs=tinysrgb&w=600',     # Wool coat
    'w5.jpg': 'https://images.pexels.com/photos/1462637/pexels-photo-1462637.jpeg?auto=compress&cs=tinysrgb&w=600',     # Linen top
    'w6.jpg': 'https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=600',     # Palazzo trousers

    # Men's products (m1-m6)
    'm1.jpg': 'https://images.pexels.com/photos/1043474/pexels-photo-1043474.jpeg?auto=compress&cs=tinysrgb&w=600',     # Man in suit
    'm2.jpg': 'https://images.pexels.com/photos/297933/pexels-photo-297933.jpeg?auto=compress&cs=tinysrgb&w=600',       # Oxford shirt
    'm3.jpg': 'https://images.pexels.com/photos/292999/pexels-photo-292999.jpeg?auto=compress&cs=tinysrgb&w=600',       # Chelsea boots
    'm4.jpg': 'https://images.pexels.com/photos/1232459/pexels-photo-1232459.jpeg?auto=compress&cs=tinysrgb&w=600',     # Wool jumper / man
    'm5.jpg': 'https://images.pexels.com/photos/1300550/pexels-photo-1300550.jpeg?auto=compress&cs=tinysrgb&w=600',     # Chino trousers / man
    'm6.jpg': 'https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg?auto=compress&cs=tinysrgb&w=600',     # Overcoat / man

    # Accessories (a1-a4)
    'a1.jpg': 'https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?auto=compress&cs=tinysrgb&w=600',     # Leather tote bag
    'a2.jpg': 'https://images.pexels.com/photos/45055/pexels-photo-45055.jpeg?auto=compress&cs=tinysrgb&w=600',         # Pocket square / silk
    'a3.jpg': 'https://images.pexels.com/photos/701877/pexels-photo-701877.jpeg?auto=compress&cs=tinysrgb&w=600',       # Aviator sunglasses
    'a4.jpg': 'https://images.pexels.com/photos/6567607/pexels-photo-6567607.jpeg?auto=compress&cs=tinysrgb&w=600',     # Cashmere scarf

    # Sale items (s1-s2)
    's1.jpg': 'https://images.pexels.com/photos/1346187/pexels-photo-1346187.jpeg?auto=compress&cs=tinysrgb&w=600',     # Polo shirt
    's2.jpg': 'https://images.pexels.com/photos/1055691/pexels-photo-1055691.jpeg?auto=compress&cs=tinysrgb&w=600',     # Summer dress
}

HERO_IMAGES = {
    'hero_women.jpg': 'https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=1200',    # Women's fashion
    'hero_men.jpg': 'https://images.pexels.com/photos/1043474/pexels-photo-1043474.jpeg?auto=compress&cs=tinysrgb&w=1200',      # Men's fashion
}


def download_all():
    print("\n" + "=" * 60)
    print("  DOWNLOADING PRODUCT IMAGES")
    print("=" * 60)

    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(HERO_DIR, exist_ok=True)

    success = 0
    total = len(PRODUCT_IMAGES) + len(HERO_IMAGES)

    print(f"\nDownloading {len(PRODUCT_IMAGES)} product images...")
    for filename, url in PRODUCT_IMAGES.items():
        if download(url, os.path.join(IMAGE_DIR, filename)):
            success += 1

    print(f"\nDownloading {len(HERO_IMAGES)} hero images...")
    for filename, url in HERO_IMAGES.items():
        if download(url, os.path.join(HERO_DIR, filename)):
            success += 1

    print(f"\n[DONE] Downloaded {success}/{total} images successfully.")
    return success


if __name__ == '__main__':
    download_all()
