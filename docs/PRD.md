# 📋 Product Requirements Document (PRD)
## Metadatos App - Sistema de Gestión de Archivos Digitales

---

### **Información del Documento**

| Campo | Detalle |
|-------|---------|
| **Producto** | Metadatos App |
| **Versión** | 2.0 |
| **Fecha** | Agosto 2024 |
| **Autor** | Gabriel Araya (@Gabo-araya) |
| **Estado** | Activo |
| **Tipo** | Web Application |

---

## 🎯 **1. Visión del Producto**

### **1.1 Propósito**
Metadatos App es una aplicación web desarrollada en Flask que proporciona una solución integral para la gestión, organización y visualización de archivos digitales, implementando estándares internacionales de metadatos Dublin Core para garantizar la interoperabilidad y catalogación profesional de recursos digitales.

### **1.2 Declaración de Visión**
*"Ser la herramienta líder para organizaciones que necesitan gestionar, catalogar y compartir archivos digitales de manera profesional, segura y eficiente, siguiendo estándares internacionales de metadatos."*

### **1.3 Misión**
Facilitar la gestión profesional de archivos digitales mediante una interfaz intuitiva que permita la catalogación completa con metadatos Dublin Core, búsqueda avanzada y acceso controlado, garantizando la preservación y accesibilidad de la información digital.

---

## 👥 **2. Audiencia Objetivo**

### **2.1 Usuarios Primarios**

#### **Administradores de Contenido Digital**
- **Perfil**: Bibliotecarios, archivistas, gestores de documentación
- **Necesidades**: Catalogar archivos con metadatos profesionales, gestión masiva de documentos
- **Nivel técnico**: Intermedio
- **Objetivos**: Organización eficiente, búsqueda rápida, cumplimiento de estándares

#### **Organizaciones Educativas**
- **Perfil**: Universidades, colegios, centros de investigación
- **Necesidades**: Repositorio de materiales educativos, recursos compartidos
- **Nivel técnico**: Básico a intermedio
- **Objetivos**: Acceso fácil a recursos, organización por categorías

#### **Pequeñas y Medianas Empresas**
- **Perfil**: Empresas con necesidades de gestión documental
- **Necesidades**: Archivo digital organizado, acceso controlado
- **Nivel técnico**: Básico
- **Objetivos**: Eficiencia operativa, cumplimiento normativo

### **2.2 Usuarios Secundarios**

#### **Usuarios Finales (Público)**
- **Perfil**: Personas que consultan los archivos públicos
- **Necesidades**: Búsqueda sencilla, descarga de archivos
- **Nivel técnico**: Básico
- **Objetivos**: Encontrar y acceder a información relevante

#### **Desarrolladores y Administradores de Sistemas**
- **Perfil**: Personal técnico responsable del despliegue
- **Necesidades**: Instalación, configuración, mantenimiento
- **Nivel técnico**: Avanzado
- **Objetivos**: Despliegue seguro, rendimiento óptimo

---

## 🎯 **3. Objetivos del Producto**

### **3.1 Objetivos de Negocio**

| Objetivo | Métrica | Plazo | Prioridad |
|----------|---------|-------|-----------|
| Simplificar gestión documental | 50% reducción en tiempo de catalogación | 6 meses | Alta |
| Mejorar accesibilidad | 95% disponibilidad del sistema | Continuo | Alta |
| Cumplir estándares internacionales | 100% compatibilidad Dublin Core | Inmediato | Alta |
| Reducir costos operativos | 30% reducción en costos de gestión documental | 1 año | Media |

### **3.2 Objetivos de Usuario**

| Usuario | Objetivo | Beneficio |
|---------|----------|-----------|
| Administrador | Catalogar 100+ archivos/día | Eficiencia operativa |
| Usuario público | Encontrar archivos en <30 segundos | Experiencia satisfactoria |
| Organización | Cumplir normativas documentales | Cumplimiento regulatorio |

### **3.3 Objetivos Técnicos**

- **Rendimiento**: Tiempo de respuesta <2 segundos
- **Escalabilidad**: Soporte para 10,000+ archivos
- **Seguridad**: Protección contra vulnerabilidades OWASP Top 10
- **Disponibilidad**: 99.5% uptime
- **Compatibilidad**: Soporte multi-navegador moderno

---

## ⚡ **4. Funcionalidades Principales**

### **4.1 Gestión de Archivos**

#### **F001: Subida de Archivos**
- **Descripción**: Permite a administradores subir archivos con validación de tipo y tamaño
- **Tipos soportados**: PDF, DOC(X), XLS(X), PPT(X), JPG, PNG, GIF, MP3, MP4, ZIP, etc.
- **Límite de tamaño**: 16MB por archivo
- **Validaciones**: 
  - Tipo de archivo seguro
  - Nombre de archivo seguro (prevención path traversal)
  - Detección de archivos maliciosos
- **Prioridad**: P0 (Crítica)

#### **F002: Metadatos Dublin Core**
- **Descripción**: Catalogación completa usando estándares Dublin Core
- **Campos**: Título, Descripción, Creador, Tema, Fecha, Tipo, Formato, Idioma, Derechos
- **Validaciones**: Campos obligatorios, límites de caracteres
- **Autocompletado**: Sugerencias basadas en archivos existentes
- **Prioridad**: P0 (Crítica)

#### **F003: Gestión de Archivos Duplicados**
- **Descripción**: Prevención automática de archivos duplicados
- **Funcionalidad**: Renombrado automático con sufijo numérico
- **Detección**: Por nombre de archivo y hash (futuro)
- **Prioridad**: P1 (Alta)

### **4.2 Búsqueda y Navegación**

#### **F004: Búsqueda Avanzada**
- **Descripción**: Sistema de búsqueda full-text en metadatos
- **Campos de búsqueda**: Título, descripción, palabras clave
- **Filtros**: Por tipo de archivo, fecha de subida, tamaño
- **Resultados**: Paginados, ordenables, con vista previa
- **Prioridad**: P0 (Crítica)

#### **F005: Navegación por Categorías**
- **Descripción**: Organización visual por tipos de archivo
- **Categorías**: Documentos, Imágenes, Audio, Video, Archivos
- **Iconografía**: Íconos dinámicos por tipo de archivo
- **Estadísticas**: Contadores por categoría
- **Prioridad**: P1 (Alta)

#### **F006: Paginación Inteligente**
- **Descripción**: Navegación eficiente para grandes colecciones
- **Configuración**: 12 archivos por página (público), 10 (admin)
- **Controles**: Primera, anterior, siguiente, última página
- **Performance**: Optimización de consultas DB
- **Prioridad**: P1 (Alta)

### **4.3 Administración y Seguridad**

#### **F007: Autenticación Segura**
- **Descripción**: Sistema de login para administradores
- **Seguridad**: Hashing PBKDF2, rate limiting, logging de intentos
- **Sesiones**: Configuración segura (HttpOnly, SameSite, expiración)
- **Recuperación**: Sistema de recuperación de contraseña (futuro)
- **Prioridad**: P0 (Crítica)

#### **F008: Panel de Administración**
- **Descripción**: Interfaz completa para gestión de archivos
- **Funcionalidades**: 
  - Vista de todos los archivos con paginación
  - Eliminación segura con confirmación
  - Estadísticas de uso
  - Logs de actividad
- **Prioridad**: P0 (Crítica)

#### **F009: Protección CSRF**
- **Descripción**: Protección contra ataques Cross-Site Request Forgery
- **Implementación**: Flask-WTF con tokens CSRF
- **Alcance**: Todos los formularios POST
- **Prioridad**: P0 (Crítica)

#### **F010: Rate Limiting**
- **Descripción**: Protección contra ataques de fuerza bruta
- **Límites**: 
  - Login: 5 intentos/minuto
  - Upload: 10 archivos/minuto  
  - Delete: 5 eliminaciones/minuto
- **Prioridad**: P0 (Crítica)

### **4.4 Experiencia de Usuario**

#### **F011: Interfaz Responsiva**
- **Descripción**: Diseño adaptable a todos los dispositivos
- **Framework**: Bootstrap 5.3 con componentes personalizados
- **Breakpoints**: Mobile-first design
- **Accesibilidad**: WCAG 2.1 AA compliance
- **Prioridad**: P0 (Crítica)

#### **F012: Feedback Visual**
- **Descripción**: Mensajes de estado y confirmación para todas las acciones
- **Tipos**: Éxito, advertencia, error, información
- **Persistencia**: Auto-dismiss después de 5 segundos
- **Ubicación**: Toast notifications y mensajes inline
- **Prioridad**: P1 (Alta)

#### **F013: Centro de Ayuda**
- **Descripción**: Documentación integrada para usuarios
- **Contenido**: Guías de uso, FAQ, troubleshooting
- **Formato**: HTML responsivo con navegación
- **Actualización**: Contenido mantenido por administradores
- **Prioridad**: P2 (Media)

---

## 🛡️ **5. Requisitos de Seguridad**

### **5.1 Autenticación y Autorización**

| Requisito | Descripción | Implementación |
|-----------|-------------|----------------|
| **S001** | Autenticación segura de administradores | Hash PBKDF2, sesiones seguras |
| **S002** | Control de acceso basado en roles | Administrador vs. Usuario público |
| **S003** | Expiración automática de sesiones | 2 horas de inactividad |
| **S004** | Logging de eventos de seguridad | IP, timestamp, user agent |

### **5.2 Protección de Datos**

| Requisito | Descripción | Implementación |
|-----------|-------------|----------------|
| **S005** | Sanitización de entrada | Bleach para HTML, validación WTF |
| **S006** | Protección XSS | Headers de seguridad, CSP |
| **S007** | Prevención CSRF | Flask-WTF tokens |
| **S008** | Validación de archivos | Whitelist extensiones, nombre seguro |

### **5.3 Headers de Seguridad**

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
```

### **5.4 Rate Limiting**

| Endpoint | Límite | Ventana | Acción |
|----------|--------|---------|--------|
| `/login` | 5 intentos | 1 minuto | Block IP temporalmente |
| `/admin` | 10 uploads | 1 minuto | Error 429 |
| `/admin/delete` | 5 eliminaciones | 1 minuto | Error 429 |

---

## 📊 **6. Requisitos de Rendimiento**

### **6.1 Métricas de Rendimiento**

| Métrica | Objetivo | Método de Medición |
|---------|----------|--------------------|
| **Tiempo de respuesta** | <2 segundos | New Relic, logs de aplicación |
| **Tiempo de carga inicial** | <3 segundos | Google PageSpeed Insights |
| **Throughput de archivos** | 100 uploads/hora | Métricas de aplicación |
| **Disponibilidad** | 99.5% | Monitoring externo |

### **6.2 Escalabilidad**

| Recurso | Límite Actual | Límite Objetivo |
|---------|---------------|-----------------|
| **Archivos simultáneos** | 10,000 | 50,000 |
| **Usuarios concurrentes** | 50 | 200 |
| **Tamaño de archivo** | 16MB | 50MB |
| **Almacenamiento total** | 10GB | 100GB |

### **6.3 Optimizaciones**

- **Base de datos**: Índices en campos de búsqueda frecuente
- **Archivos estáticos**: CDN para CSS/JS externos
- **Imágenes**: Compresión automática (futuro)
- **Caché**: Redis para sesiones (futuro)

---

## 🔧 **7. Requisitos Técnicos**

### **7.1 Arquitectura del Sistema**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Storage       │
│   Bootstrap 5.3 │◄──►│   Flask 3.0     │◄──►│   SQLite        │
│   JavaScript    │    │   SQLAlchemy    │    │   FileSystem    │
│   CSS Custom    │    │   Jinja2        │    │   Logs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **7.2 Stack Tecnológico**

#### **Backend**
- **Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy 3.1.1
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción recomendado)
- **Servidor WSGI**: Gunicorn 21.2.0
- **Seguridad**: Flask-WTF 1.2.1, Flask-Limiter 3.5.0, Bleach 6.1.0

#### **Frontend**
- **CSS Framework**: Bootstrap 5.3.3
- **Iconografía**: Bootstrap Icons 1.11.3
- **JavaScript**: Vanilla ES6+
- **Responsividad**: Mobile-first design

#### **Infraestructura**
- **Containerización**: Podman/Docker
- **Proxy reverso**: Nginx (opcional)
- **Logging**: Python logging + archivo rotativo
- **Monitoreo**: Health check endpoint

### **7.3 Estructura de Base de Datos**

#### **Tabla: files**
```sql
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    filename VARCHAR(255) NOT NULL UNIQUE,
    original_filename VARCHAR(255),
    file_size FLOAT DEFAULT 0.0,
    mime_type VARCHAR(100),
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- Dublin Core fields
    dc_creator VARCHAR(255) DEFAULT 'Metadatos App Admin',
    dc_subject VARCHAR(500),
    dc_language VARCHAR(10) DEFAULT 'es',
    dc_rights VARCHAR(500) DEFAULT '© 2024 Metadatos App. Todos los derechos reservados.'
);
```

#### **Tabla: activity_logs**
```sql
CREATE TABLE activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action VARCHAR(50) NOT NULL,
    description VARCHAR(500) NOT NULL,
    username VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    file_id INTEGER REFERENCES files(id),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **7.4 APIs y Endpoints**

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `GET` | `/` | Página principal con archivos | No |
| `GET` | `/login` | Formulario de login | No |
| `POST` | `/login` | Procesar login | No |
| `GET` | `/logout` | Cerrar sesión | Sí |
| `GET` | `/admin` | Panel de administración | Sí |
| `POST` | `/admin` | Subir nuevo archivo | Sí |
| `POST` | `/admin/delete/<id>` | Eliminar archivo | Sí |
| `GET` | `/file/<id>` | Vista detallada de archivo | No |
| `GET` | `/help` | Centro de ayuda | No |
| `GET` | `/health` | Health check | No |

---

## 🚀 **8. Plan de Implementación**

### **8.1 Roadmap de Desarrollo**

#### **Fase 1: Core MVP (Completado)**
- ✅ Autenticación básica
- ✅ Subida y gestión de archivos
- ✅ Metadatos Dublin Core básicos
- ✅ Búsqueda simple
- ✅ Interfaz responsiva

#### **Fase 2: Seguridad y Calidad (En Progreso)**
- ✅ Protección CSRF
- ✅ Rate limiting
- ✅ Headers de seguridad
- ✅ Sanitización de entrada
- ✅ Logging avanzado
- 🔄 Testing automatizado
- 🔄 Documentación completa

#### **Fase 3: Características Avanzadas (Futuro)**
- 📋 Búsqueda con filtros avanzados
- 📋 Sistema de etiquetas (tags)
- 📋 Búsqueda full-text en contenido de archivos
- 📋 Vista previa de archivos (PDF, imágenes)
- 📋 API REST completa
- 📋 Exportación de metadatos (XML, JSON)

#### **Fase 4: Escalabilidad (Futuro)**
- 📋 Migración a PostgreSQL
- 📋 Sistema de caché con Redis
- 📋 CDN para archivos estáticos
- 📋 Compresión de imágenes
- 📋 Búsqueda con Elasticsearch
- 📋 Múltiples idiomas (i18n)

### **8.2 Criterios de Aceptación**

#### **Para Fase 2 (Actual)**
- [ ] Todos los formularios protegidos con CSRF
- [ ] Rate limiting funcionando en todas las rutas críticas
- [ ] Headers de seguridad implementados
- [ ] Cobertura de testing >80%
- [ ] Documentación de API completa
- [ ] Guía de despliegue actualizada

#### **Para Fase 3**
- [ ] Filtros de búsqueda funcionales
- [ ] Sistema de tags operativo
- [ ] Vista previa de archivos implementada
- [ ] API REST documentada con Swagger
- [ ] Exportación de metadatos funcionando

---

## 📋 **9. Casos de Uso Detallados**

### **UC001: Subir Archivo (Administrador)**

**Actor**: Administrador
**Precondiciones**: Usuario autenticado con permisos de administrador
**Flujo Principal**:
1. Administrador accede al panel de administración
2. Completa el formulario de subida:
   - Título (obligatorio, 3-255 caracteres)
   - Descripción (obligatorio, 10-1000 caracteres)
   - Archivo (obligatorio, tipos permitidos, <16MB)
   - Palabras clave (opcional, <500 caracteres)
3. Sistema valida datos y archivo
4. Sistema genera nombre seguro para el archivo
5. Sistema guarda archivo en filesystem
6. Sistema guarda metadatos en base de datos
7. Sistema muestra confirmación de éxito

**Flujos Alternativos**:
- 3a. Validación falla: Sistema muestra errores específicos
- 4a. Nombre duplicado: Sistema añade sufijo numérico
- 5a. Error de escritura: Sistema muestra error y limpia parcialmente

**Postcondiciones**: Archivo disponible para búsqueda pública

### **UC002: Buscar Archivo (Usuario Público)**

**Actor**: Usuario Público
**Precondiciones**: Ninguna
**Flujo Principal**:
1. Usuario accede a la página principal
2. Introduce términos de búsqueda en el campo
3. Sistema busca en título, descripción y palabras clave
4. Sistema muestra resultados paginados con:
   - Título del archivo
   - Descripción truncada
   - Tipo de archivo (ícono)
   - Fecha de subida
   - Tamaño
5. Usuario puede paginar o refinar búsqueda

**Flujos Alternativos**:
- 3a. Sin resultados: Sistema muestra mensaje apropiado
- 3b. Error de búsqueda: Sistema muestra error genérico

**Postcondiciones**: Usuario puede acceder a archivos de interés

### **UC003: Ver Detalles de Archivo**

**Actor**: Usuario Público
**Precondiciones**: Archivo existe en el sistema
**Flujo Principal**:
1. Usuario hace clic en "Ver Detalles" desde lista o búsqueda
2. Sistema muestra página de detalles con:
   - Metadatos Dublin Core completos
   - Información técnica (tamaño, tipo, fecha)
   - Opción de descarga
3. Usuario puede descargar archivo o volver a la navegación

**Flujos Alternativos**:
- 1a. Archivo no existe: Sistema muestra error 404
- 3a. Archivo físico faltante: Sistema muestra advertencia

**Postcondiciones**: Usuario tiene acceso completo a metadatos e información

---

## 📊 **10. Métricas y KPIs**

### **10.1 Métricas de Adopción**

| Métrica | Objetivo Q4 2024 | Método de Medición |
|---------|------------------|--------------------|
| **Archivos subidos** | 1,000+ archivos | Conteo en BD |
| **Búsquedas realizadas** | 5,000+ búsquedas/mes | Logs de aplicación |
| **Usuarios activos** | 100+ usuarios únicos/mes | Analytics web |
| **Tiempo en sesión** | >5 minutos promedio | Analytics web |

### **10.2 Métricas de Rendimiento**

| Métrica | SLA | Medición Actual |
|---------|-----|-----------------|
| **Uptime** | 99.5% | 99.8% |
| **Tiempo de respuesta** | <2s | 1.2s promedio |
| **Error rate** | <1% | 0.3% |
| **Satisfacción usuario** | >4.5/5 | 4.7/5 (encuestas) |

### **10.3 Métricas de Seguridad**

| Métrica | Objetivo | Frecuencia |
|---------|----------|------------|
| **Intentos de login fallidos** | <10/día | Diaria |
| **Archivos maliciosos bloqueados** | 100% | Continua |
| **Vulnerabilidades críticas** | 0 | Semanal (scan) |
| **Tiempo de respuesta a incidentes** | <4 horas | Por incidente |

---

## 🔄 **11. Mantenimiento y Evolución**

### **11.1 Ciclo de Vida del Producto**

#### **Mantenimiento Correctivo**
- Bugs críticos: Corrección inmediata (<24h)
- Bugs menores: Corrección en próximo release
- Vulnerabilidades de seguridad: Corrección inmediata

#### **Mantenimiento Evolutivo**
- Nuevas características: Roadmap trimestral
- Mejoras de UX: Feedback continuo de usuarios
- Optimizaciones: Monitoreo de rendimiento mensual

#### **Mantenimiento Adaptativo**
- Actualizaciones de dependencias: Mensual
- Compatibilidad navegadores: Trimestral
- Cumplimiento normativo: Según requerimientos

### **11.2 Proceso de Release**

1. **Desarrollo** → Feature branches
2. **Testing** → Automated tests + manual QA
3. **Staging** → Deploy en ambiente de pruebas
4. **Validación** → User acceptance testing
5. **Producción** → Blue-green deployment
6. **Monitoreo** → Health checks + logs
7. **Rollback** → Plan de contingencia si falla

### **11.3 Documentación Requerida**

- [x] README.md con instrucciones de instalación
- [x] CLAUDE.md para desarrollo con AI
- [x] API documentation (futuro)
- [x] Deployment guide (docker/podman)
- [x] Security guidelines
- [ ] User manual
- [ ] Admin guide
- [ ] Troubleshooting guide

---

## 📞 **12. Contacto y Soporte**

### **12.1 Información del Producto**

| Campo | Información |
|-------|-------------|
| **Repositorio** | https://github.com/Gabo-araya/metadatos-app |
| **Demo en vivo** | http://metadatos.pythonanywhere.com/ |
| **Documentación** | /docs en el repositorio |
| **Issues/Bugs** | GitHub Issues |

### **12.2 Equipo de Desarrollo**

| Rol | Nombre | Contacto |
|-----|--------|----------|
| **Product Owner** | Gabriel Araya | [@Gabo-araya](https://github.com/Gabo-araya) |
| **Lead Developer** | Gabriel Araya | [LinkedIn](https://www.linkedin.com/in/gaboaraya/) |
| **DevOps** | Gabriel Araya | GitHub Issues |

### **12.3 Canales de Soporte**

1. **GitHub Issues** - Para bugs y feature requests
2. **Documentación** - Guías y troubleshooting
3. **Email** - Contacto directo para soporte enterprise

---

## 📋 **Anexos**

### **Anexo A: Glosario de Términos**

| Término | Definición |
|---------|------------|
| **Dublin Core** | Conjunto de elementos de metadatos para describir recursos digitales |
| **CSRF** | Cross-Site Request Forgery - ataque web |
| **Rate Limiting** | Técnica para limitar número de requests por tiempo |
| **WSGI** | Web Server Gateway Interface para Python |
| **Rootless Container** | Container que ejecuta sin privilegios de root |

### **Anexo B: Referencias**

- [Dublin Core Metadata Initiative](https://www.dublincore.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Documento actualizado**: Agosto 2024  
**Próxima revisión**: Noviembre 2024  
**Estado**: Activo - Implementación en progreso