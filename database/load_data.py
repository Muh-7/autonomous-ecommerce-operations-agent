"""
ETL Pipeline: Load & Clean Olist Dataset into PostgreSQL
=========================================================
This script reads raw CSVs, performs basic cleaning,
and loads data into the mart schema tables.

Usage: python database/load_data.py
"""

import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from tqdm import tqdm

# تحميل متغيرات البيئة
load_dotenv()

# إعدادات الاتصال
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# مسار ملفات البيانات
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "Datasets", "Olist")

# تعريف الملفات والجداول المقابلة
# ⚠️ ملاحظة: أسماء الأعمدة هنا يجب أن تكون الأسماء النهائية بعد التصحيح
FILES_MAP = {
    "olist_customers_dataset.csv": ("mart.customers", [
        "customer_id", "customer_unique_id",
        "customer_zip_code_prefix", "customer_city", "customer_state"
    ]),
    "olist_geolocation_dataset.csv": ("mart.geolocation", [
        "geolocation_zip_code_prefix", "geolocation_lat",
        "geolocation_lng", "geolocation_city", "geolocation_state"
    ]),
    "olist_orders_dataset.csv": ("mart.orders", [
        "order_id", "customer_id", "order_status",
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]),
    "olist_products_dataset.csv": ("mart.products", [
        "product_id", "product_category_name",
        "product_name_length", "product_description_length",  # ✅ أسماء مصححة
        "product_photos_qty", "product_weight_g",
        "product_length_cm", "product_height_cm", "product_width_cm"
    ]),
    "olist_sellers_dataset.csv": ("mart.sellers", [
        "seller_id", "seller_zip_code_prefix",
        "seller_city", "seller_state"
    ]),
    "olist_order_items_dataset.csv": ("mart.order_items", [
        "order_id", "order_item_id", "product_id",
        "seller_id", "shipping_limit_date", "price", "freight_value"
    ]),
    "olist_order_payments_dataset.csv": ("mart.order_payments", [
        "order_id", "payment_sequential", "payment_type",
        "payment_installments", "payment_value"
    ]),
    "olist_order_reviews_dataset.csv": ("mart.order_reviews", [
        "review_id", "order_id", "review_score",
        "review_comment_title", "review_comment_message",
        "review_creation_date", "review_answer_timestamp"
    ]),
    "product_category_name_translation.csv": ("mart.category_translation", [
        "product_category_name", "product_category_name_english"
    ]),
}


def clean_dataframe(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """تنظيف أساسي للبيانات حسب نوع الجدول"""
    
    # إنشاء نسخة لتجنب SettingWithCopyWarning
    df = df.copy()

    # تحويل الأعمدة الزمنية
    timestamp_cols = [c for c in df.columns if "timestamp" in c or "date" in c]
    for col in timestamp_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # إزالة التكرار في المراجعات (مشكلة معروفة في Olist)
    if "order_reviews" in table_name:
        before = len(df)
        df = df.drop_duplicates(subset=["review_id"], keep="first")
        after = len(df)
        print(f"   🧹 Removed {before - after} duplicate reviews")

    # التعامل مع القيم الفارغة في النصوص
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].str.strip()
        df[col] = df[col].replace("", None)

    return df


def load_to_postgres():
    """الدالة الرئيسية لتحميل البيانات"""

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("=" * 60)
    print("🚀 Olist ETL Pipeline Started")
    print("=" * 60)

    # ترتيب التحميل حسب الاعتماديات (الجداول المستقلة أولاً)
    load_order = [
        "olist_customers_dataset.csv",
        "olist_geolocation_dataset.csv",
        "olist_products_dataset.csv",
        "olist_sellers_dataset.csv",
        "product_category_name_translation.csv",
        "olist_orders_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_order_reviews_dataset.csv",
    ]

    for filename in tqdm(load_order, desc="Loading tables"):
        table_name, columns = FILES_MAP[filename]
        filepath = os.path.join(DATA_DIR, filename)

        if not os.path.exists(filepath):
            print(f"\n⚠️  File not found: {filename}")
            continue

        print(f"\n📂 Loading {filename} → {table_name}")

        # قراءة CSV
        df = pd.read_csv(filepath, encoding="utf-8")
        print(f"   Raw rows: {len(df)}")

        # ⚠️ إصلاح أسماء الأعمدة أولاً (قبل أي معالجة أخرى)
        # Olist products dataset has known typos in column names
        if "products" in filename:
            df = df.rename(columns={
                "product_name_lenght": "product_name_length",
                "product_description_lenght": "product_description_length",
            })
            print(f"   🔧 Fixed column name typos (lenght → length)")

        # تنظيف البيانات
        df = clean_dataframe(df, table_name)

        # التأكد من تطابق الأعمدة مع قاعدة البيانات
        missing_cols = set(columns) - set(df.columns)
        if missing_cols:
            print(f"   ❌ Missing columns after cleaning: {missing_cols}")
            print(f"   Available columns: {list(df.columns)}")
            continue

        df = df[columns]

        # تفريغ الجدول قبل التحميل (لإعادة التشغيل الآمن)
        cur.execute(f"TRUNCATE TABLE {table_name} CASCADE;")
        conn.commit()

        # إدراج البيانات
        cols_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"

        rows = [
            tuple(None if pd.isna(v) else v for v in row)
            for row in df.itertuples(index=False, name=None)
        ]

        try:
            cur.executemany(insert_query, rows)
            conn.commit()
            print(f"   ✅ Inserted {len(rows)} rows into {table_name}")
        except Exception as e:
            conn.rollback()
            print(f"   ❌ Error loading {table_name}: {e}")

    # التحقق النهائي
    print("\n" + "=" * 60)
    print("📊 Final Row Counts:")
    print("=" * 60)

    for filename in load_order:
        table_name, _ = FILES_MAP[filename]
        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cur.fetchone()[0]
        print(f"   {table_name:35s} → {count:>8,} rows")

    cur.close()
    conn.close()

    print("\n✅ ETL Pipeline Completed Successfully!")


if __name__ == "__main__":
    load_to_postgres()