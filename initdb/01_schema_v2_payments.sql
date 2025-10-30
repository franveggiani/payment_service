--
-- PostgreSQL database dump
--
-- Dumped from database version 16.4 (Debian 16.4-1.pgdg110+2)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

-- Started on 2025-10-30 16:56:35 -03

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
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA IF NOT EXISTS public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3388 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16389)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16395)
-- Name: estado_pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estado_pago (
    id integer NOT NULL,
    fecha_hora_alta timestamp without time zone,
    fecha_hora_baja timestamp without time zone,
    nombre_estado character varying NOT NULL
);


ALTER TABLE public.estado_pago OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16394)
-- Name: estado_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.estado_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.estado_pago_id_seq OWNER TO postgres;

--
-- TOC entry 3389 (class 0 OID 0)
-- Dependencies: 216
-- Name: estado_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.estado_pago_id_seq OWNED BY public.estado_pago.id;


--
-- TOC entry 219 (class 1259 OID 16405)
-- Name: gateways_metodos_pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gateways_metodos_pago (
    id integer NOT NULL,
    fecha_hora_alta timestamp without time zone,
    fecha_hora_baja timestamp without time zone,
    nombre_gateway character varying NOT NULL
);


ALTER TABLE public.gateways_metodos_pago OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16404)
-- Name: gateways_metodos_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gateways_metodos_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gateways_metodos_pago_id_seq OWNER TO postgres;

--
-- TOC entry 3390 (class 0 OID 0)
-- Dependencies: 218
-- Name: gateways_metodos_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gateways_metodos_pago_id_seq OWNED BY public.gateways_metodos_pago.id;


--
-- TOC entry 221 (class 1259 OID 16415)
-- Name: marcas_metodos_pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marcas_metodos_pago (
    id integer NOT NULL,
    fecha_hora_alta timestamp without time zone,
    fecha_hora_baja timestamp without time zone,
    nombre_marca character varying NOT NULL
);


ALTER TABLE public.marcas_metodos_pago OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16414)
-- Name: marcas_metodos_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marcas_metodos_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.marcas_metodos_pago_id_seq OWNER TO postgres;

--
-- TOC entry 3391 (class 0 OID 0)
-- Dependencies: 220
-- Name: marcas_metodos_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marcas_metodos_pago_id_seq OWNED BY public.marcas_metodos_pago.id;


--
-- TOC entry 225 (class 1259 OID 16435)
-- Name: metodos_pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metodos_pago (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    tipo_pago_id integer NOT NULL,
    marca_pago_id integer,
    gateway_pago_id integer,
    es_default boolean NOT NULL,
    identificador_wallet character varying,
    numero_tarjeta character varying,
    ultimos_cuatro_digitos character varying,
    fecha_hora_baja timestamp without time zone,
    fecha_hora_alta timestamp without time zone
);


ALTER TABLE public.metodos_pago OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16434)
-- Name: metodos_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metodos_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.metodos_pago_id_seq OWNER TO postgres;

--
-- TOC entry 3392 (class 0 OID 0)
-- Dependencies: 224
-- Name: metodos_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metodos_pago_id_seq OWNED BY public.metodos_pago.id;


--
-- TOC entry 227 (class 1259 OID 16460)
-- Name: pagos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pagos (
    id integer NOT NULL,
    fecha_hora_creacion timestamp without time zone,
    nro_cuenta character varying NOT NULL,
    monto_pagado double precision NOT NULL,
    estado_actual integer NOT NULL,
    metodo_pago_id integer NOT NULL,
    orden_id integer NOT NULL
);


ALTER TABLE public.pagos OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16459)
-- Name: pagos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pagos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pagos_id_seq OWNER TO postgres;

--
-- TOC entry 3393 (class 0 OID 0)
-- Dependencies: 226
-- Name: pagos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pagos_id_seq OWNED BY public.pagos.id;


--
-- TOC entry 223 (class 1259 OID 16425)
-- Name: tipos_metodos_pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipos_metodos_pago (
    id integer NOT NULL,
    fecha_hora_alta timestamp without time zone,
    fecha_hora_baja timestamp without time zone,
    nombre_metodo character varying NOT NULL
);


ALTER TABLE public.tipos_metodos_pago OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16424)
-- Name: tipos_metodos_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipos_metodos_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipos_metodos_pago_id_seq OWNER TO postgres;

--
-- TOC entry 3394 (class 0 OID 0)
-- Dependencies: 222
-- Name: tipos_metodos_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipos_metodos_pago_id_seq OWNED BY public.tipos_metodos_pago.id;


--
-- TOC entry 3209 (class 2604 OID 16398)
-- Name: estado_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estado_pago ALTER COLUMN id SET DEFAULT nextval('public.estado_pago_id_seq'::regclass);


--
-- TOC entry 3210 (class 2604 OID 16408)
-- Name: gateways_metodos_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gateways_metodos_pago ALTER COLUMN id SET DEFAULT nextval('public.gateways_metodos_pago_id_seq'::regclass);


--
-- TOC entry 3211 (class 2604 OID 16418)
-- Name: marcas_metodos_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas_metodos_pago ALTER COLUMN id SET DEFAULT nextval('public.marcas_metodos_pago_id_seq'::regclass);


--
-- TOC entry 3213 (class 2604 OID 16438)
-- Name: metodos_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago ALTER COLUMN id SET DEFAULT nextval('public.metodos_pago_id_seq'::regclass);


--
-- TOC entry 3214 (class 2604 OID 16463)
-- Name: pagos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagos ALTER COLUMN id SET DEFAULT nextval('public.pagos_id_seq'::regclass);


--
-- TOC entry 3212 (class 2604 OID 16428)
-- Name: tipos_metodos_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_metodos_pago ALTER COLUMN id SET DEFAULT nextval('public.tipos_metodos_pago_id_seq'::regclass);


--
-- TOC entry 3216 (class 2606 OID 16393)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3218 (class 2606 OID 16402)
-- Name: estado_pago estado_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estado_pago
    ADD CONSTRAINT estado_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3221 (class 2606 OID 16412)
-- Name: gateways_metodos_pago gateways_metodos_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gateways_metodos_pago
    ADD CONSTRAINT gateways_metodos_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3225 (class 2606 OID 16422)
-- Name: marcas_metodos_pago marcas_metodos_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas_metodos_pago
    ADD CONSTRAINT marcas_metodos_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3231 (class 2606 OID 16442)
-- Name: metodos_pago metodos_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago
    ADD CONSTRAINT metodos_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3234 (class 2606 OID 16467)
-- Name: pagos pagos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_pkey PRIMARY KEY (id);


--
-- TOC entry 3228 (class 2606 OID 16432)
-- Name: tipos_metodos_pago tipos_metodos_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_metodos_pago
    ADD CONSTRAINT tipos_metodos_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3219 (class 1259 OID 16403)
-- Name: ix_estado_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_estado_pago_id ON public.estado_pago USING btree (id);


--
-- TOC entry 3222 (class 1259 OID 16413)
-- Name: ix_gateways_metodos_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_gateways_metodos_pago_id ON public.gateways_metodos_pago USING btree (id);


--
-- TOC entry 3223 (class 1259 OID 16423)
-- Name: ix_marcas_metodos_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_marcas_metodos_pago_id ON public.marcas_metodos_pago USING btree (id);


--
-- TOC entry 3229 (class 1259 OID 16458)
-- Name: ix_metodos_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_metodos_pago_id ON public.metodos_pago USING btree (id);


--
-- TOC entry 3232 (class 1259 OID 16478)
-- Name: ix_pagos_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_pagos_id ON public.pagos USING btree (id);


--
-- TOC entry 3226 (class 1259 OID 16433)
-- Name: ix_tipos_metodos_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tipos_metodos_pago_id ON public.tipos_metodos_pago USING btree (id);


--
-- TOC entry 3235 (class 2606 OID 16443)
-- Name: metodos_pago metodos_pago_gateway_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago
    ADD CONSTRAINT metodos_pago_gateway_pago_id_fkey FOREIGN KEY (gateway_pago_id) REFERENCES public.gateways_metodos_pago(id);


--
-- TOC entry 3236 (class 2606 OID 16448)
-- Name: metodos_pago metodos_pago_marca_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago
    ADD CONSTRAINT metodos_pago_marca_pago_id_fkey FOREIGN KEY (marca_pago_id) REFERENCES public.marcas_metodos_pago(id);


--
-- TOC entry 3237 (class 2606 OID 16453)
-- Name: metodos_pago metodos_pago_tipo_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago
    ADD CONSTRAINT metodos_pago_tipo_pago_id_fkey FOREIGN KEY (tipo_pago_id) REFERENCES public.tipos_metodos_pago(id);


--
-- TOC entry 3238 (class 2606 OID 16468)
-- Name: pagos pagos_estado_actual_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_estado_actual_fkey FOREIGN KEY (estado_actual) REFERENCES public.estado_pago(id);


--
-- TOC entry 3239 (class 2606 OID 16473)
-- Name: pagos pagos_metodo_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_metodo_pago_id_fkey FOREIGN KEY (metodo_pago_id) REFERENCES public.metodos_pago(id);


-- Completed on 2025-10-30 16:56:35 -03

--
-- PostgreSQL database dump complete
--

