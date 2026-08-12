# Sistema de Gestión de Préstamo de Herramientas Comunitarias

Este programa de consola en Python permite a la junta comunal registrar herramientas, usuarios y controlar el proceso de préstamos para garantizar el buen uso, disponibilidad y seguimiento de los recursos del barrio.

---

## Estado Actual de Cumplimiento de Requerimientos

La documentación formal del estado de avance, métricas y matriz de cumplimiento de los requerimientos de la junta comunal se encuentra disponible en el informe PDF subido al repositorio (`Informe_Cumplimiento_Requerimientos.pdf`).

### Resumen de Módulos Implementados:
- **Gestión de Herramientas:** CRUD completo con atributos de `id`, `nombre`, `categoría`, `cantidad`, `estado` (`activa`, `en reparación`, `fuera de servicio`, `inactiva`) y `valor`.
- **Gestión de Usuarios:** Roles diferenciados para **Administrador** y **Residente** con control de acceso por ID.
- **Gestión de Préstamos:** Control de stock automático en registros y devoluciones, fechas estimadas y observaciones.
- **Consultas y Reportes:** Filtros de stock bajo (< 3 unidades), préstamos vencidos, historial por usuario y rankings de uso.
- **Auditoría y Persistencia:** Guardado automático en archivos JSON y registro de eventos/errores en `app.log`.

---

## Estructura del Proyecto

```text
proyecto_01/
│
├── main.py                             # Punto de entrada principal e interfaz del sistema
├── usuarios.py                         # Módulo para el CRUD de usuarios
├── gestion_herramientas.py             # Módulo para la gestión del catálogo de herramientas
├── prestamos.py                        # Módulo de préstamos, devoluciones y reportes
├── persistence.py                      # Módulo de lectura/escritura de archivos JSON
├── logger.py                           # Módulo para el registro de eventos en logs
│
├── usuarios.json                       # Almacenamiento de usuarios
├── herramientas.json                   # Almacenamiento de herramientas
├── prestamos.json                      # Almacenamiento de préstamos
├── app.log                             # Registro de auditoría y errores
└──  Informe_Cumplimiento_Requerimientos.pdf # Documento de cumplimiento entregado
```
---
## Requisitos e Instalación

* **Lenguaje:** Python 3.10 o superior.
* **Librerías:** No requiere librerías externas (utiliza módulos estándar: `json`, `os`, `datetime`).

## Instrucciones de Ejecución

1. Abre la terminal o consola de comandos en la carpeta raíz del proyecto (`proyecto_01`).
2. Ejecuta el archivo principal con el siguiente comando:

```bash
python main.py
```
---
## Roles y Funcionalidades

### 1. Administrador

* **Gestión de Usuarios:** Crear, listar, buscar, actualizar datos y eliminar usuarios.
* **Gestión de Herramientas:** Registrar herramientas, modificar stock, valor estimado y estados (`activa`, `en reparación`, `fuera de servicio`, `inactiva`).
* **Gestión de Préstamos:** Registrar solicitudes de préstamo y procesar devoluciones actualizando el inventario automáticamente.
* **Consultas y Reportes:**
  * Herramientas con stock bajo (< 3 unidades).
  * Préstamos activos y vencidos.
  * Historial de préstamos de un usuario.
  * Ranking de herramientas más solicitadas.
  * Ranking de usuarios que más herramientas solicitan.
### 2. Residente

* **Consultar Catálogo:** Ver herramientas activas disponibles en inventario.
* **Solicitar Préstamo:** Crear solicitudes de herramientas.
* **Mis Préstamos:** Consultar el historial y estado de sus préstamos.
---
## Registro de Eventos (`app.log`)

Cualquier operación crítica o fallo (intento de préstamo con stock insuficiente, error en ingreso de datos, IDs duplicados o registros exitosos) se almacena de forma automática con fecha y hora en el archivo `app.log`.
### Pasos para guardarlo y subirlo a GitHub:

1. Reemplaza el texto en tu archivo `README.md` en VS Code y presiona **`Ctrl + S`**.
2. Sube los cambios desde la terminal con:
   ```bash
   git add README.md
   git commit -m "Actualización del README con sección de informe de cumplimiento en PDF"
   git push origin main
   ```
