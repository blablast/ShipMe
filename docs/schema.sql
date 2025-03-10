--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Debian 14.13-1.pgdg110+1)
-- Dumped by pg_dump version 14.13 (Debian 14.13-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: ship_me_user
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO ship_me_user;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: ship_me_user
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO ship_me_user;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: ship_me_user
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO ship_me_user;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: ship_me_user
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ship_me_user;

--
-- Name: dim_customer; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.dim_customer (
    customer_id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    address character varying(100),
    city character varying(50),
    country character varying(50),
    customer_type character varying(20)
);


ALTER TABLE public.dim_customer OWNER TO ship_me_user;

--
-- Name: dim_customer_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.dim_customer_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_customer_customer_id_seq OWNER TO ship_me_user;

--
-- Name: dim_customer_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.dim_customer_customer_id_seq OWNED BY public.dim_customer.customer_id;


--
-- Name: dim_date; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.dim_date (
    date_id integer NOT NULL,
    full_date date,
    day integer,
    month integer,
    quarter integer,
    year integer,
    is_holiday boolean
);


ALTER TABLE public.dim_date OWNER TO ship_me_user;

--
-- Name: dim_date_date_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.dim_date_date_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_date_date_id_seq OWNER TO ship_me_user;

--
-- Name: dim_date_date_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.dim_date_date_id_seq OWNED BY public.dim_date.date_id;


--
-- Name: dim_driver; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.dim_driver (
    driver_id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    license_number character varying(20),
    experience_years double precision,
    hire_date date
);


ALTER TABLE public.dim_driver OWNER TO ship_me_user;

--
-- Name: dim_driver_driver_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.dim_driver_driver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_driver_driver_id_seq OWNER TO ship_me_user;

--
-- Name: dim_driver_driver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.dim_driver_driver_id_seq OWNED BY public.dim_driver.driver_id;


--
-- Name: dim_fuel; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.dim_fuel (
    fuel_id integer NOT NULL,
    fuel_type character varying(20),
    price_per_liter double precision,
    supplier_name character varying(50),
    purchase_date date
);


ALTER TABLE public.dim_fuel OWNER TO ship_me_user;

--
-- Name: dim_fuel_fuel_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.dim_fuel_fuel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_fuel_fuel_id_seq OWNER TO ship_me_user;

--
-- Name: dim_fuel_fuel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.dim_fuel_fuel_id_seq OWNED BY public.dim_fuel.fuel_id;


--
-- Name: dim_product; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.dim_product (
    product_id integer NOT NULL,
    product_name character varying(50),
    category character varying(50),
    weight_kg double precision,
    fragility character varying(20)
);


ALTER TABLE public.dim_product OWNER TO ship_me_user;

--
-- Name: dim_product_product_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.dim_product_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_product_product_id_seq OWNER TO ship_me_user;

--
-- Name: dim_product_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.dim_product_product_id_seq OWNED BY public.dim_product.product_id;


--
-- Name: dim_route; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.dim_route (
    route_id integer NOT NULL,
    start_location character varying(50),
    start_latitude double precision,
    start_longitude double precision,
    end_location character varying(50),
    end_latitude double precision,
    end_longitude double precision,
    distance_km double precision,
    estimated_time_hours double precision,
    road_type character varying(20)
);


ALTER TABLE public.dim_route OWNER TO ship_me_user;

--
-- Name: dim_route_route_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.dim_route_route_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_route_route_id_seq OWNER TO ship_me_user;

--
-- Name: dim_route_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.dim_route_route_id_seq OWNED BY public.dim_route.route_id;


--
-- Name: dim_vehicle; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.dim_vehicle (
    vehicle_id integer NOT NULL,
    registration_number character varying(20),
    vehicle_type character varying(20),
    capacity_kg double precision,
    fuel_type character varying(20),
    purchase_date date
);


ALTER TABLE public.dim_vehicle OWNER TO ship_me_user;

--
-- Name: dim_vehicle_vehicle_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.dim_vehicle_vehicle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_vehicle_vehicle_id_seq OWNER TO ship_me_user;

--
-- Name: dim_vehicle_vehicle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.dim_vehicle_vehicle_id_seq OWNED BY public.dim_vehicle.vehicle_id;


--
-- Name: dim_warehouse; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.dim_warehouse (
    warehouse_id integer NOT NULL,
    warehouse_name character varying(50),
    city character varying(50),
    country character varying(50),
    latitude double precision,
    longitude double precision,
    capacity_m3 double precision
);


ALTER TABLE public.dim_warehouse OWNER TO ship_me_user;

--
-- Name: dim_warehouse_warehouse_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.dim_warehouse_warehouse_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dim_warehouse_warehouse_id_seq OWNER TO ship_me_user;

--
-- Name: dim_warehouse_warehouse_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.dim_warehouse_warehouse_id_seq OWNED BY public.dim_warehouse.warehouse_id;


--
-- Name: fact_shipments; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.fact_shipments (
    shipment_id integer NOT NULL,
    customer_id integer,
    route_id integer,
    vehicle_id integer,
    driver_id integer,
    warehouse_id integer,
    date_id integer,
    weight double precision,
    shipping_cost double precision,
    delivery_time double precision
);


ALTER TABLE public.fact_shipments OWNER TO ship_me_user;

--
-- Name: fact_shipments_shipment_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.fact_shipments_shipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fact_shipments_shipment_id_seq OWNER TO ship_me_user;

--
-- Name: fact_shipments_shipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.fact_shipments_shipment_id_seq OWNED BY public.fact_shipments.shipment_id;


--
-- Name: fact_vehicle_usage; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.fact_vehicle_usage (
    usage_id integer NOT NULL,
    vehicle_id integer,
    driver_id integer,
    route_id integer,
    date_id integer,
    fuel_id integer,
    distance_km double precision,
    fuel_consumption double precision,
    maintenance_cost double precision
);


ALTER TABLE public.fact_vehicle_usage OWNER TO ship_me_user;

--
-- Name: fact_vehicle_usage_usage_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.fact_vehicle_usage_usage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fact_vehicle_usage_usage_id_seq OWNER TO ship_me_user;

--
-- Name: fact_vehicle_usage_usage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.fact_vehicle_usage_usage_id_seq OWNED BY public.fact_vehicle_usage.usage_id;


--
-- Name: fact_warehouse_activity; Type: TABLE; Schema: public; Owner: ship_me_user
--

CREATE TABLE public.fact_warehouse_activity (
    activity_id integer NOT NULL,
    product_id integer,
    warehouse_id integer,
    date_id integer,
    stock_in double precision,
    stock_out double precision,
    storage_time double precision
);


ALTER TABLE public.fact_warehouse_activity OWNER TO ship_me_user;

--
-- Name: fact_warehouse_activity_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: ship_me_user
--

CREATE SEQUENCE public.fact_warehouse_activity_activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fact_warehouse_activity_activity_id_seq OWNER TO ship_me_user;

--
-- Name: fact_warehouse_activity_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ship_me_user
--

ALTER SEQUENCE public.fact_warehouse_activity_activity_id_seq OWNED BY public.fact_warehouse_activity.activity_id;


--
-- Name: dim_customer customer_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_customer ALTER COLUMN customer_id SET DEFAULT nextval('public.dim_customer_customer_id_seq'::regclass);


--
-- Name: dim_date date_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_date ALTER COLUMN date_id SET DEFAULT nextval('public.dim_date_date_id_seq'::regclass);


--
-- Name: dim_driver driver_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_driver ALTER COLUMN driver_id SET DEFAULT nextval('public.dim_driver_driver_id_seq'::regclass);


--
-- Name: dim_fuel fuel_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_fuel ALTER COLUMN fuel_id SET DEFAULT nextval('public.dim_fuel_fuel_id_seq'::regclass);


--
-- Name: dim_product product_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_product ALTER COLUMN product_id SET DEFAULT nextval('public.dim_product_product_id_seq'::regclass);


--
-- Name: dim_route route_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_route ALTER COLUMN route_id SET DEFAULT nextval('public.dim_route_route_id_seq'::regclass);


--
-- Name: dim_vehicle vehicle_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_vehicle ALTER COLUMN vehicle_id SET DEFAULT nextval('public.dim_vehicle_vehicle_id_seq'::regclass);


--
-- Name: dim_warehouse warehouse_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_warehouse ALTER COLUMN warehouse_id SET DEFAULT nextval('public.dim_warehouse_warehouse_id_seq'::regclass);


--
-- Name: fact_shipments shipment_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_shipments ALTER COLUMN shipment_id SET DEFAULT nextval('public.fact_shipments_shipment_id_seq'::regclass);


--
-- Name: fact_vehicle_usage usage_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_vehicle_usage ALTER COLUMN usage_id SET DEFAULT nextval('public.fact_vehicle_usage_usage_id_seq'::regclass);


--
-- Name: fact_warehouse_activity activity_id; Type: DEFAULT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_warehouse_activity ALTER COLUMN activity_id SET DEFAULT nextval('public.fact_warehouse_activity_activity_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: dim_customer dim_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_customer
    ADD CONSTRAINT dim_customer_pkey PRIMARY KEY (customer_id);


--
-- Name: dim_date dim_date_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT dim_date_pkey PRIMARY KEY (date_id);


--
-- Name: dim_driver dim_driver_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_driver
    ADD CONSTRAINT dim_driver_pkey PRIMARY KEY (driver_id);


--
-- Name: dim_fuel dim_fuel_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_fuel
    ADD CONSTRAINT dim_fuel_pkey PRIMARY KEY (fuel_id);


--
-- Name: dim_product dim_product_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_product
    ADD CONSTRAINT dim_product_pkey PRIMARY KEY (product_id);


--
-- Name: dim_route dim_route_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_route
    ADD CONSTRAINT dim_route_pkey PRIMARY KEY (route_id);


--
-- Name: dim_vehicle dim_vehicle_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_vehicle
    ADD CONSTRAINT dim_vehicle_pkey PRIMARY KEY (vehicle_id);


--
-- Name: dim_warehouse dim_warehouse_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.dim_warehouse
    ADD CONSTRAINT dim_warehouse_pkey PRIMARY KEY (warehouse_id);


--
-- Name: fact_shipments fact_shipments_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_shipments
    ADD CONSTRAINT fact_shipments_pkey PRIMARY KEY (shipment_id);


--
-- Name: fact_vehicle_usage fact_vehicle_usage_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_vehicle_usage
    ADD CONSTRAINT fact_vehicle_usage_pkey PRIMARY KEY (usage_id);


--
-- Name: fact_warehouse_activity fact_warehouse_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_warehouse_activity
    ADD CONSTRAINT fact_warehouse_activity_pkey PRIMARY KEY (activity_id);


--
-- Name: idx_dim_date_full_date; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_dim_date_full_date ON public.dim_date USING btree (full_date);


--
-- Name: idx_dim_date_month_year; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_dim_date_month_year ON public.dim_date USING btree (month, year);


--
-- Name: idx_dim_route_road_type; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_dim_route_road_type ON public.dim_route USING btree (road_type);


--
-- Name: idx_dim_vehicle_vehicle_type; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_dim_vehicle_vehicle_type ON public.dim_vehicle USING btree (vehicle_type);


--
-- Name: idx_fact_shipments_customer_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_shipments_customer_id ON public.fact_shipments USING btree (customer_id);


--
-- Name: idx_fact_shipments_date_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_shipments_date_id ON public.fact_shipments USING btree (date_id);


--
-- Name: idx_fact_shipments_driver_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_shipments_driver_id ON public.fact_shipments USING btree (driver_id);


--
-- Name: idx_fact_shipments_route_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_shipments_route_id ON public.fact_shipments USING btree (route_id);


--
-- Name: idx_fact_shipments_shipping_cost; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_shipments_shipping_cost ON public.fact_shipments USING btree (shipping_cost);


--
-- Name: idx_fact_shipments_vehicle_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_shipments_vehicle_id ON public.fact_shipments USING btree (vehicle_id);


--
-- Name: idx_fact_shipments_warehouse_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_shipments_warehouse_id ON public.fact_shipments USING btree (warehouse_id);


--
-- Name: idx_fact_vehicle_usage_date_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_vehicle_usage_date_id ON public.fact_vehicle_usage USING btree (date_id);


--
-- Name: idx_fact_vehicle_usage_fuel_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_vehicle_usage_fuel_id ON public.fact_vehicle_usage USING btree (fuel_id);


--
-- Name: idx_fact_vehicle_usage_route_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_vehicle_usage_route_id ON public.fact_vehicle_usage USING btree (route_id);


--
-- Name: idx_fact_vehicle_usage_vehicle_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_vehicle_usage_vehicle_id ON public.fact_vehicle_usage USING btree (vehicle_id);


--
-- Name: idx_fact_warehouse_activity_product_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_warehouse_activity_product_id ON public.fact_warehouse_activity USING btree (product_id);


--
-- Name: idx_fact_warehouse_activity_warehouse_id; Type: INDEX; Schema: public; Owner: ship_me_user
--

CREATE INDEX idx_fact_warehouse_activity_warehouse_id ON public.fact_warehouse_activity USING btree (warehouse_id);


--
-- Name: fact_shipments fact_shipments_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_shipments
    ADD CONSTRAINT fact_shipments_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.dim_customer(customer_id);


--
-- Name: fact_shipments fact_shipments_date_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_shipments
    ADD CONSTRAINT fact_shipments_date_id_fkey FOREIGN KEY (date_id) REFERENCES public.dim_date(date_id);


--
-- Name: fact_shipments fact_shipments_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_shipments
    ADD CONSTRAINT fact_shipments_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.dim_driver(driver_id);


--
-- Name: fact_shipments fact_shipments_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_shipments
    ADD CONSTRAINT fact_shipments_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.dim_route(route_id);


--
-- Name: fact_shipments fact_shipments_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_shipments
    ADD CONSTRAINT fact_shipments_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.dim_vehicle(vehicle_id);


--
-- Name: fact_shipments fact_shipments_warehouse_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_shipments
    ADD CONSTRAINT fact_shipments_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.dim_warehouse(warehouse_id);


--
-- Name: fact_vehicle_usage fact_vehicle_usage_date_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_vehicle_usage
    ADD CONSTRAINT fact_vehicle_usage_date_id_fkey FOREIGN KEY (date_id) REFERENCES public.dim_date(date_id);


--
-- Name: fact_vehicle_usage fact_vehicle_usage_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_vehicle_usage
    ADD CONSTRAINT fact_vehicle_usage_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.dim_driver(driver_id);


--
-- Name: fact_vehicle_usage fact_vehicle_usage_fuel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_vehicle_usage
    ADD CONSTRAINT fact_vehicle_usage_fuel_id_fkey FOREIGN KEY (fuel_id) REFERENCES public.dim_fuel(fuel_id);


--
-- Name: fact_vehicle_usage fact_vehicle_usage_route_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_vehicle_usage
    ADD CONSTRAINT fact_vehicle_usage_route_id_fkey FOREIGN KEY (route_id) REFERENCES public.dim_route(route_id);


--
-- Name: fact_vehicle_usage fact_vehicle_usage_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_vehicle_usage
    ADD CONSTRAINT fact_vehicle_usage_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.dim_vehicle(vehicle_id);


--
-- Name: fact_warehouse_activity fact_warehouse_activity_date_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_warehouse_activity
    ADD CONSTRAINT fact_warehouse_activity_date_id_fkey FOREIGN KEY (date_id) REFERENCES public.dim_date(date_id);


--
-- Name: fact_warehouse_activity fact_warehouse_activity_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_warehouse_activity
    ADD CONSTRAINT fact_warehouse_activity_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.dim_product(product_id);


--
-- Name: fact_warehouse_activity fact_warehouse_activity_warehouse_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ship_me_user
--

ALTER TABLE ONLY public.fact_warehouse_activity
    ADD CONSTRAINT fact_warehouse_activity_warehouse_id_fkey FOREIGN KEY (warehouse_id) REFERENCES public.dim_warehouse(warehouse_id);


--
-- PostgreSQL database dump complete
--

