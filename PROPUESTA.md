# PROPUESTA — INTERSERVIM AI SALES AGENT

## 1. Resumen del Proyecto

Plataforma Android (APK) con backend propio que funciona como agente comercial de IA para WhatsApp, especializado en importación y comercio internacional.

### Componentes desarrollados:

| Componente | Estado | Archivos |
|------------|--------|----------|
| Backend API (FastAPI + Python) | ✅ 100% operativo | 49 archivos .py |
| App Flutter (Android APK) | ✅ Código completo | 22 archivos .dart / 15 pantallas |
| Base de Datos (SQLite/PostgreSQL) | ✅ Modelos + Seed data | 14 tablas |
| Autenticación JWT + Roles | ✅ Verificado | ADMIN / MANAGER / SALES_AGENT / VIEWER |
| API REST (11 módulos) | ✅ Verificada | Auth, Products, CRM, Quotes, AI, WhatsApp, Marketing, Knowledge, Analytics, FollowUps |
| Documentación Técnica | ✅ Completa | 6 documentos en docs/ |
| Docker / Docker Compose | ✅ Configurado | PostgreSQL, Redis, API |

## 2. Próximo Paso: Compilar el APK

Para generar el archivo `.apk` se necesita el Flutter SDK completo (incluyendo Dart SDK). Desde esta red no es posible descargar los binarios de Google (bloqueo 403).

### Opción A — GitHub Actions (Automático, recomendado)

**Pipeline ya configurado** en `.github/workflows/build_apk.yml`:
1. Al hacer push a `main`, GitHub ejecuta el workflow
2. GitHub descarga Flutter SDK (sin restricciones de red)
3. Compila el APK y AppBundle automáticamente
4. El APK queda como artefacto descargable

**Pasos para activarlo:**
```bash
# 1. Crear repositorio en github.com
# 2. Autenticar gh CLI:
echo "TU_TOKEN" | gh auth login --with-token
# 3. Crear repo y subir:
gh repo create interservim-ai --public --push --source=.
# 4. Ir a: https://github.com/tu-usuario/interservim-ai/actions
# 5. Descargar APK de los artifacts
```

### Opción B — Build local en otra PC

```bash
# En una PC sin restricciones de red:
flutter pub get
flutter build apk --release
# APK generado en: build/app/outputs/flutter-apk/app-release.apk
```

### Opción C — Codemagic.io (Cloud gratis)

1. Subir código a GitHub
2. Ir a https://codemagic.io
3. Conectar repositorio
4. Build → APK descargable

## 3. Requisitos para usar GitHub Actions

| Elemento | Detalle |
|----------|---------|
| Token GitHub | Crear en https://github.com/settings/tokens (scopes: repo, workflow) |
| Repositorio | Crear en github.com (público o privado) |
| gh CLI | ✅ Instalado |
| Git | ✅ Instalado |

## 4. Flujo completo del producto

```
Cliente WhatsApp
    ↓
Webhook → Backend → Guardar mensaje
    ↓
Clasificar Intención (IA)
    ↓
Consultar Productos (DB)
    ↓
Generar Respuesta (OpenAI/GPT)
    ↓
Actualizar Cliente + Etapa Venta
    ↓
Enviar Respuesta WhatsApp
    ↓
¿Solicitó cotización? → Generar PDF
¿Solicitó humano? → Handoff a agente
¿No respondió? → Seguimiento automático
```

## 5. Datos de prueba incluidos

| Entidad | Cantidad | Detalle |
|---------|----------|---------|
| Usuarios | 2 | admin@interservim.com / manager@interservim.com |
| Productos | 5 | Arroz, Azúcar, Maíz, Frijol (con precios reales FOB) |
| Categorías | 1 | Granos |

## 6. Próximos pasos sugeridos

1. Crear cuenta en GitHub (si no tiene)
2. Generar token de acceso
3. Ejecutar comandos de subida
4. Esperar 5-10 min a que GitHub Actions compile el APK
5. Descargar e instalar el APK

## 7. Contacto para soporte técnico

¿Desea continuar con la subida a GitHub o necesita ajustes adicionales en el código antes de compilar?
