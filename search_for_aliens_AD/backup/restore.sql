--
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.7 (Debian 15.7-1.pgdg120+1)
-- Dumped by pg_dump version 16.2

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

DROP DATABASE zdjecia;
--
-- Name: zdjecia; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE zdjecia WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE zdjecia OWNER TO postgres;

\connect zdjecia

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: commands; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.commands (
    id integer NOT NULL,
    station_id integer,
    probe_id integer,
    command character varying(255),
    "timestamp" timestamp without time zone
);


ALTER TABLE public.commands OWNER TO postgres;

--
-- Name: commands_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.commands_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.commands_id_seq OWNER TO postgres;

--
-- Name: commands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.commands_id_seq OWNED BY public.commands.id;


--
-- Name: errors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.errors (
    id integer NOT NULL,
    sensor_id integer,
    error_message character varying(255),
    "timestamp" timestamp without time zone
);


ALTER TABLE public.errors OWNER TO postgres;

--
-- Name: errors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.errors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.errors_id_seq OWNER TO postgres;

--
-- Name: errors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.errors_id_seq OWNED BY public.errors.id;


--
-- Name: photos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.photos (
    id integer NOT NULL,
    probe_id integer NOT NULL,
    zdjecie bytea,
    data_wyslania timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.photos OWNER TO postgres;

--
-- Name: photos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.photos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.photos_id_seq OWNER TO postgres;

--
-- Name: photos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.photos_id_seq OWNED BY public.photos.id;


--
-- Name: readings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.readings (
    id integer NOT NULL,
    sensor_id integer,
    "timestamp" timestamp without time zone,
    temperature double precision,
    humidity double precision,
    visibility double precision,
    passengers_count integer,
    pressure double precision
);


ALTER TABLE public.readings OWNER TO postgres;

--
-- Name: readings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.readings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.readings_id_seq OWNER TO postgres;

--
-- Name: readings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.readings_id_seq OWNED BY public.readings.id;


--
-- Name: sensors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sensors (
    id integer NOT NULL,
    probe_id character varying(255),
    location character varying(255),
    sensor_type character varying(255),
    station_id integer
);


ALTER TABLE public.sensors OWNER TO postgres;

--
-- Name: sensors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sensors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sensors_id_seq OWNER TO postgres;

--
-- Name: sensors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sensors_id_seq OWNED BY public.sensors.id;


--
-- Name: stations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stations (
    id integer NOT NULL,
    location character varying(255)
);


ALTER TABLE public.stations OWNER TO postgres;

--
-- Name: stations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stations_id_seq OWNER TO postgres;

--
-- Name: stations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stations_id_seq OWNED BY public.stations.id;


--
-- Name: temperatures; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.temperatures (
    id integer NOT NULL,
    temperature numeric,
    data_wys timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    probe_id character varying
);


ALTER TABLE public.temperatures OWNER TO postgres;

--
-- Name: temperatures_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.temperatures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.temperatures_id_seq OWNER TO postgres;

--
-- Name: temperatures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.temperatures_id_seq OWNED BY public.temperatures.id;


--
-- Name: commands id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commands ALTER COLUMN id SET DEFAULT nextval('public.commands_id_seq'::regclass);


--
-- Name: errors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.errors ALTER COLUMN id SET DEFAULT nextval('public.errors_id_seq'::regclass);


--
-- Name: photos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos ALTER COLUMN id SET DEFAULT nextval('public.photos_id_seq'::regclass);


--
-- Name: readings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readings ALTER COLUMN id SET DEFAULT nextval('public.readings_id_seq'::regclass);


--
-- Name: sensors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sensors ALTER COLUMN id SET DEFAULT nextval('public.sensors_id_seq'::regclass);


--
-- Name: stations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stations ALTER COLUMN id SET DEFAULT nextval('public.stations_id_seq'::regclass);


--
-- Name: temperatures id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.temperatures ALTER COLUMN id SET DEFAULT nextval('public.temperatures_id_seq'::regclass);


--
-- Data for Name: commands; Type: TABLE DATA; Schema: public; Owner: postgres
--

\copy public.commands (id, station_id, probe_id, command, "timestamp") FROM stdin;
\.
\copy public.commands (id, station_id, probe_id, command, "timestamp") FROM '$$PATH$$/3412.dat';

--
-- Data for Name: errors; Type: TABLE DATA; Schema: public; Owner: postgres
--

\copy public.errors (id, sensor_id, error_message, "timestamp") FROM stdin;
\.
\copy public.errors (id, sensor_id, error_message, "timestamp") FROM '$$PATH$$/3414.dat';

--
-- Data for Name: photos; Type: TABLE DATA; Schema: public; Owner: postgres
--

\copy public.photos (id, probe_id, zdjecie, data_wyslania) FROM stdin;
\.
\copy public.photos (id, probe_id, zdjecie, data_wyslania) FROM '$$PATH$$/3402.dat';

--
-- Data for Name: readings; Type: TABLE DATA; Schema: public; Owner: postgres
--

\copy public.readings (id, sensor_id, "timestamp", temperature, humidity, visibility, passengers_count, pressure) FROM stdin;
\.
\copy public.readings (id, sensor_id, "timestamp", temperature, humidity, visibility, passengers_count, pressure) FROM '$$PATH$$/3410.dat';

--
-- Data for Name: sensors; Type: TABLE DATA; Schema: public; Owner: postgres
--

\copy public.sensors (id, probe_id, location, sensor_type, station_id) FROM stdin;
\.
\copy public.sensors (id, probe_id, location, sensor_type, station_id) FROM '$$PATH$$/3408.dat';

--
-- Data for Name: stations; Type: TABLE DATA; Schema: public; Owner: postgres
--

\copy public.stations (id, location) FROM stdin;
\.
\copy public.stations (id, location) FROM '$$PATH$$/3406.dat';

--
-- Data for Name: temperatures; Type: TABLE DATA; Schema: public; Owner: postgres
--

\copy public.temperatures (id, temperature, data_wys, probe_id) FROM stdin;
\.
\copy public.temperatures (id, temperature, data_wys, probe_id) FROM '$$PATH$$/3404.dat';

--
-- Name: commands_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.commands_id_seq', 1, false);


--
-- Name: errors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.errors_id_seq', 1, false);


--
-- Name: photos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.photos_id_seq', 135, true);


--
-- Name: readings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.readings_id_seq', 478, true);


--
-- Name: sensors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sensors_id_seq', 30, true);


--
-- Name: stations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stations_id_seq', 1, true);


--
-- Name: temperatures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.temperatures_id_seq', 411, true);


--
-- Name: commands commands_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_pkey PRIMARY KEY (id);


--
-- Name: errors errors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.errors
    ADD CONSTRAINT errors_pkey PRIMARY KEY (id);


--
-- Name: photos photos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (id);


--
-- Name: readings readings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readings
    ADD CONSTRAINT readings_pkey PRIMARY KEY (id);


--
-- Name: sensors sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT sensors_pkey PRIMARY KEY (id);


--
-- Name: sensors sensors_probe_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT sensors_probe_id_key UNIQUE (probe_id);


--
-- Name: stations stations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stations
    ADD CONSTRAINT stations_pkey PRIMARY KEY (id);


--
-- Name: temperatures temperatures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.temperatures
    ADD CONSTRAINT temperatures_pkey PRIMARY KEY (id);


--
-- Name: commands commands_probe_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_probe_id_fkey FOREIGN KEY (probe_id) REFERENCES public.sensors(id);


--
-- Name: commands commands_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_station_id_fkey FOREIGN KEY (station_id) REFERENCES public.stations(id);


--
-- Name: errors errors_sensor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.errors
    ADD CONSTRAINT errors_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES public.sensors(id);


--
-- Name: readings readings_sensor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.readings
    ADD CONSTRAINT readings_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES public.sensors(id);


--
-- Name: sensors sensors_station_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT sensors_station_id_fkey FOREIGN KEY (station_id) REFERENCES public.stations(id);


--
-- PostgreSQL database dump complete
--

