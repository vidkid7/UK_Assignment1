"""
Diagram Generation Module for StyleVault Assignment
Generates all required UML, planning, and architecture diagrams using matplotlib.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'diagrams')


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# 1. GANTT CHART
# ═══════════════════════════════════════════════════════════════
def generate_gantt_chart():
    """Generate a detailed Gantt chart for project planning."""
    ensure_output_dir()

    tasks = [
        ('Project Initiation', '2026-01-12', '2026-01-14', 'Planning', 'Done'),
        ('Requirements Gathering', '2026-01-15', '2026-01-21', 'Planning', 'Done'),
        ('Literature Review', '2026-01-15', '2026-01-25', 'Planning', 'Done'),
        ('UML Diagrams', '2026-01-22', '2026-02-02', 'Design', 'Done'),
        ('Wireframe Design', '2026-01-26', '2026-02-05', 'Design', 'Done'),
        ('Database Design', '2026-02-01', '2026-02-08', 'Design', 'Done'),
        ('Website Development', '2026-02-06', '2026-03-05', 'Development', 'Done'),
        ('Frontend Implementation', '2026-02-10', '2026-03-08', 'Development', 'Done'),
        ('Backend Implementation', '2026-02-10', '2026-03-05', 'Development', 'Done'),
        ('Content & Products', '2026-03-01', '2026-03-08', 'Development', 'Done'),
        ('Unit Testing', '2026-03-06', '2026-03-14', 'Testing', 'Done'),
        ('Integration Testing', '2026-03-10', '2026-03-16', 'Testing', 'Done'),
        ('User Acceptance Testing', '2026-03-14', '2026-03-18', 'Testing', 'Done'),
        ('Documentation & Report', '2026-03-10', '2026-03-20', 'Documentation', 'Working'),
        ('Review & Submission', '2026-03-18', '2026-03-22', 'Documentation', 'Working'),
    ]

    phase_colors = {
        'Planning': '#4CAF50',
        'Design': '#2196F3',
        'Development': '#FF9800',
        'Testing': '#9C27B0',
        'Documentation': '#F44336'
    }

    fig, ax = plt.subplots(figsize=(14, 8))
    start_date = datetime(2026, 1, 12)

    for i, (task, start, end, phase, status) in enumerate(reversed(tasks)):
        s = datetime.strptime(start, '%Y-%m-%d')
        e = datetime.strptime(end, '%Y-%m-%d')
        s_offset = (s - start_date).days
        duration = (e - s).days

        color = phase_colors[phase]
        alpha = 1.0 if status == 'Done' else 0.6

        ax.barh(i, duration, left=s_offset, height=0.6,
                color=color, alpha=alpha, edgecolor='white', linewidth=0.5)

        if status == 'Done':
            ax.text(s_offset + duration / 2, i, '✓', ha='center', va='center',
                    fontsize=10, color='white', fontweight='bold')

    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t[0] for t in reversed(tasks)], fontsize=9)
    ax.set_xlabel('Days from Project Start', fontsize=10)
    ax.set_title('StyleVault Project - Gantt Chart', fontsize=14, fontweight='bold', pad=15)

    legend_patches = [mpatches.Patch(color=c, label=p) for p, c in phase_colors.items()]
    ax.legend(handles=legend_patches, loc='lower right', fontsize=8, framealpha=0.9)

    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'gantt_chart.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] Gantt chart saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 2. WORK BREAKDOWN STRUCTURE
# ═══════════════════════════════════════════════════════════════
def generate_wbs():
    """Generate a Work Breakdown Structure diagram."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    def draw_box(x, y, text, w=2.2, h=0.6, color='#2196F3'):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                             boxstyle="round,pad=0.1", facecolor=color,
                             edgecolor='#333', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=7,
                fontweight='bold', color='white', wrap=True)

    def draw_line(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color='#666', linewidth=1)

    # Level 0 - Root
    draw_box(8, 9.2, 'STYLEVAULT\nE-COMMERCE\nPROJECT', w=2.8, h=0.8, color='#1a1a1a')

    # Level 1 - Phases
    phases = [
        (2.5, 7.5, '1. Planning'),
        (5.5, 7.5, '2. Design'),
        (8.5, 7.5, '3. Development'),
        (11.5, 7.5, '4. Testing'),
        (14, 7.5, '5. Launch'),
    ]
    for px, py, label in phases:
        draw_box(px, py, label, color='#1976D2')
        draw_line(8, 9.2 - 0.4, px, py + 0.3)

    # Level 2 - Planning sub-tasks
    plan_subs = [
        (1.3, 6, 'Requirements\nAnalysis'),
        (3.7, 6, 'Scope\nDefinition'),
    ]
    for sx, sy, label in plan_subs:
        draw_box(sx, sy, label, w=1.8, h=0.6, color='#42A5F5')
        draw_line(2.5, 7.5 - 0.3, sx, sy + 0.3)

    # Level 2 - Design sub-tasks
    design_subs = [
        (4.2, 6, 'Website\nContent'),
        (5.5, 6, 'Select\nPlatform'),
        (6.8, 6, 'Prototype'),
    ]
    for sx, sy, label in design_subs:
        draw_box(sx, sy, label, w=1.4, h=0.6, color='#42A5F5')
        draw_line(5.5, 7.5 - 0.3, sx, sy + 0.3)

    # Level 2 - Development sub-tasks
    dev_subs = [
        (7.5, 6, 'Customer\nInterface'),
        (8.5, 6, 'Admin\nInterface'),
        (9.5, 6, 'Payment\nGateway'),
    ]
    for sx, sy, label in dev_subs:
        draw_box(sx, sy, label, w=1.4, h=0.6, color='#42A5F5')
        draw_line(8.5, 7.5 - 0.3, sx, sy + 0.3)

    # Level 3 - Customer Interface sub-tasks
    cust_subs = [
        (6.5, 4.5, 'Homepage'),
        (7.5, 4.5, 'User\nAccount'),
        (8.5, 4.5, 'Navigation\nBar'),
        (9.5, 4.5, 'Checkout'),
        (10.5, 4.5, 'Product\nPages'),
    ]
    for sx, sy, label in cust_subs:
        draw_box(sx, sy, label, w=1.2, h=0.6, color='#64B5F6')
        draw_line(7.5, 6 - 0.3, sx, sy + 0.3)

    # Level 2 - Testing sub-tasks
    test_subs = [
        (10.8, 6, 'Functional\nTesting'),
        (11.5, 6, 'Compatibility\nTesting'),
        (12.3, 6, 'Usability\nTesting'),
    ]
    for sx, sy, label in test_subs:
        draw_box(sx, sy, label, w=1.3, h=0.6, color='#42A5F5')
        draw_line(11.5, 7.5 - 0.3, sx, sy + 0.3)

    # Level 3 - Compatibility sub-tasks
    compat_subs = [
        (11, 4.5, 'Desktop\nBrowser'),
        (12, 4.5, 'Mobile\nFriendly'),
    ]
    for sx, sy, label in compat_subs:
        draw_box(sx, sy, label, w=1.2, h=0.6, color='#64B5F6')
        draw_line(11.5, 6 - 0.3, sx, sy + 0.3)

    ax.set_title('Work Breakdown Structure (WBS)', fontsize=14,
                 fontweight='bold', pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'wbs_diagram.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] WBS saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 3. USE CASE DIAGRAM
# ═══════════════════════════════════════════════════════════════
def generate_use_case():
    """Generate a Use Case diagram."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    def draw_actor(x, y, label):
        # Head
        circle = plt.Circle((x, y + 0.5), 0.15, fill=False, color='#333', linewidth=1.5)
        ax.add_patch(circle)
        # Body
        ax.plot([x, x], [y + 0.35, y - 0.05], color='#333', linewidth=1.5)
        # Arms
        ax.plot([x - 0.2, x + 0.2], [y + 0.2, y + 0.2], color='#333', linewidth=1.5)
        # Legs
        ax.plot([x, x - 0.15], [y - 0.05, y - 0.3], color='#333', linewidth=1.5)
        ax.plot([x, x + 0.15], [y - 0.05, y - 0.3], color='#333', linewidth=1.5)
        ax.text(x, y - 0.5, label, ha='center', fontsize=9, fontweight='bold')

    def draw_usecase(x, y, text, color='#E3F2FD'):
        ellipse = mpatches.Ellipse((x, y), 2.8, 0.7, facecolor=color,
                                    edgecolor='#1565C0', linewidth=1.2)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=8)

    def connect(x1, y1, x2, y2, style='-', color='#666'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1,
                                   connectionstyle='arc3,rad=0'))

    # System boundary
    rect = mpatches.FancyBboxPatch((3, 0.5), 8, 9, boxstyle="round,pad=0.3",
                                    facecolor='#FAFAFA', edgecolor='#333',
                                    linewidth=1.5, linestyle='--')
    ax.add_patch(rect)
    ax.text(7, 9.7, 'StyleVault E-Commerce System', ha='center',
            fontsize=12, fontweight='bold', style='italic')

    # Actors
    draw_actor(1.5, 5.5, 'Customer')
    draw_actor(1.5, 2.5, 'New Customer')
    draw_actor(12.5, 5, 'Admin')

    # Use cases
    use_cases = [
        (5.5, 8.5, 'Browse Products'),
        (5.5, 7.3, 'Search Products'),
        (5.5, 6.1, 'View Product Details'),
        (5.5, 4.9, 'Add to Cart'),
        (5.5, 3.7, 'Checkout'),
        (5.5, 2.5, 'Make Payment'),
        (5.5, 1.3, 'Contact Support'),
        (9, 8.5, 'Login / Register'),
        (9, 7.3, 'Manage Account'),
        (9, 6.1, 'Manage Products'),
        (9, 4.9, 'Manage Orders'),
        (9, 3.7, 'View Analytics'),
        (9, 2.5, 'Respond to Queries'),
    ]

    for ux, uy, label in use_cases:
        draw_usecase(ux, uy, label)

    # Customer connections
    for uy in [8.5, 7.3, 6.1, 4.9, 3.7, 2.5, 1.3]:
        connect(1.8, 5.5, 4.1, uy)

    connect(1.8, 5.5, 7.6, 8.5)  # Login
    connect(1.8, 2.5, 7.6, 8.5)  # New customer -> Register

    # Admin connections
    for uy in [8.5, 7.3, 6.1, 4.9, 3.7, 2.5]:
        connect(12.2, 5, 10.4, uy)

    # Include / Extend relationships
    ax.annotate('<<include>>', xy=(5.5, 3.2), xytext=(5.5, 2.9),
                fontsize=7, ha='center', style='italic', color='#1565C0')

    ax.annotate('<<extend>>', xy=(9, 7.8), xytext=(7.2, 7.8),
                fontsize=7, ha='center', style='italic', color='#C62828')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'use_case_diagram.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] Use case diagram saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 4. ACTIVITY DIAGRAM (User Flow)
# ═══════════════════════════════════════════════════════════════
def generate_activity_diagram():
    """Generate an Activity Diagram showing user purchase flow."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(10, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')

    def draw_rounded_box(x, y, text, w=3, h=0.6, color='#FFF8E1', edge='#F57F17'):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                             boxstyle="round,pad=0.15", facecolor=color,
                             edgecolor=edge, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9)

    def draw_diamond(x, y, text):
        diamond = plt.Polygon([[x, y+0.35], [x+0.5, y], [x, y-0.35], [x-0.5, y]],
                              facecolor='#FFF9C4', edgecolor='#F57F17', linewidth=1.5)
        ax.add_patch(diamond)
        ax.text(x, y, text, ha='center', va='center', fontsize=7)

    def draw_start(x, y):
        circle = plt.Circle((x, y), 0.2, facecolor='#333', edgecolor='#333')
        ax.add_patch(circle)

    def draw_end(x, y):
        outer = plt.Circle((x, y), 0.22, facecolor='white', edgecolor='#333', linewidth=2)
        inner = plt.Circle((x, y), 0.14, facecolor='#333', edgecolor='#333')
        ax.add_patch(outer)
        ax.add_patch(inner)

    def arrow(x1, y1, x2, y2, text=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=1.2))
        if text:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx + 0.3, my, text, fontsize=7, color='#666')

    # Flow
    draw_start(5, 13.5)
    arrow(5, 13.3, 5, 12.9)

    draw_rounded_box(5, 12.6, 'Visit Website')
    arrow(5, 12.3, 5, 11.8)

    draw_diamond(5, 11.5, 'Login?')
    arrow(5.5, 11.5, 7, 11.5, 'Yes')
    arrow(5, 11.15, 5, 10.7, 'No')

    draw_rounded_box(7.5, 11.5, 'Login / Sign Up', w=2.2)
    arrow(7.5, 11.2, 7.5, 10.7)
    draw_rounded_box(7.5, 10.4, 'Enter Credentials', w=2.2)
    arrow(7.5, 10.1, 5, 10)

    draw_rounded_box(5, 10.1, 'Browse as Guest', w=2.5)
    arrow(5, 9.8, 5, 9.3)

    draw_rounded_box(5, 9, 'Browse Products')
    arrow(5, 8.7, 5, 8.2)

    draw_rounded_box(5, 7.9, 'Search / Filter Items')
    arrow(5, 7.6, 5, 7.1)

    draw_rounded_box(5, 6.8, 'View Product Details')
    arrow(5, 6.5, 5, 6)

    draw_diamond(5, 5.7, 'Add?')
    arrow(5, 5.35, 5, 4.9, 'Yes')
    arrow(4.5, 5.7, 3, 5.7, 'No')
    ax.annotate('', xy=(3, 7.9), xytext=(3, 5.7),
                arrowprops=dict(arrowstyle='->', color='#666', lw=1))

    draw_rounded_box(5, 4.6, 'Add to Shopping Cart')
    arrow(5, 4.3, 5, 3.8)

    draw_diamond(5, 3.5, 'More?')
    arrow(4.5, 3.5, 3, 3.5, 'Yes')
    ax.annotate('', xy=(3, 7.9), xytext=(3, 3.5),
                arrowprops=dict(arrowstyle='->', color='#666', lw=1))
    arrow(5, 3.15, 5, 2.7, 'No')

    draw_rounded_box(5, 2.4, 'Proceed to Checkout')
    arrow(5, 2.1, 5, 1.6)

    draw_rounded_box(5, 1.3, 'Enter Payment Details')
    arrow(5, 1.0, 5, 0.5)

    draw_rounded_box(5, 0.2, 'Purchase Completed', color='#C8E6C9', edge='#2E7D32')

    ax.set_title('Activity Diagram - User Purchase Flow', fontsize=13,
                 fontweight='bold', pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'activity_diagram.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] Activity diagram saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 5. SEQUENCE DIAGRAM
# ═══════════════════════════════════════════════════════════════
def generate_sequence_diagram():
    """Generate a Sequence Diagram for user purchase interaction."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    actors = [
        (1.5, 'User'),
        (4, 'Website\nFrontend'),
        (6.5, 'Server'),
        (9, 'Database'),
        (11, 'Payment\nGateway'),
    ]

    # Actor boxes at top
    for x, label in actors:
        box = FancyBboxPatch((x - 0.6, 9.2), 1.2, 0.6,
                             boxstyle="round,pad=0.05", facecolor='#FFCC80',
                             edgecolor='#333', linewidth=1)
        ax.add_patch(box)
        ax.text(x, 9.5, label, ha='center', va='center', fontsize=8, fontweight='bold')
        # Lifeline
        ax.plot([x, x], [9.2, 0.5], color='#999', linewidth=0.8, linestyle='--')

    def msg(x1, x2, y, text, style='->', color='#333'):
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.2))
        mx = (x1 + x2) / 2
        ax.text(mx, y + 0.12, text, ha='center', va='bottom', fontsize=7.5)

    def reply(x1, x2, y, text):
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1,
                                   linestyle='dashed'))
        mx = (x1 + x2) / 2
        ax.text(mx, y + 0.12, text, ha='center', va='bottom', fontsize=7.5,
                color='#1565C0', style='italic')

    # Interactions
    msg(1.5, 4, 8.6, 'Browse Products')
    msg(4, 6.5, 8.2, 'GET /collection')
    msg(6.5, 9, 7.8, 'Query Products')
    reply(9, 6.5, 7.4, 'Product Data')
    reply(6.5, 4, 7.0, 'HTML Response')
    reply(4, 1.5, 6.6, 'Display Products')

    msg(1.5, 4, 6.0, 'Add to Cart')
    msg(4, 6.5, 5.6, 'POST /cart/add')
    msg(6.5, 9, 5.2, 'Save Cart Item')
    reply(9, 6.5, 4.8, 'Confirmation')
    reply(6.5, 4, 4.4, 'Cart Updated')

    msg(1.5, 4, 3.8, 'Checkout')
    msg(4, 6.5, 3.4, 'POST /checkout')
    msg(6.5, 11, 3.0, 'Process Payment')
    reply(11, 6.5, 2.6, 'Payment Approved')
    msg(6.5, 9, 2.2, 'Create Order')
    reply(9, 6.5, 1.8, 'Order Saved')
    reply(6.5, 4, 1.4, 'Order Confirmation')
    reply(4, 1.5, 1.0, 'Display Confirmation')

    ax.set_title('Sequence Diagram - Purchase Flow', fontsize=13,
                 fontweight='bold', pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'sequence_diagram.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] Sequence diagram saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 6. ER DIAGRAM
# ═══════════════════════════════════════════════════════════════
def generate_er_diagram():
    """Generate an Entity-Relationship diagram."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    def draw_entity(x, y, name, attrs, w=2.6, color='#E3F2FD'):
        h_title = 0.5
        h_attr = len(attrs) * 0.35 + 0.2
        h = h_title + h_attr

        # Title box
        title_box = FancyBboxPatch((x - w/2, y - h_title/2), w, h_title,
                                    boxstyle="square,pad=0", facecolor='#1565C0',
                                    edgecolor='#333', linewidth=1)
        ax.add_patch(title_box)
        ax.text(x, y, name, ha='center', va='center', fontsize=9,
                fontweight='bold', color='white')

        # Attributes box
        attr_box = FancyBboxPatch((x - w/2, y - h_title/2 - h_attr), w, h_attr,
                                   boxstyle="square,pad=0", facecolor=color,
                                   edgecolor='#333', linewidth=1)
        ax.add_patch(attr_box)

        for i, attr in enumerate(attrs):
            ay = y - h_title/2 - 0.2 - i * 0.35
            prefix = '🔑 ' if attr.startswith('PK') else ('🔗 ' if attr.startswith('FK') else '   ')
            clean = attr.replace('PK ', '').replace('FK ', '')
            ax.text(x - w/2 + 0.15, ay, f'{prefix}{clean}', fontsize=7, va='center')

        return (x, y - h_title/2 - h_attr/2)

    # Entities
    draw_entity(2, 8.5, 'User', [
        'PK id: INTEGER', 'email: VARCHAR(150)', 'password_hash: VARCHAR(256)',
        'first_name: VARCHAR(100)', 'last_name: VARCHAR(100)', 'is_admin: BOOLEAN'
    ])

    draw_entity(7, 8.5, 'Category', [
        'PK id: INTEGER', 'name: VARCHAR(100)', 'slug: VARCHAR(100)',
        'description: TEXT'
    ])

    draw_entity(12, 8.5, 'Product', [
        'PK id: INTEGER', 'name: VARCHAR(200)', 'price: FLOAT',
        'sale_price: FLOAT', 'brand: VARCHAR(100)', 'stock: INTEGER',
        'FK category_id: INTEGER'
    ])

    draw_entity(2, 4, 'Order', [
        'PK id: INTEGER', 'FK user_id: INTEGER', 'total: FLOAT',
        'status: VARCHAR(50)', 'shipping_address: TEXT',
        'payment_method: VARCHAR(50)'
    ])

    draw_entity(7, 4, 'OrderItem', [
        'PK id: INTEGER', 'FK order_id: INTEGER', 'FK product_id: INTEGER',
        'quantity: INTEGER', 'size: VARCHAR(20)', 'price_at_purchase: FLOAT'
    ])

    draw_entity(12, 4, 'CartItem', [
        'PK id: INTEGER', 'FK user_id: INTEGER', 'FK product_id: INTEGER',
        'quantity: INTEGER', 'size: VARCHAR(20)'
    ])

    draw_entity(7, 1, 'ContactMessage', [
        'PK id: INTEGER', 'name: VARCHAR(100)', 'email: VARCHAR(150)',
        'subject: VARCHAR(200)', 'message: TEXT'
    ])

    # Relationship lines
    def rel_line(x1, y1, x2, y2, label='', card1='1', card2='*'):
        ax.plot([x1, x2], [y1, y2], color='#666', linewidth=1.5)
        mx, my = (x1+x2)/2, (y1+y2)/2
        if label:
            ax.text(mx, my + 0.15, label, ha='center', fontsize=7, style='italic')
        ax.text(x1 + 0.2, y1 - 0.15, card1, fontsize=7, color='#C62828')
        ax.text(x2 - 0.3, y2 + 0.15, card2, fontsize=7, color='#C62828')

    rel_line(2, 7, 2, 5.5, 'places', '1', '*')
    rel_line(3.3, 4, 5.7, 4, 'contains', '1', '*')
    rel_line(8.3, 4, 10.7, 4.5, 'refers to', '*', '1')
    rel_line(8.3, 8.5, 10.7, 8.5, 'belongs to', '*', '1')
    rel_line(3.3, 8, 10.7, 4.8, '', '', '')
    rel_line(12, 7, 12, 5.5, 'contains', '1', '*')

    ax.set_title('Entity-Relationship Diagram', fontsize=14,
                 fontweight='bold', pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'er_diagram.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] ER diagram saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 7. SITE MAP
# ═══════════════════════════════════════════════════════════════
def generate_site_map():
    """Generate a site map diagram."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    def box(x, y, text, color='#FFCC80', w=1.8, h=0.55):
        b = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle="round,pad=0.1", facecolor=color,
                           edgecolor='#333', linewidth=1)
        ax.add_patch(b)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')

    def line(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color='#999', linewidth=1)

    # Home
    box(6, 7, 'HOME', color='#FFB74D', w=2)

    # Level 1
    level1 = [
        (1.5, 5.5, 'Collection'),
        (4, 5.5, 'Customer\nCare'),
        (6, 5.5, 'About Us'),
        (8, 5.5, 'Login'),
        (10, 5.5, 'Search'),
        (11.5, 5.5, 'Cart'),
    ]
    for lx, ly, label in level1:
        box(lx, ly, label)
        line(6, 7 - 0.28, lx, ly + 0.28)

    # Collection sub-pages
    coll_subs = [
        (0.5, 3.8, 'Women'),
        (1.5, 3.8, 'Men'),
        (2.5, 3.8, 'Accessories'),
        (3.5, 3.8, 'Sale'),
    ]
    for sx, sy, label in coll_subs:
        box(sx, sy, label, color='#FFE0B2', w=1.3, h=0.5)
        line(1.5, 5.5 - 0.28, sx, sy + 0.25)

    # Login sub-pages
    login_subs = [
        (7.5, 3.8, 'Sign Up'),
        (8.5, 3.8, 'My Account'),
    ]
    for sx, sy, label in login_subs:
        box(sx, sy, label, color='#FFE0B2', w=1.3, h=0.5)
        line(8, 5.5 - 0.28, sx, sy + 0.25)

    # Cart sub-pages
    cart_subs = [
        (11, 3.8, 'Order\nSummary'),
    ]
    for sx, sy, label in cart_subs:
        box(sx, sy, label, color='#FFE0B2', w=1.3, h=0.5)
        line(11.5, 5.5 - 0.28, sx, sy + 0.25)

    box(11, 2.2, 'Checkout', color='#FFE0B2', w=1.3, h=0.5)
    line(11, 3.8 - 0.25, 11, 2.2 + 0.25)

    # Product detail from collection
    box(2, 2.2, 'Product\nDetail', color='#FFE0B2', w=1.3, h=0.5)
    line(1.5, 3.8 - 0.25, 2, 2.45)
    line(2.5, 3.8 - 0.25, 2, 2.45)

    ax.set_title('Website Site Map', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'site_map.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] Site map saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 8. PERT CHART
# ═══════════════════════════════════════════════════════════════
def generate_pert_chart():
    """Generate a PERT chart showing task dependencies and durations."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')

    def pert_node(x, y, task, duration):
        box = FancyBboxPatch((x - 1, y - 0.45), 2, 0.9,
                             boxstyle="round,pad=0.1", facecolor='#B3E5FC',
                             edgecolor='#0277BD', linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y + 0.15, task, ha='center', va='center', fontsize=7.5, fontweight='bold')
        ax.text(x, y - 0.2, f'{duration} days', ha='center', va='center',
                fontsize=7, color='#555')

    def pert_arrow(x1, y1, x2, y2):
        ax.annotate('', xy=(x2 - 1, y2), xytext=(x1 + 1, y1),
                    arrowprops=dict(arrowstyle='->', color='#0277BD', lw=1.5))

    # Nodes
    pert_node(1.5, 5, 'Project\nInitiation', 2)
    pert_node(4, 5, 'Requirements\nAnalysis', 5)
    pert_node(4, 3, 'Literature\nReview', 8)
    pert_node(7, 5, 'Design &\nPrototype', 10)
    pert_node(7, 3, 'Database\nDesign', 5)
    pert_node(10, 5, 'Website\nDevelopment', 20)
    pert_node(10, 3, 'Content\nCreation', 6)
    pert_node(12.5, 4, 'Testing', 10)
    pert_node(12.5, 2, 'Documentation', 8)
    pert_node(12.5, 6, 'Launch', 1)

    # Arrows
    pert_arrow(1.5, 5, 4, 5)
    pert_arrow(1.5, 5, 4, 3)
    pert_arrow(4, 5, 7, 5)
    pert_arrow(4, 5, 7, 3)
    pert_arrow(7, 5, 10, 5)
    pert_arrow(7, 3, 10, 5)
    pert_arrow(10, 5, 12.5, 4)
    pert_arrow(10, 5, 10, 3)
    pert_arrow(10, 3, 12.5, 2)
    pert_arrow(12.5, 4, 12.5, 6)

    # Critical path highlight
    ax.text(7, 1, 'Critical Path: Initiation → Requirements → Design → Development → Testing → Launch',
            fontsize=9, ha='center', style='italic', color='#C62828',
            bbox=dict(boxstyle='round', facecolor='#FFEBEE', alpha=0.8))

    ax.set_title('PERT Chart - Project Task Dependencies', fontsize=14,
                 fontweight='bold', pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'pert_chart.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] PERT chart saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 9. WIREFRAMES
# ═══════════════════════════════════════════════════════════════
def generate_wireframes():
    """Generate wireframe mockups for key pages."""
    ensure_output_dir()
    fig, axes = plt.subplots(1, 3, figsize=(18, 10))

    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.set_aspect('equal')

    def draw_wireframe_box(ax, x, y, w, h, text='', color='#E0E0E0', text_size=7):
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                        facecolor=color, edgecolor='#999', linewidth=0.8)
        ax.add_patch(rect)
        if text:
            ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                    fontsize=text_size, color='#666')

    # ── Wireframe 1: Homepage ──
    ax = axes[0]
    ax.axis('off')
    ax.set_title('Homepage Wireframe', fontsize=11, fontweight='bold')

    # Top bar
    draw_wireframe_box(ax, 0, 13.2, 10, 0.5, 'FREE SHIPPING BAR', '#333')
    ax.text(5, 13.45, 'FREE SHIPPING BAR', ha='center', va='center',
            fontsize=6, color='white')

    # Search + Login
    draw_wireframe_box(ax, 0, 12.5, 4, 0.5, 'SEARCH...', '#F5F5F5')
    draw_wireframe_box(ax, 7, 12.5, 1.5, 0.5, 'Login', '#F5F5F5')
    draw_wireframe_box(ax, 8.8, 12.5, 1, 0.5, 'Cart', '#F5F5F5')

    # Brand
    ax.text(5, 12, 'StyleVault', ha='center', fontsize=16,
            fontfamily='serif', fontweight='bold')

    # Nav
    draw_wireframe_box(ax, 0, 11.2, 10, 0.5, 'HOME  |  COLLECTION  |  CUSTOMER CARE  |  ABOUT', '#FAFAFA')

    # Hero
    draw_wireframe_box(ax, 0.2, 7.5, 4.6, 3.5, '', '#F5E6D3')
    ax.text(2.5, 9.2, 'WOMEN\nHero Image', ha='center', fontsize=8, color='#999')
    draw_wireframe_box(ax, 5.2, 7.5, 4.6, 3.5, '', '#D3DCE6')
    ax.text(7.5, 9.2, 'MEN\nHero Image', ha='center', fontsize=8, color='#999')

    # New Arrivals
    ax.text(5, 7, 'NEW ARRIVALS', ha='center', fontsize=9, fontweight='bold')
    for i in range(4):
        draw_wireframe_box(ax, 0.3 + i * 2.4, 4, 2, 2.7, f'Product {i+1}', '#F0F0F0')

    # Newsletter
    draw_wireframe_box(ax, 1, 2.5, 8, 1.2, 'GET ON THE LIST\n[Email Input] [Subscribe]', '#FAFAFA')

    # Footer
    draw_wireframe_box(ax, 0, 0.2, 10, 2, 'FOOTER: Links | Store Info | Social Media', '#F5F5F5')

    # ── Wireframe 2: Product Page ──
    ax = axes[1]
    ax.axis('off')
    ax.set_title('Product Detail Wireframe', fontsize=11, fontweight='bold')

    draw_wireframe_box(ax, 0, 13.2, 10, 0.5, 'NAV BAR', '#FAFAFA')
    ax.text(5, 12.5, 'Home / Women / Product Name', fontsize=7, ha='center', color='#999')

    # Product image
    draw_wireframe_box(ax, 0.5, 6, 4.5, 6, '', '#F5F0EB')
    ax.text(2.75, 9, 'Product\nImage', ha='center', fontsize=10, color='#CCC')

    # Thumbnails
    for i in range(2):
        draw_wireframe_box(ax, 0.5 + i * 1.3, 5.2, 1, 0.7, 'Thumb', '#EEE')

    # Product info
    ax.text(6, 11.5, 'Product Name', fontsize=11, fontweight='bold')
    ax.text(6, 11, '£XXX.XX', fontsize=10)
    draw_wireframe_box(ax, 5.5, 9.5, 4, 0.5, 'Size: [Select ▼]', '#F5F5F5')
    draw_wireframe_box(ax, 5.5, 8.7, 4, 0.5, 'Quantity: [1]', '#F5F5F5')
    draw_wireframe_box(ax, 5.5, 7.7, 4, 0.6, 'ADD TO CART', '#333')
    ax.text(7.5, 8, 'ADD TO CART', ha='center', va='center', fontsize=8, color='white')
    draw_wireframe_box(ax, 5.5, 6.8, 4, 0.6, 'BUY NOW', '#FFF')
    ax.text(6, 6.2, 'Social: 🔗 🔗 🔗 🔗', fontsize=8, color='#999')
    ax.text(6, 5.5, 'Product Description', fontsize=9, fontweight='bold')
    draw_wireframe_box(ax, 5.5, 4, 4, 1.3, 'Description text...', '#FAFAFA')

    draw_wireframe_box(ax, 0, 0.2, 10, 3.5, 'RELATED PRODUCTS (4 items)', '#F5F5F5')

    # ── Wireframe 3: Cart/Checkout ──
    ax = axes[2]
    ax.axis('off')
    ax.set_title('Shopping Cart Wireframe', fontsize=11, fontweight='bold')

    draw_wireframe_box(ax, 0, 13.2, 10, 0.5, 'NAV BAR', '#FAFAFA')
    ax.text(5, 12.5, 'MY CART', fontsize=12, ha='center', fontweight='bold')

    # Cart items
    for i in range(3):
        y = 11 - i * 1.5
        draw_wireframe_box(ax, 0.3, y, 1, 1, 'IMG', '#EEE')
        ax.text(2, y + 0.7, f'Product Name {i+1}', fontsize=8, fontweight='bold')
        ax.text(2, y + 0.3, '£XXX.XX | Size: M', fontsize=7, color='#999')
        draw_wireframe_box(ax, 5, y + 0.2, 1.5, 0.5, '[-] 1 [+]', '#F5F5F5')
        ax.text(7.5, y + 0.5, '£XXX.XX', fontsize=8, fontweight='bold')
        ax.text(8.8, y + 0.5, '✕', fontsize=10, color='red')

    # Promo code
    draw_wireframe_box(ax, 0.3, 5.5, 4, 0.5, '[Promo Code] [Apply]', '#F5F5F5')

    # Order summary
    draw_wireframe_box(ax, 6, 4, 3.5, 3.5, '', '#F5F5F5')
    ax.text(7.75, 7, 'Order Summary', fontsize=9, fontweight='bold', ha='center')
    ax.text(6.3, 6.3, 'Subtotal:', fontsize=8)
    ax.text(9, 6.3, '£XXX.XX', fontsize=8, ha='right')
    ax.text(6.3, 5.8, 'Shipping:', fontsize=8)
    ax.text(9, 5.8, 'FREE', fontsize=8, ha='right', color='green')
    ax.plot([6.3, 9.2], [5.4, 5.4], color='#CCC', linewidth=0.5)
    ax.text(6.3, 5, 'Total:', fontsize=9, fontweight='bold')
    ax.text(9, 5, '£XXX.XX', fontsize=9, fontweight='bold', ha='right')
    draw_wireframe_box(ax, 6.2, 4.2, 3.1, 0.6, 'CHECKOUT', '#333')
    ax.text(7.75, 4.5, 'CHECKOUT', ha='center', va='center', fontsize=8, color='white')

    # Note
    draw_wireframe_box(ax, 0.3, 4, 4, 1.2, 'Add a note:\n[Text area]', '#FAFAFA')

    draw_wireframe_box(ax, 0, 0.2, 10, 3.5, 'FOOTER', '#F5F5F5')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'wireframes.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] Wireframes saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 10. RISK MATRIX
# ═══════════════════════════════════════════════════════════════
def generate_risk_matrix():
    """Generate a risk probability-impact matrix."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(8, 6))

    matrix_colors = [
        ['#A5D6A7', '#A5D6A7', '#FFF59D', '#FFF59D', '#FFCC80'],
        ['#A5D6A7', '#FFF59D', '#FFF59D', '#FFCC80', '#FFCC80'],
        ['#FFF59D', '#FFF59D', '#FFCC80', '#FFCC80', '#EF9A9A'],
        ['#FFF59D', '#FFCC80', '#FFCC80', '#EF9A9A', '#EF9A9A'],
        ['#FFCC80', '#FFCC80', '#EF9A9A', '#EF9A9A', '#E57373'],
    ]

    for i in range(5):
        for j in range(5):
            rect = mpatches.FancyBboxPatch((j, 4-i), 1, 1, boxstyle="square,pad=0",
                                            facecolor=matrix_colors[i][j],
                                            edgecolor='white', linewidth=2)
            ax.add_patch(rect)

    # Plot risks
    risks = [
        (1.5, 3.5, 'R1', 'Schedule\nDelay'),
        (3.5, 2.5, 'R2', 'Scope\nCreep'),
        (2.5, 1.5, 'R3', 'Tech\nIssues'),
        (0.5, 4.5, 'R4', 'Budget'),
        (4.5, 0.5, 'R5', 'Team\nConflict'),
        (1.5, 2.5, 'R6', 'Data\nLoss'),
        (3.5, 3.5, 'R7', 'Comm.\nFailure'),
    ]

    for rx, ry, label, desc in risks:
        circle = plt.Circle((rx, ry), 0.3, facecolor='white', edgecolor='#333',
                            linewidth=1.5, zorder=5)
        ax.add_patch(circle)
        ax.text(rx, ry + 0.05, label, ha='center', va='center', fontsize=8,
                fontweight='bold', zorder=6)

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5])
    ax.set_xticklabels(['Very Low', 'Low', 'Medium', 'High', 'Very High'], fontsize=8)
    ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
    ax.set_yticklabels(['Very Low', 'Low', 'Medium', 'High', 'Very High'], fontsize=8)
    ax.set_xlabel('Impact', fontsize=10, fontweight='bold')
    ax.set_ylabel('Probability', fontsize=10, fontweight='bold')
    ax.set_title('Project Risk Matrix', fontsize=13, fontweight='bold', pad=15)

    # Legend
    legend_text = 'R1: Schedule Delay | R2: Scope Creep | R3: Tech Issues\nR4: Budget | R5: Team Conflict | R6: Data Loss | R7: Comm. Failure'
    ax.text(2.5, -0.5, legend_text, ha='center', fontsize=7.5,
            bbox=dict(boxstyle='round', facecolor='#F5F5F5', alpha=0.8))

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'risk_matrix.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] Risk matrix saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# 11. CRITICAL PATH TABLE CHART
# ═══════════════════════════════════════════════════════════════
def generate_critical_path():
    """Generate a Critical Path Analysis network diagram."""
    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')

    tasks = [
        (1, 3, 'A', 'Project\nInit', 2, True),
        (3.2, 4, 'B', 'Require-\nments', 5, True),
        (3.2, 2, 'C', 'Lit.\nReview', 8, False),
        (5.5, 4, 'D', 'Design', 10, True),
        (5.5, 2, 'E', 'DB\nDesign', 5, True),
        (8, 3, 'F', 'Website\nDev', 20, True),
        (10.5, 4, 'G', 'Testing', 10, True),
        (10.5, 2, 'H', 'Content', 6, False),
        (12.5, 3, 'I', 'Launch', 1, True),
    ]

    for tx, ty, tid, name, dur, critical in tasks:
        color = '#EF9A9A' if critical else '#B3E5FC'
        edge = '#C62828' if critical else '#0277BD'
        box = FancyBboxPatch((tx - 0.7, ty - 0.5), 1.4, 1,
                             boxstyle="round,pad=0.08", facecolor=color,
                             edgecolor=edge, linewidth=2 if critical else 1)
        ax.add_patch(box)
        ax.text(tx, ty + 0.2, f'{tid}: {name}', ha='center', va='center',
                fontsize=6.5, fontweight='bold')
        ax.text(tx, ty - 0.3, f'{dur}d', ha='center', va='center', fontsize=7)

    # Arrows
    connections = [
        (1, 3, 3.2, 4), (1, 3, 3.2, 2),
        (3.2, 4, 5.5, 4), (3.2, 4, 5.5, 2),
        (5.5, 4, 8, 3), (5.5, 2, 8, 3),
        (8, 3, 10.5, 4), (8, 3, 10.5, 2),
        (10.5, 4, 12.5, 3), (10.5, 2, 12.5, 3),
    ]

    for x1, y1, x2, y2 in connections:
        ax.annotate('', xy=(x2 - 0.7, y2), xytext=(x1 + 0.7, y1),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=1.2))

    ax.text(7, 0.5, 'Critical Path (Red): A → B → D → F → G → I = 48 days',
            ha='center', fontsize=10, fontweight='bold', color='#C62828',
            bbox=dict(boxstyle='round', facecolor='#FFEBEE', alpha=0.9))

    ax.set_title('Critical Path Analysis - Network Diagram', fontsize=13,
                 fontweight='bold', pad=15)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'critical_path.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[DIAGRAM] Critical path saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════
# GENERATE ALL DIAGRAMS
# ═══════════════════════════════════════════════════════════════
def generate_all_diagrams():
    """Generate all diagrams and return their file paths."""
    print("\n" + "="*60)
    print("  GENERATING ALL DIAGRAMS")
    print("="*60)

    paths = {
        'gantt_chart': generate_gantt_chart(),
        'wbs': generate_wbs(),
        'use_case': generate_use_case(),
        'activity': generate_activity_diagram(),
        'sequence': generate_sequence_diagram(),
        'er_diagram': generate_er_diagram(),
        'site_map': generate_site_map(),
        'pert_chart': generate_pert_chart(),
        'wireframes': generate_wireframes(),
        'risk_matrix': generate_risk_matrix(),
        'critical_path': generate_critical_path(),
    }

    print(f"\n[DONE] Generated {len(paths)} diagrams successfully.")
    return paths


if __name__ == '__main__':
    generate_all_diagrams()
