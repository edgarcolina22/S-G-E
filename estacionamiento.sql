CREATE TABLE IF NOT EXISTS `Vehiculo` (
	`id` integer primary key NOT NULL UNIQUE,
	`placa` TEXT NOT NULL,
	`marca` TEXT NOT NULL,
	`modelo` TEXT NOT NULL,
	`color` INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS `Espacio` (
	`id` integer primary key NOT NULL UNIQUE,
	`ubicación` TEXT NOT NULL,
	`ocupado` INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS `Ticket` (
	`id` integer primary key NOT NULL UNIQUE,
	`fecha_hora_entrada` REAL NOT NULL,
	`fecha_hora_salida` REAL NOT NULL,
	`total_pagar` REAL NOT NULL,
	`vehículo_id` INTEGER NOT NULL,
	`espacio_id` INTEGER NOT NULL,
FOREIGN KEY(`vehículo_id`) REFERENCES `Vehiculo`(`id`),
FOREIGN KEY(`espacio_id`) REFERENCES `Espacio`(`id`)
);


FOREIGN KEY(`vehículo_id`) REFERENCES `Vehiculo`(`id`)
FOREIGN KEY(`espacio_id`) REFERENCES `Espacio`(`id`)