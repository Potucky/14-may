"""Each check must fail on the seeded defect that was written for it."""

from __future__ import annotations

import pytest

from dq_runner.expectations import Expectation, ExpectationResult, execute

SCHEMA = "shop_defects"


def check(db, **kwargs) -> ExpectationResult:
    return execute(db, Expectation(schema=SCHEMA, **kwargs))


def assert_failed(
    result: ExpectationResult,
    *,
    count: int | None = None,
    sample: str | None = None,
) -> None:
    assert result.success is False, result.message()
    if count is not None:
        assert result.unexpected_count == count, result.message()
    if sample is not None:
        assert any(sample in item for item in result.samples), result.message()


@pytest.mark.defects
def test_null_email_is_detected(db) -> None:
    result = check(
        db,
        name="defect.customers.email_not_null",
        type="not_null",
        table="customers",
        column="email",
    )
    assert_failed(result, count=1)


@pytest.mark.defects
def test_blank_email_is_detected(db) -> None:
    result = check(
        db,
        name="defect.customers.email_not_blank",
        type="not_blank",
        table="customers",
        column="email",
    )
    # One SQL null and one whitespace email. not_null does not see the blank.
    assert_failed(result, count=2)


@pytest.mark.defects
def test_null_customer_name_is_detected(db) -> None:
    result = check(
        db,
        name="defect.customers.full_name_not_null",
        type="not_null",
        table="customers",
        column="full_name",
    )
    assert_failed(result, count=1)


@pytest.mark.defects
def test_duplicate_email_is_detected(db) -> None:
    result = check(
        db,
        name="defect.customers.email_unique",
        type="unique",
        table="customers",
        column="email",
    )
    assert_failed(result, count=1, sample="duplicate@harborpine.example")


@pytest.mark.defects
def test_region_outside_accepted_set_is_detected(db) -> None:
    result = check(
        db,
        name="defect.customers.region_accepted",
        type="in_set",
        table="customers",
        column="region_code",
        values=("NE", "SE", "MW", "SW", "W"),
    )
    assert_failed(result, count=1, sample="XX")


@pytest.mark.defects
def test_status_outside_accepted_set_is_detected(db) -> None:
    result = check(
        db,
        name="defect.customers.status_accepted",
        type="in_set",
        table="customers",
        column="status",
        values=("active", "paused", "closed"),
    )
    assert_failed(result, count=1, sample="archived")


@pytest.mark.defects
def test_updated_before_created_is_detected(db) -> None:
    result = check(
        db,
        name="defect.customers.updated_at_on_or_after_created_at",
        type="column_gte_when_present",
        table="customers",
        column="updated_at",
        other_column="created_at",
    )
    assert_failed(result, count=1)


@pytest.mark.defects
def test_null_sku_is_detected(db) -> None:
    result = check(
        db,
        name="defect.products.sku_not_null",
        type="not_null",
        table="products",
        column="sku",
    )
    assert_failed(result, count=1)


@pytest.mark.defects
def test_duplicate_sku_is_detected(db) -> None:
    result = check(
        db,
        name="defect.products.sku_unique",
        type="unique",
        table="products",
        column="sku",
    )
    assert_failed(result, count=1, sample="HP-TENT-2P")


@pytest.mark.defects
def test_unknown_category_is_detected(db) -> None:
    result = check(
        db,
        name="defect.products.category_accepted",
        type="in_set",
        table="products",
        column="category",
        values=("shelter", "packs", "apparel", "camp"),
    )
    assert_failed(result, count=1, sample="mystery")


@pytest.mark.defects
def test_price_below_range_is_detected(db) -> None:
    result = check(
        db,
        name="defect.products.unit_price_between",
        type="between",
        table="products",
        column="unit_price",
        min="1.00",
        max="500.00",
    )
    assert_failed(result, count=2, sample="-12.50")
    assert any("0.00" in item for item in result.samples), result.message()


@pytest.mark.defects
def test_orphan_customer_is_detected(db) -> None:
    result = check(
        db,
        name="defect.orders.customer_exists",
        type="foreign_key",
        table="orders",
        column="customer_id",
        ref_table="customers",
        ref_column="customer_id",
    )
    assert_failed(result, count=1, sample="99999")


@pytest.mark.defects
def test_unknown_order_status_is_detected(db) -> None:
    result = check(
        db,
        name="defect.orders.status_accepted",
        type="in_set",
        table="orders",
        column="status",
        values=("placed", "paid", "packed", "shipped", "delivered", "cancelled"),
    )
    assert_failed(result, count=1, sample="refunded")


@pytest.mark.defects
def test_future_order_timestamp_is_detected(db) -> None:
    result = check(
        db,
        name="defect.orders.ordered_at_not_future",
        type="not_future",
        table="orders",
        column="ordered_at",
    )
    assert_failed(result, count=1)


@pytest.mark.defects
def test_negative_subtotal_is_detected(db) -> None:
    result = check(
        db,
        name="defect.orders.subtotal_between",
        type="between",
        table="orders",
        column="subtotal",
        min="0.00",
        max="2000.00",
    )
    assert_failed(result, count=1, sample="-5.00")


@pytest.mark.defects
def test_duplicate_order_number_is_detected(db) -> None:
    result = check(
        db,
        name="defect.orders.order_number_unique",
        type="unique",
        table="orders",
        column="order_number",
    )
    assert_failed(result, count=1, sample="HP-9002")


@pytest.mark.defects
def test_shipped_before_ordered_is_detected(db) -> None:
    result = check(
        db,
        name="defect.orders.shipped_at_on_or_after_ordered_at",
        type="column_gte_when_present",
        table="orders",
        column="shipped_at",
        other_column="ordered_at",
    )
    assert_failed(result, count=1)


@pytest.mark.defects
def test_stale_orders_fail_freshness(db) -> None:
    result = check(
        db,
        name="defect.orders_stale.freshness",
        type="max_age",
        table="orders_stale",
        column="ordered_at",
        max_age_hours=48,
    )
    assert result.success is False, result.message()
    age_hours = float(result.observed.split()[0])
    assert age_hours > 48, result.message()


@pytest.mark.defects
def test_orphan_product_is_detected(db) -> None:
    result = check(
        db,
        name="defect.order_items.product_exists",
        type="foreign_key",
        table="order_items",
        column="product_id",
        ref_table="products",
        ref_column="product_id",
    )
    assert_failed(result, count=1, sample="99999")


@pytest.mark.defects
def test_orphan_order_line_is_detected(db) -> None:
    result = check(
        db,
        name="defect.order_items.order_exists",
        type="foreign_key",
        table="order_items",
        column="order_id",
        ref_table="orders",
        ref_column="order_id",
    )
    assert_failed(result, count=1, sample="99999")


@pytest.mark.defects
def test_quantity_above_range_is_detected(db) -> None:
    result = check(
        db,
        name="defect.order_items.quantity_between",
        type="between",
        table="order_items",
        column="quantity",
        min="1",
        max="20",
    )
    assert_failed(result, count=1, sample="25")


@pytest.mark.defects
def test_negative_unit_price_is_detected(db) -> None:
    result = check(
        db,
        name="defect.order_items.unit_price_between",
        type="between",
        table="order_items",
        column="unit_price",
        min="1.00",
        max="500.00",
    )
    assert_failed(result, count=1, sample="-1.00")


@pytest.mark.defects
def test_null_quantity_is_detected(db) -> None:
    result = check(
        db,
        name="defect.order_items.quantity_not_null",
        type="not_null",
        table="order_items",
        column="quantity",
    )
    assert_failed(result, count=1)


@pytest.mark.defects
def test_line_total_does_not_match_quantity_times_price(db) -> None:
    result = check(
        db,
        name="defect.order_items.line_total_matches_quantity_times_price",
        type="product_equals",
        table="order_items",
        column="line_total",
        factors=("quantity", "unit_price"),
    )
    assert_failed(result, count=1, sample="line_total=10.00")


@pytest.mark.defects
def test_order_subtotal_does_not_match_lines(db) -> None:
    result = check(
        db,
        name="defect.orders.subtotal_matches_line_items",
        type="parent_sum_matches",
        parent_table="orders",
        parent_key="order_id",
        parent_amount="subtotal",
        child_table="order_items",
        child_key="order_id",
        child_amount="line_total",
    )
    assert_failed(result, count=2, sample="order_id=1 ")
    assert any(item.startswith("order_id=3 ") for item in result.samples), result.message()


@pytest.mark.defects
def test_customer_volume_below_contract(db) -> None:
    result = check(
        db,
        name="defect.customers.row_count",
        type="row_count",
        table="customers",
        min="24",
        max="24",
    )
    assert result.success is False, result.message()
    assert result.observed == "6 rows", result.message()
