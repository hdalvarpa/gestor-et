--
-- PostgreSQL database dump
--

-- Dumped from database version 17.10 (98a80fa)
-- Dumped by pg_dump version 17.0

-- Started on 2026-06-12 00:16:20

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

--
-- TOC entry 250 (class 1255 OID 81922)
-- Name: trg_prevent_delete_assigned_registro(); Type: FUNCTION; Schema: public; Owner: neondb_owner
--

CREATE FUNCTION public.trg_prevent_delete_assigned_registro() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF OLD.id_entidad_tecnica IS NOT NULL THEN
        RAISE EXCEPTION 'No se puede eliminar el código % del año % porque está asignado a una entidad.', OLD.codigo_registro, OLD.anio;
    END IF;
    RETURN OLD;
END;
$$;


ALTER FUNCTION public.trg_prevent_delete_assigned_registro() OWNER TO neondb_owner;

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
    id_ingeniero_vigente integer
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
-- TOC entry 3514 (class 0 OID 0)
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
-- TOC entry 3515 (class 0 OID 0)
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
-- TOC entry 3516 (class 0 OID 0)
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
-- TOC entry 3517 (class 0 OID 0)
-- Dependencies: 223
-- Name: ingenieros_id_ingeniero_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.ingenieros_id_ingeniero_seq OWNED BY public.ingenieros.id_ingeniero;


--
-- TOC entry 237 (class 1259 OID 98314)
-- Name: permisos; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.permisos (
    id_permiso integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion character varying(200)
);


ALTER TABLE public.permisos OWNER TO neondb_owner;

--
-- TOC entry 236 (class 1259 OID 98313)
-- Name: permisos_id_permiso_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.permisos_id_permiso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permisos_id_permiso_seq OWNER TO neondb_owner;

--
-- TOC entry 3518 (class 0 OID 0)
-- Dependencies: 236
-- Name: permisos_id_permiso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.permisos_id_permiso_seq OWNED BY public.permisos.id_permiso;


--
-- TOC entry 220 (class 1259 OID 57357)
-- Name: personas; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.personas (
    id_persona integer NOT NULL,
    id_tipo_documento integer NOT NULL,
    numero_documento character varying(20) NOT NULL,
    nombres character varying(100) NOT NULL,
    fecha_nacimiento date,
    telefono character varying(20),
    correo character varying(150),
    direccion_domicilio character varying(255),
    apellido_paterno character varying(100),
    apellido_materno character varying(100)
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
-- TOC entry 3519 (class 0 OID 0)
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
    id_entidad_tecnica integer,
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
-- TOC entry 3520 (class 0 OID 0)
-- Dependencies: 231
-- Name: registros_et_id_registro_et_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.registros_et_id_registro_et_seq OWNED BY public.registros_et.id_registro_et;


--
-- TOC entry 235 (class 1259 OID 98305)
-- Name: roles; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.roles (
    id_rol integer NOT NULL,
    nombre character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO neondb_owner;

--
-- TOC entry 234 (class 1259 OID 98304)
-- Name: roles_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.roles_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_rol_seq OWNER TO neondb_owner;

--
-- TOC entry 3521 (class 0 OID 0)
-- Dependencies: 234
-- Name: roles_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.roles_id_rol_seq OWNED BY public.roles.id_rol;


--
-- TOC entry 238 (class 1259 OID 98322)
-- Name: roles_permisos; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.roles_permisos (
    id_rol integer NOT NULL,
    id_permiso integer NOT NULL
);


ALTER TABLE public.roles_permisos OWNER TO neondb_owner;

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
-- TOC entry 3522 (class 0 OID 0)
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
    contrasena_hash character varying(255) NOT NULL,
    estado character varying(20) DEFAULT 'ACTIVO'::character varying NOT NULL,
    id_rol integer NOT NULL
);


ALTER TABLE public.usuarios OWNER TO neondb_owner;

--
-- TOC entry 233 (class 1259 OID 90112)
-- Name: usuarios_entidades; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.usuarios_entidades (
    id_usuario integer NOT NULL,
    id_entidad_tecnica integer NOT NULL,
    fecha_asignacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.usuarios_entidades OWNER TO neondb_owner;

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
-- TOC entry 3523 (class 0 OID 0)
-- Dependencies: 221
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- TOC entry 3269 (class 2604 OID 57406)
-- Name: entidades_tecnicas id_entidad_tecnica; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas ALTER COLUMN id_entidad_tecnica SET DEFAULT nextval('public.entidades_tecnicas_id_entidad_tecnica_seq'::regclass);


--
-- TOC entry 3270 (class 2604 OID 57427)
-- Name: expedientes id_expediente; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.expedientes ALTER COLUMN id_expediente SET DEFAULT nextval('public.expedientes_id_expediente_seq'::regclass);


--
-- TOC entry 3276 (class 2604 OID 57446)
-- Name: grupo_familiar id_grupo_familiar; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.grupo_familiar ALTER COLUMN id_grupo_familiar SET DEFAULT nextval('public.grupo_familiar_id_grupo_familiar_seq'::regclass);


--
-- TOC entry 3268 (class 2604 OID 57392)
-- Name: ingenieros id_ingeniero; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ingenieros ALTER COLUMN id_ingeniero SET DEFAULT nextval('public.ingenieros_id_ingeniero_seq'::regclass);


--
-- TOC entry 3282 (class 2604 OID 98317)
-- Name: permisos id_permiso; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.permisos ALTER COLUMN id_permiso SET DEFAULT nextval('public.permisos_id_permiso_seq'::regclass);


--
-- TOC entry 3265 (class 2604 OID 57360)
-- Name: personas id_persona; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.personas ALTER COLUMN id_persona SET DEFAULT nextval('public.personas_id_persona_seq'::regclass);


--
-- TOC entry 3279 (class 2604 OID 65540)
-- Name: registros_et id_registro_et; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et ALTER COLUMN id_registro_et SET DEFAULT nextval('public.registros_et_id_registro_et_seq'::regclass);


--
-- TOC entry 3281 (class 2604 OID 98308)
-- Name: roles id_rol; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.roles ALTER COLUMN id_rol SET DEFAULT nextval('public.roles_id_rol_seq'::regclass);


--
-- TOC entry 3264 (class 2604 OID 57351)
-- Name: tipos_documento id_tipo_documento; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tipos_documento ALTER COLUMN id_tipo_documento SET DEFAULT nextval('public.tipos_documento_id_tipo_documento_seq'::regclass);


--
-- TOC entry 3266 (class 2604 OID 57376)
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- TOC entry 3496 (class 0 OID 57403)
-- Dependencies: 226
-- Data for Name: entidades_tecnicas; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.entidades_tecnicas VALUES (2, '20608212575', 'INVERSIONES & SERVICIOS MULTIPLES SENIA E.I.RL.', 'AA.HH. NUEVO FLORENCIA III MZ G LOTE 17', 5, 2);
INSERT INTO public.entidades_tecnicas VALUES (1, '20607537942', 'CONSTRUCTORA E INVERSIONES COQUITOS S.A.C.', 'AA.HH. NUEVO FLORERNCIA III MZ D LOTE 30', 3, 1);
INSERT INTO public.entidades_tecnicas VALUES (3, '99999999999', 'CONTRUCTORA DE HEBERDAVIDALVAREZPAREDES', 'LINCH547 LAS QUINTANAS', 2, 4);


--
-- TOC entry 3498 (class 0 OID 57424)
-- Dependencies: 228
-- Data for Name: expedientes; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--



--
-- TOC entry 3500 (class 0 OID 57443)
-- Dependencies: 230
-- Data for Name: grupo_familiar; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--



--
-- TOC entry 3494 (class 0 OID 57389)
-- Dependencies: 224
-- Data for Name: ingenieros; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.ingenieros VALUES (1, 4, '289068');
INSERT INTO public.ingenieros VALUES (2, 6, '196235');
INSERT INTO public.ingenieros VALUES (4, 8, '111111');


--
-- TOC entry 3507 (class 0 OID 98314)
-- Dependencies: 237
-- Data for Name: permisos; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.permisos VALUES (1, 'GESTIONAR_SEGURIDAD', 'Crear, editar usuarios y gestionar roles/permisos.');
INSERT INTO public.permisos VALUES (2, 'ASIGNAR_ENTIDADES', 'Asignar entidades técnicas a los usuarios del sistema.');
INSERT INTO public.permisos VALUES (3, 'CREAR_ENTIDADES', 'Crear nuevas entidades técnicas (RUC, Empresa).');
INSERT INTO public.permisos VALUES (4, 'VER_ENTIDADES', 'Ver la lista de entidades técnicas asignadas y acceder a ellas.');
INSERT INTO public.permisos VALUES (5, 'GESTIONAR_INGENIEROS', 'Listar, crear y editar el padrón global de ingenieros.');
INSERT INTO public.permisos VALUES (6, 'ASIGNAR_INGENIEROS', 'Vincular ingenieros del padrón a las entidades técnicas asignadas.');
INSERT INTO public.permisos VALUES (7, 'GESTIONAR_REGISTROS', 'Crear y administrar códigos de registro anuales.');
INSERT INTO public.permisos VALUES (8, 'ASIGNAR_REGISTROS', 'Asignar códigos de registro a las entidades técnicas asignadas.');


--
-- TOC entry 3490 (class 0 OID 57357)
-- Dependencies: 220
-- Data for Name: personas; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.personas VALUES (1, 1, '00000000', 'Administrador', NULL, NULL, NULL, NULL, 'Sistema', '');
INSERT INTO public.personas VALUES (2, 1, '75953952', 'HEBER', NULL, NULL, 'hdalvarpa@gmail.com', NULL, 'ALVAREZ', '');
INSERT INTO public.personas VALUES (3, 1, '45478905', 'JORGE RAFAEL ', NULL, NULL, NULL, NULL, 'MENDEZ', 'CABALLERO');
INSERT INTO public.personas VALUES (4, 1, '46527913', 'LUIS ANGEL', NULL, NULL, NULL, NULL, 'GOMEZ', 'SEGURA');
INSERT INTO public.personas VALUES (5, 1, '78021878', 'NAYKO NAY', NULL, NULL, NULL, NULL, 'CERQUIN', 'CABALLERO');
INSERT INTO public.personas VALUES (6, 1, '71238683', 'CARLOS ALEJANDRO ANTONIO', NULL, NULL, NULL, NULL, 'ARAUJO', 'GUEVARA');
INSERT INTO public.personas VALUES (7, 1, '75951111', 'NOMBRE PRUEBA', NULL, NULL, 'gaaaaaaaaaaaa@gmail.com', NULL, 'APELLIDO PATERNO', 'APELLIDO MATERNO');
INSERT INTO public.personas VALUES (8, 1, '88888888', 'INGPRUEBA', NULL, NULL, NULL, NULL, 'INGPATERNO', 'INGMATERNO');


--
-- TOC entry 3502 (class 0 OID 65537)
-- Dependencies: 232
-- Data for Name: registros_et; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.registros_et VALUES (1, 1, 'LIB-1073-22-1N-26', 2026);
INSERT INTO public.registros_et VALUES (5, 3, 'COD-REG-COD-REG', 2026);


--
-- TOC entry 3505 (class 0 OID 98305)
-- Dependencies: 235
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.roles VALUES (1, 'SuperAdmin');
INSERT INTO public.roles VALUES (2, 'Usuario Básico');


--
-- TOC entry 3508 (class 0 OID 98322)
-- Dependencies: 238
-- Data for Name: roles_permisos; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.roles_permisos VALUES (1, 1);
INSERT INTO public.roles_permisos VALUES (1, 2);
INSERT INTO public.roles_permisos VALUES (1, 3);
INSERT INTO public.roles_permisos VALUES (1, 4);
INSERT INTO public.roles_permisos VALUES (1, 5);
INSERT INTO public.roles_permisos VALUES (1, 6);
INSERT INTO public.roles_permisos VALUES (1, 7);
INSERT INTO public.roles_permisos VALUES (1, 8);
INSERT INTO public.roles_permisos VALUES (2, 4);
INSERT INTO public.roles_permisos VALUES (2, 5);
INSERT INTO public.roles_permisos VALUES (2, 6);
INSERT INTO public.roles_permisos VALUES (2, 7);
INSERT INTO public.roles_permisos VALUES (2, 8);


--
-- TOC entry 3488 (class 0 OID 57348)
-- Dependencies: 218
-- Data for Name: tipos_documento; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.tipos_documento VALUES (1, 'DNI');


--
-- TOC entry 3492 (class 0 OID 57373)
-- Dependencies: 222
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.usuarios VALUES (1, 1, 'admin1', 'admin@sistema.com', 'scrypt:32768:8:1$5xjOkHpMOP0Ixz9b$77083d976a1e42b07191c616b70a03b43db00573687e21aff9882d26bd67c8d3aec3c09024898a52ae75ec15523417f328da1acd6cc453964203a864709074dc', 'ACTIVO', 1);
INSERT INTO public.usuarios VALUES (5, 2, 'HDALVARPA', 'hdalvarpa@gmail.com', 'scrypt:32768:8:1$Nfh7YEYM3yXXNWrx$4b4a8fd9b7e356e7477e86f55a69e05f6456ccedae39b49c7ecd6a27dea1c86089062f8ad551677eb0cbdfd3511550ecb9e989a2dfbe71fbe270dec058693124', 'ACTIVO', 2);
INSERT INTO public.usuarios VALUES (6, 5, 'NAYKO', 'cambiarcorreo@gmail.com', 'scrypt:32768:8:1$GGU8OTM9tRcIIdeW$34e7cedb480c8737edaa317ba9239499be288a77d50e1776cce7b4bf656eb2198c2722101bf019846bcc45330e071402e5d586d20913d096f96ac9ddf8645050', 'ACTIVO', 2);


--
-- TOC entry 3503 (class 0 OID 90112)
-- Dependencies: 233
-- Data for Name: usuarios_entidades; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

INSERT INTO public.usuarios_entidades VALUES (5, 3, '2026-06-11 08:23:57.27885');
INSERT INTO public.usuarios_entidades VALUES (6, 2, '2026-06-11 08:28:09.497367');
INSERT INTO public.usuarios_entidades VALUES (6, 1, '2026-06-11 08:28:29.871611');


--
-- TOC entry 3524 (class 0 OID 0)
-- Dependencies: 225
-- Name: entidades_tecnicas_id_entidad_tecnica_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.entidades_tecnicas_id_entidad_tecnica_seq', 3, true);


--
-- TOC entry 3525 (class 0 OID 0)
-- Dependencies: 227
-- Name: expedientes_id_expediente_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.expedientes_id_expediente_seq', 1, false);


--
-- TOC entry 3526 (class 0 OID 0)
-- Dependencies: 229
-- Name: grupo_familiar_id_grupo_familiar_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.grupo_familiar_id_grupo_familiar_seq', 1, false);


--
-- TOC entry 3527 (class 0 OID 0)
-- Dependencies: 223
-- Name: ingenieros_id_ingeniero_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.ingenieros_id_ingeniero_seq', 4, true);


--
-- TOC entry 3528 (class 0 OID 0)
-- Dependencies: 236
-- Name: permisos_id_permiso_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.permisos_id_permiso_seq', 8, true);


--
-- TOC entry 3529 (class 0 OID 0)
-- Dependencies: 219
-- Name: personas_id_persona_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.personas_id_persona_seq', 8, true);


--
-- TOC entry 3530 (class 0 OID 0)
-- Dependencies: 231
-- Name: registros_et_id_registro_et_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.registros_et_id_registro_et_seq', 5, true);


--
-- TOC entry 3531 (class 0 OID 0)
-- Dependencies: 234
-- Name: roles_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.roles_id_rol_seq', 2, true);


--
-- TOC entry 3532 (class 0 OID 0)
-- Dependencies: 217
-- Name: tipos_documento_id_tipo_documento_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tipos_documento_id_tipo_documento_seq', 1, true);


--
-- TOC entry 3533 (class 0 OID 0)
-- Dependencies: 221
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 6, true);


--
-- TOC entry 3302 (class 2606 OID 57408)
-- Name: entidades_tecnicas entidades_tecnicas_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas
    ADD CONSTRAINT entidades_tecnicas_pkey PRIMARY KEY (id_entidad_tecnica);


--
-- TOC entry 3304 (class 2606 OID 57410)
-- Name: entidades_tecnicas entidades_tecnicas_ruc_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas
    ADD CONSTRAINT entidades_tecnicas_ruc_key UNIQUE (ruc);


--
-- TOC entry 3306 (class 2606 OID 57436)
-- Name: expedientes expedientes_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.expedientes
    ADD CONSTRAINT expedientes_pkey PRIMARY KEY (id_expediente);


--
-- TOC entry 3308 (class 2606 OID 57452)
-- Name: grupo_familiar grupo_familiar_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.grupo_familiar
    ADD CONSTRAINT grupo_familiar_pkey PRIMARY KEY (id_grupo_familiar);


--
-- TOC entry 3298 (class 2606 OID 57396)
-- Name: ingenieros ingenieros_cip_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ingenieros
    ADD CONSTRAINT ingenieros_cip_key UNIQUE (cip);


--
-- TOC entry 3300 (class 2606 OID 57394)
-- Name: ingenieros ingenieros_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ingenieros
    ADD CONSTRAINT ingenieros_pkey PRIMARY KEY (id_ingeniero);


--
-- TOC entry 3322 (class 2606 OID 98321)
-- Name: permisos permisos_nombre_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.permisos
    ADD CONSTRAINT permisos_nombre_key UNIQUE (nombre);


--
-- TOC entry 3324 (class 2606 OID 98319)
-- Name: permisos permisos_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.permisos
    ADD CONSTRAINT permisos_pkey PRIMARY KEY (id_permiso);


--
-- TOC entry 3288 (class 2606 OID 57366)
-- Name: personas personas_numero_documento_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_numero_documento_key UNIQUE (numero_documento);


--
-- TOC entry 3290 (class 2606 OID 57364)
-- Name: personas personas_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id_persona);


--
-- TOC entry 3310 (class 2606 OID 65544)
-- Name: registros_et registros_et_id_entidad_tecnica_anio_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et
    ADD CONSTRAINT registros_et_id_entidad_tecnica_anio_key UNIQUE (id_entidad_tecnica, anio);


--
-- TOC entry 3312 (class 2606 OID 65542)
-- Name: registros_et registros_et_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et
    ADD CONSTRAINT registros_et_pkey PRIMARY KEY (id_registro_et);


--
-- TOC entry 3318 (class 2606 OID 98312)
-- Name: roles roles_nombre_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_nombre_key UNIQUE (nombre);


--
-- TOC entry 3326 (class 2606 OID 98326)
-- Name: roles_permisos roles_permisos_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_pkey PRIMARY KEY (id_rol, id_permiso);


--
-- TOC entry 3320 (class 2606 OID 98310)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_rol);


--
-- TOC entry 3284 (class 2606 OID 57355)
-- Name: tipos_documento tipos_documento_codigo_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tipos_documento
    ADD CONSTRAINT tipos_documento_codigo_key UNIQUE (codigo);


--
-- TOC entry 3286 (class 2606 OID 57353)
-- Name: tipos_documento tipos_documento_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tipos_documento
    ADD CONSTRAINT tipos_documento_pkey PRIMARY KEY (id_tipo_documento);


--
-- TOC entry 3314 (class 2606 OID 81921)
-- Name: registros_et uk_entidad_anio; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et
    ADD CONSTRAINT uk_entidad_anio UNIQUE (id_entidad_tecnica, anio);


--
-- TOC entry 3292 (class 2606 OID 57382)
-- Name: usuarios usuarios_correo_electronico_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_electronico_key UNIQUE (correo_electronico);


--
-- TOC entry 3316 (class 2606 OID 90117)
-- Name: usuarios_entidades usuarios_entidades_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios_entidades
    ADD CONSTRAINT usuarios_entidades_pkey PRIMARY KEY (id_usuario, id_entidad_tecnica);


--
-- TOC entry 3294 (class 2606 OID 57378)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 3296 (class 2606 OID 57380)
-- Name: usuarios usuarios_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_username_key UNIQUE (username);


--
-- TOC entry 3341 (class 2620 OID 81923)
-- Name: registros_et trg_check_delete_registro; Type: TRIGGER; Schema: public; Owner: neondb_owner
--

CREATE TRIGGER trg_check_delete_registro BEFORE DELETE ON public.registros_et FOR EACH ROW EXECUTE FUNCTION public.trg_prevent_delete_assigned_registro();


--
-- TOC entry 3331 (class 2606 OID 106496)
-- Name: entidades_tecnicas entidades_tecnicas_id_ingeniero_vigente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas
    ADD CONSTRAINT entidades_tecnicas_id_ingeniero_vigente_fkey FOREIGN KEY (id_ingeniero_vigente) REFERENCES public.ingenieros(id_ingeniero) ON DELETE SET NULL;


--
-- TOC entry 3332 (class 2606 OID 57413)
-- Name: entidades_tecnicas entidades_tecnicas_id_representante_legal_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.entidades_tecnicas
    ADD CONSTRAINT entidades_tecnicas_id_representante_legal_fkey FOREIGN KEY (id_representante_legal) REFERENCES public.personas(id_persona);


--
-- TOC entry 3333 (class 2606 OID 57437)
-- Name: expedientes expedientes_id_entidad_tecnica_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.expedientes
    ADD CONSTRAINT expedientes_id_entidad_tecnica_fkey FOREIGN KEY (id_entidad_tecnica) REFERENCES public.entidades_tecnicas(id_entidad_tecnica);


--
-- TOC entry 3337 (class 2606 OID 90123)
-- Name: usuarios_entidades fk_entidad; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios_entidades
    ADD CONSTRAINT fk_entidad FOREIGN KEY (id_entidad_tecnica) REFERENCES public.entidades_tecnicas(id_entidad_tecnica) ON DELETE CASCADE;


--
-- TOC entry 3338 (class 2606 OID 90118)
-- Name: usuarios_entidades fk_usuario; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios_entidades
    ADD CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE;


--
-- TOC entry 3334 (class 2606 OID 57453)
-- Name: grupo_familiar grupo_familiar_id_expediente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.grupo_familiar
    ADD CONSTRAINT grupo_familiar_id_expediente_fkey FOREIGN KEY (id_expediente) REFERENCES public.expedientes(id_expediente);


--
-- TOC entry 3335 (class 2606 OID 57458)
-- Name: grupo_familiar grupo_familiar_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.grupo_familiar
    ADD CONSTRAINT grupo_familiar_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona);


--
-- TOC entry 3330 (class 2606 OID 57397)
-- Name: ingenieros ingenieros_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ingenieros
    ADD CONSTRAINT ingenieros_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona);


--
-- TOC entry 3327 (class 2606 OID 57367)
-- Name: personas personas_id_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_id_tipo_documento_fkey FOREIGN KEY (id_tipo_documento) REFERENCES public.tipos_documento(id_tipo_documento);


--
-- TOC entry 3336 (class 2606 OID 65545)
-- Name: registros_et registros_et_id_entidad_tecnica_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.registros_et
    ADD CONSTRAINT registros_et_id_entidad_tecnica_fkey FOREIGN KEY (id_entidad_tecnica) REFERENCES public.entidades_tecnicas(id_entidad_tecnica);


--
-- TOC entry 3339 (class 2606 OID 98332)
-- Name: roles_permisos roles_permisos_id_permiso_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_id_permiso_fkey FOREIGN KEY (id_permiso) REFERENCES public.permisos(id_permiso) ON DELETE CASCADE;


--
-- TOC entry 3340 (class 2606 OID 98327)
-- Name: roles_permisos roles_permisos_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.roles_permisos
    ADD CONSTRAINT roles_permisos_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol) ON DELETE CASCADE;


--
-- TOC entry 3328 (class 2606 OID 57383)
-- Name: usuarios usuarios_id_persona_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_id_persona_fkey FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona);


--
-- TOC entry 3329 (class 2606 OID 98337)
-- Name: usuarios usuarios_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol);


--
-- TOC entry 2099 (class 826 OID 16394)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- TOC entry 2098 (class 826 OID 16393)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


-- Completed on 2026-06-12 00:16:38

--
-- PostgreSQL database dump complete
--

