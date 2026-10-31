
import logging
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

raw_dir = ROOT / "data" / "raw"
bronze_dir = ROOT / "data" / "bronze"
silver_dir = ROOT / "data" / "silver"
gold_dir = ROOT / "data" / "gold"
log_dir = ROOT / "logs"

# Create output folders
for folder in [bronze_dir, silver_dir, gold_dir, log_dir]:
    folder.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

log_file = log_dir / "pipeline.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. BRONZE LAYER - RAW DATA INGESTION
# --------------------------------------------------

def load_bronze():

    logger.info("Pipeline started")
    logger.info("Bronze layer processing started")

    raw_file = raw_dir / "sales.csv"

    if not raw_file.exists():
        logger.error(f"Input file not found: {raw_file}")
        raise FileNotFoundError(f"Input file not found: {raw_file}")

    sales = pd.read_csv(raw_file)

    if sales.empty:
        logger.error("Input sales file is empty")
        raise ValueError("Input sales file is empty")

    required_columns = [
        "order_id",
        "product",
        "quantity",
        "unit_price"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in sales.columns
    ]

    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Preserve original data
    sales.to_csv(
        bronze_dir / "sales_bronze.csv",
        index=False
    )

    logger.info(f"Bronze records: {len(sales)}")
    logger.info("Bronze layer completed")

    return sales


# --------------------------------------------------
# 4. SILVER LAYER - DATA VALIDATION
# --------------------------------------------------

def clean_data(sales):

    logger.info("Silver layer processing started")

    cleaned = sales.copy()

    # Normalize blank strings
    cleaned["order_id"] = cleaned["order_id"].replace(
        r"^\s*$", pd.NA, regex=True
    )

    cleaned["product"] = cleaned["product"].replace(
        r"^\s*$", pd.NA, regex=True
    )

    # Convert numeric columns
    cleaned["quantity"] = pd.to_numeric(
        cleaned["quantity"], errors="coerce"
    )

    cleaned["unit_price"] = pd.to_numeric(
        cleaned["unit_price"], errors="coerce"
    )

    # Store rejection reasons
    reasons = pd.Series(
        "",
        index=cleaned.index,
        dtype="object"
    )

    def add_reason(mask, message):
        reasons.loc[mask] = reasons.loc[mask].apply(
            lambda current: (
                current + "; " if current else ""
            ) + message
        )

    # Validation rules
    add_reason(
        cleaned["order_id"].isna(),
        "Missing order_id"
    )

    add_reason(
        cleaned["product"].isna(),
        "Missing product"
    )

    add_reason(
        cleaned["quantity"].isna(),
        "Invalid or missing quantity"
    )

    add_reason(
        cleaned["unit_price"].isna(),
        "Invalid or missing unit_price"
    )

    add_reason(
        cleaned["quantity"].notna() &
        (cleaned["quantity"] <= 0),
        "Quantity must be greater than zero"
    )

    add_reason(
        cleaned["unit_price"].notna() &
        (cleaned["unit_price"] < 0),
        "Unit price cannot be negative"
    )

    # Detect duplicate order IDs
    duplicate_mask = (
        cleaned["order_id"].notna() &
        cleaned["order_id"].duplicated(keep="first")
    )

    add_reason(
        duplicate_mask,
        "Duplicate order_id"
    )

    # Save rejected records
    rejected = cleaned.loc[reasons != ""].copy()

    rejected["rejection_reason"] = reasons.loc[
        reasons != ""
    ]

    rejected.to_csv(
        silver_dir / "rejected_records.csv",
        index=False
    )

    # Keep valid records
    valid_mask = reasons == ""

    silver = cleaned.loc[valid_mask].copy()

    # Calculate revenue
    silver["total_amount"] = (
        silver["quantity"] * silver["unit_price"]
    )

    silver.to_csv(
        silver_dir / "sales_silver.csv",
        index=False
    )

    logger.info(f"Silver records: {len(silver)}")
    logger.info(f"Rejected records: {len(rejected)}")
    logger.info("Silver layer completed")

    return silver, rejected


# --------------------------------------------------
# 5. GOLD LAYER - BUSINESS AGGREGATION
# --------------------------------------------------

def create_gold_summary(silver):

    logger.info("Gold layer processing started")

    gold = (
        silver.groupby("product", as_index=False)
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("total_amount", "sum")
        )
    )

    gold.to_csv(
        gold_dir / "sales_summary.csv",
        index=False
    )

    logger.info("Gold summary generated")

    return gold


# --------------------------------------------------
# 6. MAIN PIPELINE EXECUTION
# --------------------------------------------------

def run_pipeline():

    try:
        # Bronze
        sales = load_bronze()

        # Silver
        silver, rejected = clean_data(sales)

        # Gold
        gold = create_gold_summary(silver)

        print("Bronze records:", len(sales))
        print("Silver records:", len(silver))
        print("Rejected records:", len(rejected))

        print("\nGold sales summary:")
        print(gold)

        logger.info("Pipeline completed successfully")

    except Exception:
        logger.exception("Pipeline failed")
        raise


# --------------------------------------------------
# 7. EXECUTE PIPELINE
# --------------------------------------------------

if __name__ == "__main__":
    run_pipeline()
