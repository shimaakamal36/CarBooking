def CreateTables(conn,cur):
    cursor =cur
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    cursor.execute("set global sql_mode = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'")
    tables=['vehicleImages','vehicles','brands','categories','owners','locations','admins','customers','payments','bookings','invoices','reviews']
    tablesDrop=['drop table if EXISTS `'+table+"`" for table in tables]
    
    for tabledrop in tablesDrop:
        cursor.execute(tabledrop)
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

    vehicles='''CREATE TABLE IF NOT EXISTS `vehicles`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `automatic` TINYINT(1) NOT NULL COMMENT '1:Automatic,0:Manual',
    `airconditionar` TINYINT(1) NOT NULL COMMENT '1:Have Airconditioner,0:No airconditioner',
    `code` VARCHAR(50) UNIQUE NOT NULL,
    `model` VARCHAR(50) NOT NULL,
     `year` INT(10) UNSIGNED NOT NULL,
    `status` TINYINT(1) DEFAULT 1 COMMENT '1:Avaliable,0:Not avilable',
    `brand_id` INT(10) UNSIGNED NOT NULL,
    `admin_id` INT(10) UNSIGNED NULL,
    `category_id` INT(10) UNSIGNED NOT NULL,
    `location_id` INT(10) UNSIGNED NOT NULL,
    `owner_id` INT(10) UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    vehicleImages='''CREATE TABLE IF NOT EXISTS `vehicleImages`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `vehicle_id` INT(10) UNSIGNED NOT NULL)'''

    locations='''CREATE TABLE IF NOT EXISTS `locations`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255)  UNIQUE NOT NULL,
    `status` TINYINT(1) DEFAULT 1 COMMENT '1:Active,0:Not active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''
     
    owners='''CREATE TABLE IF NOT EXISTS `owners`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `phone` INT(11) UNIQUE NOT NULL,
    `email` VARCHAR(100) UNIQUE NUll,
    `image`VARCHAR(255) DEFAULT 'default.png',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    brands='''CREATE TABLE IF NOT EXISTS `brands`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) UNIQUE NOT NULL,
    `image`VARCHAR(255) NOT NULL,
    `status` TINYINT(1) DEFAULT 1 COMMENT '1:Active,0:Not active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    categories='''CREATE TABLE IF NOT EXISTS `categories`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) UNIQUE NOT NULL,
    `no_of_passengers` TINYINT(1) NOT NULL,
    `status` TINYINT(1) DEFAULT 1 COMMENT '1:Active,0:Not active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    reviews='''CREATE TABLE IF NOT EXISTS `reviews`(
    `comment` VARCHAR(255) NULL,
    `rate` TINYINT(1) DEFAULT 1 COMMENT '1:Low rate,5:Heigh rate',
    `veh_id` INT(10) UNSIGNED NOT NULL,
    `customer_id` INT(10) UNSIGNED NOT NULL,
    PRIMARY KEY(`veh_id`, `customer_id`),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    customers='''CREATE TABLE IF NOT EXISTS `customers`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `phone` INT(11) UNIQUE NULL,
    `email` VARCHAR(100) UNIQUE NOT NULL,
    `image` VARCHAR(255) DEFAULT 'default.png',
    `password` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''
    
        # `payment_id` INT(10) UNSIGNED NOT NULL,

    admins='''CREATE TABLE IF NOT EXISTS `admins`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `phone` INT(11) UNIQUE  NULL,
    `email` VARCHAR(100) UNIQUE NOT NUll,
    `image`VARCHAR(255) DEFAULT 'default.png',
    `password` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    payments='''CREATE TABLE IF NOT EXISTS `payments`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) UNIQUE NOT NULL,
    `status` TINYINT(1) DEFAULT 1 COMMENT '1:Available ,0:Not available',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    bookings='''CREATE TABLE IF NOT EXISTS `bookings`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `code` VARCHAR(50) UNIQUE NOT NULL,
    `hired_at` TIMESTAMP NOT NULL,
    `returned_at` TIMESTAMP NOT NULL,
    `customerId` INT(10) UNSIGNED NULL,
    `vehicleId` INT(10) UNSIGNED NOT NULL,
    `admId` INT(10) UNSIGNED NULL,
    `invoice_id` INT(10) UNSIGNED NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    invoices='''CREATE TABLE IF NOT EXISTS `invoices`(
    `id` INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `code` VARCHAR(50) UNIQUE NOT NULL,
    `hire_price` DECIMAL(10,1) NOT NULL,
    `add_charges`DECIMAL(5,2)  NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'''

    columns=[vehicleImages,vehicles,brands,categories,owners,locations,admins,customers,payments,bookings,invoices,reviews]
    for column in columns:
        cursor.execute(column)

    vehiclesRelations='''Alter TABLE `vehicles` 
    Add CONSTRAINT `FK_brandvehicle` FOREIGN KEY(`brand_id`) REFERENCES `brands`(`id`) ON UPDATE CASCADE ON DELETE CASCADE,
    ADD CONSTRAINT `FK_adminvehicle` FOREIGN KEY(`admin_id`) REFERENCES `admins`(`id`) ON UPDATE CASCADE ON DELETE CASCADE,
    ADD CONSTRAINT `FK_categoryvehicle` FOREIGN KEY(`category_id`) REFERENCES `categories`(`id`) ON UPDATE CASCADE ON DELETE CASCADE,
    ADD CONSTRAINT `FK_locationvehicle` FOREIGN KEY(`location_id`) REFERENCES `locations`(`id`) ON UPDATE CASCADE ON DELETE CASCADE,
    ADD CONSTRAINT `FK_ownervehicle` FOREIGN KEY(`owner_id`) REFERENCES `owners`(`id`) ON UPDATE CASCADE ON DELETE CASCADE'''

    vehicleImagesRelations='''ALTER TABLE `vehicleImages`
    ADD CONSTRAINT `FK_vehicleImage` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles`(`id`) ON DELETE CASCADE ON UPDATE CASCADE'''

    reviewsRelations='''ALTER TABLE `reviews`
    ADD CONSTRAINT `FK_customerreview` FOREIGN KEY(`customer_id`) REFERENCES `customers`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT `FK_vehiclereview` FOREIGN KEY(`veh_id`) REFERENCES `vehicles`(`id`) ON DELETE CASCADE ON UPDATE CASCADE'''

    # customersRelation='''AlTER TABLE `customers` 
    # ADD CONSTRAINT `FK_admincustomer` FOREIGN KEY(`adminId`) REFERENCES `admins`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    # ADD CONSTRAINT `FK_customerpayment` FOREIGN KEY(`payment_id`) REFERENCES `payments`(`id`) ON DELETE CASCADE ON UPDATE CASCADE'''

    bookingsRelation='''ALTER TABLE `bookings`
    ADD CONSTRAINT `FK_bookingcustomer` FOREIGN KEY(`customerId`) REFERENCES `customers`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT `FK_bookingvehicle` FOREIGN KEY(`vehicleId`) REFERENCES `vehicles`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT `FK_adminbooking` FOREIGN KEY(`admId`) REFERENCES `admins`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT `FK_bookinginvoice` FOREIGN KEY(`invoice_id`) REFERENCES `invoices`(`id`) ON DELETE CASCADE ON UPDATE CASCADE'''

    relations=[vehiclesRelations, vehicleImagesRelations, reviewsRelations,bookingsRelation]
    for relation in relations:
        cursor.execute(relation)

    conn.commit()
    # cursor.close()
    # conn.close() 

