"""
StyleVault E-Commerce Group Project — Main Orchestration Script
================================================================
This script orchestrates the complete assignment generation pipeline:
1. Installs dependencies
2. Starts the Flask web server
3. Generates all UML and planning diagrams
4. Captures website screenshots via Selenium
5. Generates the final .docx report

Usage:
    python main.py              # Full pipeline
    python main.py --diagrams   # Diagrams only
    python main.py --report     # Report only (requires existing diagrams/screenshots)
    python main.py --website    # Run website only (for manual inspection)
"""

import os
import sys
import time
import threading
import argparse

# Project root
ROOT = os.path.dirname(os.path.abspath(__file__))
WEBSITE_DIR = os.path.join(ROOT, 'website')
OUTPUT_DIR = os.path.join(ROOT, 'output')


def ensure_directories():
    """Create all required output directories."""
    dirs = [
        os.path.join(OUTPUT_DIR),
        os.path.join(OUTPUT_DIR, 'diagrams'),
        os.path.join(OUTPUT_DIR, 'screenshots'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("[SETUP] Output directories created.")


def start_flask_server():
    """Start the Flask development server in a background thread."""
    sys.path.insert(0, WEBSITE_DIR)
    os.chdir(WEBSITE_DIR)

    from app import create_app
    from models import db, Product

    app = create_app()
    with app.app_context():
        db.create_all()
        if not Product.query.first():
            from seed_data import seed_database
            seed_database(db)
            print("[SERVER] Database seeded with sample data.")

    def run_server():
        app.run(port=5000, debug=False, use_reloader=False)

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    print("[SERVER] Flask server starting on http://127.0.0.1:5000 ...")
    time.sleep(3)
    print("[SERVER] Flask server is ready.")
    return server_thread


def generate_diagrams():
    """Generate all project diagrams."""
    sys.path.insert(0, os.path.join(ROOT, 'diagrams'))
    from generate_all_v2 import generate_all_diagrams
    return generate_all_diagrams()


def capture_screenshots():
    """Capture website screenshots using Selenium."""
    sys.path.insert(0, os.path.join(ROOT, 'screenshots'))
    from capture import capture_all_screenshots
    return capture_all_screenshots()


def generate_report():
    """Generate the final .docx report."""
    sys.path.insert(0, os.path.join(ROOT, 'report'))
    from generate_report_v2 import generate_report as gen_report
    return gen_report()


def run_full_pipeline():
    """Execute the complete assignment generation pipeline."""
    print("\n" + "=" * 70)
    print("  STYLEVAULT — GROUP PROJECT ASSIGNMENT GENERATOR")
    print("  Full Pipeline: Diagrams → Website → Screenshots → Report")
    print("=" * 70)

    ensure_directories()

    # Step 1: Generate diagrams
    print("\n[STEP 1/4] Generating project diagrams...")
    diagram_paths = generate_diagrams()

    # Step 2: Start Flask server
    print("\n[STEP 2/4] Starting Flask web server...")
    server = start_flask_server()

    # Step 3: Capture screenshots
    print("\n[STEP 3/4] Capturing website screenshots...")
    try:
        screenshot_paths = capture_screenshots()
    except Exception as e:
        print(f"[WARNING] Screenshot capture failed: {e}")
        print("[WARNING] Report will be generated without screenshots.")
        print("[TIP] Ensure Google Chrome is installed and accessible.")
        screenshot_paths = {}

    # Step 4: Generate report
    print("\n[STEP 4/4] Generating .docx report...")
    os.chdir(ROOT)
    report_path = generate_report()

    # Summary
    print("\n" + "=" * 70)
    print("  PIPELINE COMPLETE!")
    print("=" * 70)
    print(f"  Diagrams generated: {len(diagram_paths)}")
    print(f"  Screenshots captured: {len(screenshot_paths)}")
    print(f"  Report saved to: {report_path}")
    print()
    print("  IMPORTANT: After opening the .docx file in Microsoft Word:")
    print("  1. Press Ctrl+A to select all")
    print("  2. Press F9 to update all fields (TOC, TOF, page numbers)")
    print("  3. Review and adjust formatting as needed")
    print("=" * 70)


def run_website_only():
    """Run just the Flask website for manual inspection."""
    print("\n[MODE] Running website only for manual inspection.")
    print("[MODE] Press Ctrl+C to stop.\n")
    ensure_directories()

    sys.path.insert(0, WEBSITE_DIR)
    os.chdir(WEBSITE_DIR)

    from app import create_app
    from models import db, Product

    app = create_app()
    with app.app_context():
        db.create_all()
        if not Product.query.first():
            from seed_data import seed_database
            seed_database(db)

    app.run(port=5000, debug=True)


def main():
    parser = argparse.ArgumentParser(
        description='StyleVault Group Project Assignment Generator'
    )
    parser.add_argument('--diagrams', action='store_true',
                        help='Generate diagrams only')
    parser.add_argument('--report', action='store_true',
                        help='Generate report only (requires existing diagrams/screenshots)')
    parser.add_argument('--website', action='store_true',
                        help='Run Flask website only for manual inspection')
    parser.add_argument('--screenshots', action='store_true',
                        help='Capture screenshots only (requires running Flask server)')

    args = parser.parse_args()

    if args.website:
        run_website_only()
    elif args.diagrams:
        ensure_directories()
        generate_diagrams()
    elif args.report:
        ensure_directories()
        generate_report()
    elif args.screenshots:
        ensure_directories()
        start_flask_server()
        capture_screenshots()
    else:
        run_full_pipeline()


if __name__ == '__main__':
    main()
