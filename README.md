# INTERSERVIM AI SALES AGENT

Plataforma Android de agente comercial de inteligencia artificial para WhatsApp, especializada en importación y comercio internacional.

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Mobile App | Flutter 3.x + Dart |
| Backend API | Python 3.12 + FastAPI |
| Base de Datos | PostgreSQL 15 (SQLite para desarrollo) |
| Cache/Queue | Redis 7 |
| Autenticación | JWT (Access + Refresh Tokens) |
| AI Engine | OpenAI / Anthropic (configurable) |
| WhatsApp | Meta Cloud API (oficial) |
| Contenedores | Docker + Docker Compose |

## Estructura del Proyecto

```
interservim-ai/
├── apps/
│   ├── mobile/flutter_app/     # Aplicación Flutter (Android APK)
│   └── backend/api/            # API REST con FastAPI
├── packages/
│   ├── shared_models/          # Modelos compartidos
│   ├── shared_constants/       # Constantes compartidas
│   └── shared_utils/           # Utilidades compartidas
├── infrastructure/
│   ├── docker/                 # Configuraciones Docker
│   ├── database/               # Scripts SQL iniciales
│   └── deployment/             # Configuración de despliegue
├── docs/                       # Documentación técnica
├── tests/                      # Pruebas
├── .env.example                # Variables de entorno de ejemplo
├── docker-compose.yml          # Orquestación Docker
└── setup.ps1                   # Script de instalación
```

## Requisitos

- Python 3.12+
- Flutter SDK 3.x
- Docker Desktop (opcional, para PostgreSQL/Redis)
- Android Studio + Android SDK (para build APK)

## Instalación y Desarrollo

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd interservim-ai
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus claves API y configuraciones
```

### 3. Backend (API)

```bash
cd apps/backend/api
pip install -r requirements.txt
python seed.py           # Poblar base de datos con datos iniciales
python -m uvicorn app.main:app --reload
```

La API estará disponible en: http://localhost:8000
Documentación Swagger: http://localhost:8000/docs

### 4. Frontend (Flutter)

```bash
cd apps/mobile/flutter_app
flutter pub get
flutter run              # Para ejecutar en dispositivo/emulador
flutter build apk        # Para generar APK
```

### 5. Docker (Producción)

```bash
docker-compose up -d
```

## Credenciales por Defecto (Desarrollo)

| Rol | Email | Contraseña |
|-----|-------|------------|
| ADMIN | admin@interservim.com | Admin123! |
| MANAGER | manager@interservim.com | Manager123! |

## Productos Semilla

- Arroz Blanco Premium - $450 USD/Ton (Vietnam)
- Arroz Blanco Estándar - $380 USD/Ton (Tailandia)
- Azúcar Refinada - $380 USD/Ton (Brasil)
- Maíz Amarillo - $320 USD/Ton (Estados Unidos)
- Frijol Negro - $550 USD/Ton (Uganda)

## Documentación

- [Arquitectura](docs/ARCHITECTURE.md)
- [Base de Datos](docs/DATABASE.md)
- [API Reference](docs/API.md)
- [Agente IA](docs/AI_AGENT.md)
- [Seguridad](docs/SECURITY.md)
- [Roadmap](docs/ROADMAP.md)

## Licencia

Proyecto privado - InterServim-SL
