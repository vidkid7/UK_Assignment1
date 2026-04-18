"""
Seed Data for StyleVault E-Commerce Database
Populates the database with sample products, categories, and admin user.
"""

from werkzeug.security import generate_password_hash
from models import User, Category, Product


def seed_database(db):
    """Populate the database with initial data."""

    # ── Categories ──────────────────────────────────────────
    categories = [
        Category(name='Women', slug='women',
                 description='Premium womenswear collection'),
        Category(name='Men', slug='men',
                 description='Luxury menswear collection'),
        Category(name='Accessories', slug='accessories',
                 description='Designer accessories and jewellery'),
        Category(name='Sale', slug='sale',
                 description='Discounted items across all categories'),
    ]
    for cat in categories:
        db.session.add(cat)
    db.session.flush()

    cat_map = {c.slug: c.id for c in categories}

    # ── Products ────────────────────────────────────────────
    products = [
        # Women's products
        Product(name='Silk Midi Dress', slug='silk-midi-dress',
                description='Elegant hand-crafted silk midi dress with subtle pleating. Perfect for evening occasions. Features a flattering A-line silhouette with adjustable waist tie.',
                price=485.00, brand='Valentina Roma', image_url='/static/images/w1.jpg',
                stock=15, sizes='XS,S,M,L,XL', category_id=cat_map['women'], is_featured=True),
        Product(name='Cashmere Blazer', slug='cashmere-blazer',
                description='Tailored cashmere-blend blazer in classic navy. Double-breasted design with gold-tone buttons. Fully lined with interior pockets.',
                price=695.00, brand='House of Laurent', image_url='/static/images/w2.jpg',
                stock=10, sizes='XS,S,M,L', category_id=cat_map['women'], is_featured=True),
        Product(name='Embroidered Maxi Skirt', slug='embroidered-maxi-skirt',
                description='Floor-length maxi skirt with intricate floral embroidery. Crafted from lightweight cotton with a comfortable elastic waistband.',
                price=320.00, brand='Aria Collective', image_url='/static/images/w3.jpg',
                stock=20, sizes='XS,S,M,L,XL', category_id=cat_map['women']),
        Product(name='Structured Wool Coat', slug='structured-wool-coat',
                description='Premium Italian wool overcoat with structured shoulders. Features deep pockets and a classic notch lapel design.',
                price=890.00, brand='House of Laurent', image_url='/static/images/w4.jpg',
                stock=8, sizes='S,M,L', category_id=cat_map['women'], is_featured=True),
        Product(name='Linen Wrap Top', slug='linen-wrap-top',
                description='Breathable pure linen wrap top in ivory. Features delicate lace trim at the sleeves and adjustable wrap closure.',
                price=195.00, brand='Aria Collective', image_url='/static/images/w5.jpg',
                stock=25, sizes='XS,S,M,L,XL', category_id=cat_map['women']),
        Product(name='Pleated Palazzo Trousers', slug='pleated-palazzo-trousers',
                description='Wide-leg palazzo trousers in soft crepe fabric. High-waisted design with elegant front pleats. Available in midnight black.',
                price=275.00, brand='Valentina Roma', image_url='/static/images/w6.jpg',
                stock=18, sizes='XS,S,M,L,XL', category_id=cat_map['women']),

        # Men's products
        Product(name='Italian Wool Suit', slug='italian-wool-suit',
                description='Two-piece slim-fit suit crafted from super 120s Italian wool. Single-breasted jacket with flat-front trousers. A wardrobe essential for the modern gentleman.',
                price=1250.00, brand='Savile & Co', image_url='/static/images/m1.jpg',
                stock=12, sizes='S,M,L,XL,XXL', category_id=cat_map['men'], is_featured=True),
        Product(name='Oxford Cotton Shirt', slug='oxford-cotton-shirt',
                description='Classic button-down Oxford shirt in premium Egyptian cotton. Features mother-of-pearl buttons and a comfortable regular fit.',
                price=145.00, brand='Sterling & James', image_url='/static/images/m2.jpg',
                stock=30, sizes='S,M,L,XL,XXL', category_id=cat_map['men']),
        Product(name='Leather Chelsea Boots', slug='leather-chelsea-boots',
                description='Hand-stitched leather Chelsea boots with Goodyear welt construction. Features elasticated side panels and a rubber-studded sole for grip.',
                price=395.00, brand='Savile & Co', image_url='/static/images/m3.jpg',
                stock=20, sizes='7,8,9,10,11,12', category_id=cat_map['men'], is_featured=True),
        Product(name='Merino Wool Jumper', slug='merino-wool-jumper',
                description='Luxuriously soft fine-gauge merino wool crewneck jumper. Ribbed cuffs and hem. Available in charcoal grey.',
                price=210.00, brand='Sterling & James', image_url='/static/images/m4.jpg',
                stock=25, sizes='S,M,L,XL', category_id=cat_map['men']),
        Product(name='Slim Chino Trousers', slug='slim-chino-trousers',
                description='Tailored slim-fit chino trousers in stretch cotton twill. Features a zip fly, button closure, and four functional pockets.',
                price=165.00, brand='Sterling & James', image_url='/static/images/m5.jpg',
                stock=35, sizes='28,30,32,34,36,38', category_id=cat_map['men']),
        Product(name='Double-Breasted Overcoat', slug='double-breasted-overcoat',
                description='Statement double-breasted overcoat in camel wool-cashmere blend. Peak lapels with horn buttons. Fully lined.',
                price=980.00, brand='Savile & Co', image_url='/static/images/m6.jpg',
                stock=10, sizes='S,M,L,XL', category_id=cat_map['men'], is_featured=True),

        # Accessories
        Product(name='Leather Tote Bag', slug='leather-tote-bag',
                description='Full-grain leather tote bag with suede lining. Features internal zip pocket, magnetic snap closure, and detachable shoulder strap.',
                price=450.00, brand='Maison Luxe', image_url='/static/images/a1.jpg',
                stock=15, sizes='One Size', category_id=cat_map['accessories'], is_featured=True),
        Product(name='Silk Pocket Square Set', slug='silk-pocket-square-set',
                description='Set of three hand-rolled Italian silk pocket squares in complementary patterns. Presented in a luxury gift box.',
                price=95.00, brand='Sterling & James', image_url='/static/images/a2.jpg',
                stock=40, sizes='One Size', category_id=cat_map['accessories']),
        Product(name='Aviator Sunglasses', slug='aviator-sunglasses',
                description='Premium polarised aviator sunglasses with titanium frames. UV400 protection lenses. Comes with branded leather case.',
                price=285.00, brand='Maison Luxe', image_url='/static/images/a3.jpg',
                stock=22, sizes='One Size', category_id=cat_map['accessories'], is_featured=True),
        Product(name='Cashmere Scarf', slug='cashmere-scarf',
                description='Ultra-soft 100% cashmere scarf in classic houndstooth pattern. Generous size for multiple styling options.',
                price=175.00, brand='House of Laurent', image_url='/static/images/a4.jpg',
                stock=30, sizes='One Size', category_id=cat_map['accessories']),

        # Sale items
        Product(name='Cotton Polo Shirt', slug='cotton-polo-shirt',
                description='Pique cotton polo shirt with contrast collar trim. Relaxed fit with ribbed cuffs. Previously season stock.',
                price=120.00, sale_price=72.00, brand='Sterling & James',
                image_url='/static/images/s1.jpg', stock=50,
                sizes='S,M,L,XL,XXL', category_id=cat_map['sale']),
        Product(name='Printed Summer Dress', slug='printed-summer-dress',
                description='Vibrant floral print summer dress in lightweight viscose. Features smocked bodice and tiered skirt.',
                price=245.00, sale_price=147.00, brand='Aria Collective',
                image_url='/static/images/s2.jpg', stock=15,
                sizes='XS,S,M,L', category_id=cat_map['sale']),

        # Additional Women's products
        Product(name='Velvet Evening Gown', slug='velvet-evening-gown',
                description='Luxurious deep-blue velvet floor-length gown with sweetheart neckline and dramatic side slit. Perfect for black-tie occasions. Features a self-tie sash at the waist.',
                price=750.00, brand='Valentina Roma', image_url='/static/images/w5.jpg',
                stock=8, sizes='XS,S,M,L', category_id=cat_map['women'], is_featured=True),
        Product(name='Tailored Trench Coat', slug='tailored-trench-coat',
                description='Classic double-breasted trench coat in water-resistant gabardine. Features epaulettes, storm flap, and adjustable belt. A timeless wardrobe essential.',
                price=620.00, brand='House of Laurent', image_url='/static/images/w6.jpg',
                stock=12, sizes='XS,S,M,L,XL', category_id=cat_map['women']),

        # Additional Men's product
        Product(name='Linen Summer Suit', slug='linen-summer-suit',
                description='Lightweight two-piece linen suit in natural ecru. Unlined jacket with patch pockets and slightly relaxed trousers. Perfect for warm-weather occasions.',
                price=895.00, brand='Savile & Co', image_url='/static/images/m5.jpg',
                stock=10, sizes='S,M,L,XL', category_id=cat_map['men']),
    ]

    for prod in products:
        db.session.add(prod)

    # ── Admin User ──────────────────────────────────────────
    admin = User(
        email='admin@stylevault.com',
        password_hash=generate_password_hash('Admin123!'),
        first_name='Admin',
        last_name='StyleVault',
        is_admin=True
    )
    db.session.add(admin)

    # ── Demo User ───────────────────────────────────────────
    demo = User(
        email='demo@stylevault.com',
        password_hash=generate_password_hash('Demo123!'),
        first_name='Jane',
        last_name='Smith',
        is_admin=False
    )
    db.session.add(demo)

    db.session.commit()
    print("[SEED] Database seeded with categories, products, and users.")
