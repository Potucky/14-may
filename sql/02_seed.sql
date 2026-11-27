-- Harbor & Pine demo data. The retailer is fictional.
-- Timestamps use now() so freshness checks stay valid on later runs.
set timezone to 'UTC';

insert into shop.customers (
  customer_id, email, full_name, region_code, status, created_at, updated_at
) values
  (1, 'avery.lang@harborpine.example', 'Avery Lang', 'NE', 'active', now() - interval '39 days', now() - interval '2 days'),
  (2, 'blake.okonkwo@harborpine.example', 'Blake Okonkwo', 'SE', 'active', now() - interval '38 days', now() - interval '2 days'),
  (3, 'cameron.shah@harborpine.example', 'Cameron Shah', 'MW', 'active', now() - interval '37 days', now() - interval '2 days'),
  (4, 'devon.alvarez@harborpine.example', 'Devon Alvarez', 'SW', 'active', now() - interval '36 days', now() - interval '2 days'),
  (5, 'ellis.nguyen@harborpine.example', 'Ellis Nguyen', 'W', 'active', now() - interval '35 days', now() - interval '2 days'),
  (6, 'finley.brooks@harborpine.example', 'Finley Brooks', 'NE', 'active', now() - interval '34 days', now() - interval '2 days'),
  (7, 'gray.ibarra@harborpine.example', 'Gray Ibarra', 'SE', 'active', now() - interval '33 days', now() - interval '2 days'),
  (8, 'harper.singh@harborpine.example', 'Harper Singh', 'MW', 'active', now() - interval '32 days', now() - interval '2 days'),
  (9, 'indigo.patel@harborpine.example', 'Indigo Patel', 'SW', 'active', now() - interval '31 days', now() - interval '2 days'),
  (10, 'jules.moreau@harborpine.example', 'Jules Moreau', 'W', 'active', now() - interval '30 days', now() - interval '2 days'),
  (11, 'kai.nakamura@harborpine.example', 'Kai Nakamura', 'NE', 'active', now() - interval '29 days', now() - interval '2 days'),
  (12, 'logan.petrov@harborpine.example', 'Logan Petrov', 'SE', 'active', now() - interval '28 days', now() - interval '2 days'),
  (13, 'marlowe.chen@harborpine.example', 'Marlowe Chen', 'MW', 'active', now() - interval '27 days', now() - interval '2 days'),
  (14, 'noor.haddad@harborpine.example', 'Noor Haddad', 'SW', 'active', now() - interval '26 days', now() - interval '2 days'),
  (15, 'oakley.berg@harborpine.example', 'Oakley Berg', 'W', 'active', now() - interval '25 days', now() - interval '2 days'),
  (16, 'parker.silva@harborpine.example', 'Parker Silva', 'NE', 'active', now() - interval '24 days', now() - interval '2 days'),
  (17, 'quinn.adeyemi@harborpine.example', 'Quinn Adeyemi', 'SE', 'active', now() - interval '23 days', now() - interval '2 days'),
  (18, 'reese.kowalski@harborpine.example', 'Reese Kowalski', 'MW', 'active', now() - interval '22 days', now() - interval '2 days'),
  (19, 'sasha.rahman@harborpine.example', 'Sasha Rahman', 'SW', 'active', now() - interval '21 days', now() - interval '2 days'),
  (20, 'tatum.bergstrom@harborpine.example', 'Tatum Bergstrom', 'W', 'active', now() - interval '20 days', now() - interval '2 days'),
  (21, 'uma.desai@harborpine.example', 'Uma Desai', 'NE', 'paused', now() - interval '19 days', now() - interval '2 days'),
  (22, 'val.rivera@harborpine.example', 'Val Rivera', 'SE', 'paused', now() - interval '18 days', now() - interval '2 days'),
  (23, 'winter.cole@harborpine.example', 'Winter Cole', 'MW', 'closed', now() - interval '17 days', now() - interval '2 days'),
  (24, 'yael.hoffman@harborpine.example', 'Yael Hoffman', 'SW', 'closed', now() - interval '16 days', now() - interval '2 days')
;

insert into shop.products (
  product_id, sku, product_name, category, unit_price, is_active
) values
  (1, 'HP-TENT-2P', 'Summit Two-Person Tent', 'shelter', 189.00, true),
  (2, 'HP-TARP-01', 'Ridge Line Tarp', 'shelter', 64.00, true),
  (3, 'HP-PACK-40', 'Cedar 40L Pack', 'packs', 129.00, true),
  (4, 'HP-PACK-20', 'Cedar 20L Day Pack', 'packs', 79.00, true),
  (5, 'HP-SOCK-WL', 'Trail Wool Socks', 'apparel', 18.00, true),
  (6, 'HP-JKT-ST', 'Storm Shell Jacket', 'apparel', 149.00, true),
  (7, 'HP-STV-01', 'Aluminum Camp Stove', 'camp', 54.00, true),
  (8, 'HP-MUG-TI', 'Titanium Mug', 'camp', 32.00, true),
  (9, 'HP-LAMP-01', 'LED Headlamp', 'camp', 28.00, true),
  (10, 'HP-POLE-01', 'Trekking Poles', 'camp', 89.00, true),
  (11, 'HP-BTL-1L', 'Insulated Bottle 1L', 'camp', 34.00, true),
  (12, 'HP-CMP-01', 'Map Compass', 'camp', 16.00, false)
;

insert into shop.orders (
  order_id, order_number, customer_id, status, ordered_at, shipped_at, subtotal
) values
  (1, 'HP-1001', 1, 'placed', now() - interval '251 hours', null, 317.00),
  (2, 'HP-1002', 2, 'paid', now() - interval '244 hours', null, 322.00),
  (3, 'HP-1003', 3, 'packed', now() - interval '237 hours', null, 208.00),
  (4, 'HP-1004', 4, 'shipped', now() - interval '230 hours', now() - interval '226 hours', 115.00),
  (5, 'HP-1005', 5, 'delivered', now() - interval '223 hours', now() - interval '219 hours', 316.00),
  (6, 'HP-1006', 6, 'cancelled', now() - interval '216 hours', null, 203.00),
  (7, 'HP-1007', 7, 'placed', now() - interval '209 hours', null, 118.00),
  (8, 'HP-1008', 8, 'paid', now() - interval '202 hours', null, 88.00),
  (9, 'HP-1009', 9, 'packed', now() - interval '195 hours', null, 117.00),
  (10, 'HP-1010', 10, 'shipped', now() - interval '188 hours', now() - interval '184 hours', 157.00),
  (11, 'HP-1011', 11, 'delivered', now() - interval '181 hours', now() - interval '177 hours', 66.00),
  (12, 'HP-1012', 12, 'cancelled', now() - interval '174 hours', null, 205.00),
  (13, 'HP-1013', 13, 'placed', now() - interval '167 hours', null, 317.00),
  (14, 'HP-1014', 14, 'paid', now() - interval '160 hours', null, 322.00),
  (15, 'HP-1015', 15, 'packed', now() - interval '153 hours', null, 208.00),
  (16, 'HP-1016', 16, 'shipped', now() - interval '146 hours', now() - interval '142 hours', 115.00),
  (17, 'HP-1017', 17, 'delivered', now() - interval '139 hours', now() - interval '135 hours', 316.00),
  (18, 'HP-1018', 18, 'cancelled', now() - interval '132 hours', null, 203.00),
  (19, 'HP-1019', 19, 'placed', now() - interval '125 hours', null, 118.00),
  (20, 'HP-1020', 20, 'paid', now() - interval '118 hours', null, 88.00),
  (21, 'HP-1021', 21, 'packed', now() - interval '111 hours', null, 117.00),
  (22, 'HP-1022', 22, 'shipped', now() - interval '104 hours', now() - interval '100 hours', 157.00),
  (23, 'HP-1023', 23, 'delivered', now() - interval '97 hours', now() - interval '93 hours', 66.00),
  (24, 'HP-1024', 24, 'cancelled', now() - interval '90 hours', null, 205.00),
  (25, 'HP-1025', 1, 'placed', now() - interval '83 hours', null, 317.00),
  (26, 'HP-1026', 2, 'paid', now() - interval '76 hours', null, 322.00),
  (27, 'HP-1027', 3, 'packed', now() - interval '69 hours', null, 208.00),
  (28, 'HP-1028', 4, 'shipped', now() - interval '62 hours', now() - interval '58 hours', 115.00),
  (29, 'HP-1029', 5, 'delivered', now() - interval '55 hours', now() - interval '51 hours', 316.00),
  (30, 'HP-1030', 6, 'cancelled', now() - interval '48 hours', null, 203.00),
  (31, 'HP-1031', 7, 'placed', now() - interval '41 hours', null, 118.00),
  (32, 'HP-1032', 8, 'paid', now() - interval '34 hours', null, 88.00),
  (33, 'HP-1033', 9, 'packed', now() - interval '27 hours', null, 117.00),
  (34, 'HP-1034', 10, 'shipped', now() - interval '20 hours', now() - interval '16 hours', 157.00),
  (35, 'HP-1035', 11, 'delivered', now() - interval '13 hours', now() - interval '9 hours', 66.00),
  (36, 'HP-1036', 12, 'cancelled', now() - interval '6 hours', null, 205.00)
;

insert into shop.order_items (
  order_item_id, order_id, product_id, quantity, unit_price, line_total
) values
  (1, 1, 1, 1, 189.00, 189.00),
  (2, 1, 2, 2, 64.00, 128.00),
  (3, 2, 2, 1, 64.00, 64.00),
  (4, 2, 3, 2, 129.00, 258.00),
  (5, 3, 3, 1, 129.00, 129.00),
  (6, 3, 4, 1, 79.00, 79.00),
  (7, 4, 4, 1, 79.00, 79.00),
  (8, 4, 5, 2, 18.00, 36.00),
  (9, 5, 5, 1, 18.00, 18.00),
  (10, 5, 6, 2, 149.00, 298.00),
  (11, 6, 6, 1, 149.00, 149.00),
  (12, 6, 7, 1, 54.00, 54.00),
  (13, 7, 7, 1, 54.00, 54.00),
  (14, 7, 8, 2, 32.00, 64.00),
  (15, 8, 8, 1, 32.00, 32.00),
  (16, 8, 9, 2, 28.00, 56.00),
  (17, 9, 9, 1, 28.00, 28.00),
  (18, 9, 10, 1, 89.00, 89.00),
  (19, 10, 10, 1, 89.00, 89.00),
  (20, 10, 11, 2, 34.00, 68.00),
  (21, 11, 11, 1, 34.00, 34.00),
  (22, 11, 12, 2, 16.00, 32.00),
  (23, 12, 12, 1, 16.00, 16.00),
  (24, 12, 1, 1, 189.00, 189.00),
  (25, 13, 1, 1, 189.00, 189.00),
  (26, 13, 2, 2, 64.00, 128.00),
  (27, 14, 2, 1, 64.00, 64.00),
  (28, 14, 3, 2, 129.00, 258.00),
  (29, 15, 3, 1, 129.00, 129.00),
  (30, 15, 4, 1, 79.00, 79.00),
  (31, 16, 4, 1, 79.00, 79.00),
  (32, 16, 5, 2, 18.00, 36.00),
  (33, 17, 5, 1, 18.00, 18.00),
  (34, 17, 6, 2, 149.00, 298.00),
  (35, 18, 6, 1, 149.00, 149.00),
  (36, 18, 7, 1, 54.00, 54.00),
  (37, 19, 7, 1, 54.00, 54.00),
  (38, 19, 8, 2, 32.00, 64.00),
  (39, 20, 8, 1, 32.00, 32.00),
  (40, 20, 9, 2, 28.00, 56.00),
  (41, 21, 9, 1, 28.00, 28.00),
  (42, 21, 10, 1, 89.00, 89.00),
  (43, 22, 10, 1, 89.00, 89.00),
  (44, 22, 11, 2, 34.00, 68.00),
  (45, 23, 11, 1, 34.00, 34.00),
  (46, 23, 12, 2, 16.00, 32.00),
  (47, 24, 12, 1, 16.00, 16.00),
  (48, 24, 1, 1, 189.00, 189.00),
  (49, 25, 1, 1, 189.00, 189.00),
  (50, 25, 2, 2, 64.00, 128.00),
  (51, 26, 2, 1, 64.00, 64.00),
  (52, 26, 3, 2, 129.00, 258.00),
  (53, 27, 3, 1, 129.00, 129.00),
  (54, 27, 4, 1, 79.00, 79.00),
  (55, 28, 4, 1, 79.00, 79.00),
  (56, 28, 5, 2, 18.00, 36.00),
  (57, 29, 5, 1, 18.00, 18.00),
  (58, 29, 6, 2, 149.00, 298.00),
  (59, 30, 6, 1, 149.00, 149.00),
  (60, 30, 7, 1, 54.00, 54.00),
  (61, 31, 7, 1, 54.00, 54.00),
  (62, 31, 8, 2, 32.00, 64.00),
  (63, 32, 8, 1, 32.00, 32.00),
  (64, 32, 9, 2, 28.00, 56.00),
  (65, 33, 9, 1, 28.00, 28.00),
  (66, 33, 10, 1, 89.00, 89.00),
  (67, 34, 10, 1, 89.00, 89.00),
  (68, 34, 11, 2, 34.00, 68.00),
  (69, 35, 11, 1, 34.00, 34.00),
  (70, 35, 12, 2, 16.00, 32.00),
  (71, 36, 12, 1, 16.00, 16.00),
  (72, 36, 1, 1, 189.00, 189.00)
;

-- Seeded defects. Each bad value is asserted by tests/test_defect_detection.py.
insert into shop_defects.customers (
  customer_id, email, full_name, region_code, status, created_at, updated_at
) values
  (1, null, 'Rowan Blake', 'NE', 'active', now() - interval '12 days', now() - interval '1 day'),
  (2, 'duplicate@harborpine.example', 'Ada Quinn', 'SE', 'active', now() - interval '12 days', now() - interval '1 day'),
  (3, 'duplicate@harborpine.example', 'Ada Quinn Copy', 'SE', 'active', now() - interval '11 days', now() - interval '1 day'),
  (4, 'bad.region@harborpine.example', 'Miles Ortega', 'XX', 'active', now() - interval '8 days', now() - interval '10 days'),
  (5, 'bad.status@harborpine.example', null, 'MW', 'archived', now() - interval '8 days', now() - interval '1 day'),
  (6, '   ', 'Blank Email', 'W', 'active', now() - interval '7 days', now() - interval '1 day');

insert into shop_defects.products (
  product_id, sku, product_name, category, unit_price, is_active
) values
  (1, 'HP-TENT-2P', 'Summit Two-Person Tent', 'shelter', -12.50, true),
  (2, 'HP-TENT-2P', 'Duplicate Tent SKU', 'mystery', 189.00, true),
  (3, null, null, 'packs', 0.00, true);

insert into shop_defects.orders (
  order_id, order_number, customer_id, status, ordered_at, shipped_at, subtotal
) values
  (1, 'HP-9001', 99999, 'refunded', now() + interval '10 days', null, -5.00),
  (2, 'HP-9002', 1, 'delivered', now() - interval '1 day', now() - interval '5 days', 189.00),
  (3, 'HP-9003', 1, 'paid', now() - interval '2 days', null, 10.00),
  (4, 'HP-9004', 1, 'paid', now() - interval '3 days', null, 18.00),
  (5, 'HP-9005', 1, 'placed', now() - interval '4 days', null, 10.00),
  (6, 'HP-9002', 1, 'placed', now() - interval '2 days', null, 0.00);

insert into shop_defects.order_items (
  order_item_id, order_id, product_id, quantity, unit_price, line_total
) values
  (1, 2, 1, 1, 189.00, 189.00),
  (2, 3, 1, 1, 189.00, 189.00),
  (3, 4, 99999, 1, 18.00, 18.00),
  (4, 4, 1, null, 18.00, null),
  (5, 5, 1, 25, -1.00, 10.00),
  (6, 99999, 1, 1, 16.00, 16.00);

insert into shop_defects.orders_stale (
  order_id, order_number, customer_id, status, ordered_at, shipped_at, subtotal
) values
  (1, 'HP-8001', 1, 'delivered', now() - interval '40 days', now() - interval '39 days', 64.00),
  (2, 'HP-8002', 1, 'placed', now() - interval '30 days', null, 18.00);

