-- Harbor & Pine staging schemas for a local data-quality demo.
-- The retailer is fictional. These tables mimic a warehouse landing area:
-- surrogate keys are primary keys, and columns used like foreign keys are
-- indexed, but business rules (required fields, domains, references, ranges)
-- are not database constraints. The expectation suite is what accepts or
-- rejects a load.

create schema shop;
create schema shop_defects;

comment on schema shop is
  'Clean Harbor & Pine staging load. Local demo data only.';
comment on schema shop_defects is
  'Known-bad rows used to prove each data-quality check can fail.';

do $outer$
declare
  target_schema text;
begin
  foreach target_schema in array array['shop', 'shop_defects']
  loop
    execute format(
      'create table %I.customers (
         customer_id bigint primary key,
         email text,
         full_name text,
         region_code text,
         status text,
         created_at timestamptz,
         updated_at timestamptz
       )',
      target_schema
    );
    execute format(
      'create table %I.products (
         product_id bigint primary key,
         sku text,
         product_name text,
         category text,
         unit_price numeric(10, 2),
         is_active boolean
       )',
      target_schema
    );
    execute format(
      'create table %I.orders (
         order_id bigint primary key,
         order_number text,
         customer_id bigint,
         status text,
         ordered_at timestamptz,
         shipped_at timestamptz,
         subtotal numeric(10, 2)
       )',
      target_schema
    );
    execute format(
      'create index orders_customer_id_idx on %I.orders (customer_id)',
      target_schema
    );
    execute format(
      'create index orders_ordered_at_idx on %I.orders (ordered_at)',
      target_schema
    );
    execute format(
      'create table %I.order_items (
         order_item_id bigint primary key,
         order_id bigint,
         product_id bigint,
         quantity integer,
         unit_price numeric(10, 2),
         line_total numeric(10, 2)
       )',
      target_schema
    );
    execute format(
      'create index order_items_order_id_idx on %I.order_items (order_id)',
      target_schema
    );
    execute format(
      'create index order_items_product_id_idx on %I.order_items (product_id)',
      target_schema
    );
  end loop;
end
$outer$;

-- Separate freshness fixture. A future-dated row in shop_defects.orders would
-- make max(ordered_at) look new, so staleness lives on its own table.
create table shop_defects.orders_stale (
  order_id bigint primary key,
  order_number text,
  customer_id bigint,
  status text,
  ordered_at timestamptz,
  shipped_at timestamptz,
  subtotal numeric(10, 2)
);

create index orders_stale_customer_id_idx
  on shop_defects.orders_stale (customer_id);
