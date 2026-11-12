#!/usr/bin/env python3
"""
scripts/index_crops_db.py
Index all 18,247 bounding box crops into crops.db SQLite database
with full metadata for fast querying, filtering, and class transfers.
"""

import os
import sys
import sqlite3
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "crops_review", "crops.db")
REVIEW_DIR = os.path.join(ROOT, "crops_review")
CROPS_DIR = os.path.join(REVIEW_DIR, "crops")

def get_class_folder_name(cid, cname):
    return f"{cid:02d}_{cname}"

def main():
    names_file = os.path.join(REVIEW_DIR, "labels", "vifood", "obj.names")
    if not os.path.exists(names_file):
        print(f"Error: {names_file} not found!")
        sys.exit(1)

    with open(names_file, "r", encoding="utf-8") as f:
        classes = [l.strip() for l in f if l.strip()]

    print(f"Loaded {len(classes)} classes from obj.names")

    # Connect to SQLite using URI with nolock=1 for network filesystem compatibility
    db_uri = f"file:{os.path.abspath(DB_PATH)}?nolock=1"
    con = sqlite3.connect(db_uri, uri=True)
    cur = con.cursor()

    cur.execute("PRAGMA synchronous = OFF;")
    cur.execute("PRAGMA journal_mode = MEMORY;")

    cur.execute("DROP TABLE IF EXISTS crops;")
    cur.execute("DROP TABLE IF EXISTS classes;")
    cur.execute("DROP TABLE IF EXISTS audit_log;")

    cur.execute("""
    CREATE TABLE classes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        folder TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE crops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_id TEXT UNIQUE NOT NULL,
        source TEXT NOT NULL,
        img_stem TEXT NOT NULL,
        img_filename TEXT NOT NULL,
        img_rel_path TEXT NOT NULL,
        label_rel_path TEXT NOT NULL,
        box_idx INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        class_name TEXT NOT NULL,
        orig_class_id INTEGER NOT NULL,
        orig_class_name TEXT NOT NULL,
        cx REAL NOT NULL,
        cy REAL NOT NULL,
        bw REAL NOT NULL,
        bh REAL NOT NULL,
        crop_rel_path TEXT NOT NULL,
        is_deleted INTEGER DEFAULT 0,
        updated_at TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_id TEXT NOT NULL,
        action TEXT NOT NULL,
        old_class_id INTEGER,
        old_class_name TEXT,
        new_class_id INTEGER,
        new_class_name TEXT,
        timestamp TEXT NOT NULL,
        note TEXT
    );
    """)

    classes_rows = []
    for cid, cname in enumerate(classes):
        folder = get_class_folder_name(cid, cname)
        classes_rows.append((cid, cname, folder))
    cur.executemany("INSERT INTO classes (id, name, folder) VALUES (?, ?, ?);", classes_rows)

    sources_config = [
        ("vifood", "grounding_data/vifood54/images/vifood", "crops_review/labels/vifood/train.txt", "crops_review/labels/vifood/obj_train_data"),
        ("vifood2999", "vifood_2999_extracted", "crops_review/labels/vifood2999/train.txt", "crops_review/labels/vifood2999/obj_train_data")
    ]

    records = []
    missing_crops = 0
    t0 = time.time()

    for src_name, img_dir, train_txt, label_dir in sources_config:
        abs_train = os.path.join(ROOT, train_txt)
        with open(abs_train, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]

        print(f"Processing source '{src_name}' ({len(lines)} images)...")
        for line in lines:
            img_fname = os.path.basename(line)
            stem = os.path.splitext(img_fname)[0]
            img_rel = os.path.join(img_dir, img_fname)
            lbl_rel = os.path.join(label_dir, f"{stem}.txt")
            abs_lbl = os.path.join(ROOT, lbl_rel)

            if not os.path.exists(abs_lbl):
                continue

            with open(abs_lbl, "r", encoding="utf-8") as lf:
                label_lines = [l.strip() for l in lf if l.strip()]

            for box_idx, lline in enumerate(label_lines):
                parts = lline.split()
                if len(parts) < 5:
                    continue
                try:
                    cid = int(parts[0])
                    cx, cy, bw, bh = map(float, parts[1:5])
                except ValueError:
                    continue

                if cid < 0 or cid >= len(classes):
                    continue

                cname = classes[cid]
                folder_name = get_class_folder_name(cid, cname)
                crop_filename = f"{src_name}__{stem}__box{box_idx}.jpg"
                crop_rel = os.path.join("crops_review", "crops", folder_name, crop_filename)
                crop_id = f"{src_name}__{stem}__box{box_idx}"

                records.append((
                    crop_id,
                    src_name,
                    stem,
                    img_fname,
                    img_rel,
                    lbl_rel,
                    box_idx,
                    cid,
                    cname,
                    cid,
                    cname,
                    cx, cy, bw, bh,
                    crop_rel,
                    0,
                    None
                ))

    print(f"Collected {len(records)} crop records in {time.time() - t0:.2f}s. Inserting into SQLite...")
    t1 = time.time()
    cur.executemany("""
    INSERT INTO crops (
        crop_id, source, img_stem, img_filename, img_rel_path,
        label_rel_path, box_idx, class_id, class_name,
        orig_class_id, orig_class_name, cx, cy, bw, bh,
        crop_rel_path, is_deleted, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, records)

    print("Building indexes...")
    cur.execute("CREATE INDEX idx_crops_class ON crops (class_id, is_deleted);")
    cur.execute("CREATE INDEX idx_crops_source ON crops (source);")
    cur.execute("CREATE INDEX idx_crops_orig ON crops (orig_class_id);")
    cur.execute("CREATE INDEX idx_crops_stem ON crops (img_stem);")

    con.commit()
    con.close()

    print(f"Successfully indexed {len(records)} crops in {time.time() - t1:.2f}s!")
    print(f"Database ready at: {DB_PATH}")

if __name__ == "__main__":
    main()
