
import pandas as pd


def test_revenue_calculation():
    quantity = 2
    unit_price = 500

    total = quantity * unit_price

    assert total == 1000


def test_duplicate_removal():
    sales = pd.DataFrame({
        "order_id": [101, 101, 102],
        "product": ["iPhone", "iPhone", "iPad"]
    })

    cleaned = sales.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

    assert len(cleaned) == 2


def test_missing_values():
    sales = pd.DataFrame({
        "unit_price": [100, None, 300]
    })

    cleaned = sales.dropna(
        subset=["unit_price"]
    )

    assert len(cleaned) == 2


def test_invalid_quantity():
    sales = pd.DataFrame({
        "quantity": [2, 0, -1, 5]
    })

    cleaned = sales[sales["quantity"] > 0]

    assert len(cleaned) == 2

from pathlib import Path
import pytest

from src.pipeline import load_bronze


def test_missing_input_file(monkeypatch, tmp_path):

    monkeypatch.setattr(
        "src.pipeline.raw_dir",
        tmp_path
    )

    with pytest.raises(FileNotFoundError):
        load_bronze()


def test_empty_input_file(monkeypatch, tmp_path):

    empty_file = tmp_path / "sales.csv"
    empty_file.write_text(
        "order_id,product,quantity,unit_price\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "src.pipeline.raw_dir",
        tmp_path
    )

    with pytest.raises(ValueError):
        load_bronze()
