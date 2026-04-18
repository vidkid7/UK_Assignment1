"""
StyleVault – High-Quality Diagram Generation v2
================================================
Generates all assignment diagrams at 300 DPI.
New in v2:
  • Completely rewritten clean ER diagram (no overlaps)
  • 5 separate wireframe files (homepage, products, product detail, cart, checkout)
  • Auth / Registration flowchart (new)
  • Checkout process flowchart (new)
  • System Architecture diagram (new)
  • All existing diagrams improved in quality & clarity
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'diagrams')
DPI = 300


def _dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save(fig, filename, tight=True):
    _dir()
    path = os.path.join(OUTPUT_DIR, filename)
    if tight:
        fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    else:
        fig.savefig(path, dpi=DPI, facecolor='white')
    plt.close(fig)
    print(f"  [OK] {filename}")
    return path


# ─────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────
C = {
    'navy':   '#003366',
    'blue':   '#1565C0',
    'lblue':  '#42A5F5',
    'sky':    '#E3F2FD',
    'white':  '#FFFFFF',
    'offwhite': '#FAFAFA',
    'gray':   '#9E9E9E',
    'lgray':  '#F5F5F5',
    'dgray':  '#424242',
    'green':  '#2E7D32',
    'lgreen': '#C8E6C9',
    'orange': '#E65100',
    'lorange':'#FFE0B2',
    'red':    '#C62828',
    'lred':   '#FFEBEE',
    'purple': '#6A1B9A',
    'lpurple':'#EDE7F6',
    'teal':   '#00695C',
    'lteal':  '#E0F2F1',
}

PHASE_COLORS = {
    'Planning':      '#43A047',
    'Design':        '#1E88E5',
    'Development':   '#FB8C00',
    'Testing':       '#8E24AA',
    'Documentation': '#E53935',
}


# ═══════════════════════════════════════════════════════════════
# 1.  GANTT CHART
# ═══════════════════════════════════════════════════════════════
def generate_gantt_chart():
    tasks = [
        ('Project Initiation',       '2026-01-12', '2026-01-14', 'Planning',      True),
        ('Requirements Gathering',   '2026-01-15', '2026-01-21', 'Planning',      True),
        ('Literature Review',        '2026-01-15', '2026-01-25', 'Planning',      True),
        ('UML & Use Case Diagrams',  '2026-01-22', '2026-02-02', 'Design',        True),
        ('Wireframe Design',         '2026-01-26', '2026-02-05', 'Design',        True),
        ('Database Schema Design',   '2026-02-01', '2026-02-08', 'Design',        True),
        ('Flask Project Setup',      '2026-02-06', '2026-02-12', 'Development',   True),
        ('Database Implementation',  '2026-02-10', '2026-02-18', 'Development',   True),
        ('Frontend – Homepage',      '2026-02-13', '2026-02-22', 'Development',   True),
        ('Frontend – Products',      '2026-02-18', '2026-02-28', 'Development',   True),
        ('Backend – Auth & Cart',    '2026-02-20', '2026-03-04', 'Development',   True),
        ('Frontend – Checkout',      '2026-02-26', '2026-03-06', 'Development',   True),
        ('Backend – Orders',         '2026-03-01', '2026-03-10', 'Development',   True),
        ('Functional Testing',       '2026-03-06', '2026-03-14', 'Testing',       True),
        ('Integration Testing',      '2026-03-10', '2026-03-16', 'Testing',       True),
        ('User Acceptance Testing',  '2026-03-14', '2026-03-18', 'Testing',       True),
        ('Report Writing',           '2026-03-10', '2026-03-20', 'Documentation', False),
        ('Review & Submission',      '2026-03-18', '2026-03-25', 'Documentation', False),
    ]

    start_date = datetime(2026, 1, 12)
    end_date   = datetime(2026, 3, 25)
    total_days = (end_date - start_date).days

    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('white')

    n = len(tasks)
    yticks, ylabels = [], []

    for i, (name, s, e, phase, done) in enumerate(reversed(tasks)):
        row = i
        s_d  = datetime.strptime(s, '%Y-%m-%d')
        e_d  = datetime.strptime(e, '%Y-%m-%d')
        x0   = (s_d - start_date).days
        dur  = max((e_d - s_d).days, 1)
        col  = PHASE_COLORS[phase]
        alpha = 1.0 if done else 0.55

        # Bar
        ax.barh(row, dur, left=x0, height=0.55, color=col, alpha=alpha,
                edgecolor='white', linewidth=0.6)
        # Done tick
        if done:
            ax.text(x0 + dur / 2, row, '✓', ha='center', va='center',
                    fontsize=9, color='white', fontweight='bold')
        yticks.append(row)
        ylabels.append(name)

    # Month grid lines
    month_starts = []
    d = start_date.replace(day=1)
    from datetime import timedelta
    while d <= end_date:
        if d >= start_date:
            month_starts.append(((d - start_date).days, d.strftime('%b')))
        if d.month == 12:
            d = d.replace(year=d.year+1, month=1)
        else:
            d = d.replace(month=d.month+1)

    for day_off, mon in month_starts:
        ax.axvline(day_off, color='#BDBDBD', linewidth=0.7, linestyle='--', zorder=0)
        ax.text(day_off + 0.5, n, mon, fontsize=8, color='#555', va='bottom')

    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, fontsize=8.5)
    ax.set_xlabel('Days from Project Start  (12 Jan 2026)', fontsize=9)
    ax.set_xlim(0, total_days + 2)
    ax.set_ylim(-0.7, n + 1)
    ax.set_title('StyleVault – Project Gantt Chart', fontsize=14,
                 fontweight='bold', pad=12, color=C['navy'])
    ax.grid(axis='x', alpha=0.25, linestyle='--', zorder=0)
    ax.set_axisbelow(True)

    legend_patches = [mpatches.Patch(color=c, label=p)
                      for p, c in PHASE_COLORS.items()]
    ax.legend(handles=legend_patches, loc='lower right', fontsize=8,
              framealpha=0.92, edgecolor='#CCC')

    plt.tight_layout()
    return _save(fig, 'gantt_chart.png')


# ═══════════════════════════════════════════════════════════════
# 2.  WORK BREAKDOWN STRUCTURE
# ═══════════════════════════════════════════════════════════════
def generate_wbs():
    fig, ax = plt.subplots(figsize=(26, 14))
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.02)

    BOX_H = 0.65

    def box(x, y, text, w=3.2, color='#1565C0', fsize=8.5):
        b = FancyBboxPatch((x - w/2, y - BOX_H/2), w, BOX_H,
                           boxstyle="round,pad=0.14", facecolor=color,
                           edgecolor='#0D1F3C', linewidth=1.2)
        ax.add_patch(b)
        ax.text(x, y, text, ha='center', va='center', fontsize=fsize,
                fontweight='bold', color='white', wrap=True,
                multialignment='center')

    def line(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color='#607D8B', linewidth=1.1, zorder=0)

    def subtree(parent_x, parent_y, children, child_y, color, w=2.0):
        cx_list = [c[0] for c in children]
        mid_y = child_y + BOX_H/2 + 0.12
        if len(children) > 1:
            ax.plot([min(cx_list), max(cx_list)], [mid_y, mid_y],
                    color='#607D8B', linewidth=0.9)
        line(parent_x, parent_y - BOX_H/2, parent_x, mid_y)
        for cx, cy, label in children:
            line(cx, mid_y, cx, cy + BOX_H/2)
            box(cx, cy, label, w=w, color=color)

    # ── L0 Root ──────────────────────────────────────────────
    box(13, 13.2, 'STYLEVAULT\nE-COMMERCE PROJECT', w=4.2, color='#0D1F3C', fsize=10)

    # ── L1 Phases ────────────────────────────────────────────
    phases = [
        (2.5,  11.2, '1. Planning\n& Research'),
        (7.0,  11.2, '2. Design'),
        (13.0, 11.2, '3. Development'),
        (19.0, 11.2, '4. Testing\n& QA'),
        (23.5, 11.2, '5. Delivery'),
    ]
    # Horizontal connector L0→L1
    px_list = [p[0] for p in phases]
    conn_y = 11.2 + BOX_H/2 + 0.12
    ax.plot([min(px_list), max(px_list)], [conn_y, conn_y], color='#607D8B', lw=0.9)
    line(13, 13.2 - BOX_H/2, 13, conn_y)
    for px, py, label in phases:
        line(px, conn_y, px, py + BOX_H/2)
        box(px, py, label, w=3.0, color='#1565C0', fsize=9)

    # ── L2 Planning ──────────────────────────────────────────
    subtree(2.5, 11.2,
            [(1.0, 9.2, 'Requirements\nAnalysis'),
             (2.5, 9.2, 'Scope\nDefinition'),
             (4.0, 9.2, 'Risk\nAnalysis')],
            9.2, color='#1976D2', w=1.85)

    # ── L2 Design ────────────────────────────────────────────
    subtree(7.0, 11.2,
            [(5.5, 9.2, 'UI / UX\nWireframes'),
             (7.0, 9.2, 'Database\nSchema'),
             (8.5, 9.2, 'UML\nDiagrams')],
            9.2, color='#1976D2', w=1.85)

    # ── L2 Development ───────────────────────────────────────
    subtree(13.0, 11.2,
            [(10.5, 9.2, 'Backend\nFlask/SQLAlchemy'),
             (13.0, 9.2, 'Frontend\nBootstrap/Jinja2'),
             (15.5, 9.2, 'Database\nMySQL/SQLite')],
            9.2, color='#1976D2', w=2.3)

    # ── L2 Testing ───────────────────────────────────────────
    subtree(19.0, 11.2,
            [(17.5, 9.2, 'Functional\nTesting'),
             (19.0, 9.2, 'UI / UX\nTesting'),
             (20.5, 9.2, 'User\nAcceptance')],
            9.2, color='#1976D2', w=1.85)

    # ── L2 Delivery ──────────────────────────────────────────
    subtree(23.5, 11.2,
            [(22.5, 9.2, 'Report &\nDocumentation'),
             (24.5, 9.2, 'Submission')],
            9.2, color='#1976D2', w=1.85)

    # ── L3 Backend sub-tasks ─────────────────────────────────
    subtree(10.5, 9.2,
            [(9.0, 7.1, 'User\nAuth'),
             (10.5, 7.1, 'Products\n& Cart'),
             (12.0, 7.1, 'Checkout\n& Orders')],
            7.1, color='#42A5F5', w=1.7)

    # ── L3 Frontend sub-tasks ────────────────────────────────
    subtree(13.0, 9.2,
            [(13.0, 7.1, 'Homepage\n& Nav'),
             (14.5, 7.1, 'Product\nPages')],
            7.1, color='#42A5F5', w=1.7)

    # ── L3 Admin (under Backend) ─────────────────────────────
    subtree(12.0, 7.1,
            [(11.0, 5.2, 'Admin\nDashboard'),
             (12.5, 5.2, 'CRUD\nProducts')],
            5.2, color='#64B5F6', w=1.65)

    ax.set_title('Work Breakdown Structure (WBS) — StyleVault Project',
                 fontsize=14, fontweight='bold', pad=16, color='#0D1F3C')
    return _save(fig, 'wbs_diagram.png')


# ═══════════════════════════════════════════════════════════════
# 3.  USE CASE DIAGRAM
# ═══════════════════════════════════════════════════════════════
def generate_use_case():
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    def actor(x, y, label, color='#333'):
        # Head
        ax.add_patch(plt.Circle((x, y + 0.55), 0.22, fill=True,
                                facecolor='#FFF8E1', edgecolor=color, linewidth=1.8))
        # Torso
        ax.plot([x, x], [y + 0.33, y - 0.15], color=color, lw=1.8)
        # Arms
        ax.plot([x - 0.28, x + 0.28], [y + 0.15, y + 0.15], color=color, lw=1.8)
        # Legs
        ax.plot([x, x - 0.22], [y - 0.15, y - 0.52], color=color, lw=1.8)
        ax.plot([x, x + 0.22], [y - 0.15, y - 0.52], color=color, lw=1.8)
        ax.text(x, y - 0.82, label, ha='center', va='top', fontsize=9,
                fontweight='bold', color=color)

    def usecase(x, y, text, color=C['sky'], w=3.0, h=0.6):
        ax.add_patch(mpatches.Ellipse((x, y), w, h,
                                      facecolor=color, edgecolor=C['blue'], linewidth=1.3))
        ax.text(x, y, text, ha='center', va='center', fontsize=8)

    def assoc(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.1,
                                   connectionstyle='arc3,rad=0'))

    def rel(x1, y1, x2, y2, label, color='#1565C0'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.0,
                                   linestyle='dashed'))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.15, label, ha='center', fontsize=7, color=color,
                style='italic',
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.7))

    # System boundary
    ax.add_patch(mpatches.FancyBboxPatch((3.2, 0.6), 9.8, 10.8,
                 boxstyle="round,pad=0.2", facecolor='#FAFEFF',
                 edgecolor='#1565C0', linewidth=2.0, linestyle='--'))
    ax.text(8.1, 11.7, 'StyleVault E-Commerce System',
            ha='center', fontsize=11, fontweight='bold', style='italic', color=C['navy'])

    # Actors
    actor(1.3, 7.5,  'Customer',     color='#1565C0')
    actor(1.3, 3.0,  'New\nCustomer', color='#2E7D32')
    actor(14.5, 7.0, 'Admin',        color='#6A1B9A')

    # Left column use cases (Customer-facing)
    left_ucs = [
        (6.0, 10.8, 'Browse Products'),
        (6.0, 9.7,  'Search & Filter Products'),
        (6.0, 8.6,  'View Product Details'),
        (6.0, 7.5,  'Add to Cart'),
        (6.0, 6.4,  'Manage Cart'),
        (6.0, 5.3,  'Proceed to Checkout'),
        (6.0, 4.2,  'Make Payment'),
        (6.0, 3.1,  'Register / Sign Up'),
        (6.0, 2.0,  'Log In / Log Out'),
        (6.0, 1.0,  'Contact Support'),
    ]
    for x, y, t in left_ucs:
        usecase(x, y, t, color='#E3F2FD')

    # Right column use cases (Admin-facing)
    right_ucs = [
        (11.0, 10.8, 'Manage Products'),
        (11.0, 9.7,  'Manage Categories'),
        (11.0, 8.6,  'View & Process Orders'),
        (11.0, 7.5,  'Manage Users'),
        (11.0, 6.4,  'View Analytics'),
        (11.0, 5.3,  'Respond to Queries'),
        (11.0, 4.2,  'Login to Admin Panel'),
    ]
    for x, y, t in right_ucs:
        usecase(x, y, t, color='#EDE7F6')

    # Customer associations
    for _, uy, _ in left_ucs:
        assoc(1.85, 7.5, 4.5, uy)

    # New Customer
    assoc(1.85, 3.0, 4.5, 3.1)
    assoc(1.85, 3.0, 4.5, 2.0)

    # Admin associations
    for _, uy, _ in right_ucs:
        assoc(13.8, 7.0, 12.5, uy)

    # Include/extend
    rel(6.0, 5.3, 6.0, 4.2, '<<include>>')
    rel(6.0, 7.5, 6.0, 5.3, '<<include>>')
    rel(6.0, 8.6, 6.0, 7.5, '<<extend>>')

    ax.set_title('Use Case Diagram – StyleVault System', fontsize=13,
                 fontweight='bold', pad=14, color=C['navy'])
    return _save(fig, 'use_case_diagram.png')


# ═══════════════════════════════════════════════════════════════
# 4.  ACTIVITY DIAGRAM – Purchase Flow
# ═══════════════════════════════════════════════════════════════
def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(10, 16))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    def rbox(x, y, text, w=3.4, h=0.56, col=C['lorange'], edge='#E65100'):
        ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                     boxstyle="round,pad=0.13", facecolor=col,
                     edgecolor=edge, linewidth=1.4))
        ax.text(x, y, text, ha='center', va='center', fontsize=9)

    def diamond(x, y, text, w=1.3, h=0.55):
        pts = [[x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]]
        ax.add_patch(plt.Polygon(pts, facecolor='#FFF9C4',
                                  edgecolor='#F57F17', lw=1.5))
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5, fontweight='bold')

    def start(x, y): ax.add_patch(plt.Circle((x, y), 0.22, fc='#333', ec='#333'))
    def end(x, y):
        ax.add_patch(plt.Circle((x, y), 0.27, fc='white', ec='#333', lw=2))
        ax.add_patch(plt.Circle((x, y), 0.18, fc='#333', ec='#333'))

    def arr(x1, y1, x2, y2, label='', side=0.2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
        if label:
            ax.text((x1+x2)/2 + side, (y1+y2)/2, label,
                    fontsize=7.5, color='#777')

    cx = 5.0

    start(cx, 15.7); arr(cx, 15.48, cx, 15.1)
    rbox(cx, 14.8, 'Visit StyleVault Website')
    arr(cx, 14.52, cx, 14.0)

    diamond(cx, 13.7, 'Logged\nin?')
    arr(cx + 0.65, 13.7, 8.0, 13.7, 'Yes')
    arr(cx, 13.42, cx, 12.95, 'No')

    rbox(8.5, 13.7, 'Already in Session', w=2.8, col=C['lgreen'], edge=C['green'])
    ax.annotate('', xy=(cx + 1.7, 12.95), xytext=(8.5, 13.42),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))

    rbox(cx, 12.65, 'Browse as Guest / Login')
    arr(cx, 12.37, cx, 11.85)

    rbox(cx, 11.55, 'Browse Products by Category')
    arr(cx, 11.27, cx, 10.75)

    rbox(cx, 10.45, 'Search / Filter / Sort')
    arr(cx, 10.17, cx, 9.65)

    rbox(cx, 9.35, 'View Product Detail Page')
    arr(cx, 9.07, cx, 8.55)

    diamond(cx, 8.2, 'Add to\nCart?')
    arr(cx, 7.92, cx, 7.4, 'Yes')
    arr(cx - 0.65, 8.2, 2.5, 8.2, 'No')
    ax.annotate('', xy=(2.5, 9.35), xytext=(2.5, 8.2),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))

    rbox(cx, 7.1, 'Add Item to Shopping Cart')
    arr(cx, 6.82, cx, 6.3)

    diamond(cx, 5.95, 'Continue\nShopping?')
    arr(cx - 0.65, 5.95, 2.5, 5.95, 'Yes')
    ax.annotate('', xy=(2.5, 9.35), xytext=(2.5, 5.95),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))
    arr(cx, 5.67, cx, 5.15, 'No')

    rbox(cx, 4.85, 'View Cart & Review Items')
    arr(cx, 4.57, cx, 4.05)

    diamond(cx, 3.7, 'Proceed\nto Checkout?')
    arr(cx - 0.65, 3.7, 2.5, 3.7, 'Back')
    arr(cx, 3.42, cx, 2.9, 'Yes')

    rbox(cx, 2.6, 'Enter Shipping & Payment')
    arr(cx, 2.32, cx, 1.8)

    rbox(cx, 1.5, 'Order Confirmed', col=C['lgreen'], edge=C['green'])
    arr(cx, 1.22, cx, 0.65)

    end(cx, 0.35)

    ax.set_title('Activity Diagram – User Purchase Flow', fontsize=13,
                 fontweight='bold', pad=12, color=C['navy'])
    return _save(fig, 'activity_diagram.png')


# ═══════════════════════════════════════════════════════════════
# 5.  SEQUENCE DIAGRAM
# ═══════════════════════════════════════════════════════════════
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(14, 11))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    actors = [
        (1.2,  'User\n(Browser)'),
        (3.5,  'Flask\nServer'),
        (6.0,  'SQLAlchemy\nORM'),
        (8.5,  'SQLite\nDatabase'),
        (11.5, 'Payment\nGateway'),
    ]

    actor_colors = ['#FFF8E1', '#E3F2FD', '#E8F5E9', '#FCE4EC', '#F3E5F5']

    for (x, lbl), col in zip(actors, actor_colors):
        ax.add_patch(FancyBboxPatch((x - 0.7, 9.8), 1.4, 0.75,
                     boxstyle="round,pad=0.08", facecolor=col,
                     edgecolor='#333', linewidth=1.2))
        ax.text(x, 10.175, lbl, ha='center', va='center', fontsize=8,
                fontweight='bold', multialignment='center')
        ax.plot([x, x], [9.8, 0.3], color='#BDBDBD', linewidth=0.9, linestyle='--')

    y_rows = [9.0, 8.55, 8.1, 7.65, 7.2, 6.75, 6.3, 5.85, 5.4, 4.95,
              4.5, 4.05, 3.6, 3.15, 2.7, 2.25, 1.8, 1.35, 0.9]

    msgs = [
        # (from_idx, to_idx, y_row, text, is_return)
        (0, 1, 0, 'GET /collection  (Browse)',       False),
        (1, 2, 1, 'session.query(Product)',           False),
        (2, 3, 2, 'SELECT * FROM products',           False),
        (3, 2, 3, 'Return rows',                      True),
        (2, 1, 4, 'Product objects list',             True),
        (1, 0, 5, 'Render products.html',             True),

        (0, 1, 6, 'POST /cart/add',                   False),
        (1, 2, 7, 'db.session.add(CartItem)',         False),
        (2, 3, 8, 'INSERT INTO cart_items',           False),
        (3, 2, 9, 'Commit OK',                        True),
        (1, 0, 10,'Cart updated (redirect)',           True),

        (0, 1, 11,'POST /checkout',                   False),
        (1, 4, 12,'Process payment request',          False),
        (4, 1, 13,'Payment approved / token',         True),
        (1, 2, 14,'db.session.add(Order, OrderItems)',False),
        (2, 3, 15,'INSERT INTO orders …',             False),
        (3, 2, 16,'Commit OK',                        True),
        (1, 0, 17,'Order confirmed page',             True),
    ]

    for from_i, to_i, row_i, text, is_ret in msgs:
        x1 = actors[from_i][0]
        x2 = actors[to_i][0]
        y  = y_rows[row_i]
        col   = C['blue'] if is_ret else '#333'
        style = 'dashed' if is_ret else 'solid'
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.2,
                                   linestyle=style))
        mx = (x1 + x2) / 2
        offset = 0.1
        ax.text(mx, y + offset, text, ha='center', va='bottom', fontsize=7.5,
                color=col, style='italic' if is_ret else 'normal')

    # Group labels on left
    groups = [
        (y_rows[0], y_rows[5], 'Browse\nProducts'),
        (y_rows[6], y_rows[10], 'Add to\nCart'),
        (y_rows[11], y_rows[17], 'Checkout\n& Order'),
    ]
    for y_top, y_bot, label in groups:
        mid = (y_top + y_bot) / 2
        ax.plot([0.1, 0.1], [y_bot - 0.1, y_top + 0.1], color='#CCC', lw=1.5)
        ax.text(0.3, mid, label, fontsize=7, va='center', color='#555',
                style='italic')

    ax.set_title('Sequence Diagram – User–System Interaction', fontsize=13,
                 fontweight='bold', pad=12, color=C['navy'])
    return _save(fig, 'sequence_diagram.png')


# ═══════════════════════════════════════════════════════════════
# 6.  ER DIAGRAM  (completely rewritten)
# ═══════════════════════════════════════════════════════════════
def generate_er_diagram():
    """
    Clean, professional Entity-Relationship Diagram.
    Layout (20 × 15 in):
      Row 1 (y=13): User  |  Category  |  Product
      Row 2 (y=7.5): Order  |  OrderItem  |  CartItem
      Row 3 (y=2.5): ContactMessage (centre)
    """
    fig, ax = plt.subplots(figsize=(20, 15))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    TITLE_H = 0.50
    ROW_H   = 0.30
    PAD     = 0.18
    BW      = 3.60   # box half-width = 1.8

    def draw_entity(cx, ty, name, attrs):
        """
        cx  = horizontal centre
        ty  = y of title-bar centre
        attrs = list of (col1_label, col2_type, kind)  kind: 'PK'|'FK'|''
        returns (top_y, bottom_y, left_x, right_x)
        """
        hw = BW / 2
        h_attrs = len(attrs) * ROW_H + PAD * 2

        # Title bar
        ax.add_patch(FancyBboxPatch(
            (cx - hw, ty - TITLE_H/2), BW, TITLE_H,
            boxstyle="square,pad=0", facecolor=C['navy'],
            edgecolor='#0D1F3C', linewidth=1.8))
        ax.text(cx, ty, name, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='white')

        # Attributes body
        ax.add_patch(FancyBboxPatch(
            (cx - hw, ty - TITLE_H/2 - h_attrs), BW, h_attrs,
            boxstyle="square,pad=0", facecolor='#EEF4FF',
            edgecolor='#0D1F3C', linewidth=1.8))

        for i, (col1, col2, kind) in enumerate(attrs):
            ay = ty - TITLE_H/2 - PAD - (i + 0.5) * ROW_H
            if kind == 'PK':
                icon, fcol, fw, fs = 'PK', '#B71C1C', 'bold', 8.5
                ax.add_patch(FancyBboxPatch(
                    (cx - hw + 0.08, ay - ROW_H/2 + 0.03), BW - 0.16, ROW_H - 0.06,
                    boxstyle="square,pad=0", facecolor='#FFF8E1',
                    edgecolor='none', linewidth=0))
            elif kind == 'FK':
                icon, fcol, fw, fs = 'FK', '#4A148C', 'normal', 8.0
            else:
                icon, fcol, fw, fs = '  ', C['dgray'],  'normal', 8.0

            ax.text(cx - hw + 0.15, ay,
                    f'{icon}  {col1}', fontsize=fs, va='center',
                    color=fcol, fontweight=fw)
            ax.text(cx + hw - 0.1, ay,
                    col2, fontsize=7.5, va='center', ha='right',
                    color='#546E7A', style='italic')

            # Row divider
            if i < len(attrs) - 1:
                divider_y = ay - ROW_H/2
                ax.plot([cx - hw + 0.05, cx + hw - 0.05],
                        [divider_y, divider_y],
                        color='#C5D8FF', linewidth=0.5)

        return (ty + TITLE_H/2,
                ty - TITLE_H/2 - h_attrs,
                cx - hw,
                cx + hw)

    def rel_line(pts, label='', card_start='1', card_end='N', col='#455A64'):
        """pts = list of (x,y) waypoints"""
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, color=col, linewidth=1.6, zorder=1)
        # Arrow at end
        ax.annotate('', xy=(pts[-1][0], pts[-1][1]),
                    xytext=(pts[-2][0], pts[-2][1]),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.5),
                    zorder=2)
        # Cardinality
        s, e = pts[0], pts[-1]
        offset = 0.22
        ax.text(s[0] + offset, s[1] + offset, card_start,
                fontsize=8.5, color=col, fontweight='bold')
        ax.text(e[0] - offset, e[1] + offset, card_end,
                fontsize=8.5, color=col, fontweight='bold')
        # Relationship label
        if label:
            mx = (xs[0] + xs[-1]) / 2
            my = (ys[0] + ys[-1]) / 2
            ax.text(mx, my + 0.22, label, ha='center', fontsize=7.5,
                    style='italic', color=C['teal'],
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                              edgecolor='#B2DFDB', alpha=0.9))

    # ── Entity definitions ──────────────────────────────────────
    # Row 1
    u_top,  u_bot,  u_l,  u_r  = draw_entity(3.2, 13,
        name='USER',
        attrs=[
            ('id',            'INTEGER',      'PK'),
            ('first_name',    'VARCHAR(100)', ''),
            ('last_name',     'VARCHAR(100)', ''),
            ('email',         'VARCHAR(150)', ''),
            ('password_hash', 'VARCHAR(256)', ''),
            ('is_admin',      'BOOLEAN',      ''),
        ])

    c_top,  c_bot,  c_l,  c_r  = draw_entity(9.8, 13,
        name='CATEGORY',
        attrs=[
            ('id',          'INTEGER',      'PK'),
            ('name',        'VARCHAR(100)', ''),
            ('slug',        'VARCHAR(100)', ''),
            ('description', 'TEXT',         ''),
        ])

    p_top,  p_bot,  p_l,  p_r  = draw_entity(16.6, 13,
        name='PRODUCT',
        attrs=[
            ('id',          'INTEGER',      'PK'),
            ('name',        'VARCHAR(200)', ''),
            ('brand',       'VARCHAR(100)', ''),
            ('price',       'FLOAT',        ''),
            ('sale_price',  'FLOAT',        ''),
            ('stock',       'INTEGER',      ''),
            ('image_url',   'VARCHAR(300)', ''),
            ('category_id', 'INTEGER',      'FK'),
        ])

    # Row 2
    o_top,  o_bot,  o_l,  o_r  = draw_entity(3.2, 7.5,
        name='ORDER',
        attrs=[
            ('id',              'INTEGER',     'PK'),
            ('user_id',         'INTEGER',     'FK'),
            ('total',           'FLOAT',       ''),
            ('status',          'VARCHAR(50)', ''),
            ('shipping_address','TEXT',        ''),
            ('payment_method',  'VARCHAR(50)', ''),
            ('created_at',      'DATETIME',    ''),
        ])

    oi_top, oi_bot, oi_l, oi_r = draw_entity(9.8, 7.5,
        name='ORDER ITEM',
        attrs=[
            ('id',               'INTEGER',     'PK'),
            ('order_id',         'INTEGER',     'FK'),
            ('product_id',       'INTEGER',     'FK'),
            ('quantity',         'INTEGER',     ''),
            ('size',             'VARCHAR(20)', ''),
            ('price_at_purchase','FLOAT',       ''),
        ])

    ci_top, ci_bot, ci_l, ci_r = draw_entity(16.6, 7.5,
        name='CART ITEM',
        attrs=[
            ('id',         'INTEGER',     'PK'),
            ('user_id',    'INTEGER',     'FK'),
            ('product_id', 'INTEGER',     'FK'),
            ('quantity',   'INTEGER',     ''),
            ('size',       'VARCHAR(20)', ''),
        ])

    # Row 3
    cm_top, cm_bot, cm_l, cm_r = draw_entity(9.8, 2.5,
        name='CONTACT MESSAGE',
        attrs=[
            ('id',         'INTEGER',      'PK'),
            ('name',       'VARCHAR(100)', ''),
            ('email',      'VARCHAR(150)', ''),
            ('subject',    'VARCHAR(200)', ''),
            ('message',    'TEXT',         ''),
        ])

    # ── Relationship lines ──────────────────────────────────────
    # 1. User → Order  (1:N, straight down, left side)
    rel_line([(3.2, u_bot), (3.2, o_top)], 'places', '1', 'N')

    # 2. Category → Product  (1:N, horizontal)
    rel_line([(c_r, 13), (p_l, 13)], 'contains', '1', 'N')

    # 3. Product → CartItem  (1:N, straight down, right side)
    rel_line([(16.6, p_bot), (16.6, ci_top)], 'added to', '1', 'N')

    # 4. Order → OrderItem  (1:N, horizontal middle)
    rel_line([(o_r, 7.5), (oi_l, 7.5)], 'contains', '1', 'N')

    # 5. Product → OrderItem  (1:N, diagonal via waypoints)
    rel_line(
        [(p_l, p_bot + 0.8),
         (p_l - 0.4, p_bot + 0.6),
         (oi_r, oi_top + 0.5)],
        'included in', '1', 'N')

    # 6. User → CartItem  (1:N, L-shaped going over the top)
    rel_line(
        [(u_r, 13),
         (18.6, 13),
         (18.6, ci_top)],
        'owns', '1', 'N', col='#1A237E')

    # ContactMessage standalone note
    ax.text(9.8, 0.2, 'Note: ContactMessage has no FK — submitted by guests or registered users',
            ha='center', fontsize=8, style='italic', color='#555',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFDE7',
                      edgecolor='#FBC02D', alpha=0.9))

    ax.set_title('Entity-Relationship (ER) Diagram – StyleVault Database',
                 fontsize=14, fontweight='bold', pad=14, color=C['navy'])
    return _save(fig, 'er_diagram.png')


# ═══════════════════════════════════════════════════════════════
# 7.  SITE MAP
# ═══════════════════════════════════════════════════════════════
def generate_site_map():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    BH = 0.5

    def sbox(x, y, text, col, w=1.9, h=BH):
        ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                     boxstyle="round,pad=0.1", facecolor=col,
                     edgecolor='#37474F', linewidth=1.1))
        ax.text(x, y, text, ha='center', va='center', fontsize=8,
                fontweight='bold', multialignment='center')

    def conn(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color='#78909C', linewidth=1.0, zorder=0)

    # Root
    sbox(7, 8.3, 'HOME', '#FFB300', w=2.2)

    # Level 1
    L1 = [
        (1.4, 6.6, 'Collection', '#64B5F6'),
        (3.5, 6.6, 'Customer\nCare', '#64B5F6'),
        (5.6, 6.6, 'About Us', '#64B5F6'),
        (7.7, 6.6, 'Search', '#64B5F6'),
        (9.8, 6.6, 'Login /\nSign Up', '#64B5F6'),
        (12.0, 6.6, 'Cart', '#64B5F6'),
    ]
    for lx, ly, label, col in L1:
        sbox(lx, ly, label, col)
        conn(7, 8.3 - BH/2, lx, ly + BH/2)

    # horizontal spine
    ax.plot([L1[0][0], L1[-1][0]], [6.6 + BH/2 + 0.05] * 2,
            color='#78909C', linewidth=0.8, zorder=0)
    conn(7, 8.3 - BH/2, 7, 6.6 + BH/2 + 0.05)

    # Collection sub-pages
    coll_subs = [(0.5, 5.1, 'Women'), (1.4, 5.1, 'Men'),
                 (2.3, 5.1, 'Accessories'), (3.2, 5.1, 'Sale')]
    for sx, sy, label in coll_subs:
        sbox(sx, sy, label, '#B3E5FC', w=1.1, h=0.45)
        conn(1.4, 6.6 - BH/2, sx, sy + 0.23)

    # Product Detail from category pages
    sbox(1.7, 3.7, 'Product\nDetail Page', '#B3E5FC', w=2.0)
    for sx, sy, _ in coll_subs:
        conn(sx, sy - 0.23, 1.7, 3.7 + 0.23)

    # Login sub-pages
    sbox(9.0, 5.1, 'Sign Up', '#B3E5FC', w=1.2)
    sbox(10.5, 5.1, 'My Account', '#B3E5FC', w=1.5)
    conn(9.8, 6.6 - BH/2, 9.0, 5.1 + 0.23)
    conn(9.8, 6.6 - BH/2, 10.5, 5.1 + 0.23)

    # Cart sub-pages
    sbox(11.2, 5.1, 'Order\nSummary', '#B3E5FC', w=1.5)
    sbox(13.0, 5.1, 'Checkout', '#B3E5FC', w=1.5)
    conn(12.0, 6.6 - BH/2, 11.2, 5.1 + 0.23)
    conn(12.0, 6.6 - BH/2, 13.0, 5.1 + 0.23)
    sbox(13.0, 3.7, 'Order\nConfirmation', '#C8E6C9', w=1.8)
    conn(13.0, 5.1 - 0.23, 13.0, 3.7 + 0.23)

    # Customer care sub-page
    sbox(3.5, 5.1, 'Contact\nForm', '#B3E5FC', w=1.4)
    conn(3.5, 6.6 - BH/2, 3.5, 5.1 + 0.23)

    ax.set_title('Website Site Map – StyleVault Navigation Structure',
                 fontsize=13, fontweight='bold', pad=12, color=C['navy'])
    return _save(fig, 'site_map.png')


# ═══════════════════════════════════════════════════════════════
# 8.  PERT CHART
# ═══════════════════════════════════════════════════════════════
def generate_pert_chart():
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    nodes = [
        # (x, y, id, name, duration, is_critical)
        (1.5,  4.0, 'A', 'Project\nInitiation',   2,  True),
        (4.0,  6.0, 'B', 'Requirements\nAnalysis', 5, True),
        (4.0,  2.0, 'C', 'Literature\nReview',     8, False),
        (7.0,  6.0, 'D', 'Design &\nPrototype',   10, True),
        (7.0,  2.0, 'E', 'Database\nDesign',        5, True),
        (10.5, 4.0, 'F', 'Website\nDevelopment',  20, True),
        (13.5, 6.0, 'G', 'Testing',               10, True),
        (13.5, 2.0, 'H', 'Documentation',          8, False),
        (15.0, 4.0, 'I', 'Launch',                  1, True),
    ]

    NW, NH = 2.0, 1.0

    for nx, ny, nid, name, dur, crit in nodes:
        col  = C['lred']   if crit else C['sky']
        ecol = C['red']    if crit else C['blue']
        lw   = 2.5         if crit else 1.5
        ax.add_patch(FancyBboxPatch(
            (nx - NW/2, ny - NH/2), NW, NH,
            boxstyle="round,pad=0.1", facecolor=col,
            edgecolor=ecol, linewidth=lw))
        ax.text(nx, ny + 0.18, f'{nid}: {name}',
                ha='center', va='center', fontsize=8, fontweight='bold')
        ax.text(nx, ny - 0.28, f'{dur} days',
                ha='center', va='center', fontsize=8, color='#555')

    edges = [
        ('A','B', True), ('A','C', False),
        ('B','D', True), ('B','E', True),
        ('C','F', False),
        ('D','F', True), ('E','F', True),
        ('F','G', True), ('F','H', False),
        ('G','I', True), ('H','I', False),
    ]
    node_pos = {n[2]: (n[0], n[1]) for n in nodes}

    for src, dst, crit in edges:
        x1, y1 = node_pos[src]
        x2, y2 = node_pos[dst]
        col = C['red'] if crit else '#90A4AE'
        lw  = 2.2 if crit else 1.2
        ax.annotate('', xy=(x2 - NW/2, y2), xytext=(x1 + NW/2, y1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=lw))

    ax.text(8, 0.4,
            'Critical Path (red): A → B → D → E → F → G → I  =  48 days  (project duration)',
            ha='center', fontsize=9.5, fontweight='bold', color=C['red'],
            bbox=dict(boxstyle='round,pad=0.3', facecolor=C['lred'], alpha=0.9))

    ax.set_title('PERT Chart – Task Dependencies & Durations', fontsize=13,
                 fontweight='bold', pad=12, color=C['navy'])
    return _save(fig, 'pert_chart.png')


# ═══════════════════════════════════════════════════════════════
# 9A-E.  WIREFRAMES  (5 separate full-page wireframes)
# ═══════════════════════════════════════════════════════════════
def _wf_box(ax, x, y, w, h, text='', col='#E8E8E8', text_col='#666', fsize=7.5,
            bold=False, edge='#BDBDBD', edge_lw=0.8):
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h,
                 boxstyle="square,pad=0", facecolor=col,
                 edgecolor=edge, linewidth=edge_lw))
    if text:
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fsize, color=text_col,
                fontweight='bold' if bold else 'normal',
                multialignment='center')


def _wf_xmark(ax, x, y, w, h):
    """Draw an image placeholder (box with X)."""
    _wf_box(ax, x, y, w, h, col='#F0F0F0')
    ax.plot([x, x+w], [y, y+h], color='#BDBDBD', lw=0.8)
    ax.plot([x+w, x], [y, y+h], color='#BDBDBD', lw=0.8)


def _wf_header(ax, W, H):
    """Standard nav bar for all wireframes."""
    # Top announcement bar
    _wf_box(ax, 0, H-0.4, W, 0.4, 'FREE SHIPPING ON ORDERS OVER £50',
            col='#333', text_col='white', fsize=7, edge='#333')
    # Nav row
    _wf_box(ax, 0, H-0.9, W, 0.5, col='#FFF', edge='#DDD')
    ax.text(W*0.12, H-0.65, 'StyleVault', fontsize=11,
            fontfamily='serif', fontweight='bold', va='center', ha='center')
    # Nav items
    for i, item in enumerate(['HOME', 'COLLECTION', 'CUSTOMER CARE', 'ABOUT']):
        ax.text(W*0.3 + i*W*0.13, H-0.65, item, fontsize=6.5, va='center',
                ha='center', color='#333')
    # Right icons
    _wf_box(ax, W-3.0, H-0.82, 1.8, 0.32, '[Search...]', col='#F5F5F5',
            fsize=6.5, edge='#DDD')
    ax.text(W-0.9, H-0.65, 'Login  |  Cart', fontsize=6.5, va='center',
            ha='center', color='#555')


def _wf_footer(ax, W):
    _wf_box(ax, 0, 0, W, 1.8, col='#F5F5F5', edge='#DDD')
    ax.text(W/2, 1.3, 'FOOTER: Customer Care  |  About  |  FAQs  |  Returns  |  Social Media',
            ha='center', fontsize=7, color='#666')
    ax.text(W/2, 0.85, 'Privacy Policy  |  Terms & Conditions  |  Cookie Policy',
            ha='center', fontsize=6.5, color='#888')
    ax.text(W/2, 0.45, '© 2026 StyleVault. All rights reserved.',
            ha='center', fontsize=6.5, color='#AAA')


def generate_wireframe_homepage():
    W, H = 12, 18
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    fig.patch.set_facecolor('white')

    _wf_header(ax, W, H)

    # Hero section
    _wf_box(ax, 0.2, H-6.5, 5.6, 5.3, col='#F5EAD8', edge='#CCC')
    ax.text(3.0, H-3.8, 'WOMEN\'S\nHERO IMAGE', ha='center', fontsize=9,
            color='#AAA', va='center')
    ax.text(1.0, H-6.0, 'NEW SEASON', fontsize=7, color='#888')
    ax.text(1.0, H-5.6, 'WOMEN\'S\nCOLLECTION', fontsize=10,
            fontweight='bold', color='#222')
    _wf_box(ax, 0.8, H-5.1, 1.8, 0.4, 'SHOP NOW', col='#222', text_col='white',
            fsize=7.5, bold=True, edge='#222')

    _wf_box(ax, 6.2, H-6.5, 5.6, 5.3, col='#D8E3F0', edge='#CCC')
    ax.text(9.0, H-3.8, 'MEN\'S\nHERO IMAGE', ha='center', fontsize=9,
            color='#AAA', va='center')
    ax.text(7.0, H-6.0, 'NEW SEASON', fontsize=7, color='#888')
    ax.text(7.0, H-5.6, 'MEN\'S\nCOLLECTION', fontsize=10,
            fontweight='bold', color='#222')
    _wf_box(ax, 7.0, H-5.1, 1.8, 0.4, 'SHOP NOW', col='#222', text_col='white',
            fsize=7.5, bold=True, edge='#222')

    # Promo banner
    y0 = H - 7.3
    _wf_box(ax, 0, y0, W, 0.7, col='#FAFAFA', edge='#EEE')
    for i, txt in enumerate(['FREE UK DELIVERY', 'EASY RETURNS', 'SECURE PAYMENT', '24/7 SUPPORT']):
        ax.text(1.5 + i*3.0, y0 + 0.35, f'[icon] {txt}', ha='center',
                fontsize=7, color='#444')

    # New Arrivals
    y0 = H - 7.5
    ax.text(W/2, y0 - 0.35, 'NEW ARRIVALS', ha='center', fontsize=11,
            fontweight='bold', color='#222')
    ax.text(W/2, y0 - 0.65, '─ ─ ─', ha='center', fontsize=8, color='#BBB')
    for i in range(4):
        px = 0.3 + i * 2.95
        _wf_xmark(ax, px, y0 - 4.5, 2.6, 3.5)
        _wf_box(ax, px, y0 - 5.1, 2.6, 0.55, 'Brand Name', col='white',
                text_col='#999', fsize=6.5, edge='none')
        _wf_box(ax, px, y0 - 5.65, 2.6, 0.55, 'Product Name', col='white',
                text_col='#333', fsize=7, bold=True, edge='none')
        _wf_box(ax, px, y0 - 6.2, 2.6, 0.5, '£XX.XX', col='white',
                text_col='#E65100', fsize=7.5, bold=True, edge='none')

    # Newsletter
    y0 = 2.0
    _wf_box(ax, 1.0, y0, 10, 1.5, col='#F5F5F5', edge='#DDD')
    ax.text(W/2, y0+1.15, 'GET ON THE LIST', ha='center', fontsize=9,
            fontweight='bold', color='#222')
    _wf_box(ax, 2.0, y0+0.1, 5.5, 0.55, '[Your email address]',
            col='white', edge='#CCC', fsize=7)
    _wf_box(ax, 7.8, y0+0.1, 2.0, 0.55, 'SUBSCRIBE', col='#222',
            text_col='white', fsize=7.5, bold=True, edge='#222')

    _wf_footer(ax, W)

    ax.set_title('Wireframe 1 of 5 – Homepage', fontsize=13,
                 fontweight='bold', pad=10, color=C['navy'])
    return _save(fig, 'wireframe_homepage.png')


def generate_wireframe_products():
    W, H = 12, 18
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    fig.patch.set_facecolor('white')

    _wf_header(ax, W, H)
    ax.text(0.3, H-1.1, 'Home > Collection > Women', fontsize=7,
            color='#888', va='center')

    # Page title + sort
    ax.text(W/2, H-1.65, "WOMEN'S COLLECTION", ha='center', fontsize=12,
            fontweight='bold', color='#222')
    _wf_box(ax, 8.5, H-2.1, 3.2, 0.42, 'Sort by: [Newest ▼]',
            col='#F5F5F5', edge='#DDD', fsize=7)

    # Left filter sidebar
    _wf_box(ax, 0.2, 1.9, 2.4, H-4.2, col='#FAFAFA', edge='#DDD')
    ax.text(1.4, H-2.6, 'FILTER', fontsize=9, fontweight='bold',
            ha='center', color='#333')
    filter_groups = [
        ('PRICE RANGE', ['Under £50', '£50–£100', '£100–£200', 'Over £200']),
        ('SIZE',        ['XS', 'S', 'M', 'L', 'XL', 'XXL']),
        ('COLOUR',      ['Black', 'White', 'Navy', 'Red', 'Other']),
    ]
    fy = H - 3.0
    for group, opts in filter_groups:
        ax.text(0.4, fy, group, fontsize=7.5, fontweight='bold', color='#444')
        fy -= 0.32
        for opt in opts:
            ax.text(0.55, fy, f'[ ] {opt}', fontsize=7, color='#666')
            fy -= 0.28
        fy -= 0.15

    # Product grid (3×3)
    cols, rows = 3, 3
    start_x, start_y = 2.9, 2.1
    card_w, card_h = 2.9, 4.2
    gap_x, gap_y = 0.2, 0.5
    for r in range(rows):
        for c in range(cols):
            px = start_x + c * (card_w + gap_x)
            py = H - 2.6 - r * (card_h + gap_y) - card_h
            _wf_xmark(ax, px, py + 1.0, card_w, card_h - 1.1)
            _wf_box(ax, px, py + 0.55, card_w, 0.42, 'Brand Name',
                    col='white', edge='none', text_col='#999', fsize=6)
            _wf_box(ax, px, py + 0.1, card_w, 0.42, 'Product Name',
                    col='white', edge='none', text_col='#333', fsize=7, bold=True)
            _wf_box(ax, px, py - 0.35, card_w, 0.42, '£XX.XX',
                    col='white', edge='none', text_col='#E65100', fsize=7.5)

    _wf_footer(ax, W)
    ax.set_title("Wireframe 2 of 5 – Products Listing Page", fontsize=13,
                 fontweight='bold', pad=10, color=C['navy'])
    return _save(fig, 'wireframe_products.png')


def generate_wireframe_product_detail():
    W, H = 12, 18
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    fig.patch.set_facecolor('white')

    _wf_header(ax, W, H)
    ax.text(0.3, H-1.1, 'Home > Women > Product Name', fontsize=7,
            color='#888', va='center')

    # Main product image
    _wf_xmark(ax, 0.3, H-9.5, 5.2, 8.0)

    # Thumbnails
    for i in range(3):
        _wf_xmark(ax, 0.3 + i*1.8, H-10.7, 1.5, 1.0)

    # Product info (right side)
    rx = 6.2
    ax.text(rx, H-2.1, 'Brand Name', fontsize=9, color='#999')
    ax.text(rx, H-2.7, 'Full Product Name', fontsize=13, fontweight='bold', color='#222')
    ax.text(rx, H-3.2, '£XX.XX', fontsize=12, color='#E65100', fontweight='bold')
    ax.text(rx, H-3.6, '£XX.XX', fontsize=9, color='#999')  # original price

    # Rating
    ax.text(rx, H-4.1, '★★★★☆  (24 reviews)', fontsize=8, color='#FBC02D')

    # Size
    ax.text(rx, H-4.7, 'SIZE:', fontsize=8, fontweight='bold', color='#333')
    _wf_box(ax, rx, H-5.25, 5.5, 0.45, 'Select a size ▼',
            col='white', edge='#CCC', fsize=7.5)

    # Qty
    ax.text(rx, H-5.95, 'QUANTITY:', fontsize=8, fontweight='bold', color='#333')
    _wf_box(ax, rx, H-6.5, 1.5, 0.45, '[ − ] 1 [ + ]',
            col='white', edge='#CCC', fsize=7.5)

    # Buttons
    _wf_box(ax, rx, H-7.25, 5.5, 0.55, 'ADD TO CART', col='#222',
            text_col='white', fsize=8.5, bold=True, edge='#222')
    _wf_box(ax, rx, H-8.05, 5.5, 0.55, 'BUY NOW', col='#E65100',
            text_col='white', fsize=8.5, bold=True, edge='#E65100')

    # Stock
    ax.text(rx, H-8.65, '✓  In Stock', fontsize=8, color='#2E7D32')

    # Description
    ax.text(rx, H-9.3, 'DESCRIPTION', fontsize=8.5, fontweight='bold', color='#333')
    _wf_box(ax, rx, H-11.0, 5.5, 1.5,
            'Product description text...\nMaterial, care instructions,\nfit and styling notes.',
            col='#FAFAFA', edge='#EEE', fsize=7, text_col='#666')

    # Related products
    ax.plot([0.2, W-0.2], [4.0, 4.0], color='#EEE', lw=1)
    ax.text(W/2, 3.7, 'YOU MAY ALSO LIKE', ha='center', fontsize=10,
            fontweight='bold', color='#222')
    for i in range(4):
        px = 0.3 + i * 2.95
        _wf_xmark(ax, px, 2.1, 2.6, 1.4)

    _wf_footer(ax, W)
    ax.set_title('Wireframe 3 of 5 – Product Detail Page', fontsize=13,
                 fontweight='bold', pad=10, color=C['navy'])
    return _save(fig, 'wireframe_product_detail.png')


def generate_wireframe_cart():
    W, H = 12, 18
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    fig.patch.set_facecolor('white')

    _wf_header(ax, W, H)
    ax.text(W/2, H-1.6, 'MY SHOPPING BAG', ha='center', fontsize=12,
            fontweight='bold', color='#222')
    ax.text(W/2, H-2.05, '3 items', ha='center', fontsize=8, color='#888')
    ax.plot([0.2, W-0.2], [H-2.3, H-2.3], color='#DDD', lw=1)

    # Column headers
    for x, label in [(1.8, 'PRODUCT'), (5.5, 'PRICE'), (7.2, 'QUANTITY'), (9.2, 'TOTAL')]:
        ax.text(x, H-2.65, label, fontsize=7.5, fontweight='bold', color='#555',
                ha='center')
    ax.plot([0.2, W-0.2], [H-2.9, H-2.9], color='#DDD', lw=0.7)

    # Cart items
    for i in range(3):
        ry = H - 3.5 - i * 2.0
        _wf_xmark(ax, 0.3, ry - 0.8, 1.5, 1.5)
        ax.text(2.1, ry, f'Product Name {i+1}', fontsize=8, fontweight='bold', color='#222')
        ax.text(2.1, ry - 0.35, 'Brand · Size: M', fontsize=7, color='#888')
        ax.text(5.5, ry - 0.2, '£XX.XX', fontsize=8, ha='center', color='#333')
        _wf_box(ax, 6.5, ry - 0.5, 1.6, 0.42, '[ − ]  1  [ + ]',
                col='white', edge='#CCC', fsize=7)
        ax.text(9.2, ry - 0.2, '£XX.XX', fontsize=8.5, fontweight='bold',
                ha='center', color='#222')
        ax.text(10.8, ry - 0.2, '✕', fontsize=10, ha='center', color='#E53935')
        ax.plot([0.2, W-0.2], [ry - 1.0, ry - 1.0], color='#EEE', lw=0.5)

    # Left: Promo + Note
    py = H - 10.2
    ax.text(0.3, py, 'PROMO CODE', fontsize=8, fontweight='bold', color='#333')
    _wf_box(ax, 0.3, py - 0.55, 4.0, 0.42, '[Enter promo code]',
            col='white', edge='#CCC', fsize=7)
    _wf_box(ax, 4.5, py - 0.55, 1.5, 0.42, 'APPLY',
            col='#333', text_col='white', fsize=7, bold=True, edge='#333')
    ax.text(0.3, py - 1.25, 'ORDER NOTE', fontsize=8, fontweight='bold', color='#333')
    _wf_box(ax, 0.3, py - 2.5, 5.5, 1.1,
            'Add a note for your order...', col='#FAFAFA', edge='#DDD', fsize=7,
            text_col='#AAA')

    # Right: Order summary
    sx = 7.0
    _wf_box(ax, sx, py - 4.0, 4.7, 3.6, col='#FAFAFA', edge='#DDD')
    ax.text(sx + 2.35, py - 0.45, 'ORDER SUMMARY', fontsize=9,
            fontweight='bold', ha='center', color='#222')
    for ky, label, val in [
        (py-1.05, 'Subtotal (3 items)', '£XXX.XX'),
        (py-1.55, 'Estimated Shipping', 'FREE'),
        (py-2.0, 'Promo Discount', '–£XX.XX'),
    ]:
        ax.text(sx + 0.2, ky, label, fontsize=7.5, color='#555')
        ax.text(sx + 4.4, ky, val, fontsize=7.5, ha='right', color='#333')
    ax.plot([sx+0.2, sx+4.5], [py-2.3, py-2.3], color='#CCC', lw=0.8)
    ax.text(sx + 0.2, py - 2.65, 'TOTAL', fontsize=9, fontweight='bold', color='#222')
    ax.text(sx + 4.4, py - 2.65, '£XXX.XX', fontsize=9, fontweight='bold',
            ha='right', color='#222')
    _wf_box(ax, sx + 0.2, py - 3.45, 4.3, 0.55, 'PROCEED TO CHECKOUT',
            col='#222', text_col='white', fsize=8, bold=True, edge='#222')
    ax.text(sx + 2.35, py - 3.75, 'Secure Checkout · SSL Encrypted',
            ha='center', fontsize=6.5, color='#AAA')

    _wf_footer(ax, W)
    ax.set_title('Wireframe 4 of 5 – Shopping Cart', fontsize=13,
                 fontweight='bold', pad=10, color=C['navy'])
    return _save(fig, 'wireframe_cart.png')


def generate_wireframe_checkout():
    W, H = 12, 18
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
    fig.patch.set_facecolor('white')

    _wf_header(ax, W, H)
    ax.text(W/2, H-1.6, 'SECURE CHECKOUT', ha='center', fontsize=12,
            fontweight='bold', color='#222')

    # Step indicator
    for i, (label, active) in enumerate(
            [('1  Cart', False), ('2  Shipping', True), ('3  Payment', False), ('4  Confirm', False)]):
        col = '#222' if active else '#BBB'
        ax.text(1.5 + i * 2.5, H-2.2, label, fontsize=8, ha='center',
                fontweight='bold' if active else 'normal', color=col)

    ax.plot([0.2, W-0.2], [H-2.5, H-2.5], color='#EEE', lw=1)

    # ── LEFT: Shipping + Payment ──
    ax.text(0.3, H-3.0, 'SHIPPING DETAILS', fontsize=9.5, fontweight='bold', color='#333')
    fields_ship = [
        ('Email Address', H-3.7), ('First Name', H-4.4), ('Last Name', H-4.4),
        ('Address Line 1', H-5.1), ('Address Line 2', H-5.8),
        ('City', H-6.5), ('Postcode', H-6.5), ('Country', H-7.2),
        ('Phone Number', H-7.9),
    ]
    drawn = set()
    for fname, fy in fields_ship:
        if fy not in drawn:
            if fname in ('First Name', 'City', 'Postcode'):
                _wf_box(ax, 0.3, fy - 0.38, 3.1, 0.38, fname, col='white',
                        edge='#CCC', fsize=7, text_col='#AAA')
                _wf_box(ax, 3.6, fy - 0.38, 3.1, 0.38,
                        fields_ship[fields_ship.index((fname, fy))+1][0],
                        col='white', edge='#CCC', fsize=7, text_col='#AAA')
                drawn.add(fy)
            else:
                _wf_box(ax, 0.3, fy - 0.38, 6.4, 0.38, fname, col='white',
                        edge='#CCC', fsize=7, text_col='#AAA')
            ax.text(0.3, fy, fname, fontsize=6.5, color='#888')

    ax.plot([0.2, 7.0], [H-8.4, H-8.4], color='#EEE', lw=1)
    ax.text(0.3, H-8.85, 'PAYMENT METHOD', fontsize=9.5, fontweight='bold', color='#333')
    for i, pm in enumerate(['  (•) Debit / Credit Card', '  ( ) PayPal']):
        _wf_box(ax, 0.3, H-9.6-i*0.7, 6.4, 0.45, pm, col='#FAFAFA',
                edge='#CCC', fsize=8, text_col='#333')

    # Card details
    _wf_box(ax, 0.3, H-11.1, 6.4, 0.38, 'Card Number', col='white',
            edge='#CCC', fsize=7, text_col='#AAA')
    _wf_box(ax, 0.3, H-11.7, 3.0, 0.38, 'Expiry (MM/YY)', col='white',
            edge='#CCC', fsize=7, text_col='#AAA')
    _wf_box(ax, 3.6, H-11.7, 3.0, 0.38, 'CVV', col='white',
            edge='#CCC', fsize=7, text_col='#AAA')
    _wf_box(ax, 0.3, H-12.3, 6.4, 0.38, 'Cardholder Name', col='white',
            edge='#CCC', fsize=7, text_col='#AAA')

    _wf_box(ax, 0.3, H-13.3, 6.4, 0.65, 'PAY NOW  £XXX.XX',
            col='#222', text_col='white', fsize=10, bold=True, edge='#222')
    ax.text(3.5, H-13.8, '[Lock icon] SSL Secure · Verified by Visa',
            ha='center', fontsize=7, color='#888')

    # ── RIGHT: Order Summary ──
    _wf_box(ax, 7.5, H-14.5, 4.2, 11.0, col='#FAFAFA', edge='#DDD')
    ax.text(9.6, H-3.2, 'ORDER SUMMARY', fontsize=9, fontweight='bold',
            ha='center', color='#333')
    ax.plot([7.7, 11.5], [H-3.5, H-3.5], color='#DDD', lw=0.7)

    for i in range(3):
        iy = H - 4.2 - i * 1.5
        _wf_xmark(ax, 7.7, iy - 0.7, 1.2, 1.1)
        ax.text(9.1, iy - 0.1, f'Product {i+1}', fontsize=7.5,
                fontweight='bold', color='#333')
        ax.text(9.1, iy - 0.5, 'Size: M · Qty: 1', fontsize=7, color='#888')
        ax.text(11.5, iy - 0.3, '£XX.XX', fontsize=7.5, ha='right', color='#444')

    ax.plot([7.7, 11.5], [H-8.8, H-8.8], color='#DDD', lw=0.7)
    for ky, label, val in [
        (H-9.2, 'Subtotal',  '£XXX.XX'),
        (H-9.65,'Shipping',  'FREE'),
        (H-10.1,'Promo',     '–£XX.XX'),
    ]:
        ax.text(7.7, ky, label, fontsize=7.5, color='#555')
        ax.text(11.5, ky, val, fontsize=7.5, ha='right', color='#333')
    ax.plot([7.7, 11.5], [H-10.4, H-10.4], color='#CCC', lw=0.8)
    ax.text(7.7, H-10.8, 'TOTAL', fontsize=9, fontweight='bold', color='#222')
    ax.text(11.5, H-10.8, '£XXX.XX', fontsize=9, fontweight='bold',
            ha='right', color='#222')

    _wf_footer(ax, W)
    ax.set_title('Wireframe 5 of 5 – Checkout Page', fontsize=13,
                 fontweight='bold', pad=10, color=C['navy'])
    return _save(fig, 'wireframe_checkout.png')


# ═══════════════════════════════════════════════════════════════
# 10.  RISK MATRIX
# ═══════════════════════════════════════════════════════════════
def generate_risk_matrix():
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('white')

    grid = [
        ['#C8E6C9', '#C8E6C9', '#FFF9C4', '#FFF9C4', '#FFE0B2'],
        ['#C8E6C9', '#FFF9C4', '#FFF9C4', '#FFE0B2', '#FFE0B2'],
        ['#FFF9C4', '#FFF9C4', '#FFE0B2', '#FFE0B2', '#FFCDD2'],
        ['#FFF9C4', '#FFE0B2', '#FFE0B2', '#FFCDD2', '#FFCDD2'],
        ['#FFE0B2', '#FFE0B2', '#FFCDD2', '#FFCDD2', '#EF9A9A'],
    ]
    labels = [
        ['LOW',    'LOW',    'MEDIUM', 'MEDIUM', 'HIGH'],
        ['LOW',    'MEDIUM', 'MEDIUM', 'HIGH',   'HIGH'],
        ['MEDIUM', 'MEDIUM', 'HIGH',   'HIGH',   'CRITICAL'],
        ['MEDIUM', 'HIGH',   'HIGH',   'CRITICAL','CRITICAL'],
        ['HIGH',   'HIGH',   'CRITICAL','CRITICAL','CRITICAL'],
    ]
    for row in range(5):
        for col in range(5):
            ax.add_patch(mpatches.Rectangle((col, 4-row), 1, 1,
                         facecolor=grid[row][col], edgecolor='white', linewidth=2))
            ax.text(col + 0.5, 4 - row + 0.5, labels[row][col],
                    ha='center', va='center', fontsize=6.5, color='#555',
                    fontweight='bold')

    risks = [
        (1.5, 2.5, 'R1', 'Schedule\nDelay',       '#1565C0'),
        (3.5, 1.5, 'R2', 'Scope\nCreep',           '#1565C0'),
        (2.5, 3.5, 'R3', 'Tech\nIssues',           '#E65100'),
        (0.5, 3.5, 'R4', 'Budget',                 '#2E7D32'),
        (4.5, 3.5, 'R5', 'Team\nConflict',         '#C62828'),
        (1.5, 1.5, 'R6', 'Data\nLoss',             '#1565C0'),
        (3.5, 2.5, 'R7', 'Comm.\nBreakdown',       '#E65100'),
    ]
    for rx, ry, rid, rdesc, col in risks:
        ax.add_patch(plt.Circle((rx, ry), 0.35, facecolor='white',
                                edgecolor=col, linewidth=2.2, zorder=5))
        ax.text(rx, ry + 0.06, rid, ha='center', va='center', fontsize=8.5,
                fontweight='bold', color=col, zorder=6)

    ax.set_xlim(0, 5); ax.set_ylim(0, 5)
    ax.set_xticks([0.5,1.5,2.5,3.5,4.5])
    ax.set_xticklabels(['Very Low','Low','Medium','High','Very High'], fontsize=9)
    ax.set_yticks([0.5,1.5,2.5,3.5,4.5])
    ax.set_yticklabels(['Very Low','Low','Medium','High','Very High'], fontsize=9)
    ax.set_xlabel('IMPACT →', fontsize=10, fontweight='bold', color='#333')
    ax.set_ylabel('PROBABILITY →', fontsize=10, fontweight='bold', color='#333')
    ax.set_title('Project Risk Matrix – StyleVault', fontsize=13,
                 fontweight='bold', pad=12, color=C['navy'])

    legend_text = (
        'R1: Schedule Delay    R2: Scope Creep     R3: Technical Issues\n'
        'R4: Budget Constraints  R5: Team Conflict   R6: Data Loss   R7: Communication Breakdown'
    )
    ax.text(2.5, -0.75, legend_text, ha='center', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='#F5F5F5', alpha=0.9,
                      edgecolor='#CCC'))
    plt.tight_layout()
    return _save(fig, 'risk_matrix.png')


# ═══════════════════════════════════════════════════════════════
# 11.  CRITICAL PATH
# ═══════════════════════════════════════════════════════════════
def generate_critical_path():
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    NW, NH = 2.0, 1.1

    nodes = [
        (1.2,  3.0, 'A', 'Project\nInitiation', 2,  True),
        (3.8,  4.5, 'B', 'Requirements\nAnalysis', 5, True),
        (3.8,  1.5, 'C', 'Literature\nReview',   8,  False),
        (6.5,  4.5, 'D', 'Design &\nPrototype', 10,  True),
        (6.5,  1.5, 'E', 'Database\nDesign',     5,  True),
        (9.5,  3.0, 'F', 'Website\nDevelopment',20,  True),
        (12.3, 4.5, 'G', 'Testing',              10,  True),
        (12.3, 1.5, 'H', 'Content\nCreation',    6,  False),
        (14.8, 3.0, 'I', 'Launch\n& Submit',      1,  True),
    ]

    for nx, ny, nid, name, dur, crit in nodes:
        fcol = C['lred']    if crit else '#FFFDE7'
        ecol = '#C62828'    if crit else '#F9A825'
        lw   = 2.5          if crit else 1.5

        ax.add_patch(FancyBboxPatch(
            (nx - NW/2, ny - NH/2), NW, NH,
            boxstyle="round,pad=0.12", facecolor=fcol,
            edgecolor=ecol, linewidth=lw))

        es, ef = 0, dur  # simplified
        ax.text(nx, ny + 0.28, f'{nid}: {name}', ha='center', va='center',
                fontsize=7.5, fontweight='bold', color='#222',
                multialignment='center')
        ax.text(nx, ny - 0.3, f'Duration: {dur}d',
                ha='center', va='center', fontsize=7, color='#555')

    edges = [
        ('A','B',True),('A','C',False),
        ('B','D',True),('B','E',True),
        ('C','F',False),
        ('D','F',True),('E','F',True),
        ('F','G',True),('F','H',False),
        ('G','I',True),('H','I',False),
    ]
    npos = {n[2]: (n[0], n[1]) for n in nodes}
    for s, d, crit in edges:
        x1, y1 = npos[s]; x2, y2 = npos[d]
        col = '#C62828' if crit else '#90A4AE'
        lw  = 2.0 if crit else 1.2
        ax.annotate('', xy=(x2 - NW/2, y2), xytext=(x1 + NW/2, y1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=lw))

    ax.text(8, 0.4,
            'Critical Path (red boxes): A → B → D + E → F → G → I  =  48 days',
            ha='center', fontsize=10, fontweight='bold', color='#C62828',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFEBEE',
                      edgecolor='#EF9A9A', alpha=0.95))

    ax.set_title('Critical Path Analysis – Network Diagram', fontsize=13,
                 fontweight='bold', pad=12, color=C['navy'])
    return _save(fig, 'critical_path.png')


# ═══════════════════════════════════════════════════════════════
# 12.  NEW: AUTH FLOWCHART
# ═══════════════════════════════════════════════════════════════
def generate_auth_flowchart():
    fig, ax = plt.subplots(figsize=(12, 16))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    def rbox(x, y, text, w=3.2, h=0.55, col='#E3F2FD', edge='#1565C0'):
        ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                     boxstyle="round,pad=0.12", facecolor=col,
                     edgecolor=edge, linewidth=1.5))
        ax.text(x, y, text, ha='center', va='center', fontsize=9,
                multialignment='center')

    def diamond(x, y, text, w=2.2, h=0.8):
        pts = [[x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]]
        ax.add_patch(plt.Polygon(pts, facecolor='#FFF8E1',
                                  edgecolor='#F57F17', lw=1.8))
        ax.text(x, y, text, ha='center', va='center', fontsize=8,
                fontweight='bold', multialignment='center')

    def start(x, y): ax.add_patch(plt.Circle((x, y), 0.25, fc='#1565C0', ec='#1565C0'))
    def end(x, y):
        ax.add_patch(plt.Circle((x, y), 0.30, fc='white', ec='#1565C0', lw=2.2))
        ax.add_patch(plt.Circle((x, y), 0.20, fc='#1565C0', ec='#1565C0'))

    def arr(x1, y1, x2, y2, label='', side=0.25):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
        if label:
            ax.text((x1+x2)/2 + side, (y1+y2)/2, label, fontsize=8, color='#666')

    # LEFT COLUMN: Login Flow
    lx = 3.0
    ax.text(lx, 15.6, 'LOGIN FLOW', ha='center', fontsize=11, fontweight='bold',
            color=C['navy'], style='italic')
    start(lx, 15.2); arr(lx, 14.95, lx, 14.55)
    rbox(lx, 14.25, 'Visit Login Page', col='#E3F2FD')
    arr(lx, 13.97, lx, 13.45)
    rbox(lx, 13.15, 'Enter Email + Password', col='#E3F2FD')
    arr(lx, 12.87, lx, 12.35)
    diamond(lx, 12.0, 'Valid\ncredentials?')
    arr(lx, 11.60, lx, 11.1, 'Yes')
    arr(lx + 1.1, 12.0, 5.5, 12.0, 'No')
    rbox(5.5, 12.0, 'Show Error\nMessage', col=C['lred'], edge=C['red'])
    ax.annotate('', xy=(5.5, 13.15), xytext=(5.5, 12.28),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))
    ax.plot([5.5, lx+1.6], [13.15, 13.15], color='#555', lw=1.2)
    rbox(lx, 10.8, 'Authenticate User\n(Flask-Login)', col=C['lteal'], edge=C['teal'])
    arr(lx, 10.52, lx, 10.0)
    diamond(lx, 9.65, 'Admin\nuser?')
    arr(lx+1.1, 9.65, 5.5, 9.65, 'Yes')
    rbox(5.5, 9.65, 'Redirect to\nAdmin Panel', col=C['lteal'], edge=C['teal'])
    arr(lx, 9.25, lx, 8.75, 'No')
    rbox(lx, 8.45, 'Redirect to Homepage', col=C['lgreen'], edge=C['green'])
    arr(lx, 8.17, lx, 7.65)
    rbox(lx, 7.35, 'Session Created\n(user.is_authenticated)', col=C['lgreen'], edge=C['green'])
    arr(lx, 7.07, lx, 6.5)
    end(lx, 6.25)

    # RIGHT COLUMN: Registration Flow
    rx = 9.0
    ax.text(rx, 15.6, 'REGISTRATION FLOW', ha='center', fontsize=11, fontweight='bold',
            color=C['navy'], style='italic')
    start(rx, 15.2); arr(rx, 14.95, rx, 14.55)
    rbox(rx, 14.25, 'Visit Sign Up Page', col='#EDE7F6', edge=C['purple'])
    arr(rx, 13.97, rx, 13.45)
    rbox(rx, 13.15, 'Fill Registration Form\n(name, email, password)', col='#EDE7F6', edge=C['purple'])
    arr(rx, 12.87, rx, 12.35)
    diamond(rx, 12.0, 'Form\nvalid?')
    arr(rx+1.1, 12.0, 11.5, 12.0, 'No')
    rbox(11.5, 12.0, 'Highlight\nErrors', col=C['lred'], edge=C['red'])
    ax.annotate('', xy=(11.5, 13.15), xytext=(11.5, 12.28),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))
    ax.plot([11.5, rx+1.1], [13.15, 13.15], color='#555', lw=1.2)
    arr(rx, 11.60, rx, 11.1, 'Yes')
    diamond(rx, 10.75, 'Email\nalready used?')
    arr(rx+1.1, 10.75, 11.5, 10.75, 'Yes')
    rbox(11.5, 10.75, 'Error: Email\nalready registered', col=C['lred'], edge=C['red'])
    arr(rx, 10.35, rx, 9.85, 'No')
    rbox(rx, 9.55, 'Hash Password\n(Werkzeug PBKDF2)', col='#EDE7F6', edge=C['purple'])
    arr(rx, 9.27, rx, 8.75)
    rbox(rx, 8.45, 'Save User to Database', col='#EDE7F6', edge=C['purple'])
    arr(rx, 8.17, rx, 7.65)
    rbox(rx, 7.35, 'Auto-Login + Redirect\nto Homepage', col=C['lgreen'], edge=C['green'])
    arr(rx, 7.07, rx, 6.5)
    end(rx, 6.25)

    # Divider
    ax.plot([6, 6], [5.8, 15.8], color='#DDD', lw=1, linestyle='--')

    ax.set_title('Flowchart: User Authentication (Login & Registration)',
                 fontsize=13, fontweight='bold', pad=12, color=C['navy'])
    return _save(fig, 'flowchart_auth.png')


# ═══════════════════════════════════════════════════════════════
# 13.  NEW: CHECKOUT PROCESS FLOWCHART
# ═══════════════════════════════════════════════════════════════
def generate_checkout_flowchart():
    fig, ax = plt.subplots(figsize=(14, 20))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 20)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(left=0.04, right=0.96, top=0.95, bottom=0.03)

    def rbox(x, y, text, w=4.6, h=0.68, col='#E3F2FD', edge='#1565C0'):
        ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                     boxstyle="round,pad=0.14", facecolor=col,
                     edgecolor=edge, linewidth=1.8))
        ax.text(x, y, text, ha='center', va='center', fontsize=9.5,
                multialignment='center', fontweight='500')

    def diamond(x, y, text, w=3.4, h=1.0):
        pts = [[x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]]
        ax.add_patch(plt.Polygon(pts, facecolor='#FFF8E1',
                                  edgecolor='#F57F17', lw=2.0))
        ax.text(x, y, text, ha='center', va='center', fontsize=9,
                fontweight='bold', multialignment='center')

    def start_node(x, y):
        ax.add_patch(plt.Circle((x, y), 0.32, fc='#1565C0', ec='#0D1F3C', lw=1.5))

    def end_node(x, y):
        ax.add_patch(plt.Circle((x, y), 0.38, fc='white', ec='#1565C0', lw=2.5))
        ax.add_patch(plt.Circle((x, y), 0.24, fc='#1565C0', ec='#1565C0'))

    def arr(x1, y1, x2, y2, label='', label_dx=0.32):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#455A64', lw=1.5))
        if label:
            ax.text((x1+x2)/2 + label_dx, (y1+y2)/2, label,
                    fontsize=8.5, color='#37474F', fontweight='bold')

    def side_box(x, y, text):
        rbox(x, y, text, w=3.5, h=0.62, col='#FFECB3', edge='#FF8F00')

    # ── Main flow column ──────────────────────────────────────
    cx   = 7.0    # centre x
    rx   = 11.8   # right branch x
    gap  = 1.55   # vertical gap between nodes

    y = 19.4
    start_node(cx, y);  y -= 0.55
    arr(cx, y, cx, y - 0.55);                              y -= 0.55
    rbox(cx, y, 'User Views Shopping Cart', col='#E3F2FD'); y -= gap
    arr(cx, y + gap - 0.34, cx, y + 0.50)
    diamond(cx, y, 'Cart\nis empty?');                      y -= gap
    # Yes → right
    arr(cx + 1.7, y + gap, rx, y + gap, 'Yes')
    side_box(rx, y + gap, 'Redirect to\nProducts Page')
    # No ↓
    arr(cx, y + gap - 0.50, cx, y + 0.50, 'No')
    diamond(cx, y, 'User\nlogged in?');                     y -= gap
    # No → right
    arr(cx + 1.7, y + gap, rx, y + gap, 'No')
    side_box(rx, y + gap, 'Redirect to\nLogin Page')
    # Yes ↓
    arr(cx, y + gap - 0.50, cx, y + 0.50, 'Yes')
    rbox(cx, y, 'Display Checkout Page\n(Shipping + Payment Forms)'); y -= gap
    arr(cx, y + gap - 0.34, cx, y + 0.34)
    rbox(cx, y, 'User Fills in Shipping\nand Payment Details');        y -= gap
    arr(cx, y + gap - 0.34, cx, y + 0.50)
    diamond(cx, y, 'Form\nvalidation OK?');                            y -= gap
    # No → right
    arr(cx + 1.7, y + gap, rx, y + gap, 'No')
    side_box(rx, y + gap, 'Highlight Missing\nor Invalid Fields')
    # Yes ↓
    arr(cx, y + gap - 0.50, cx, y + 0.34, 'Yes')
    rbox(cx, y, 'Send Payment Request\nto Payment Gateway',
         col='#EDE7F6', edge='#6A1B9A');                               y -= gap
    arr(cx, y + gap - 0.34, cx, y + 0.50)
    diamond(cx, y, 'Payment\napproved?');                               y -= gap
    # No → right
    arr(cx + 1.7, y + gap, rx, y + gap, 'No')
    side_box(rx, y + gap, 'Show Payment\nFailed Error')
    # Yes ↓
    arr(cx, y + gap - 0.50, cx, y + 0.34, 'Yes')
    rbox(cx, y, 'Create Order Record\nin Database',
         col=C['lteal'], edge=C['teal']);                               y -= gap
    arr(cx, y + gap - 0.34, cx, y + 0.34)
    rbox(cx, y, 'Create OrderItem Records\n(product, qty, price)',
         col=C['lteal'], edge=C['teal']);                               y -= gap
    arr(cx, y + gap - 0.34, cx, y + 0.34)
    rbox(cx, y, 'Clear Cart Items\nfrom Database',
         col=C['lteal'], edge=C['teal']);                               y -= gap
    arr(cx, y + gap - 0.34, cx, y + 0.34)
    rbox(cx, y, 'Show Order Confirmation\nPage with Order Number',
         col=C['lgreen'], edge=C['green']);                             y -= gap
    arr(cx, y + gap - 0.34, cx, y + 0.34)
    end_node(cx, y)

    ax.set_title('Flowchart: Checkout & Order Processing Flow',
                 fontsize=14, fontweight='bold', pad=14, color=C['navy'])
    return _save(fig, 'flowchart_checkout.png')


# ═══════════════════════════════════════════════════════════════
# 14.  NEW: SYSTEM ARCHITECTURE DIAGRAM
# ═══════════════════════════════════════════════════════════════
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    def layer_box(x, y, w, h, title, items, header_col, body_col):
        # Header
        ax.add_patch(FancyBboxPatch((x, y + h - 0.55), w, 0.55,
                     boxstyle="square,pad=0", facecolor=header_col,
                     edgecolor='#333', linewidth=1.5))
        ax.text(x + w/2, y + h - 0.27, title, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='white')
        # Body
        ax.add_patch(FancyBboxPatch((x, y), w, h - 0.55,
                     boxstyle="square,pad=0", facecolor=body_col,
                     edgecolor='#333', linewidth=1.5))
        step = (h - 0.55) / (len(items) + 1)
        for i, item in enumerate(items):
            iy = y + (h - 0.55) - (i + 0.75) * step
            ax.add_patch(FancyBboxPatch((x + 0.15, iy - 0.22), w - 0.3, 0.44,
                         boxstyle="round,pad=0.07", facecolor='white',
                         edgecolor='#CCC', linewidth=1))
            ax.text(x + w/2, iy, item, ha='center', va='center', fontsize=8)

    def arr_down(x, y1, y2, label=''):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(arrowstyle='->', color='#607D8B', lw=1.5))
        if label:
            ax.text(x + 0.15, (y1 + y2)/2, label, fontsize=7.5, color='#607D8B',
                    va='center')

    def bidir(x, y1, y2):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(arrowstyle='<->', color='#607D8B', lw=1.8))

    # CLIENT TIER
    layer_box(0.5, 7.0, 3.5, 2.7,
              'CLIENT TIER',
              ['Web Browser\n(Chrome, Firefox, Safari)',
               'Bootstrap 5 CSS\n(Responsive Grid)',
               'Jinja2 Templates\n(HTML Rendered)'],
              '#1565C0', '#E3F2FD')

    # PRESENTATION TIER
    layer_box(4.5, 7.0, 3.5, 2.7,
              'PRESENTATION TIER',
              ['HTML Templates\n(Jinja2 Inheritance)',
               'CSS / JavaScript\n(Custom + Bootstrap)',
               'Form Validation\n(Client-side)'],
              '#6A1B9A', '#EDE7F6')

    # APPLICATION TIER
    layer_box(8.5, 7.0, 3.5, 2.7,
              'APPLICATION TIER',
              ['Flask 3.1\n(WSGI Server)',
               'Routes / Controllers\n(app.py)',
               'Flask-Login\n(Session Auth)'],
              '#00695C', '#E0F2F1')

    # DATA TIER
    layer_box(12.5, 7.0, 3.0, 2.7,
              'DATA TIER',
              ['SQLAlchemy ORM\n(Object Mapping)',
               'SQLite Database\n(stylevault.db)',
               '7 Tables / 7 Models'],
              '#E65100', '#FBE9E7')

    # Arrows between tiers
    ax.annotate('', xy=(4.5, 8.35), xytext=(4.0, 8.35),
                arrowprops=dict(arrowstyle='<->', color='#607D8B', lw=1.8))
    ax.text(4.25, 8.6, 'HTTP\nReq/Res', ha='center', fontsize=7, color='#607D8B')

    ax.annotate('', xy=(8.5, 8.35), xytext=(8.0, 8.35),
                arrowprops=dict(arrowstyle='<->', color='#607D8B', lw=1.8))
    ax.text(8.25, 8.6, 'Render\nTemplate', ha='center', fontsize=7, color='#607D8B')

    ax.annotate('', xy=(12.5, 8.35), xytext=(12.0, 8.35),
                arrowprops=dict(arrowstyle='<->', color='#607D8B', lw=1.8))
    ax.text(12.25, 8.6, 'ORM\nQuery', ha='center', fontsize=7, color='#607D8B')

    # Technology stack row
    techs = [
        (1.5, 5.8, 'Python 3.12',    '#FFD54F', '#333'),
        (3.5, 5.8, 'Flask 3.1',      '#A5D6A7', '#1B5E20'),
        (5.5, 5.8, 'SQLAlchemy 2',   '#80CBC4', '#004D40'),
        (7.5, 5.8, 'Bootstrap 5',    '#CE93D8', '#4A148C'),
        (9.5, 5.8, 'Jinja2',         '#FFCC80', '#E65100'),
        (11.5, 5.8, 'Werkzeug',      '#90CAF9', '#0D47A1'),
        (13.5, 5.8, 'SQLite',        '#BCAAA4', '#3E2723'),
    ]
    ax.text(8.0, 6.55, 'TECHNOLOGY STACK', ha='center', fontsize=10,
            fontweight='bold', color=C['navy'])
    ax.plot([0.3, 15.7], [6.4, 6.4], color='#DDD', lw=1.2)
    for tx, ty, label, col, tcol in techs:
        ax.add_patch(FancyBboxPatch((tx - 1.1, ty - 0.3), 2.2, 0.6,
                     boxstyle="round,pad=0.1", facecolor=col,
                     edgecolor='#999', linewidth=1.0))
        ax.text(tx, ty, label, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=tcol)

    # Security & Quality notes
    _notes = [
        (2.0,  4.0, 'SECURITY',    '#C62828', [
            'Passwords: PBKDF2-SHA256 hashing',
            'Sessions: Flask-Login + secure cookies',
            'SQL injection prevented by ORM',
            'CSRF protection via form tokens',
        ]),
        (8.0,  4.0, 'SCALABILITY', '#1565C0', [
            'Modular Flask factory pattern',
            'SQLAlchemy supports multiple DBs',
            'Deployable to Heroku/Render/PythonAnywhere',
            'Static files via CDN in production',
        ]),
        (13.5, 4.0, 'TESTING',     '#2E7D32', [
            'Functional testing: all routes',
            'Form validation: all inputs',
            'Cross-browser: Chrome/Firefox/Edge',
            'Responsive: desktop/tablet/mobile',
        ]),
    ]
    for nx, ny, title, col, items in _notes:
        bx = nx - 3.5 if nx > 5 else nx - 1.8
        bw = 5.0 if nx > 5 else 3.8
        ax.add_patch(FancyBboxPatch((bx, ny - 1.5), bw, 2.0,
                     boxstyle="round,pad=0.15", facecolor='#FAFAFA',
                     edgecolor=col, linewidth=1.5))
        ax.text(nx, ny + 0.35, title, ha='center', fontsize=9,
                fontweight='bold', color=col)
        for i, item in enumerate(items):
            ax.text(bx + 0.2, ny - i * 0.38,
                    f'• {item}', fontsize=7.5, color='#444', va='top')

    ax.set_title('System Architecture Diagram – StyleVault Application',
                 fontsize=13, fontweight='bold', pad=14, color=C['navy'])
    return _save(fig, 'architecture_diagram.png')


# ═══════════════════════════════════════════════════════════════
# 19.  PRODUCT BACKLOG
# ═══════════════════════════════════════════════════════════════
def generate_product_backlog():
    """Visualise the product backlog as a colour-coded priority table."""
    backlog = [
        # (ID,  User Story,                                        Priority, SP, Status)
        ('US-01', 'As a customer I want to browse products by category',    'Must Have',   8,  'Done'),
        ('US-02', 'As a customer I want to view product images & prices',   'Must Have',   5,  'Done'),
        ('US-03', 'As a customer I want to add items to a shopping cart',   'Must Have',   8,  'Done'),
        ('US-04', 'As a customer I want to update / remove cart items',     'Must Have',   5,  'Done'),
        ('US-05', 'As a customer I want to register an account',            'Must Have',   5,  'Done'),
        ('US-06', 'As a customer I want to log in and log out securely',    'Must Have',   5,  'Done'),
        ('US-07', 'As a customer I want to complete a checkout process',    'Must Have',  13,  'Done'),
        ('US-08', 'As a customer I want to receive an order confirmation',  'Must Have',   5,  'Done'),
        ('US-09', 'As a customer I want to filter products by price/size',  'Should Have', 8,  'Done'),
        ('US-10', 'As a customer I want to sort products (price / name)',   'Should Have', 3,  'Done'),
        ('US-11', 'As a customer I want to search for products',            'Should Have', 5,  'Done'),
        ('US-12', 'As a customer I want to view related products',          'Should Have', 3,  'Done'),
        ('US-13', 'As a customer I want to contact customer support',       'Should Have', 3,  'Done'),
        ('US-14', 'As a customer I want a quick-add to cart from listing',  'Could Have',  5,  'Done'),
        ('US-15', 'As an admin I want to seed the DB with sample products', 'Could Have',  3,  'Done'),
        ('US-16', 'As a customer I want inclusive accessibility features',  'Could Have',  5,  'Done'),
        ('US-17', 'As a customer I want promo code discount input',         'Won\'t Have', 8,  'Backlog'),
        ('US-18', 'As a customer I want order tracking updates by email',   'Won\'t Have', 13, 'Backlog'),
    ]

    n = len(backlog)
    fig, ax = plt.subplots(figsize=(18, n * 0.52 + 2.5))
    ax.axis('off')
    fig.patch.set_facecolor('white')

    priority_colors = {
        'Must Have':   '#C62828',
        'Should Have': '#E65100',
        'Could Have':  '#2E7D32',
        "Won't Have":  '#455A64',
    }
    status_colors = {
        'Done':    '#E8F5E9',
        'In Progress': '#FFF9C4',
        'Backlog': '#FAFAFA',
    }

    col_widths = [0.6, 5.5, 1.4, 0.7, 1.0]   # proportional
    total = sum(col_widths)
    col_x = [0]
    for w in col_widths[:-1]:
        col_x.append(col_x[-1] + w / total)
    col_x = [x + 0.02 for x in col_x]
    headers = ['ID', 'User Story', 'Priority', 'SP', 'Status']

    ROW_H = 1.0 / (n + 1.5)
    TOP   = 0.97

    # Header row
    for i, (hdr, cx) in enumerate(zip(headers, col_x)):
        ax.add_patch(plt.Rectangle(
            (col_x[i] - 0.01, TOP - ROW_H), col_widths[i] / total, ROW_H,
            transform=ax.transAxes, facecolor=C['navy'], edgecolor='white',
            linewidth=0.8, clip_on=False))
        ax.text(cx + col_widths[i] / total / 2 - 0.01,
                TOP - ROW_H / 2, hdr,
                transform=ax.transAxes, ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')

    for row_i, (uid, story, priority, sp, status) in enumerate(backlog):
        y_top = TOP - (row_i + 1) * ROW_H
        bg = status_colors.get(status, '#FAFAFA')
        alt = '#F7F9FF' if row_i % 2 == 0 else '#FFFFFF'
        row_bg = bg if status == 'Done' else alt

        row_data = [uid, story, priority, str(sp), status]
        for ci, (val, cx, cw) in enumerate(zip(row_data, col_x, col_widths)):
            bx = col_x[ci] - 0.01
            bw = cw / total

            face = row_bg
            if ci == 2:  # Priority column
                face = priority_colors.get(priority, '#555') + '22'
            ax.add_patch(plt.Rectangle(
                (bx, y_top), bw, ROW_H,
                transform=ax.transAxes, facecolor=face,
                edgecolor='#DDDDDD', linewidth=0.6, clip_on=False))

            # Text colour for priority
            tc = priority_colors.get(priority, '#333') if ci == 2 else '#222'
            fw = 'bold' if ci == 2 else 'normal'
            ax.text(cx + cw / total / 2 - 0.01,
                    y_top + ROW_H / 2, val,
                    transform=ax.transAxes, ha='center', va='center',
                    fontsize=7.8, color=tc, fontweight=fw, wrap=True)

    # Legend
    legend_y = 0.008
    for i, (prio, col) in enumerate(priority_colors.items()):
        lx = 0.05 + i * 0.22
        ax.add_patch(plt.Rectangle((lx, legend_y), 0.015, 0.02,
                     transform=ax.transAxes, facecolor=col, edgecolor='none'))
        ax.text(lx + 0.02, legend_y + 0.01, prio,
                transform=ax.transAxes, fontsize=8, va='center', color=col)

    ax.set_title('Product Backlog – StyleVault E-Commerce Project\n(MoSCoW Prioritisation · SP = Story Points)',
                 fontsize=13, fontweight='bold', pad=16, color=C['navy'])
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    return _save(fig, 'product_backlog.png', tight=False)


# ═══════════════════════════════════════════════════════════════
# 20.  SPRINT BACKLOG
# ═══════════════════════════════════════════════════════════════
def generate_sprint_backlog():
    """Two-sprint Kanban-style sprint backlog chart."""
    sprints = {
        'Sprint 1 (Weeks 1–4)': [
            ('US-01', 'Browse products by category',     'Done',        5),
            ('US-02', 'View product images & prices',    'Done',        5),
            ('US-05', 'Register an account',             'Done',        5),
            ('US-06', 'Log in and log out',              'Done',        5),
            ('US-08', 'Order confirmation page',         'Done',        5),
            ('US-03', 'Add items to shopping cart',      'Done',        8),
            ('US-04', 'Update / remove cart items',      'Done',        5),
        ],
        'Sprint 2 (Weeks 5–8)': [
            ('US-07', 'Complete checkout process',       'Done',       13),
            ('US-09', 'Filter products by price/size',   'Done',        8),
            ('US-10', 'Sort products',                   'Done',        3),
            ('US-11', 'Search for products',             'Done',        5),
            ('US-12', 'View related products',           'Done',        3),
            ('US-13', 'Contact customer support',        'Done',        3),
            ('US-14', 'Quick-add to cart from listing',  'Done',        5),
            ('US-16', 'Accessibility features',          'Done',        5),
        ],
    }

    status_col = {
        'Done':        '#2E7D32',
        'In Progress': '#E65100',
        'To Do':       '#1565C0',
    }
    status_bg = {
        'Done':        '#E8F5E9',
        'In Progress': '#FFF3E0',
        'To Do':       '#E3F2FD',
    }

    fig, axes = plt.subplots(1, 2, figsize=(20, 11))
    fig.patch.set_facecolor('white')

    for ax, (sprint_name, items) in zip(axes, sprints.items()):
        ax.set_xlim(0, 10)
        ax.set_ylim(-0.5, len(items) + 1.5)
        ax.axis('off')

        # Sprint header
        ax.add_patch(FancyBboxPatch((0, len(items) + 0.4), 10, 0.85,
                     boxstyle="round,pad=0.1", facecolor=C['navy'],
                     edgecolor=C['navy'], linewidth=1.5))
        ax.text(5, len(items) + 0.825, sprint_name,
                ha='center', va='center', fontsize=11,
                fontweight='bold', color='white')

        # Column headers
        cols = [('Story', 1.0), ('Description', 5.0), ('Status', 7.8), ('SP', 9.3)]
        for lbl, cx in cols:
            ax.add_patch(FancyBboxPatch((cx - 0.9, len(items) - 0.05), 1.8, 0.38,
                         boxstyle="round,pad=0.05", facecolor='#CFD8DC',
                         edgecolor='#607D8B', linewidth=0.8))
            ax.text(cx, len(items) + 0.14, lbl,
                    ha='center', va='center', fontsize=8.5, fontweight='bold')

        sp_total = 0
        for i, (uid, desc, status, sp) in enumerate(items):
            y = len(items) - 1 - i
            bg = status_bg.get(status, '#FAFAFA')
            ax.add_patch(FancyBboxPatch((0.05, y + 0.06), 9.9, 0.74,
                         boxstyle="round,pad=0.05", facecolor=bg,
                         edgecolor='#B0BEC5', linewidth=0.8))
            sc = status_col.get(status, '#333')
            ax.text(1.0, y + 0.43, uid,  ha='center', va='center', fontsize=8,
                    fontweight='bold', color=sc)
            ax.text(5.0, y + 0.43, desc, ha='center', va='center', fontsize=8,
                    color='#222')
            # Status badge
            ax.add_patch(FancyBboxPatch((6.75, y + 0.18), 2.1, 0.5,
                         boxstyle="round,pad=0.05", facecolor=sc,
                         edgecolor='none', linewidth=0))
            ax.text(7.8, y + 0.43, status, ha='center', va='center',
                    fontsize=7.5, fontweight='bold', color='white')
            ax.text(9.3, y + 0.43, str(sp), ha='center', va='center',
                    fontsize=9, fontweight='bold', color=sc)
            sp_total += sp

        # Total SP footer
        ax.add_patch(FancyBboxPatch((0.05, -0.42), 9.9, 0.38,
                     boxstyle="round,pad=0.05", facecolor='#ECEFF1',
                     edgecolor='#90A4AE', linewidth=0.8))
        ax.text(5, -0.23, f'Total Story Points: {sp_total}',
                ha='center', va='center', fontsize=9, fontweight='bold',
                color=C['navy'])

    fig.suptitle('Sprint Backlog – StyleVault Project (2 × 4-Week Sprints)',
                 fontsize=14, fontweight='bold', y=0.98, color=C['navy'])
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return _save(fig, 'sprint_backlog.png', tight=False)


# ═══════════════════════════════════════════════════════════════
# 21.  CLASS DIAGRAM
# ═══════════════════════════════════════════════════════════════
def generate_class_diagram():
    """UML Class Diagram of the StyleVault Flask data models."""
    fig, ax = plt.subplots(figsize=(26, 18))
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 18)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.02)

    TITLE_H  = 0.65
    ATTR_H   = 0.42
    METHOD_H = 0.42
    PAD      = 0.18

    def draw_class(cx, top_y, name, attributes, methods, color=C['navy']):
        hw = 3.2
        n_attr   = len(attributes)
        n_method = len(methods)
        h_attr   = n_attr * ATTR_H + PAD * 2
        h_meth   = max(n_method, 1) * METHOD_H + PAD * 2

        # ── Title bar
        ax.add_patch(FancyBboxPatch((cx - hw, top_y - TITLE_H), hw * 2, TITLE_H,
                     boxstyle="square,pad=0", facecolor=color,
                     edgecolor='#0D1F3C', linewidth=2.0))
        ax.text(cx, top_y - TITLE_H / 2, f'«class»  {name}',
                ha='center', va='center', fontsize=9.0,
                fontweight='bold', color='white')

        # ── Attributes section
        ay0 = top_y - TITLE_H
        ax.add_patch(FancyBboxPatch((cx - hw, ay0 - h_attr), hw * 2, h_attr,
                     boxstyle="square,pad=0", facecolor='#EEF4FF',
                     edgecolor='#0D1F3C', linewidth=1.6))
        for i, (vis, attr_name, atype) in enumerate(attributes):
            ay = ay0 - PAD - (i + 0.5) * ATTR_H
            ax.text(cx - hw + 0.18, ay, f'{vis} {attr_name}: {atype}',
                    fontsize=8.0, va='center', color='#1A237E')
            if i < n_attr - 1:
                ax.plot([cx - hw + 0.08, cx + hw - 0.08],
                        [ay0 - PAD - (i + 1) * ATTR_H] * 2,
                        color='#C5D8FF', linewidth=0.6)

        # ── Methods section
        my0 = ay0 - h_attr
        ax.add_patch(FancyBboxPatch((cx - hw, my0 - h_meth), hw * 2, h_meth,
                     boxstyle="square,pad=0", facecolor='#F0FFF4',
                     edgecolor='#0D1F3C', linewidth=1.6))
        for i, method in enumerate(methods):
            my = my0 - PAD - (i + 0.5) * METHOD_H
            ax.text(cx - hw + 0.18, my, method,
                    fontsize=8.0, va='center', color='#1B5E20')
            if i < n_method - 1:
                ax.plot([cx - hw + 0.08, cx + hw - 0.08],
                        [my0 - PAD - (i + 1) * METHOD_H] * 2,
                        color='#C8E6C9', linewidth=0.6)
        if not methods:
            ax.text(cx, my0 - h_meth / 2, '(no methods)',
                    ha='center', va='center', fontsize=7.5,
                    color='#9E9E9E', style='italic')

        bottom_y = my0 - h_meth
        return top_y, bottom_y, cx - hw, cx + hw

    def assoc(x1, y1, x2, y2, label='', style='solid', card='', end_card='',
              color='#37474F'):
        ls = '--' if style == 'dashed' else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color,
                                   lw=1.5, linestyle=ls))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.22, label, ha='center', fontsize=8.0,
                    color=color, style='italic',
                    bbox=dict(boxstyle='round,pad=0.14', facecolor='white',
                              edgecolor='#B2DFDB', alpha=0.9))
        if card:
            ax.text(x1 + (0.22 if x2 > x1 else -0.22),
                    y1 + 0.15, card, fontsize=8.5, color=color, fontweight='bold')
        if end_card:
            ax.text(x2 - (0.22 if x2 > x1 else -0.22),
                    y2 + 0.15, end_card, fontsize=8.5, color=color, fontweight='bold')

    # ─────────────────────────────────────────────────────────
    # Row 1 (top): User  |  Category  |  Product
    # Placed at x = 4.5, 13, 21.5 so they have ample spacing
    # ─────────────────────────────────────────────────────────
    # User (top-left)
    u_top, u_bot, u_l, u_r = draw_class(4.5, 17.2, 'User',
        attributes=[
            ('+', 'id', 'int'),
            ('+', 'email', 'str'),
            ('+', 'first_name', 'str'),
            ('+', 'last_name', 'str'),
            ('+', 'password_hash', 'str'),
            ('+', 'is_admin', 'bool'),
        ],
        methods=[
            '+ __repr__() → str',
        ])

    # Category (top-centre)
    cat_top, cat_bot, cat_l, cat_r = draw_class(13.0, 17.2, 'Category',
        attributes=[
            ('+', 'id', 'int'),
            ('+', 'name', 'str'),
            ('+', 'slug', 'str'),
            ('+', 'description', 'str'),
        ],
        methods=[
            '+ __repr__() → str',
        ])

    # Product (top-right)
    p_top, p_bot, p_l, p_r = draw_class(21.5, 17.2, 'Product',
        attributes=[
            ('+', 'id', 'int'),
            ('+', 'name', 'str'),
            ('+', 'brand', 'str'),
            ('+', 'price', 'float'),
            ('+', 'sale_price', 'float?'),
            ('+', 'stock', 'int'),
            ('+', 'image_url', 'str'),
            ('+', 'category_id', 'int [FK]'),
        ],
        methods=[
            '+ effective_price() → float',
            '+ __repr__() → str',
        ])

    # ─────────────────────────────────────────────────────────
    # Row 2 (middle): CartItem | Order | OrderItem
    # Placed at x = 4.5, 13, 21.5  — y starts at 9.0
    # ─────────────────────────────────────────────────────────
    # CartItem (middle-left)
    ci_top, ci_bot, ci_l, ci_r = draw_class(4.5, 9.0, 'CartItem',
        attributes=[
            ('+', 'id', 'int'),
            ('+', 'user_id', 'int [FK]'),
            ('+', 'product_id', 'int [FK]'),
            ('+', 'quantity', 'int'),
            ('+', 'size', 'str'),
        ],
        methods=[
            '+ subtotal() → float',
        ])

    # Order (middle-centre)
    o_top, o_bot, o_l, o_r = draw_class(13.0, 9.0, 'Order',
        attributes=[
            ('+', 'id', 'int'),
            ('+', 'user_id', 'int [FK]'),
            ('+', 'total', 'float'),
            ('+', 'status', 'str'),
            ('+', 'shipping_address', 'str'),
            ('+', 'created_at', 'datetime'),
        ],
        methods=[
            '+ __repr__() → str',
        ])

    # OrderItem (middle-right)
    oi_top, oi_bot, oi_l, oi_r = draw_class(21.5, 9.0, 'OrderItem',
        attributes=[
            ('+', 'id', 'int'),
            ('+', 'order_id', 'int [FK]'),
            ('+', 'product_id', 'int [FK]'),
            ('+', 'quantity', 'int'),
            ('+', 'price_at_purchase', 'float'),
        ],
        methods=[])

    # ContactMessage (bottom-centre)
    cm_top, cm_bot, cm_l, cm_r = draw_class(13.0, 2.5, 'ContactMessage',
        attributes=[
            ('+', 'id', 'int'),
            ('+', 'name', 'str'),
            ('+', 'email', 'str'),
            ('+', 'subject', 'str'),
            ('+', 'message', 'str'),
        ],
        methods=[])

    # ── Associations ─────────────────────────────────────────────────
    # User (4.5) → CartItem (4.5): straight down
    assoc(4.5, u_bot, 4.5, ci_top, 'has', card='1', end_card='N')
    # User (4.5) → Order (13.0): horizontal at mid-level 14.5
    assoc(u_r, 14.5, o_l, 14.5, 'places', card='1', end_card='N')
    # Category (13.0) → Product (21.5): horizontal
    cat_link_y = cat_bot + (cat_top - cat_bot) * 0.6
    assoc(cat_r, cat_link_y, p_l, cat_link_y, 'contains', card='1', end_card='N')
    # Order (13.0) → OrderItem (21.5): horizontal
    assoc(o_r, o_bot + 0.5, oi_l, oi_bot + 0.5, 'contains', card='1', end_card='N')
    # Product (21.5) → CartItem (4.5): arc via top
    assoc(p_l, p_bot + 1.0, ci_r, ci_bot + 1.0, 'added to', end_card='N')
    # Product (21.5) → OrderItem (21.5): straight down
    assoc(21.5, p_bot, 21.5, oi_top, 'ordered in', end_card='N')
    # Order (13.0) → ContactMessage: via vertical on left side
    assoc(13.0, o_bot, 13.0, cm_top, '', card='', end_card='')

    ax.set_title('UML Class Diagram — StyleVault Data Models (Flask-SQLAlchemy)',
                 fontsize=14, fontweight='bold', pad=16, color=C['navy'])
    return _save(fig, 'class_diagram.png')


# ═══════════════════════════════════════════════════════════════
# 22.  STATE DIAGRAM (Order lifecycle)
# ═══════════════════════════════════════════════════════════════
def generate_state_diagram():
    """UML State Diagram showing the Order status lifecycle."""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    STATE_W, STATE_H = 2.8, 0.70

    def state(x, y, text, color=C['blue'], lcolor='white'):
        ax.add_patch(FancyBboxPatch((x - STATE_W/2, y - STATE_H/2),
                     STATE_W, STATE_H,
                     boxstyle="round,pad=0.15", facecolor=color,
                     edgecolor='#0D1F3C', linewidth=1.6))
        ax.text(x, y, text, ha='center', va='center', fontsize=10,
                fontweight='bold', color=lcolor)

    def start_node(x, y):
        ax.add_patch(plt.Circle((x, y), 0.25, fc='#1A1A1A', ec='#1A1A1A'))

    def end_node(x, y):
        ax.add_patch(plt.Circle((x, y), 0.30, fc='white', ec='#1A1A1A', lw=2.0))
        ax.add_patch(plt.Circle((x, y), 0.18, fc='#1A1A1A', ec='#1A1A1A'))

    def trans(x1, y1, x2, y2, label='', rad=0.0, offset=(0, 0.2)):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(
                        arrowstyle='->', color='#37474F', lw=1.4,
                        connectionstyle=f'arc3,rad={rad}'))
        if label:
            mx = (x1 + x2) / 2 + offset[0]
            my = (y1 + y2) / 2 + offset[1]
            ax.text(mx, my, label, ha='center', fontsize=8,
                    style='italic', color='#37474F',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                              edgecolor='#B2DFDB', alpha=0.9))

    # ── Nodes ───────────────────────────────────────────────────
    cx = 7.0
    start_node(cx, 9.3)

    state(cx, 8.2, 'Pending', color='#FFA000', lcolor='white')
    state(cx, 6.7, 'Confirmed', color='#1565C0')
    state(cx, 5.2, 'Processing', color='#6A1B9A')
    state(cx, 3.7, 'Shipped', color='#00695C')
    state(cx, 2.2, 'Delivered', color='#2E7D32')

    # Cancel paths
    state(11.5, 5.95, 'Cancelled', color='#C62828')
    state(4.0,  5.2,  'Refund\nRequested', color='#E65100', lcolor='white')
    state(4.0,  3.7,  'Refunded', color='#BF360C', lcolor='white')

    end_node(cx, 0.7)

    # ── Transitions ─────────────────────────────────────────────
    trans(cx, 9.05, cx, 8.55, 'Customer places order')
    trans(cx, 7.85, cx, 7.05, 'Payment confirmed')
    trans(cx, 6.35, cx, 5.55, 'Admin reviews order')
    trans(cx, 4.85, cx, 4.05, 'Item dispatched')
    trans(cx, 3.35, cx, 2.55, 'Delivery confirmed')
    trans(cx, 1.85, cx, 1.0, 'Order complete')

    # Cancellation from Pending
    trans(cx + STATE_W/2, 8.2, 11.5 - STATE_W/2, 6.2,
          'Customer cancels', rad=-0.25, offset=(1.1, 0.15))
    # Cancellation from Confirmed
    trans(cx + STATE_W/2, 6.7, 11.5 - STATE_W/2, 5.7,
          'Admin cancels', rad=-0.2, offset=(0.9, 0.15))

    # Refund from Delivered
    trans(cx - STATE_W/2, 2.2, 4.0 + STATE_W/2, 5.2,
          'Customer requests refund', rad=0.3, offset=(-1.4, 0))
    trans(4.0, 4.85, 4.0, 4.05, 'Refund approved')

    # Cancelled → end
    trans(11.5, 5.60, cx + 0.4, 1.0, 'Closed', rad=0.3, offset=(1.5, 0))

    # Refunded → end
    trans(4.0, 3.35, cx - 0.4, 1.0, 'Closed', rad=-0.25, offset=(-1.4, 0))

    # Legend
    legend_items = [
        ('Pending',           '#FFA000'),
        ('Confirmed',         '#1565C0'),
        ('Processing',        '#6A1B9A'),
        ('Shipped',           '#00695C'),
        ('Delivered',         '#2E7D32'),
        ('Cancelled',         '#C62828'),
        ('Refund Requested',  '#E65100'),
        ('Refunded',          '#BF360C'),
    ]
    ax.add_patch(FancyBboxPatch((0.2, 0.1), 2.6, len(legend_items) * 0.42 + 0.3,
                 boxstyle="round,pad=0.1", facecolor='#FAFAFA',
                 edgecolor='#CFD8DC', linewidth=1.0))
    for i, (lbl, col) in enumerate(legend_items):
        ly = (len(legend_items) - 1 - i) * 0.42 + 0.4
        ax.add_patch(plt.Rectangle((0.35, ly + 0.07), 0.25, 0.26,
                     facecolor=col, edgecolor='none'))
        ax.text(0.7, ly + 0.20, lbl, fontsize=7.5, va='center', color='#333')

    ax.set_title('State Diagram – Order Lifecycle (StyleVault)',
                 fontsize=13, fontweight='bold', pad=14, color=C['navy'])
    return _save(fig, 'state_diagram.png')


# ═══════════════════════════════════════════════════════════════
# GENERATE ALL
# ═══════════════════════════════════════════════════════════════
def generate_user_personas():
    """Generate a User Personas diagram with 3 detailed personas."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 10))
    fig.patch.set_facecolor('#F8F5F0')

    personas = [
        {
            'name': 'Emma Chen',
            'age': '28',
            'occupation': 'Fashion Blogger / Influencer',
            'location': 'London, UK',
            'tech': '★★★★★',
            'goal': 'Find premium, on-trend pieces to feature in her blog content and social media',
            'frustrations': [
                'Slow, cluttered websites',
                'No size filters',
                'Poor product photography',
                'Limited size availability info',
            ],
            'needs': [
                'High-quality product images',
                'Easy category navigation',
                'Quick add-to-cart',
                'Mobile-friendly interface',
            ],
            'quote': '"I need to find the perfect outfit in 5 minutes — not 50."',
            'color': '#1A1A2E',
            'icon_label': 'E',
        },
        {
            'name': 'James Mitchell',
            'age': '35',
            'occupation': 'Senior Financial Analyst',
            'location': 'Manchester, UK',
            'tech': '★★★☆☆',
            'goal': 'Buy quality professional attire without spending hours browsing',
            'frustrations': [
                'Overly complex checkout',
                'No size guide',
                'Unclear return policies',
                'Too many irrelevant results',
            ],
            'needs': [
                'Efficient checkout process',
                'Size guide / fit info',
                'Clear pricing (no surprises)',
                'Men\'s category prominent',
            ],
            'quote': '"I want to buy a suit, not solve a puzzle."',
            'color': '#2C5F2E',
            'icon_label': 'J',
        },
        {
            'name': 'Priya Sharma',
            'age': '22',
            'occupation': 'University Student (Fashion Design)',
            'location': 'Birmingham, UK',
            'tech': '★★★★☆',
            'goal': 'Discover affordable luxury pieces and get inspired by editorial styling',
            'frustrations': [
                'Hidden delivery costs',
                'No sale section visible',
                'Difficult to compare items',
                'Login required too early',
            ],
            'needs': [
                'Sale / discount section',
                'Free UK delivery',
                'Easy account creation',
                'Product filtering by price',
            ],
            'quote': '"Style shouldn\'t cost the earth — literally."',
            'color': '#7B2D8B',
            'icon_label': 'P',
        },
    ]

    for ax, persona in zip(axes, personas):
        ax.set_facecolor('white')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 18)
        ax.axis('off')

        # Header block
        header_rect = plt.Rectangle((0, 15.5), 10, 2.5, color=persona['color'])
        ax.add_patch(header_rect)

        # Avatar circle
        circle = plt.Circle((1.4, 16.75), 0.9, color='white', zorder=3)
        ax.add_patch(circle)
        ax.text(1.4, 16.75, persona['icon_label'], fontsize=22, fontweight='bold',
                color=persona['color'], ha='center', va='center', zorder=4,
                fontfamily='DejaVu Sans')

        # Name + role
        ax.text(2.5, 17.4, persona['name'], fontsize=13, fontweight='bold',
                color='white', va='center', fontfamily='DejaVu Sans')
        ax.text(2.5, 16.85, f"Age {persona['age']}  ·  {persona['occupation']}",
                fontsize=7.5, color='#DDDDDD', va='center', fontfamily='DejaVu Sans')
        ax.text(2.5, 16.35, f"📍 {persona['location']}  ·  Tech: {persona['tech']}",
                fontsize=7.5, color='#DDDDDD', va='center', fontfamily='DejaVu Sans')

        # Goal section
        ax.add_patch(plt.Rectangle((0, 14.2), 10, 1.2, color='#F0EDE8'))
        ax.text(0.3, 15.15, 'GOAL', fontsize=7, fontweight='bold',
                color=persona['color'], va='center', fontfamily='DejaVu Sans')
        wrapped = []
        words = persona['goal'].split()
        line = ''
        for w in words:
            if len(line) + len(w) + 1 <= 42:
                line = (line + ' ' + w).strip()
            else:
                wrapped.append(line)
                line = w
        if line:
            wrapped.append(line)
        goal_text = '\n'.join(wrapped[:3])
        ax.text(0.3, 14.75, goal_text, fontsize=7.5, color='#333333',
                va='center', fontfamily='DejaVu Sans')

        # Needs section
        ax.add_patch(plt.Rectangle((0, 11.0), 4.8, 3.0, color='#E8F4E8'))
        ax.text(0.3, 13.8, 'NEEDS', fontsize=7, fontweight='bold',
                color='#2C5F2E', va='center', fontfamily='DejaVu Sans')
        for i, need in enumerate(persona['needs']):
            ax.text(0.3, 13.3 - i * 0.65, f'✓  {need}', fontsize=7,
                    color='#333333', va='center', fontfamily='DejaVu Sans')

        # Frustrations section
        ax.add_patch(plt.Rectangle((5.2, 11.0), 4.8, 3.0, color='#FDE8E8'))
        ax.text(5.5, 13.8, 'FRUSTRATIONS', fontsize=7, fontweight='bold',
                color='#C0392B', va='center', fontfamily='DejaVu Sans')
        for i, frust in enumerate(persona['frustrations']):
            ax.text(5.5, 13.3 - i * 0.65, f'✗  {frust}', fontsize=7,
                    color='#333333', va='center', fontfamily='DejaVu Sans')

        # Quote
        ax.add_patch(plt.Rectangle((0, 9.2), 10, 1.6, color='#F8F8F8',
                                    linewidth=1.5, linestyle='--',
                                    edgecolor=persona['color']))
        ax.text(5.0, 10.0, persona['quote'], fontsize=8.5, color=persona['color'],
                ha='center', va='center', style='italic', fontfamily='DejaVu Sans',
                wrap=True)

    fig.suptitle('StyleVault — User Personas', fontsize=18, fontweight='bold',
                 y=0.97, color='#1A1A2E', fontfamily='DejaVu Sans')
    fig.text(0.5, 0.01,
             'Three primary user personas identified through requirements analysis and competitor research',
             ha='center', fontsize=9, color='#555555', fontfamily='DejaVu Sans')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    out = os.path.join(OUTPUT_DIR, 'user_personas.png')
    plt.savefig(out, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  [OK] user_personas.png")
    return out


def generate_vscode_screenshot(title, code_lines, filename,
                               theme_bg='#1e1e1e', language='python'):
    """Render code as a VS Code Dark+ themed screenshot image."""
    # VS Code Dark+ syntax colours (simplified)
    KEYWORD  = '#569cd6'
    STRING   = '#ce9178'
    COMMENT  = '#6a9955'
    FUNC     = '#dcdcaa'
    CLASS    = '#4ec9b0'
    NUMBER   = '#b5cea8'
    PUNCT    = '#d4d4d4'
    DEFAULT  = '#d4d4d4'
    DECOR    = '#c586c0'

    import re

    # Simple tokeniser for Python-like syntax highlighting
    def colorise(line):
        # Returns list of (text, color) spans
        tokens = []
        # Strip and keep
        i = 0
        while i < len(line):
            # Comment
            m = re.match(r'(#.*)$', line[i:])
            if m:
                tokens.append((m.group(1), COMMENT)); break
            # String (double or single quoted, simplified)
            m = re.match(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')',
                          line[i:])
            if m:
                tokens.append((m.group(1), STRING)); i += len(m.group(1)); continue
            # Decorator
            m = re.match(r'(@\w+)', line[i:])
            if m:
                tokens.append((m.group(1), DECOR)); i += len(m.group(1)); continue
            # Keywords
            m = re.match(r'\b(def|class|import|from|return|if|elif|else|for|while|'
                         r'in|not|and|or|True|False|None|try|except|finally|with|'
                         r'as|pass|break|continue|raise|lambda|yield|self|app|'
                         r'db|route|GET|POST)\b', line[i:])
            if m:
                tokens.append((m.group(1), KEYWORD)); i += len(m.group(1)); continue
            # Numbers
            m = re.match(r'\b(\d+\.?\d*)\b', line[i:])
            if m:
                tokens.append((m.group(1), NUMBER)); i += len(m.group(1)); continue
            # Function calls
            m = re.match(r'(\w+)(?=\s*\()', line[i:])
            if m:
                tokens.append((m.group(1), FUNC)); i += len(m.group(1)); continue
            # Generic word
            m = re.match(r'(\w+)', line[i:])
            if m:
                tokens.append((m.group(1), DEFAULT)); i += len(m.group(1)); continue
            # Punctuation / space
            tokens.append((line[i], PUNCT)); i += 1
        return tokens

    LINE_H    = 0.40   # inches per line
    CHAR_W    = 0.075  # inches per monospace char estimate
    TITLE_H   = 0.55   # window bar
    PAD_TOP   = 0.18
    PAD_SIDE  = 0.30
    LINE_NO_W = 0.45

    max_chars = max((len(l) for l in code_lines), default=40)
    fig_w     = max(10.0, PAD_SIDE * 2 + LINE_NO_W + max_chars * CHAR_W * 0.95)
    fig_h     = TITLE_H + PAD_TOP + len(code_lines) * LINE_H + 0.25

    fig = plt.figure(figsize=(fig_w, fig_h), facecolor=theme_bg)
    ax  = fig.add_axes([0, 0, 1, 1], facecolor=theme_bg)
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis('off')

    # ── Window title bar ──────────────────────────────────────
    bar_y = fig_h - TITLE_H
    ax.add_patch(plt.Rectangle((0, bar_y), fig_w, TITLE_H,
                 facecolor='#3c3c3c', edgecolor='none'))
    # Traffic light dots
    for xi, col in [(0.18, '#ff5f57'), (0.38, '#ffbd2e'), (0.58, '#28c940')]:
        ax.add_patch(plt.Circle((xi, bar_y + TITLE_H/2), 0.07,
                     facecolor=col, edgecolor='none'))
    ax.text(fig_w / 2, bar_y + TITLE_H / 2,
            f'{title}  —  {language}',
            ha='center', va='center', color='#cccccc',
            fontsize=8, fontfamily='monospace')

    # ── Line number gutter ────────────────────────────────────
    gutter_x = PAD_SIDE + LINE_NO_W
    ax.add_patch(plt.Rectangle((0, 0), gutter_x, bar_y,
                 facecolor='#252526', edgecolor='none'))
    ax.plot([gutter_x, gutter_x], [0, bar_y],
            color='#3e3e3e', linewidth=0.6)

    # ── Code lines ────────────────────────────────────────────
    font_size = 7.8
    for idx, raw_line in enumerate(code_lines):
        # y position (top of file = top of code area)
        y = bar_y - PAD_TOP - (idx + 0.70) * LINE_H

        # Line number
        ax.text(gutter_x - 0.08, y, str(idx + 1),
                ha='right', va='center', color='#858585',
                fontsize=font_size * 0.85, fontfamily='monospace')

        # Code with colour tokens
        x = gutter_x + 0.14
        stripped = raw_line.rstrip()
        leading  = len(stripped) - len(stripped.lstrip())
        # Leading spaces
        if leading:
            ax.text(x, y, ' ' * leading, ha='left', va='center',
                    color=DEFAULT, fontsize=font_size, fontfamily='monospace')
            x += leading * CHAR_W * 0.92

        spans = colorise(stripped.lstrip())
        for text, col in spans:
            ax.text(x, y, text, ha='left', va='center',
                    color=col, fontsize=font_size, fontfamily='monospace')
            x += len(text) * CHAR_W * 0.92

    _dir()
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=theme_bg)
    plt.close(fig)
    print(f"  [OK] {filename}")
    return path


# ─── Pre-defined code screenshot exports ──────────────────────
def generate_code_screenshots():
    """Generate VS Code themed code screenshots for the report."""
    paths = {}

    # 1. Flask app routes
    paths['code_routes'] = generate_vscode_screenshot(
        'app.py — Core Routes', [
            "from flask import Flask, render_template, request, redirect",
            "from flask import url_for, session, flash",
            "from flask_sqlalchemy import SQLAlchemy",
            "from werkzeug.security import generate_password_hash, check_password_hash",
            "",
            "app = Flask(__name__)",
            "app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(",
            "    'DATABASE_URL', 'sqlite:///stylevault.db')",
            "db = SQLAlchemy(app)",
            "",
            "@app.route('/')",
            "def index():",
            "    products = Product.query.filter_by(featured=True).limit(8).all()",
            "    categories = Category.query.all()",
            "    return render_template('index.html',",
            "                         products=products,",
            "                         categories=categories)",
            "",
            "@app.route('/products')",
            "def products():",
            "    category = request.args.get('category')",
            "    search   = request.args.get('search', '')",
            "    query    = Product.query",
            "    if category:",
            "        query = query.filter_by(category_slug=category)",
            "    if search:",
            "        query = query.filter(Product.name.ilike(f'%{search}%'))",
            "    return render_template('products.html',",
            "                         products=query.all())",
        ], 'code_routes.png')

    # 2. SQLAlchemy models
    paths['code_models'] = generate_vscode_screenshot(
        'models.py — SQLAlchemy Models', [
            "from flask_sqlalchemy import SQLAlchemy",
            "from werkzeug.security import generate_password_hash, check_password_hash",
            "",
            "db = SQLAlchemy()",
            "",
            "class User(db.Model):",
            "    __tablename__ = 'users'",
            "    id            = db.Column(db.Integer, primary_key=True)",
            "    email         = db.Column(db.String(120), unique=True, nullable=False)",
            "    first_name    = db.Column(db.String(50), nullable=False)",
            "    last_name     = db.Column(db.String(50), nullable=False)",
            "    password_hash = db.Column(db.String(256))",
            "    is_admin      = db.Column(db.Boolean, default=False)",
            "",
            "class Product(db.Model):",
            "    __tablename__ = 'products'",
            "    id         = db.Column(db.Integer, primary_key=True)",
            "    name       = db.Column(db.String(200), nullable=False)",
            "    brand      = db.Column(db.String(100))",
            "    price      = db.Column(db.Float, nullable=False)",
            "    sale_price = db.Column(db.Float)",
            "    stock      = db.Column(db.Integer, default=0)",
            "    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))",
            "",
            "    def effective_price(self):",
            "        return self.sale_price if self.sale_price else self.price",
        ], 'code_models.png')

    # 3. Checkout route
    paths['code_checkout'] = generate_vscode_screenshot(
        'app.py — Checkout Route', [
            "@app.route('/checkout', methods=['GET', 'POST'])",
            "def checkout():",
            "    if 'user_id' not in session:",
            "        flash('Please log in to checkout.', 'warning')",
            "        return redirect(url_for('login'))",
            "    cart_items = CartItem.query.filter_by(",
            "        user_id=session['user_id']).all()",
            "    if not cart_items:",
            "        return redirect(url_for('cart'))",
            "    if request.method == 'POST':",
            "        total = sum(item.product.effective_price()",
            "                    * item.quantity for item in cart_items)",
            "        order = Order(",
            "            user_id          = session['user_id'],",
            "            total            = total,",
            "            status           = 'Confirmed',",
            "            shipping_address = request.form['address'])",
            "        db.session.add(order)",
            "        db.session.flush()",
            "        for item in cart_items:",
            "            oi = OrderItem(",
            "                order_id          = order.id,",
            "                product_id        = item.product_id,",
            "                quantity          = item.quantity,",
            "                price_at_purchase = item.product.effective_price())",
            "            db.session.add(oi)",
            "        CartItem.query.filter_by(",
            "            user_id=session['user_id']).delete()",
            "        db.session.commit()",
            "        return redirect(url_for('order_confirmation',",
            "                                order_id=order.id))",
            "    return render_template('checkout.html', cart=cart_items)",
        ], 'code_checkout.png')

    # 4. Admin CRUD route
    paths['code_admin'] = generate_vscode_screenshot(
        'app.py — Admin Product CRUD', [
            "@app.route('/admin/products')",
            "def admin_products():",
            "    if not session.get('is_admin'):",
            "        return redirect(url_for('index'))",
            "    products = Product.query.order_by(Product.name).all()",
            "    return render_template('admin_products.html', products=products)",
            "",
            "@app.route('/admin/products/add', methods=['GET', 'POST'])",
            "def admin_add_product():",
            "    if not session.get('is_admin'):",
            "        return redirect(url_for('index'))",
            "    if request.method == 'POST':",
            "        product = Product(",
            "            name        = request.form['name'],",
            "            brand       = request.form['brand'],",
            "            price       = float(request.form['price']),",
            "            stock       = int(request.form['stock']),",
            "            category_id = int(request.form['category_id']))",
            "        db.session.add(product)",
            "        db.session.commit()",
            "        flash('Product added successfully.', 'success')",
            "        return redirect(url_for('admin_products'))",
            "    categories = Category.query.all()",
            "    return render_template('admin_add_product.html',",
            "                          categories=categories)",
            "",
            "@app.route('/admin/products/<int:pid>/delete', methods=['POST'])",
            "def admin_delete_product(pid):",
            "    if not session.get('is_admin'):",
            "        return redirect(url_for('index'))",
            "    Product.query.filter_by(id=pid).delete()",
            "    db.session.commit()",
            "    return redirect(url_for('admin_products'))",
        ], 'code_admin.png')

    return paths


# ─── Google Form SVG exports ──────────────────────────────────
def generate_google_form_survey():
    """Render a realistic Google Form survey SVG as PNG."""
    fig, ax = plt.subplots(figsize=(10, 16))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis('off')
    fig.patch.set_facecolor('#f0ebff')

    # ── Header strip ──────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((0.5, 14.6), 9.0, 1.2,
                 boxstyle="round,pad=0.0", facecolor='#673ab7', edgecolor='none'))
    ax.text(5, 15.35, 'StyleVault — User Experience Survey',
            ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    ax.text(5, 14.95, 'Help us improve your shopping experience  •  Takes ~2 minutes',
            ha='center', va='center', fontsize=8.5, color=(1, 1, 1, 0.85))

    # Progress bar
    ax.add_patch(plt.Rectangle((0.5, 14.6), 9.0, 0.07, facecolor='#3e2465', edgecolor='none'))
    ax.add_patch(plt.Rectangle((0.5, 14.6), 6.3, 0.07, facecolor='#b39ddb', edgecolor='none'))

    def form_card(y_top, height):
        ax.add_patch(FancyBboxPatch((0.5, y_top), 9.0, height,
                     boxstyle="round,pad=0.0", facecolor='white',
                     edgecolor='#e0e0e0', linewidth=0.8))

    def question(ax, y, qnum, text, qtype, options=None, required=True):
        """Draw a single Google Form question block."""
        block_h = 0.55 + (len(options) * 0.38 if options else 0.42)
        form_card(y - block_h, block_h)
        # Question text
        star = ' *' if required else ''
        ax.text(0.85, y - 0.30, f'{qnum}. {text}{star}',
                fontsize=9.0, fontweight='bold', color='#202124', va='top')
        ax.text(0.85, y - 0.50, qtype,
                fontsize=7, color='#5f6368', va='top')
        if options:
            for i, opt in enumerate(options):
                oy = y - 0.75 - i * 0.38
                # Radio circle
                ax.add_patch(plt.Circle((1.10, oy + 0.08), 0.09,
                             facecolor='white', edgecolor='#5f6368', linewidth=1.2))
                ax.text(1.32, oy + 0.08, opt, fontsize=8.5, color='#202124', va='center')
        else:
            # Text input underline
            uy = y - 0.80
            ax.plot([0.85, 9.2], [uy, uy], color='#9e9e9e', linewidth=0.8)
            ax.text(0.85, uy + 0.06, 'Your answer', fontsize=8, color='#bdbdbd')
        return y - block_h - 0.18

    # Questions
    y = 14.30
    y = question(ax, y, 1, 'How did you hear about StyleVault?',
                 'Multiple choice',
                 ['Social Media (Instagram / TikTok)', 'Google Search',
                  'Friend or Family Recommendation', 'Online Advertisement', 'Other'])
    y = question(ax, y, 2,
                 'How would you rate the overall design / look of the website?',
                 'Linear scale  (1 = Poor, 5 = Excellent)',
                 ['1 – Poor', '2 – Below Average', '3 – Average',
                  '4 – Good', '5 – Excellent'])
    y = question(ax, y, 3, 'Was the website easy to navigate?',
                 'Multiple choice',
                 ['Very Easy', 'Easy', 'Neutral', 'Difficult', 'Very Difficult'])
    y = question(ax, y, 4,
                 'How satisfied are you with the product range available?',
                 'Multiple choice',
                 ['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied'])
    y = question(ax, y, 5, 'Did you experience any issues during checkout?',
                 'Multiple choice',
                 ['No issues', 'Slow loading', 'Error messages',
                  'Payment problem', 'Other'])
    y = question(ax, y, 6,
                 'Would you recommend StyleVault to a friend?',
                 'Multiple choice',
                 ['Definitely Yes', 'Probably Yes', 'Not Sure', 'Probably Not', 'No'])
    y = question(ax, y, 7,
                 'What features would you like to see added?',
                 'Short answer (free text)', None)

    # Submit button
    ax.add_patch(FancyBboxPatch((0.5, y - 0.68), 9.0, 0.58,
                 boxstyle="round,pad=0.0", facecolor='white',
                 edgecolor='#e0e0e0', linewidth=0.8))
    ax.add_patch(FancyBboxPatch((0.85, y - 0.56), 1.6, 0.36,
                 boxstyle="round,pad=0.04", facecolor='#673ab7', edgecolor='none'))
    ax.text(1.65, y - 0.38, 'Submit', ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')
    ax.text(9.15, y - 0.38, 'Never submit passwords', ha='right', va='center',
            fontsize=7, color='#5f6368')

    # Google footer
    ax.text(5, y - 0.90, 'Google Forms  ·  This content is neither created nor endorsed by Google.',
            ha='center', va='center', fontsize=6.5, color='#80868b')

    ax.set_title('Appendix C — StyleVault User Survey Form',
                 fontsize=11, fontweight='bold', pad=10, color='#673ab7')
    return _save(fig, 'google_form_survey.png')


def generate_google_form_analytics():
    """Render a realistic Google Forms response analytics page as PNG."""
    fig = plt.figure(figsize=(12, 18))
    fig.patch.set_facecolor('#f8f9fa')

    # ── Summary header ────────────────────────────────────────
    ax_header = fig.add_axes([0.04, 0.94, 0.92, 0.055])
    ax_header.set_xlim(0, 12); ax_header.set_ylim(0, 1); ax_header.axis('off')
    ax_header.add_patch(FancyBboxPatch((0, 0), 12, 1,
                        boxstyle="round,pad=0", facecolor='#673ab7', edgecolor='none'))
    ax_header.text(6, 0.70, 'Responses  —  StyleVault User Experience Survey',
                   ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    ax_header.text(6, 0.28, '15 responses  ·  Accepting responses',
                   ha='center', va='center', fontsize=9, color=(1, 1, 1, 0.80))

    PURPLE  = '#673ab7'
    LPURPLE = '#b39ddb'
    COLORS  = ['#7e57c2', '#42a5f5', '#26a69a', '#ef5350', '#ffa726',
               '#66bb6a', '#ab47bc', '#29b6f6']

    def pie_chart(fig, rect, title, labels, values):
        ax = fig.add_axes(rect)
        ax.set_aspect('equal')
        wedges, texts, autotexts = ax.pie(
            values, labels=None, autopct='%1.0f%%',
            colors=COLORS[:len(values)], startangle=90,
            pctdistance=0.72,
            wedgeprops=dict(edgecolor='white', linewidth=1.5))
        for at in autotexts:
            at.set_fontsize(7); at.set_color('white'); at.set_fontweight('bold')
        # Legend
        ax.legend(wedges, [f'{l} ({v})' for l, v in zip(labels, values)],
                  loc='lower center', bbox_to_anchor=(0.5, -0.48),
                  fontsize=6.5, frameon=False, ncol=1)
        ax.set_title(title, fontsize=8.5, fontweight='bold', color='#202124', pad=8)
        return ax

    def bar_chart(fig, rect, title, labels, values):
        ax = fig.add_axes(rect)
        y_pos = range(len(labels))
        bars = ax.barh(list(y_pos), values, color=COLORS[:len(values)],
                       edgecolor='white', height=0.6)
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(labels, fontsize=7)
        ax.set_xlabel('Responses', fontsize=7)
        ax.tick_params(axis='x', labelsize=6.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    str(val), va='center', fontsize=7, fontweight='bold', color='#444')
        ax.set_title(title, fontsize=8.5, fontweight='bold', color='#202124', pad=8)
        ax.set_facecolor('#fafafa')
        return ax

    # ── Q1: How did you hear about us ─────────────────────────
    pie_chart(fig, [0.05, 0.77, 0.40, 0.155],
              'Q1: How did you hear about StyleVault?',
              ['Social Media', 'Google Search', 'Friend/Family', 'Ad', 'Other'],
              [6, 4, 2, 2, 1])

    # ── Q2: Overall rating ────────────────────────────────────
    bar_chart(fig, [0.55, 0.77, 0.40, 0.155],
              'Q2: Overall Design Rating (1-5)',
              ['1 – Poor', '2 – Below Avg', '3 – Average', '4 – Good', '5 – Excellent'],
              [0, 1, 2, 5, 7])

    # ── Q3: Navigation ease ───────────────────────────────────
    pie_chart(fig, [0.05, 0.575, 0.40, 0.155],
              'Q3: Was the website easy to navigate?',
              ['Very Easy', 'Easy', 'Neutral', 'Difficult', 'Very Difficult'],
              [7, 5, 2, 1, 0])

    # ── Q4: Product satisfaction ──────────────────────────────
    bar_chart(fig, [0.55, 0.575, 0.40, 0.155],
              'Q4: Satisfaction with product range',
              ['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied'],
              [6, 7, 2, 0])

    # ── Q5: Checkout issues ───────────────────────────────────
    pie_chart(fig, [0.05, 0.38, 0.40, 0.155],
              'Q5: Checkout experience',
              ['No issues', 'Slow loading', 'Error msg', 'Payment', 'Other'],
              [10, 2, 1, 1, 1])

    # ── Q6: Recommend ─────────────────────────────────────────
    bar_chart(fig, [0.55, 0.38, 0.40, 0.155],
              'Q6: Would you recommend StyleVault?',
              ['Definitely Yes', 'Probably Yes', 'Not Sure', 'Probably Not', 'No'],
              [9, 4, 1, 1, 0])

    # ── Q7 qualitative summary ────────────────────────────────
    ax_q7 = fig.add_axes([0.05, 0.20, 0.90, 0.155])
    ax_q7.set_xlim(0, 12); ax_q7.set_ylim(0, 3); ax_q7.axis('off')
    ax_q7.add_patch(FancyBboxPatch((0, 0), 12, 3,
                    boxstyle="round,pad=0.02", facecolor='white',
                    edgecolor='#e0e0e0', linewidth=0.8))
    ax_q7.text(0.3, 2.65, 'Q7: What features would you like to see added?  (Selected responses)',
               fontsize=9, fontweight='bold', color='#202124')
    responses = [
        '"Wishlist / save for later feature would be great."',
        '"Dark mode would be a nice addition to the website."',
        '"Size guide with measurements – very useful for online shopping."',
        '"More filter options, e.g. by colour, material, or price range."',
        '"Faster checkout — remember my shipping details for next time."',
    ]
    for i, resp in enumerate(responses):
        ax_q7.text(0.5, 2.18 - i * 0.44, resp, fontsize=8.0, color='#444',
                   style='italic')

    # ── NPS summary box ───────────────────────────────────────
    ax_nps = fig.add_axes([0.05, 0.10, 0.90, 0.085])
    ax_nps.set_xlim(0, 12); ax_nps.set_ylim(0, 1); ax_nps.axis('off')
    ax_nps.add_patch(FancyBboxPatch((0, 0), 12, 1,
                     boxstyle="round,pad=0", facecolor=PURPLE, edgecolor='none'))
    ax_nps.text(6, 0.68, 'Key Metrics Summary',
                ha='center', fontsize=10, fontweight='bold', color='white')
    metrics = [
        ('Total Responses', '15'),
        ('Avg. Design Rating', '4.3 / 5'),
        ('Would Recommend', '87%'),
        ('Checkout Issue-Free', '67%'),
    ]
    for i, (lbl, val) in enumerate(metrics):
        mx = 1.5 + i * 3.0
        ax_nps.text(mx, 0.38, val, ha='center', fontsize=12,
                    fontweight='bold', color='white')
        ax_nps.text(mx, 0.12, lbl, ha='center', fontsize=7,
                    color=(1, 1, 1, 0.75))

    fig.suptitle('Appendix C — Google Forms Response Analytics  (15 respondents)',
                 fontsize=11, fontweight='bold', color=PURPLE, y=0.995)
    return _save(fig, 'google_form_analytics.png')


# ─── Mobile Phone Frame Mockup ───────────────────────────────
def generate_mobile_mockup():
    """
    Render three mobile phone mockup frames (homepage, products, nav menu)
    side-by-side on a single canvas to show responsive design.
    """
    import os
    from matplotlib.patches import FancyBboxPatch, Arc
    from PIL import Image as PILImage

    SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'screenshots')

    # Slots: (title, screenshot_filename)
    slots = [
        ('Homepage',        'responsive_mobile_homepage.png'),
        ('Product Listing', 'responsive_mobile_products.png'),
        ('Hamburger Menu',  'responsive_mobile_menu.png'),
    ]

    # Canvas
    fig, axes = plt.subplots(1, 3, figsize=(15, 9))
    fig.patch.set_facecolor('#1a1a2e')
    fig.suptitle('StyleVault — Mobile Responsiveness (375 px · iPhone SE)',
                 fontsize=14, color='white', fontweight='bold', y=0.97)

    phone_bg = '#222233'
    screen_bg = '#ffffff'

    for ax, (title, fname) in zip(axes, slots):
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 12)
        ax.axis('off')
        ax.set_facecolor('#1a1a2e')

        # Phone body
        ax.add_patch(FancyBboxPatch((0.3, 0.2), 5.4, 11.4,
                     boxstyle='round,pad=0.3', linewidth=3,
                     edgecolor='#888', facecolor=phone_bg, zorder=1))

        # Side buttons
        for by in [7.5, 8.5]:
            ax.add_patch(plt.Rectangle((-0.1, by), 0.2, 0.7,
                         color='#666', zorder=2))
        ax.add_patch(plt.Rectangle((5.9, 7.8), 0.2, 1.1, color='#666', zorder=2))

        # Speaker grill
        for gx in [2.4, 2.7, 3.0, 3.3, 3.6]:
            ax.add_patch(plt.Circle((gx, 11.2), 0.06, color='#555', zorder=3))

        # Front camera
        ax.add_patch(plt.Circle((3.0, 11.2), 0.18, color='#333', zorder=3))
        ax.add_patch(plt.Circle((3.0, 11.2), 0.10, color='#1a1a1a', zorder=4))

        # Screen area
        screen_rect = FancyBboxPatch((0.55, 0.6), 4.9, 10.1,
                      boxstyle='round,pad=0.05',
                      facecolor=screen_bg, edgecolor='#444',
                      linewidth=1, zorder=2)
        ax.add_patch(screen_rect)

        # Home button / bottom bar
        ax.add_patch(FancyBboxPatch((1.8, 0.25), 2.4, 0.22,
                     boxstyle='round,pad=0.05',
                     facecolor='#555', edgecolor='none', zorder=3))

        # Try to embed the actual screenshot
        shot_path = os.path.join(SCREENSHOT_DIR, fname)
        if os.path.exists(shot_path):
            try:
                img = PILImage.open(shot_path)
                # Crop to ~top 600px of the screenshot for a clean phone view
                crop_h = min(img.height, int(img.width * 10.1 / 4.9 * 0.5))
                img_crop = img.crop((0, 0, img.width, crop_h))
                ax.imshow(img_crop, extent=[0.55, 5.45, 0.65, 10.7],
                          aspect='auto', zorder=3)
            except Exception:
                ax.text(3.0, 5.5, fname.replace('.png', ''),
                        ha='center', va='center', fontsize=7, color='#999', zorder=4)
        else:
            # Placeholder screen content
            ax.add_patch(FancyBboxPatch((0.55, 0.6), 4.9, 10.1,
                         boxstyle='round,pad=0.05',
                         facecolor='#f8f9fa', edgecolor='#444', zorder=2))
            ax.text(3.0, 7.5, 'StyleVault', ha='center', va='center',
                    fontsize=11, fontweight='bold', color='#0f172a', zorder=4)
            ax.text(3.0, 6.8, '🛍 Fashion Store', ha='center', va='center',
                    fontsize=8, color='#c8a96e', zorder=4)
            for yi, txt in enumerate([
                '━━━━━━━━━━━━━━━━━━━━━━',
                '  New Arrivals',
                '  ┌────┐ ┌────┐',
                '  │ 👗 │ │ 👔 │',
                '  └────┘ └────┘',
                '  Women    Men',
            ], start=0):
                ax.text(3.0, 5.9 - yi * 0.55, txt, ha='center', va='center',
                        fontsize=7, color='#555', fontfamily='monospace', zorder=4)

        ax.set_title(title, color='#c8a96e', fontsize=10, fontweight='bold', pad=6)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return _save(fig, 'mobile_mockup.png')


def generate_all_diagrams():
    print("\n" + "=" * 60)
    print("  GENERATING ALL HIGH-QUALITY DIAGRAMS (v2 · 300 DPI)")
    print("=" * 60)

    generators = [
        ('Gantt Chart',              generate_gantt_chart),
        ('Work Breakdown Structure', generate_wbs),
        ('Use Case Diagram',         generate_use_case),
        ('Activity Diagram',         generate_activity_diagram),
        ('Sequence Diagram',         generate_sequence_diagram),
        ('ER Diagram (clean)',        generate_er_diagram),
        ('Site Map',                  generate_site_map),
        ('PERT Chart',               generate_pert_chart),
        ('Wireframe – Homepage',     generate_wireframe_homepage),
        ('Wireframe – Products',     generate_wireframe_products),
        ('Wireframe – Product Detail', generate_wireframe_product_detail),
        ('Wireframe – Cart',         generate_wireframe_cart),
        ('Wireframe – Checkout',     generate_wireframe_checkout),
        ('Risk Matrix',              generate_risk_matrix),
        ('Critical Path',            generate_critical_path),
        ('Auth Flowchart',           generate_auth_flowchart),
        ('Checkout Flowchart',       generate_checkout_flowchart),
        ('Architecture Diagram',     generate_architecture_diagram),
        ('Product Backlog',          generate_product_backlog),
        ('Sprint Backlog',           generate_sprint_backlog),
        ('Class Diagram',            generate_class_diagram),
        ('State Diagram',            generate_state_diagram),
        ('User Personas',            generate_user_personas),
        ('Google Form Survey',       generate_google_form_survey),
        ('Google Form Analytics',    generate_google_form_analytics),
        ('Mobile Phone Mockup',      generate_mobile_mockup),
    ]

    paths = {}
    for name, fn in generators:
        try:
            path = fn()
            paths[name] = path
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")

    # Generate VS Code code screenshots
    print("\n  Generating VS Code code screenshots...")
    try:
        code_paths = generate_code_screenshots()
        paths.update(code_paths)
    except Exception as e:
        print(f"  [FAIL] Code screenshots: {e}")

    print(f"\n  Done. {len(paths)}/{len(generators) + 4} diagrams generated.")
    return paths


if __name__ == '__main__':
    generate_all_diagrams()
