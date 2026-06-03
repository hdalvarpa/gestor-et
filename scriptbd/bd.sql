--
-- PostgreSQL database dump
--

-- Dumped from database version 17.10 (6a49db4)
-- Dumped by pg_dump version 17.0

-- Started on 2026-06-03 00:38:31

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 226 (class 1259 OID 57403)
-- Name: entidades_tecnicas; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.entidades_tecnicas (
    id_entidad_tecnica integer NOT NULL,
    ruc character(11) NOT NULL,
    razon_social character varying(150) NOT NULL,
    direccion character varying(255),
    id_representante_legal integer NOT NULL,
    id_ingeniero_actual integer NOT NULL
);


ALTER TABLE public.entidades_tecnicas OWNER TO neondb_owner;

--
-- TOC entry 225 (class 1259 OID 57402)
-- Name: entidades_tecnicas_id_entidad_tecnica_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.entidades_tecnicas_id_entidad_tecnica_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.entidades_tecnicas_id_entidad_tecnica_seq OWNER TO neondb_owner;

--
-- TOC entry 3465 (class 0 OID 0)
-- Dependencies: 225
-- Name: entidades_tecnicas_id_entidad_tecnica_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.entidades_tecnicas_id_entidad_tecnica_seq OWNED BY public.entidades_tecnicas.id_entidad_tecnica;


--
-- TOC entry 228 (class 1259 OID 57424)
-- Name: expedientes; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.expedientes (
    id_expediente integer NOT NULL,
    id_entidad_tecnica integer NOT NULL,
    departamento character varying(50) DEFAULT 'LA LIBERTAD'::character varying,
    provincia character varying(50) DEFAULT 'TRUJILLO'::character varying,
    distrito character varying(50) NOT NULL,
    direccion character varying(255) NOT NULL,
    manzana character varying(10),
    lote character varying(10),
    sublote character varying(10),
    centro_poblado character varying(150),
    referencia character varying(255),
    partida_registral character varying(50),
    tiene_agua boolean DEFAULT false,
    tiene_saneamiento boolean DEFAULT false,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.expedientes OWNER TO neondb_owner;

--
-- TOC entry 227 (class 1259 OID 57423)
-- Name: expedientes_id_expediente_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.expedientes_id_expediente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.expedientes_id_expediente_seq OWNER TO neondb_owner;

--
-- TOC entry 3466 (class 0 OID 0)
-- Dependencies: 227
-- Name: expedientes_id_expediente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.expedientes_id_expediente_seq OWNED BY public.expedientes.id_expediente;


--
-- TOC entry 230 (class 1259 OID 57443)
-- Name: grupo_familiar; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.grupo_familiar (
    id_grupo_familiar integer NOT NULL,
    id_expediente integer NOT NULL,
    id_persona integer NOT NULL,
    vinculo character varying(50) NOT NULL,
    estado_civil character varying(50),
    grado_instruccion character varying(100),
    ocupacion character varying(150),
    situacion_laboral character varying(50),
    condicion_laboral character varying(50),
    discapacidad character varying(50) DEFAULT 'Ninguna'::character varying,
    ingreso_mensual numeric(10,2) DEFAULT 0.00
);


ALTER TABLE public.grupo_familiar OWNER TO neondb_owner;

--
-- TOC entry 229 (class 1259 OID 57442)
-- Name: grupo_familiar_id_grupo_familiar_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.grupo_familiar_id_grupo_familiar_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.grupo_familiar_id_grupo_familiar_seq OWNER TO neondb_owner;

--
-- TOC entry 3467 (class 0 OID 0)
-- Dependencies: 229
-- Name: grupo_familiar_id_grupo_familiar_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.grupo_familiar_id_grupo_familiar_seq OWNED BY public.grupo_familiar.id_grupo_familiar;


--
-- TOC entry 224 (class 1259 OID 57389)
-- Name: ingenieros; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.ingenieros (
    id_ingeniero integer NOT NULL,
    id_persona integer NOT NULL,
    cip character varying(20) NOT NULL
);


ALTER TABLE public.ingenieros OWNER TO neondb_owner;

--
-- TOC entry 223 (class 1259 OID 57388)
-- Name: ingenieros_id_ingeniero_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.ingenieros_id_ingeniero_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingenieros_id_ingeniero_seq OWNER TO neondb_owner;

--
-- TOC entry 3468 (class 0 OID 0)
-- Dependencies: 223
-- Name: ingenieros_id_ingeniero_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.ingenieros_id_ingeniero_seq OWNED BY public.ingenieros.id_ingeniero;


--
-- TOC entry 220 (class 1259 OID 57357)
-- Name: personas; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.personas (
    id_persona integer NOT NULL,
    id_tipo_documento integer NOT NULL,
    numero_documento character varying(20) NOT NULL,
    nombres character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    fecha_nacimiento date,
    telefono character varying(20),
    correo character varying(150),
    direccion_domicilio character varying(255)
);


ALTER TABLE public.personas OWNER TO neondb_owner;

--
-- TOC entry 219 (class 1259 OID 57356)
-- Name: personas_id_persona_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.personas_id_persona_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.personas_id_persona_seq OWNER TO neondb_owner;

--
-- TOC entry 3469 (class 0 OID 0)
-- Dependencies: 219
-- Name: personas_id_persona_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.personas_id_persona_seq OWNED BY public.personas.id_persona;


--
-- TOC entry 232 (class 1259 OID 65537)
-- Name: registros_et; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.registros_et (
    id_registro_et integer NOT NULL,
    id_entidad_tecnica integer NOT NULL,
    codigo_registro character varying(50) NOT NULL,
    anio integer NOT NULL
);


ALTER TABLE public.registros_et OWNER TO neondb_owner;

--
-- TOC entry 231 (class 1259 OID 65536)
-- Name: registros_et_id_registro_et_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.registros_et_id_registro_et_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.registros_et_id_registro_et_seq OWNER TO neondb_owner;

--
-- TOC entry 3470 (class 0 OID 0)
-- Dependencies: 231
-- Name: registros_et_id_registro_et_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.registros_et_id_registro_et_seq OWNED BY public.registros_et.id_registro_et;


--
-- TOC entry 218 (class 1259 OID 57348)
-- Name: tipos_documento; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tipos_documento (
    id_tipo_documento integer NOT NULL,
    codigo character varying(10) NOT NULL
);


ALTER TABLE public.tipos_documento OWNER TO neondb_owner;

--
-- TOC entry 217 (class 1259 OID 57347)
-- Name: tipos_documento_id_tipo_documento_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tipos_documento_id_tipo_documento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipos_documento_id_tipo_documento_seq OWNER TO neondb_owner;

--
-- TOC entry 3471 (class 0 OID 0)
-- Dependencies: 217
-- Name: tipos_documento_id_tipo_documento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tipos_documento_id_tipo_documento_seq OWNED BY public.tipos_documento.id_tipo_documento;


--
-- TOC entry 222 (class 1259 OID 57373)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    id_persona integer NOT NULL,
    username character varying(50) NOT NULL,
    correo_electronico character varying(150) NOT NULL,
    contrasena_hash character varying(255) NOT NULL
);


ALTER TABLE public.usuarios OWNER TO neondb_owner;

--
-- TOC entry 221 (class 1259 OID 57372)
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_usuario_seq OWNER TO neondb_owner;

--
-- TOC entry 3472 (class 0 OID 0)
-- Dependencies: 221
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- TOC entry 3249 (class 2604 OID 57406)
-- Name: entidades_tecnicas id_entidad_tecnica; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas ALTER COLUMN id_entidad_tecnica SET DEFAULT nextval('public.entidades_tecnicas_id_entidad_tecnica_seq'::regclass);


--
-- TOC entry 3250 (class 2604 OID 57427)
-- Name: expedientes id_expediente; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.expedientes ALTER COLUMN id_expediente SET DEFAULT nextval('public.expedientes_id_expediente_seq'::regclass);


--
-- TOC entry 3256 (class 2604 OID 57446)
-- Name: grupo_familiar id_grupo_familiar; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.grupo_familiar ALTER COLUMN id_grupo_familiar SET DEFAULT nextval('public.grupo_familiar_id_grupo_familiar_seq'::regclass);


--
-- TOC entry 3248 (class 2604 OID 57392)
-- Name: ingenieros id_ingeniero; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ingenieros ALTER COLUMN id_ingeniero SET DEFAULT nextval('public.ingenieros_id_ingeniero_seq'::regclass);


--
-- TOC entry 3246 (class 2604 OID 57360)
-- Name: personas id_persona; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.personas ALTER COLUMN id_persona SET DEFAULT nextval('public.personas_id_persona_seq'::regclass);


--
-- TOC entry 3259 (class 2604 OID 65540)
-- Name: registros_et id_registro_et; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et ALTER COLUMN id_registro_et SET DEFAULT nextval('public.registros_et_id_registro_et_seq'::regclass);


--
-- TOC entry 3245 (class 2604 OID 57351)
-- Name: tipos_documento id_tipo_documento; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tipos_documento ALTER COLUMN id_tipo_documento SET DEFAULT nextval('public.tipos_documento_id_tipo_documento_seq'::regclass);


--
-- TOC entry 3247 (class 2604 OID 57376)
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- TOC entry 3453 (class 0 OID 57403)
-- Dependencies: 226
-- Data for Name: entidades_tecnicas; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.entidades_tecnicas VALUES (1, '20607537942', 'CONSTRUCTORA E INVERSIONES COQUITOS S.A.C.', 'AA.HH. NUEVO FLORERNCIA III MZ D LOTE 30', 3, 1);


--
-- TOC entry 3455 (class 0 OID 57424)
-- Dependencies: 228
-- Data for Name: expedientes; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--



--
-- TOC entry 3457 (class 0 OID 57443)
-- Dependencies: 230
-- Data for Name: grupo_familiar; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--



--
-- TOC entry 3451 (class 0 OID 57389)
-- Dependencies: 224
-- Data for Name: ingenieros; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.ingenieros VALUES (1, 4, '289068');


--
-- TOC entry 3447 (class 0 OID 57357)
-- Dependencies: 220
-- Data for Name: personas; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.personas VALUES (1, 1, '00000000', 'Administrador', 'Sistema', NULL, NULL, NULL, NULL);
INSERT INTO public.personas VALUES (2, 1, '75953952', 'HEBER', 'ALVAREZ', NULL, NULL, 'hdalvarpa@gmail.com', NULL);
INSERT INTO public.personas VALUES (3, 1, '45478905', 'JORGE RAFAEL ', 'MENDEZ CABALLERO', NULL, NULL, NULL, NULL);
INSERT INTO public.personas VALUES (4, 1, '46527913', 'LUIS ANGEL', 'GOMEZ SEGURA', NULL, NULL, NULL, NULL);


--
-- TOC entry 3459 (class 0 OID 65537)
-- Dependencies: 232
-- Data for Name: registros_et; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.registros_et VALUES (1, 1, 'LIB-1073-22-1N-26', 2026);


--
-- TOC entry 3445 (class 0 OID 57348)
-- Dependencies: 218
-- Data for Name: tipos_documento; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.tipos_documento VALUES (1, 'DNI');


--
-- TOC entry 3449 (class 0 OID 57373)
-- Dependencies: 222
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.usuarios VALUES (3, 2, 'heber1', 'hdalvarpa@gmail.com', 'scrypt:32768:8:1$ZtkInDaGA5T1HFZI$180a2d08746fbc8bcca730f410d1b0cd3a7a710dab0fbd7ee90fd82198322728fc402b753f45d87cb1b2d158fe74f13793a269656d69ae84366b2331db2b922d');
INSERT INTO public.usuarios VALUES (1, 1, 'admin1', 'admin@sistema.com', 'scrypt:32768:8:1$5xjOkHpMOP0Ixz9b$77083d976a1e42b07191c616b70a03b43db00573687e21aff9882d26bd67c8d3aec3c09024898a52ae75ec15523417f328da1acd6cc453964203a864709074dc');


--
-- TOC entry 3473 (class 0 OID 0)
-- Dependencies: 225
-- Name: entidades_tecnicas_id_entidad_tecnica_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.entidades_tecnicas_id_entidad_tecnica_seq', 1, true);


--
-- TOC entry 3474 (class 0 OID 0)
-- Dependencies: 227
-- Name: expedientes_id_expediente_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.expedientes_id_expediente_seq', 1, false);


--
-- TOC entry 3475 (class 0 OID 0)
-- Dependencies: 229
-- Name: grupo_familiar_id_grupo_familiar_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.grupo_familiar_id_grupo_familiar_seq', 1, false);


--
-- TOC entry 3476 (class 0 OID 0)
-- Dependencies: 223
-- Name: ingenieros_id_ingeniero_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.ingenieros_id_ingeniero_seq', 1, true);


--
-- TOC entry 3477 (class 0 OID 0)
-- Dependencies: 219
-- Name: personas_id_persona_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.personas_id_persona_seq', 4, true);


--
-- TOC entry 3478 (class 0 OID 0)
-- Dependencies: 231
-- Name: registros_et_id_registro_et_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.registros_et_id_registro_et_seq', 1, true);


--
-- TOC entry 3479 (class 0 OID 0)
-- Dependencies: 217
-- Name: tipos_documento_id_tipo_documento_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tipos_documento_id_tipo_documento_seq', 1, true);


--
-- TOC entry 3480 (class 0 OID 0)
-- Dependencies: 221
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 3, true);


--
-- TOC entry 3279 (class 2606 OID 57408)
-- Name: entidades_tecnicas entidades_tecnicas_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas
    ADD CONSTRAINT entidades_tecnicas_pkey PRIMARY KEY (id_entidad_tecnica);


--
-- TOC entry 3281 (class 2606 OID 57410)
-- Name: entidades_tecnicas entidades_tecnicas_ruc_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas
    ADD CONSTRAINT entidades_tecnicas_ruc_key UNIQUE (ruc);


--
-- TOC entry 3283 (class 2606 OID 57436)
-- Name: expedientes expedientes_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.expedientes
    ADD CONSTRAINT expedientes_pkey PRIMARY KEY (id_expediente);


--
-- TOC entry 3285 (class 2606 OID 57452)
-- Name: grupo_familiar grupo_familiar_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.grupo_familiar
    ADD CONSTRAINT grupo_familiar_pkey PRIMARY KEY (id_grupo_familiar);


--
-- TOC entry 3275 (class 2606 OID 57396)
-- Name: ingenieros ingenieros_cip_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ingenieros
    ADD CONSTRAINT ingenieros_cip_key UNIQUE (cip);


--
-- TOC entry 3277 (class 2606 OID 57394)
-- Name: ingenieros ingenieros_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ingenieros
    ADD CONSTRAINT ingenieros_pkey PRIMARY KEY (id_ingeniero);


--
-- TOC entry 3265 (class 2606 OID 57366)
-- Name: personas personas_numero_documento_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_numero_documento_key UNIQUE (numero_documento);


--
-- TOC entry 3267 (class 2606 OID 57364)
-- Name: personas personas_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id_persona);


--
-- TOC entry 3287 (class 2606 OID 65544)
-- Name: registros_et registros_et_id_entidad_tecnica_anio_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et
    ADD CONSTRAINT registros_et_id_entidad_tecnica_anio_key UNIQUE (id_entidad_tecnica, anio);


--
-- TOC entry 3289 (class 2606 OID 65542)
-- Name: registros_et registros_et_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et
    ADD CONSTRAINT registros_et_pkey PRIMARY KEY (id_registro_et);


--
-- TOC entry 3261 (class 2606 OID 57355)
-- Name: tipos_documento tipos_documento_codigo_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tipos_documento
    ADD CONSTRAINT tipos_documento_codigo_key UNIQUE (codigo);


--
-- TOC entry 3263 (class 2606 OID 57353)
-- Name: tipos_documento tipos_documento_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tipos_documento
    ADD CONSTRAINT tipos_documento_pkey PRIMARY KEY (id_tipo_documento);


--
-- TOC entry 3269 (class 2606 OID 57382)
-- Name: usuarios usuarios_correo_electronico_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_electronico_key UNIQUE (correo_electronico);


--
-- TOC entry 3271 (class 2606 OID 57378)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 3273 (class 2606 OID 57380)
-- Name: usuarios usuarios_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_username_key UNIQUE (username);


--
-- TOC entry 3293 (class 2606 OID 57418)
-- Name: entidades_tecnicas entidades_tecnicas_id_ingeniero_actual_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas
    ADD CONSTRAINT entidades_tecnicas_id_ingeniero_actual_fkey FOREIGN KEY (id_ingeniero_actual) REFERENCES public.ingenieros(id_ingeniero);


--
-- TOC entry 3294 (class 2606 OID 57413)
-- Name: entidades_tecnicas entidades_tecnicas_id_representante_legal_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas
    ADD CONSTRAINT entidades_tecnicas_id_representante_legal_fkey FOREIGN KEY (id_representante_legal) REFERENCES public.personas(id_persona);


--
-- TOC entry 3295 (class 2606 OID 57437)
-- Name: expedientes expedientes_id_entidad_tecnica_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.expedientes
    ADD CONSTRAINT expedientes_id_entidad_tecnica_fkey FOREIGN KEY (id_entidad_tecnica) REFERENCES public.entidades_tecnicas(id_entidad_tecnica);


--
-- TOC entry 3296 (class 2606 OID 57453)
-- Name: grupo_familiar grupo_familiar_id_expediente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.grupo_familiar
    ADD CONSTRAINT grupo_familiar_id_expediente_fkey FOREIGN KEY (id_expediente) REFERENCES public.expedientes(id_expediente);


--
-- TOC entry 3297 (class 2606 OID 57458)
-- Name: grupo_familiar grupo_familiar_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.grupo_familiar
    ADD CONSTRAINT grupo_familiar_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona);


--
-- TOC entry 3292 (class 2606 OID 57397)
-- Name: ingenieros ingenieros_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ingenieros
    ADD CONSTRAINT ingenieros_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona);


--
-- TOC entry 3290 (class 2606 OID 57367)
-- Name: personas personas_id_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_tipo_documento_fkey FOREIGN KEY (id_tipo_documento) REFERENCES public.tipos_documento(id_tipo_documento);


--
-- TOC entry 3298 (class 2606 OID 65545)
-- Name: registros_et registros_et_id_entidad_tecnica_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et
    ADD CONSTRAINT registros_et_id_entidad_tecnica_fkey FOREIGN KEY (id_entidad_tecnica) REFERENCES public.entidades_tecnicas(id_entidad_tecnica);


--
-- TOC entry 3291 (class 2606 OID 57383)
-- Name: usuarios usuarios_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona);


--
-- TOC entry 2080 (class 826 OID 16394)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- TOC entry 2079 (class 826 OID 16393)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


-- Completed on 2026-06-03 00:38:45

--
-- PostgreSQL database dump complete
--

-- 1. Agregamos las dos nuevas columnas a la tabla Personas
ALTER TABLE personas ADD COLUMN apellido_paterno VARCHAR(100);
ALTER TABLE personas ADD COLUMN apellido_materno VARCHAR(100);

-- 2. Migramos los datos cortando el texto por el primer espacio
UPDATE personas 
SET 
    apellido_paterno = split_part(apellidos, ' ', 1),
    apellido_materno = CASE 
        -- Si hay más de un apellido (hay espacio), ponemos todo lo que sigue en materno
        WHEN strpos(apellidos, ' ') > 0 THEN substring(apellidos from strpos(apellidos, ' ') + 1)
        -- Si la persona solo tenía registrado un apellido (no hay espacio), lo dejamos en blanco
        ELSE '' 
    END;

-- 3. Eliminamos la columna vieja para dejar la base de datos limpia
ALTER TABLE personas DROP COLUMN apellidos;


CREATE TABLE Asignacion_Ingenieros (
    id_asignacion SERIAL PRIMARY KEY,
    id_entidad_tecnica INT NOT NULL,
    id_ingeniero INT NOT NULL,
    estado VARCHAR(20) DEFAULT 'VIGENTE',
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_entidad_tecnica) REFERENCES Entidades_Tecnicas(id_entidad_tecnica),
    FOREIGN KEY (id_ingeniero) REFERENCES Ingenieros(id_ingeniero)
);
-- 2. Migrar los ingenieros actuales hacia la nueva tabla de asignaciones
INSERT INTO Asignacion_Ingenieros (id_entidad_tecnica, id_ingeniero, estado)
SELECT id_entidad_tecnica, id_ingeniero_actual, 'VIGENTE'
FROM Entidades_Tecnicas
WHERE id_ingeniero_actual IS NOT NULL;
-- 3. Eliminar la columna de la tabla Entidades_Tecnicas (el CASCADE elimina la llave foránea automáticamente)
ALTER TABLE Entidades_Tecnicas DROP COLUMN id_ingeniero_actual CASCADE;

-- ==============================================================================================
-- ACTUALIZACIÓN 3: Independización de Códigos de Registro ET (Registros Anuales huérfanos)
-- ==============================================================================================

-- 1. Quitar la obligatoriedad (NOT NULL) de la columna id_entidad_tecnica
ALTER TABLE registros_et ALTER COLUMN id_entidad_tecnica DROP NOT NULL;

-- ==============================================================================================
-- ACTUALIZACIÓN 4: Restricciones de Base de Datos para Códigos ET (Doble Capa de Seguridad)
-- ==============================================================================================

-- A. CONSTRAINT UNIQUE: Una Entidad Técnica solo puede tener un código de registro por año
ALTER TABLE registros_et 
ADD CONSTRAINT uk_entidad_anio UNIQUE (id_entidad_tecnica, anio);

-- B. TRIGGER: Evitar que se elimine un RegistroET si ya está asignado a una Entidad
CREATE OR REPLACE FUNCTION trg_prevent_delete_assigned_registro()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.id_entidad_tecnica IS NOT NULL THEN
        RAISE EXCEPTION 'No se puede eliminar el código % del año % porque está asignado a una entidad.', OLD.codigo_registro, OLD.anio;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_delete_registro
BEFORE DELETE ON registros_et
FOR EACH ROW
EXECUTE FUNCTION trg_prevent_delete_assigned_registro();