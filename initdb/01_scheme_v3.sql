--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg110+2)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

-- Started on 2025-11-19 21:54:14 -03

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
-- TOC entry 3438 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16385)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16670)
-- Name: bancos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bancos (
    id integer NOT NULL,
    nombre_banco character varying NOT NULL,
    fecha_hora_baja timestamp without time zone,
    fecha_hora_alta timestamp without time zone
);


ALTER TABLE public.bancos OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16669)
-- Name: bancos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bancos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bancos_id_seq OWNER TO postgres;

--
-- TOC entry 3439 (class 0 OID 0)
-- Dependencies: 226
-- Name: bancos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bancos_id_seq OWNED BY public.bancos.id;


--
-- TOC entry 216 (class 1259 OID 16388)
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
-- TOC entry 217 (class 1259 OID 16393)
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
-- TOC entry 3440 (class 0 OID 0)
-- Dependencies: 217
-- Name: estado_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.estado_pago_id_seq OWNED BY public.estado_pago.id;


--
-- TOC entry 218 (class 1259 OID 16400)
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
-- TOC entry 219 (class 1259 OID 16405)
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
-- TOC entry 3441 (class 0 OID 0)
-- Dependencies: 219
-- Name: marcas_metodos_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marcas_metodos_pago_id_seq OWNED BY public.marcas_metodos_pago.id;


--
-- TOC entry 220 (class 1259 OID 16406)
-- Name: metodos_pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metodos_pago (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    tipo_pago_id integer NOT NULL,
    es_default boolean NOT NULL,
    fecha_hora_baja timestamp without time zone,
    fecha_hora_alta timestamp without time zone,
    moneda_id integer NOT NULL,
    metodo_pago_detalle_id integer NOT NULL
);


ALTER TABLE public.metodos_pago OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16700)
-- Name: metodos_pago_billetera; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metodos_pago_billetera (
    id integer NOT NULL,
    proveedor_id integer NOT NULL,
    wallet_id character varying,
    fecha_hora_baja timestamp without time zone,
    fecha_hora_alta timestamp without time zone,
    moneda_id integer NOT NULL
);


ALTER TABLE public.metodos_pago_billetera OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16699)
-- Name: metodos_pago_billetera_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metodos_pago_billetera_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.metodos_pago_billetera_id_seq OWNER TO postgres;

--
-- TOC entry 3442 (class 0 OID 0)
-- Dependencies: 232
-- Name: metodos_pago_billetera_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metodos_pago_billetera_id_seq OWNED BY public.metodos_pago_billetera.id;


--
-- TOC entry 221 (class 1259 OID 16411)
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
-- TOC entry 3443 (class 0 OID 0)
-- Dependencies: 221
-- Name: metodos_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metodos_pago_id_seq OWNED BY public.metodos_pago.id;


--
-- TOC entry 235 (class 1259 OID 16725)
-- Name: metodos_pago_tarjeta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metodos_pago_tarjeta (
    id integer NOT NULL,
    marca_pago_id integer NOT NULL,
    numero_tarjeta character varying NOT NULL,
    ultimos_cuatro_digitos character varying,
    fecha_vencimiento character varying NOT NULL,
    fecha_hora_baja timestamp without time zone,
    fecha_hora_alta timestamp without time zone,
    nombre_titular character varying NOT NULL,
    banco_id integer NOT NULL
);


ALTER TABLE public.metodos_pago_tarjeta OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 16724)
-- Name: metodos_pago_tarjeta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metodos_pago_tarjeta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.metodos_pago_tarjeta_id_seq OWNER TO postgres;

--
-- TOC entry 3444 (class 0 OID 0)
-- Dependencies: 234
-- Name: metodos_pago_tarjeta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metodos_pago_tarjeta_id_seq OWNED BY public.metodos_pago_tarjeta.id;


--
-- TOC entry 229 (class 1259 OID 16680)
-- Name: monedas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.monedas (
    id integer NOT NULL,
    moneda_nombre character varying NOT NULL,
    fecha_hora_baja timestamp without time zone,
    fecha_hora_alta timestamp without time zone
);


ALTER TABLE public.monedas OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16679)
-- Name: monedas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.monedas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.monedas_id_seq OWNER TO postgres;

--
-- TOC entry 3445 (class 0 OID 0)
-- Dependencies: 228
-- Name: monedas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.monedas_id_seq OWNED BY public.monedas.id;


--
-- TOC entry 237 (class 1259 OID 16745)
-- Name: orden_pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orden_pago (
    id integer NOT NULL,
    orden_externa_id integer NOT NULL,
    id_pago integer NOT NULL,
    id_estado_pago integer NOT NULL,
    fecha_hora_alta timestamp without time zone,
    fecha_hora_baja timestamp without time zone,
    nombre_estado character varying NOT NULL
);


ALTER TABLE public.orden_pago OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16744)
-- Name: orden_pago_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orden_pago_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orden_pago_id_seq OWNER TO postgres;

--
-- TOC entry 3446 (class 0 OID 0)
-- Dependencies: 236
-- Name: orden_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orden_pago_id_seq OWNED BY public.orden_pago.id;


--
-- TOC entry 222 (class 1259 OID 16412)
-- Name: pagos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pagos (
    id integer NOT NULL,
    fecha_hora_creacion timestamp without time zone,
    estado_actual integer NOT NULL,
    metodo_pago_id integer NOT NULL,
    orden_id integer NOT NULL
);


ALTER TABLE public.pagos OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16417)
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
-- TOC entry 3447 (class 0 OID 0)
-- Dependencies: 223
-- Name: pagos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pagos_id_seq OWNED BY public.pagos.id;


--
-- TOC entry 231 (class 1259 OID 16690)
-- Name: proveedores_billetera; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proveedores_billetera (
    id integer NOT NULL,
    fecha_hora_alta timestamp without time zone,
    fecha_hora_baja timestamp without time zone,
    nombre_gateway character varying NOT NULL
);


ALTER TABLE public.proveedores_billetera OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16689)
-- Name: proveedores_billetera_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proveedores_billetera_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proveedores_billetera_id_seq OWNER TO postgres;

--
-- TOC entry 3448 (class 0 OID 0)
-- Dependencies: 230
-- Name: proveedores_billetera_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proveedores_billetera_id_seq OWNED BY public.proveedores_billetera.id;


--
-- TOC entry 224 (class 1259 OID 16418)
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
-- TOC entry 225 (class 1259 OID 16423)
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
-- TOC entry 3449 (class 0 OID 0)
-- Dependencies: 225
-- Name: tipos_metodos_pago_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipos_metodos_pago_id_seq OWNED BY public.tipos_metodos_pago.id;


--
-- TOC entry 3239 (class 2604 OID 16673)
-- Name: bancos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bancos ALTER COLUMN id SET DEFAULT nextval('public.bancos_id_seq'::regclass);


--
-- TOC entry 3234 (class 2604 OID 16424)
-- Name: estado_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estado_pago ALTER COLUMN id SET DEFAULT nextval('public.estado_pago_id_seq'::regclass);


--
-- TOC entry 3235 (class 2604 OID 16426)
-- Name: marcas_metodos_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas_metodos_pago ALTER COLUMN id SET DEFAULT nextval('public.marcas_metodos_pago_id_seq'::regclass);


--
-- TOC entry 3236 (class 2604 OID 16427)
-- Name: metodos_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago ALTER COLUMN id SET DEFAULT nextval('public.metodos_pago_id_seq'::regclass);


--
-- TOC entry 3242 (class 2604 OID 16703)
-- Name: metodos_pago_billetera id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago_billetera ALTER COLUMN id SET DEFAULT nextval('public.metodos_pago_billetera_id_seq'::regclass);


--
-- TOC entry 3243 (class 2604 OID 16728)
-- Name: metodos_pago_tarjeta id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago_tarjeta ALTER COLUMN id SET DEFAULT nextval('public.metodos_pago_tarjeta_id_seq'::regclass);


--
-- TOC entry 3240 (class 2604 OID 16683)
-- Name: monedas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monedas ALTER COLUMN id SET DEFAULT nextval('public.monedas_id_seq'::regclass);


--
-- TOC entry 3244 (class 2604 OID 16748)
-- Name: orden_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_pago ALTER COLUMN id SET DEFAULT nextval('public.orden_pago_id_seq'::regclass);


--
-- TOC entry 3237 (class 2604 OID 16428)
-- Name: pagos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagos ALTER COLUMN id SET DEFAULT nextval('public.pagos_id_seq'::regclass);


--
-- TOC entry 3241 (class 2604 OID 16693)
-- Name: proveedores_billetera id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedores_billetera ALTER COLUMN id SET DEFAULT nextval('public.proveedores_billetera_id_seq'::regclass);


--
-- TOC entry 3238 (class 2604 OID 16429)
-- Name: tipos_metodos_pago id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_metodos_pago ALTER COLUMN id SET DEFAULT nextval('public.tipos_metodos_pago_id_seq'::regclass);


--
-- TOC entry 3246 (class 2606 OID 16431)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3263 (class 2606 OID 16677)
-- Name: bancos bancos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bancos
    ADD CONSTRAINT bancos_pkey PRIMARY KEY (id);


--
-- TOC entry 3248 (class 2606 OID 16433)
-- Name: estado_pago estado_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estado_pago
    ADD CONSTRAINT estado_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3252 (class 2606 OID 16437)
-- Name: marcas_metodos_pago marcas_metodos_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marcas_metodos_pago
    ADD CONSTRAINT marcas_metodos_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3273 (class 2606 OID 16707)
-- Name: metodos_pago_billetera metodos_pago_billetera_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago_billetera
    ADD CONSTRAINT metodos_pago_billetera_pkey PRIMARY KEY (id);


--
-- TOC entry 3255 (class 2606 OID 16439)
-- Name: metodos_pago metodos_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago
    ADD CONSTRAINT metodos_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3276 (class 2606 OID 16732)
-- Name: metodos_pago_tarjeta metodos_pago_tarjeta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago_tarjeta
    ADD CONSTRAINT metodos_pago_tarjeta_pkey PRIMARY KEY (id);


--
-- TOC entry 3267 (class 2606 OID 16687)
-- Name: monedas monedas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monedas
    ADD CONSTRAINT monedas_pkey PRIMARY KEY (id);


--
-- TOC entry 3279 (class 2606 OID 16752)
-- Name: orden_pago orden_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_pago
    ADD CONSTRAINT orden_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3258 (class 2606 OID 16441)
-- Name: pagos pagos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_pkey PRIMARY KEY (id);


--
-- TOC entry 3270 (class 2606 OID 16697)
-- Name: proveedores_billetera proveedores_billetera_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedores_billetera
    ADD CONSTRAINT proveedores_billetera_pkey PRIMARY KEY (id);


--
-- TOC entry 3261 (class 2606 OID 16443)
-- Name: tipos_metodos_pago tipos_metodos_pago_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_metodos_pago
    ADD CONSTRAINT tipos_metodos_pago_pkey PRIMARY KEY (id);


--
-- TOC entry 3264 (class 1259 OID 16678)
-- Name: ix_bancos_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_bancos_id ON public.bancos USING btree (id);


--
-- TOC entry 3249 (class 1259 OID 16444)
-- Name: ix_estado_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_estado_pago_id ON public.estado_pago USING btree (id);


--
-- TOC entry 3250 (class 1259 OID 16446)
-- Name: ix_marcas_metodos_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_marcas_metodos_pago_id ON public.marcas_metodos_pago USING btree (id);


--
-- TOC entry 3271 (class 1259 OID 16723)
-- Name: ix_metodos_pago_billetera_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_metodos_pago_billetera_id ON public.metodos_pago_billetera USING btree (id);


--
-- TOC entry 3253 (class 1259 OID 16447)
-- Name: ix_metodos_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_metodos_pago_id ON public.metodos_pago USING btree (id);


--
-- TOC entry 3274 (class 1259 OID 16743)
-- Name: ix_metodos_pago_tarjeta_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_metodos_pago_tarjeta_id ON public.metodos_pago_tarjeta USING btree (id);


--
-- TOC entry 3265 (class 1259 OID 16688)
-- Name: ix_monedas_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_monedas_id ON public.monedas USING btree (id);


--
-- TOC entry 3277 (class 1259 OID 16763)
-- Name: ix_orden_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orden_pago_id ON public.orden_pago USING btree (id);


--
-- TOC entry 3256 (class 1259 OID 16448)
-- Name: ix_pagos_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_pagos_id ON public.pagos USING btree (id);


--
-- TOC entry 3268 (class 1259 OID 16698)
-- Name: ix_proveedores_billetera_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_proveedores_billetera_id ON public.proveedores_billetera USING btree (id);


--
-- TOC entry 3259 (class 1259 OID 16449)
-- Name: ix_tipos_metodos_pago_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tipos_metodos_pago_id ON public.tipos_metodos_pago USING btree (id);


--
-- TOC entry 3284 (class 2606 OID 16713)
-- Name: metodos_pago_billetera metodos_pago_billetera_moneda_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago_billetera
    ADD CONSTRAINT metodos_pago_billetera_moneda_id_fkey FOREIGN KEY (moneda_id) REFERENCES public.monedas(id);


--
-- TOC entry 3285 (class 2606 OID 16718)
-- Name: metodos_pago_billetera metodos_pago_billetera_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago_billetera
    ADD CONSTRAINT metodos_pago_billetera_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES public.proveedores_billetera(id);


--
-- TOC entry 3280 (class 2606 OID 16764)
-- Name: metodos_pago metodos_pago_moneda_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago
    ADD CONSTRAINT metodos_pago_moneda_id_fkey FOREIGN KEY (moneda_id) REFERENCES public.monedas(id);


--
-- TOC entry 3286 (class 2606 OID 16770)
-- Name: metodos_pago_tarjeta metodos_pago_tarjeta_banco_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago_tarjeta
    ADD CONSTRAINT metodos_pago_tarjeta_banco_id_fkey FOREIGN KEY (banco_id) REFERENCES public.bancos(id);


--
-- TOC entry 3287 (class 2606 OID 16733)
-- Name: metodos_pago_tarjeta metodos_pago_tarjeta_marca_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago_tarjeta
    ADD CONSTRAINT metodos_pago_tarjeta_marca_pago_id_fkey FOREIGN KEY (marca_pago_id) REFERENCES public.marcas_metodos_pago(id);


--
-- TOC entry 3281 (class 2606 OID 16460)
-- Name: metodos_pago metodos_pago_tipo_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metodos_pago
    ADD CONSTRAINT metodos_pago_tipo_pago_id_fkey FOREIGN KEY (tipo_pago_id) REFERENCES public.tipos_metodos_pago(id);


--
-- TOC entry 3288 (class 2606 OID 16753)
-- Name: orden_pago orden_pago_id_estado_pago_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_pago
    ADD CONSTRAINT orden_pago_id_estado_pago_fkey FOREIGN KEY (id_estado_pago) REFERENCES public.estado_pago(id);


--
-- TOC entry 3289 (class 2606 OID 16758)
-- Name: orden_pago orden_pago_id_pago_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_pago
    ADD CONSTRAINT orden_pago_id_pago_fkey FOREIGN KEY (id_pago) REFERENCES public.pagos(id);


--
-- TOC entry 3282 (class 2606 OID 16465)
-- Name: pagos pagos_estado_actual_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_estado_actual_fkey FOREIGN KEY (estado_actual) REFERENCES public.estado_pago(id);


--
-- TOC entry 3283 (class 2606 OID 16470)
-- Name: pagos pagos_metodo_pago_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pagos
    ADD CONSTRAINT pagos_metodo_pago_id_fkey FOREIGN KEY (metodo_pago_id) REFERENCES public.metodos_pago(id);


-- Completed on 2025-11-19 21:54:14 -03

--
-- PostgreSQL database dump complete
--

