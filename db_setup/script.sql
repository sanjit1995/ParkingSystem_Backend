create table login(
    id varchar not null unique,
    password varchar(255),
    is_active boolean
);

create table users(
    user_id varchar(255) not null unique,
    email varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    address varchar(255),
    dob date,
    contact_number decimal,
    gender char
);

create table parking_spots(
    spot_id varchar(255) not null unique,
    parking_type_id varchar(255),
    city varchar(255),
    address varchar(255),
    location varchar(255),
    is_available boolean,
    is_functional boolean
);

insert into parking_spots values ('nd101','4w_normal','New Delhi','Dhaula Kuan','45.2, 23.9',True,True);
insert into parking_spots values ('be201','4w_executive','Bengaluru','MG Road','62.5, 45.4',True,True);

create table parking_history(
    parking_id varchar(255) not null unique,
    spot_id varchar(255) not null,
    user_id varchar(255) not null,
    booking_start timestamp,
    booking_end timestamp,
    transaction_id varchar,
    amount_paid float,
    mode_of_payment integer
);

create table parking_types(
    type_id varchar(255) not null unique,
    description varchar(255),
    parking_charge float
);

insert into parking_types values ('4w_normal','Four Wheeler : Normal',15);
insert into parking_types values ('2w_normal','Four Wheeler : Normal',10);
insert into parking_types values ('4w_executive','Four Wheeler : Normal',30);
insert into parking_types values ('2w_executive','Four Wheeler : Normal',20);

create table payment_modes(
    mode_id integer not null unique,
    description varchar(255)
);

insert into payment_modes values (1,'CARD');
insert into parking_types values (2,'PAYPAL');
insert into parking_types values (3,'CREDIT');
insert into parking_types values (4,'CASH');