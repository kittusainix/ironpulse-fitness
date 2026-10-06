-- =====================================================================
-- IRONPULSE FITNESS & GYM MANAGEMENT SYSTEM
-- Oracle PL/SQL: Seed Data (Admin, Plans, Categories, 40 Products, Demo Users)
-- File: 05_seed_products_and_plans.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Insert Admin and Initial Demo Users
-- Note: Password is 'admin123' and 'user123'
-- ---------------------------------------------------------------------
INSERT INTO users (id, full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url, created_at, updated_at)
VALUES (1, 'IronPulse Master Admin', 'admin@ironpulse.gym', 'scrypt:32768:8:1$uH3q3n9W$44cf19d7d3d789073708e967a57a1e0b04a0e980327f12eef43ab1a6da137452d9a3bfa99b4566d5be5a210d7159bb84013444458f0cbcd7208d24b6118d0537', '+91 98765 00001', 'admin', 32, 'Male', 180, 82.5, 25.46, 'Overweight', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80', SYSDATE, SYSDATE);

INSERT INTO users (id, full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url, created_at, updated_at)
VALUES (2, 'Rahul Sharma (Student)', 'rahul@student.edu', 'scrypt:32768:8:1$uH3q3n9W$44cf19d7d3d789073708e967a57a1e0b04a0e980327f12eef43ab1a6da137452d9a3bfa99b4566d5be5a210d7159bb84013444458f0cbcd7208d24b6118d0537', '+91 98111 22334', 'member', 20, 'Male', 175, 68.0, 22.20, 'Normal Weight', 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=400&q=80', SYSDATE, SYSDATE);

INSERT INTO users (id, full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url, created_at, updated_at)
VALUES (3, 'Aman & Priya Verma', 'couple@titan.in', 'scrypt:32768:8:1$uH3q3n9W$44cf19d7d3d789073708e967a57a1e0b04a0e980327f12eef43ab1a6da137452d9a3bfa99b4566d5be5a210d7159bb84013444458f0cbcd7208d24b6118d0537', '+91 98222 33445', 'member', 27, 'Male', 178, 76.0, 23.99, 'Normal Weight', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80', SYSDATE, SYSDATE);

INSERT INTO users (id, full_name, email, password_hash, phone, role, age, gender, height_cm, weight_kg, bmi_value, bmi_category, photo_url, created_at, updated_at)
VALUES (4, 'Vikram Rajput (VIP Athlete)', 'vikram@fitness.com', 'scrypt:32768:8:1$uH3q3n9W$44cf19d7d3d789073708e967a57a1e0b04a0e980327f12eef43ab1a6da137452d9a3bfa99b4566d5be5a210d7159bb84013444458f0cbcd7208d24b6118d0537', '+91 98333 44556', 'member', 29, 'Male', 185, 92.0, 26.88, 'Overweight', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80', SYSDATE, SYSDATE);

-- ---------------------------------------------------------------------
-- 2. Insert Subscription Plans
-- ---------------------------------------------------------------------
INSERT INTO subscription_plans (id, plan_code, name, description, duration_days, price, original_price, is_special_offer, offer_tag, features, is_active)
VALUES (1, 'STUDENT_OFFER', 'Student Discount Pass', 'Exclusive discounted gym access for university & high school students with valid ID.', 30, 799.00, 1499.00, 1, '45% OFF STUDENT SPECIAL', 'Unlimited Gym Floor Access, Locker Room & Showers, Free Fitness Assessment, Valid Student ID Verification', 1);

INSERT INTO subscription_plans (id, plan_code, name, description, duration_days, price, original_price, is_special_offer, offer_tag, features, is_active)
VALUES (2, 'COUPLE_OFFER', 'Couple Power Duo Pass', 'Work out together with your partner! Dual membership at massive savings with joint workout plans.', 30, 1999.00, 3200.00, 1, 'POPULAR COUPLE DEAL', '2 Memberships Included, Free Partner Workout Guide, All Group Aerobic & Zumba Classes, Locker Access', 1);

INSERT INTO subscription_plans (id, plan_code, name, description, duration_days, price, original_price, is_special_offer, offer_tag, features, is_active)
VALUES (3, 'MONTHLY_STARTER', 'Monthly Starter Plan', 'Flexible month-to-month membership with zero long-term commitments.', 30, 1299.00, 1699.00, 0, 'FLEXIBLE', 'Full Equipment & Free Weight Access, Locker & Showers, Cardio Deck, 1 Free Trainer Guidance Session', 1);

INSERT INTO subscription_plans (id, plan_code, name, description, duration_days, price, original_price, is_special_offer, offer_tag, features, is_active)
VALUES (4, 'QUARTERLY_BEAST', 'Quarterly Beast (3 Months)', '3-month power pack designed for visible body transformation and strength building.', 90, 3499.00, 4500.00, 0, 'TRANSFORMATION', 'Full Gym Access 7 Days a Week, 2 Personal Trainer Consultations, Customized Diet Chart, 10% Supplement Discount', 1);

INSERT INTO subscription_plans (id, plan_code, name, description, duration_days, price, original_price, is_special_offer, offer_tag, features, is_active)
VALUES (5, 'ANNUAL_TITAN', 'Annual Titan Pass (12 Months)', 'Our most popular annual membership. Unrestricted 365-day access with premium amenities.', 365, 11999.00, 18000.00, 0, 'BEST VALUE - SAVE 40%', 'Unlimited 365-Day Access, Steam & Sauna Facilities, 4 Guest Passes Every Month, 15% Flat Discount in Shop, Free Gym Duffle Bag', 1);

INSERT INTO subscription_plans (id, plan_code, name, description, duration_days, price, original_price, is_special_offer, offer_tag, features, is_active)
VALUES (6, 'VIP_PRO_ATHLETE', 'VIP Elite Pro Athlete Pass', 'The pinnacle fitness experience with dedicated personal coach and nutrition monitoring.', 365, 24999.00, 35000.00, 1, 'ALL-INCLUSIVE LUXURY', 'Dedicated 1-on-1 Personal Trainer, Weekly Body Composition Scans (InBody), Custom Macro Nutrition Coaching, VIP Locker & Reserved Parking, Monthly Free Supplement Pack', 1);

-- ---------------------------------------------------------------------
-- 3. Insert Demo User Subscriptions
-- ---------------------------------------------------------------------
-- Rahul: Active Student Offer (24 days remaining)
INSERT INTO user_subscriptions (id, user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes, created_at)
VALUES (1, 2, 1, SYSDATE - 6, SYSDATE + 24, 799.00, 'PAID', 'ACTIVE', 'College ID: STU-2024-88912 (Delhi University)', SYSDATE - 6);

-- Couple: Active Couple Offer (18 days remaining)
INSERT INTO user_subscriptions (id, user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes, created_at)
VALUES (2, 3, 2, SYSDATE - 12, SYSDATE + 18, 1999.00, 'PAID', 'ACTIVE', 'Partner: Priya Verma (Ph: +91 98222 99887)', SYSDATE - 12);

-- Vikram: Active VIP Athlete (310 days remaining)
INSERT INTO user_subscriptions (id, user_id, plan_id, start_date, end_date, amount_paid, payment_status, status, notes, created_at)
VALUES (3, 4, 6, SYSDATE - 55, SYSDATE + 310, 24999.00, 'PAID', 'ACTIVE', 'Assigned Master Coach: Arjun Dev', SYSDATE - 55);

-- ---------------------------------------------------------------------
-- 4. Insert Shop Categories
-- ---------------------------------------------------------------------
INSERT INTO categories (id, name, slug, description, icon_class)
VALUES (1, 'Proteins & Gainers', 'proteins-gainers', '100% Whey Isolate, Raw Whey, Mass Gainers & Plant Protein for maximum muscle hypertrophy.', 'fa-dumbbell');

INSERT INTO categories (id, name, slug, description, icon_class)
VALUES (2, 'Pre-Workout & Energy', 'pre-workout-energy', 'High-stimulant pre-workouts, pump enhancers, and clean sustained explosive energy.', 'fa-bolt');

INSERT INTO categories (id, name, slug, description, icon_class)
VALUES (3, 'Creatine & Recovery', 'creatine-recovery', 'Micronized Creatine, BCAAs, EAAs and Glutamine for rapid cellular ATP recovery.', 'fa-capsules');

INSERT INTO categories (id, name, slug, description, icon_class)
VALUES (4, 'Shakers & Bottles', 'shakers-bottles', 'Leak-proof stainless steel, electric vortex, and BPA-free high capacity gym shakers.', 'fa-wine-bottle');

INSERT INTO categories (id, name, slug, description, icon_class)
VALUES (5, 'Gym Gear & Accessories', 'gear-accessories', 'Powerlifting leather lever belts, wrist wraps, knee sleeves, lifting straps and chalk.', 'fa-shield-halved');

-- ---------------------------------------------------------------------
-- 5. Insert Exactly 40 High-Quality Gym Products (8 per category)
-- ---------------------------------------------------------------------

-- CATEGORY 1: PROTEINS & GAINERS (8 Products)
INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (1, 1, 'Gold Standard 100% Whey Protein (5 lbs)', 'Optimum Nutrition', 5999.00, 7299.00, 4.9, 842, 60,
'https://images.unsplash.com/photo-1579722821273-0f6c7d44362f?auto=format&fit=crop&w=700&q=80',
'The world’s best-selling whey protein powder. Delivers 24g of high quality whey protein primarily from Whey Protein Isolate to support muscle growth and repair.',
'74 Servings • 24g Protein • 5.5g BCAAs', 'Double Rich Chocolate', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (2, 1, 'ISO 100 Hydrolyzed 100% Whey Isolate (5 lbs)', 'Dymatize', 7499.00, 8999.00, 4.9, 615, 45,
'https://images.unsplash.com/photo-1593095948071-474c5cc2989d?auto=format&fit=crop&w=700&q=80',
'Fastest absorbing whey isolate designed for elite athletes and hard gainers. Ultra-filtered to remove excess lactose, fat, and sugar.',
'71 Servings • 25g Hydrolyzed Isolate • <1g Sugar', 'Gourmet Vanilla', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (3, 1, 'NitroTech Ripped Lean Protein & Fat Burner (4 lbs)', 'MuscleTech', 5299.00, 6499.00, 4.7, 390, 35,
'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80',
'Advanced 7-in-1 musclebuilding whey isolate peptide formula enhanced with L-Carnitine, CLA, and Green Tea Extract for shredded lean muscle mass.',
'42 Servings • 30g Protein • 500mg L-Carnitine', 'French Vanilla Creme', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (4, 1, 'Impact Whey Protein Isolate (2.5 kg)', 'MyProtein', 6199.00, 7599.00, 4.8, 520, 50,
'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=700&q=80',
'Grade A premium whey isolate tested for extreme purity. Ideal for meeting daily macro targets with zero guilt and incredible mixability.',
'100 Servings • 23g Protein • 0.1g Fat', 'Salted Caramel', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (5, 1, 'Biozyme Performance Whey Protein (2 kg)', 'MuscleBlaze', 4499.00, 5499.00, 4.8, 710, 80,
'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
'Clinically tested Enhanced Absorption Formula (EAF) ensuring 50% higher protein absorption and zero stomach bloating.',
'60 Servings • 25g Protein • Labdoor Certified', 'Rich Chocolate Fudge', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (6, 1, 'Serious Mass High Calorie Weight Gainer (6 lbs)', 'Optimum Nutrition', 3699.00, 4599.00, 4.6, 420, 30,
'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=700&q=80',
'Formulated with 1,250 calories per serving and 50g of protein to facilitate rapid healthy mass gains for ectomorphs and hardgainers.',
'16 Huge Servings • 1250 Calories • 250g Carbs', 'Chocolate Peanut Butter', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (7, 1, 'Classic Plus Organic Vegan Plant Protein (1 kg)', 'Sunwarrior', 4199.00, 4999.00, 4.7, 215, 25,
'https://images.unsplash.com/photo-1532444458054-01a7dd3e9fca?auto=format&fit=crop&w=700&q=80',
'Raw superfood organic plant protein packed with fermented pea, brown rice, quinoa, and chia seeds. 100% dairy and soy-free.',
'40 Servings • 20g Clean Plant Protein • Non-GMO', 'Rich Mocha', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (8, 1, 'Elite 100% Micellar Casein Slow Digestion (4 lbs)', 'Dymatize', 5899.00, 6999.00, 4.8, 180, 20,
'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=700&q=80',
'Sustained-release micellar casein protein providing continuous amino acid flow for 7-8 hours overnight muscle recovery.',
'55 Servings • 25g Micellar Casein • Anti-Catabolic', 'Cookies & Cream', 0);

-- CATEGORY 2: PRE-WORKOUT & ENERGY (8 Products)
INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (9, 2, 'C4 Original Explosive Pre-Workout (60 Servings)', 'Cellucor', 2899.00, 3699.00, 4.8, 920, 75,
'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
'America’s #1 selling pre-workout powder with CarnoSyn Beta-Alanine, Creatine Nitrate, and 150mg caffeine for legendary pumps and endurance.',
'60 Scoops • 150mg Caffeine • 1.6g Beta-Alanine', 'Fruit Punch', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (10, 2, 'Hyde Nightmare High Stimulant Pre-Workout', 'ProSupps', 3199.00, 3999.00, 4.9, 430, 40,
'https://images.unsplash.com/photo-1550345332-09e3ac987658?auto=format&fit=crop&w=700&q=80',
'Hardcore pre-workout formulated for heavy lifters demanding intense vascularity, tunnel-vision focus, and unyielding energy.',
'30 Servings • 300mg Caffeine Matrix • 2.5g Citrulline', 'Blue Razz Freeze', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (11, 2, 'Ghost Legend V2 Premium Pre-Workout', 'Ghost Lifestyle', 3799.00, 4599.00, 4.9, 510, 35,
'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=700&q=80',
'Full disclosure label with 4g L-Citrulline, 3.2g Beta-Alanine, and Senactiv for unmatched stamina, clarity, and skin-splitting pumps.',
'30 Servings • 4000mg Pure Citrulline • Vegan Friendly', 'Sour Watermelon', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (12, 2, 'Psychotic Insane High Energy Pre-Workout', 'Insane Labz', 2699.00, 3499.00, 4.7, 380, 50,
'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=700&q=80',
'Loaded with AMPiberry patent to extend the stimulant energy curve up to 3 hours with zero post-workout crash.',
'35 Servings • Extreme Energy Matrix', 'Gummy Candy', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (13, 2, 'Gorilla Mode Max Potency Pre-Workout', 'Gorilla Mind', 4599.00, 5499.00, 5.0, 780, 28,
'https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?auto=format&fit=crop&w=700&q=80',
'The most heavily dosed nitric oxide and intramuscular hydration formula on earth with 9000mg pure L-Citrulline.',
'40 Scoops • 9g L-Citrulline • 5g Creatine', 'Tiger’s Blood', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (14, 2, 'Total War Military Grade Pre-Workout', 'Redcon1', 2999.00, 3799.00, 4.7, 460, 45,
'https://images.unsplash.com/photo-1549476464-37392f717541?auto=format&fit=crop&w=700&q=80',
'Award-winning formula that combines rapid-acting caffeine with sustained Green Tea caffeine for non-stop battlefield aggression.',
'30 Servings • 6g Citrulline Malate • 320mg Caffeine', 'Rainbow Candy', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (15, 2, 'Outlift Clinically Dosed All-in-One Pre-Workout', 'Nutrex Research', 3499.00, 4299.00, 4.8, 290, 30,
'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=700&q=80',
'Complete 10 clinical-dose powerhouse ingredients including 8g Citrulline Malate, 3g Creapure, and 6g BCAAs.',
'20 Heavy Scoops • 350mg Caffeine • Zero Filler', 'Miami Vice', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (16, 2, 'N.O.-XPLODE Legendary Pre-Workout Igniter', 'BSN', 2799.00, 3599.00, 4.6, 520, 60,
'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?auto=format&fit=crop&w=700&q=80',
'Engineered with advanced thermal energy matrices to elevate physical work capacity and muscle pump endurance.',
'30 Servings • 275mg Caffeine • Beta-Alanine', 'Grape Slam', 0);

-- CATEGORY 3: CREATINE & RECOVERY (8 Products)
INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (17, 3, 'Creapure 100% German Micronized Creatine (250g)', 'IronPulse Pure', 1299.00, 1699.00, 4.9, 1120, 120,
'https://images.unsplash.com/photo-1594381898411-846e7d193883?auto=format&fit=crop&w=700&q=80',
'The purest 99.99% HPLC tested Creapure monohydrate produced in Bavaria, Germany. Boosts muscular ATP and heavy lifting power.',
'83 Servings • 3g Creapure Per Scoop • 0 Sugar', 'Unflavored (Neutral)', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (18, 3, 'Micronized Creatine Powder 300g (100 Servings)', 'Optimum Nutrition', 1499.00, 1899.00, 4.9, 950, 90,
'https://images.unsplash.com/photo-1579722821273-0f6c7d44362f?auto=format&fit=crop&w=700&q=80',
'Micro-milled into ultra-fine particles for effortless mixing in water, shakes, or fruit juices without gritty sedimentation.',
'100 Servings • 3g Pure Monohydrate', 'Unflavored', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (19, 3, 'Xtend BCAA 7g Muscle Recovery Electrolytes (30 Serv)', 'Scivation', 2199.00, 2799.00, 4.8, 640, 70,
'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80',
'The original gold standard intra-workout BCAA with 7g of 2:1:1 branched chain amino acids and replenishing electrolytes.',
'30 Servings • 7g BCAA • 2.5g Glutamine', 'Blue Raspberry Ice', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (20, 3, 'Creatine Monohydrate with Fast Absorb 250g', 'MuscleBlaze', 999.00, 1399.00, 4.7, 830, 110,
'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
'Informed-choice certified pure creatine monohydrate to fuel strength progression and muscle cell volumization.',
'83 Servings • 3g Creatine • Zero Preservatives', 'Unflavored', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (21, 3, 'Fermented L-Glutamine Powder 500g', 'Kaged Muscle', 1899.00, 2399.00, 4.8, 310, 40,
'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=700&q=80',
'100% plant-fermented, non-animal sourced L-Glutamine to prevent post-workout immune suppression and muscle soreness.',
'100 Servings • 5g L-Glutamine • Micro-Pure', 'Unflavored', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (22, 3, 'Pure L-Citrulline Malate 2:1 Powder (300g)', 'Nutricost', 1799.00, 2299.00, 4.7, 240, 50,
'https://images.unsplash.com/photo-1550345332-09e3ac987658?auto=format&fit=crop&w=700&q=80',
'Pharmaceutical grade Citrulline Malate 2:1 for massive nitric oxide vasodilation, blood flow, and lactate clearance.',
'100 Servings • 3000mg Citrulline Malate', 'Tart Lemon', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (23, 3, 'Animal Pak The Complete Training Pack (44 Packs)', 'Universal Nutrition', 3899.00, 4699.00, 4.9, 580, 35,
'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80',
'The legendary all-in-one vitamin, mineral, digestive enzyme, and antioxidant pack built specifically for heavy bodybuilders.',
'44 Packs • 85+ Nutrients • Amino Complex', 'Convenient Daily Packs', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (24, 3, 'EAA Max Full Spectrum Essential Amino Acids', 'Primeval Labs', 2599.00, 3299.00, 4.8, 290, 45,
'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=700&q=80',
'All 9 Essential Amino Acids including BCAAs with Pink Himalayan Salt and coconut water powder for cellular rehydration.',
'30 Servings • 9 Essential Aminos • Zero Calorie', 'Pink Lemonade', 0);

-- CATEGORY 4: SHAKERS, BOTTLES & HYDRATION (8 Products)
INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (25, 4, 'Pro Series 28-Oz Leakproof Shaker with BlenderBall', 'BlenderBottle', 699.00, 999.00, 4.9, 1420, 150,
'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=700&q=80',
'Patented surgical-grade 316 stainless steel wire whisk ball blends thick protein powders into silk in 10 seconds. BPA-free Eastman Tritan.',
'800ml Capacity • Leak-proof SpoutGuard • Dishwasher Safe', 'Matte Black Carbon', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (26, 4, 'Revive Multi-Storage Smart Shaker Bottle', 'SmartShake', 849.00, 1199.00, 4.8, 620, 85,
'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=700&q=80',
'Features 2 detachable compartments at the bottom for storing protein powder scoops, creatine, BCAAs, and daily gym vitamins.',
'750ml • 2 Storage Pods • Soft Loop Handle', 'Stealth Gunmetal', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (27, 4, 'Voltrx Premium Electric Vortex Protein Shaker', 'VOLTRX', 1899.00, 2499.00, 4.9, 540, 60,
'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=700&q=80',
'USB-C rechargeable high-torque electric motor generates a silent 5000 RPM vortex for 100% lump-free protein shakes on the go.',
'700ml • USB-C Quick Charge • Glowing LED Base', 'Midnight Onyx', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (28, 4, 'Stainless Steel Vacuum Insulated Gym Flask 32oz', 'Hydro Titan', 1499.00, 1999.00, 4.8, 380, 50,
'https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=700&q=80',
'Double-wall copper vacuum insulation keeps ice cold water chilled for 24 hours during grueling weight training sessions.',
'950ml • 18/8 Pro Food Grade Steel • Chug Cap', 'Tactical Olive Green', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (29, 4, 'Titan 2.2L Half Gallon Water Jug with Hourly Markers', 'IronPulse Gear', 799.00, 1099.00, 4.7, 720, 100,
'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=700&q=80',
'Huge 2.2-liter BPA-free indestructible jug with motivational hourly hydration tracking markers and heavy-duty paracord strap.',
'2200ml • Time Markings • Leakproof Flip Top', 'Frosted Smoke Black', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (30, 4, 'ShakeSphere Matte Capsule Tumbler (No Corners)', 'ShakeSphere', 1699.00, 2199.00, 4.8, 310, 40,
'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=700&q=80',
'No whisk ball needed! Patented centrifugal rounded capsule design ensures no powder ever gets stuck in the corners.',
'700ml • Capsule Shape • Slide Cap', 'Matte Jet Black', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (31, 4, 'Strada Heavy Insulated Stainless Steel Shaker 24oz', 'BlenderBottle', 1999.00, 2699.00, 4.9, 410, 45,
'https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=700&q=80',
'Push-button flip cap with sliding safety lock and vacuum insulated steel keeping pre-workouts freezing cold.',
'710ml • Push-Button Lock • Whisk Included', 'Brushed Titanium', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (32, 4, 'Cyclone Cup Metallic High Shear Shaker 20oz', 'Cyclone', 949.00, 1299.00, 4.6, 280, 65,
'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=700&q=80',
'Stationary vortex turbine mixer blade that blasts through stubborn casein and whey clumps with absolute ease.',
'600ml • Cyclone Mixing Blade • Pill Storage', 'Crimson Red / Black', 0);

-- CATEGORY 5: GYM GEAR, ACCESSORIES & EQUIPMENT (8 Products)
INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (33, 5, 'Heavy Duty 10mm Leather Powerlifting Lever Belt', 'IronPulse Pro', 3299.00, 4499.00, 5.0, 890, 55,
'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
'Competition legal genuine top-grain cowhide leather with alloy quick-release lever buckle for rock-solid intra-abdominal spine bracing during 200kg+ squats and deadlifts.',
'10mm Thickness • Alloy Lever • S/M/L/XL Sizing', 'Matte Black / Red Suede Inner', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (34, 5, 'Heavy Duty 18" Elastic Weightlifting Wrist Wraps', 'Titan Force', 599.00, 899.00, 4.8, 670, 130,
'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=700&q=80',
'Reinforced thumb loop and military grade Velcro provide maximum wrist joint stability for heavy bench press and overhead presses.',
'Pair • 18-inch Length • Heavy Elastic Stitching', 'Black with Cyber Red Lines', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (35, 5, '7mm Neoprene Compression Knee Sleeves (Pair)', 'IronPulse Pro', 1799.00, 2499.00, 4.9, 530, 70,
'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=700&q=80',
'Anatomically contoured 7mm SCR neoprene delivering optimal joint warmth, patellar tracking, and rebound spring during deep squats.',
'Pair • 7mm Dense Neoprene • Anti-Slip Interior', 'Stealth Black', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (36, 5, 'Heavy Duty Figure 8 Deadlift Lifting Straps', 'BeastGear', 499.00, 799.00, 4.9, 740, 140,
'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?auto=format&fit=crop&w=700&q=80',
'Locked-in figure-8 webbing rated to withstand over 1,000 lbs. Eliminates grip fatigue so you can lift maximum poundage on barbell shrugs and deadlifts.',
'Pair • Cotton Webbing Rated to 500kg', 'Tactical Black', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (37, 5, 'Premium Fast-Drying Liquid Gym Chalk 250ml', 'GripMaster', 449.00, 699.00, 4.8, 610, 110,
'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80',
'Dries in 5 seconds into a thin sweat-resistant magnesium carbonate coating. Zero chalk dust cloud, gym compliant.',
'250ml Squeeze Bottle • 99% Pure Magnesium Carbonate', 'Citrus Scent', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (38, 5, 'Heavy Duty Pull-Up Assistance Resistance Bands Set', 'IronPulse Pro', 1299.00, 1899.00, 4.8, 480, 80,
'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=700&q=80',
'Set of 5 100% natural layered Malaysian latex bands ranging from 10 lbs to 125 lbs resistance for mobility, stretching, and pull-up assist.',
'5 Multi-Color Bands • Door Anchor • Carry Pouch', '5 Levels (10-125 lbs)', 0);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (39, 5, 'Tactical Gym Duffle Bag with Vented Shoe Compartment', 'IronPulse Gear', 2199.00, 2999.00, 4.9, 390, 65,
'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=700&q=80',
'Water-resistant 900D Oxford fabric with dedicated wet/sweaty clothes pocket, separate shoe chamber, and shaker bottle holsters.',
'45L Capacity • Water Repellent 900D Fabric', 'Matte Shadow Camo', 1);

INSERT INTO products (id, category_id, name, brand, price, original_price, rating, reviews_count, stock_quantity, image_url, description, serving_specs, flavor_variant, is_featured)
VALUES (40, 5, 'Pro Speed Jump Rope with 360° Double Ball Bearings', 'SpeedMaster', 549.00, 849.00, 4.7, 510, 95,
'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=700&q=80',
'Self-locking length adjuster with dual smooth stainless steel ball bearings for lightning fast double-unders and high-intensity cardio HIIT.',
'3-Meter Coated Steel Cable • Aluminum Handles', 'Cyber Crimson Red', 0);

COMMIT;
