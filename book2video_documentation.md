# 📚 Documentação Completa - Book2Video

## 📖 Índice

1. [Visão Geral do Projeto](#-visão-geral-do-projeto)
2. [Arquitetura do Sistema](#-arquitetura-do-sistema)
3. [Guia de Instalação](#-guia-de-instalação)
4. [Documentação da API](#-documentação-da-api)
5. [Guia do Desenvolvedor](#-guia-do-desenvolvedor)
6. [Documentação do Frontend](#-documentação-do-frontend)
7. [Pipeline de Processamento](#-pipeline-de-processamento)
8. [Banco de Dados](#-banco-de-dados)
9. [Deployment](#-deployment)
10. [Testes](#-testes)
11. [Monitoring](#-monitoring)
12. [Segurança](#-segurança)
13. [Troubleshooting](#-troubleshooting)

---

## 🎯 Visão Geral do Projeto

### Descrição
Book2Video é uma plataforma SaaS que transforma livros (PDF, TXT, EPUB, MP3) em vídeos narrados automaticamente usando IA. O sistema processa o conteúdo, gera resumos, cria imagens para cada cena e produz narração profissional.

### Objetivos de Negócio
- **Democratizar o acesso ao conteúdo**: Tornar livros acessíveis através de vídeos
- **Economizar tempo**: Consumir livros em formato resumido
- **Experiência visual**: Combinar texto, imagem e áudio
- **Monetização**: Modelo freemium com planos pagos

### Público-Alvo
- Estudantes e profissionais com pouco tempo
- Pessoas com dificuldades de leitura
- Criadores de conteúdo educativo
- Instituições de ensino

### Proposta de Valor
```
Input: Livro (qualquer formato)
↓
Processamento: IA (GPT-4 + DALL-E + ElevenLabs)
↓
Output: Vídeo profissional (MP4, 720p/1080p)
```

---

## 🏗️ Arquitetura do Sistema

### Visão de Alto Nível

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web App - Next.js]
        B[Mobile App - React Native]
    end
    
    subgraph "API Gateway"
        C[Load Balancer]
        D[Rate Limiter]
        E[Authentication]
    end
    
    subgraph "Application Layer"
        F[FastAPI Backend]
        G[Worker Nodes - Celery]
        H[File Processor]
    end
    
    subgraph "AI Services"
        I[OpenAI GPT-4]
        J[DALL-E 3]
        K[ElevenLabs TTS]
        L[Whisper STT]
    end
    
    subgraph "Data Layer"
        M[PostgreSQL]
        N[Redis Cache]
        O[S3 Storage]
    end
    
    subgraph "Infrastructure"
        P[Docker Containers]
        Q[Railway/Fly.io]
        R[CloudFlare CDN]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    H --> J
    H --> K
    H --> L
    F --> M
    F --> N
    F --> O
    P --> Q
    O --> R
```

### Componentes Principais

#### 1. **Frontend (Next.js)**
- Interface do usuário responsiva
- Upload de arquivos com drag & drop
- Monitoramento de progresso em tempo real
- Player de vídeo integrado
- Dashboard de usuário

#### 2. **Backend (FastAPI)**
- API RESTful assíncrona
- Autenticação JWT
- Validação de dados com Pydantic
- Rate limiting por usuário
- Logging estruturado

#### 3. **Workers (Celery)**
- Processamento assíncrono
- Queue distribuída
- Retry automático
- Monitoramento de tarefas
- Escalabilidade horizontal

#### 4. **Storage**
- **PostgreSQL**: Metadados, usuários, projetos
- **Redis**: Cache, sessions, message broker
- **S3**: Arquivos, imagens, vídeos
- **CDN**: Entrega de conteúdo global

---

## 🛠️ Guia de Instalação

### Pré-requisitos

```bash
# Requisitos de sistema
- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
- FFmpeg

# APIs necessárias
- OpenAI API Key
- ElevenLabs API Key
- AWS S3 Credentials (ou CloudFlare R2)
```

### Instalação Local

#### 1. **Clone do Repositório**
```bash
git clone https://github.com/seu-usuario/book2video.git
cd book2video
```

#### 2. **Setup do Backend**
```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Setup do banco de dados
alembic upgrade head

# Variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves de API
```

#### 3. **Setup do Frontend**
```bash
cd frontend

# Instalar dependências
npm install

# Variáveis de ambiente
cp .env.local.example .env.local
# Configurar NEXT_PUBLIC_API_URL
```

#### 4. **Inicialização com Docker**
```bash
# Na raiz do projeto
docker-compose up -d

# Verificar status
docker-compose ps
```

### Configuração das Variáveis de Ambiente

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/book2video
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...

# Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_BUCKET_NAME=book2video-storage
AWS_REGION=us-east-1

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Celery
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379

# Environment
ENVIRONMENT=development
DEBUG=True
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

---

## 📡 Documentação da API

### Base URL
```
Production: https://api.book2video.com
Development: http://localhost:8000
```

### Autenticação
Todas as rotas protegidas requerem JWT token no header:
```bash
Authorization: Bearer <token>
```

### Endpoints Principais

#### **Authentication**

##### POST /auth/register
Cadastro de novo usuário.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "João Silva"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "João Silva",
    "subscription_tier": "free"
  }
}
```

##### POST /auth/login
Login do usuário.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "João Silva"
  }
}
```

#### **Projects**

##### POST /projects/upload
Upload de arquivo para processamento.

**Request (multipart/form-data):**
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -F "file=@book.pdf" \
  -F "duration=5" \
  -F "style=default" \
  -F "voice_id=rachel" \
  http://localhost:8000/projects/upload
```

**Response:**
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "uploaded",
  "message": "File uploaded successfully",
  "estimated_processing_time": 300
}
```

##### POST /projects/{project_id}/process
Iniciar processamento do projeto.

**Response:**
```json
{
  "task_id": "celery-task-id",
  "status": "processing",
  "estimated_completion": "2024-01-15T10:30:00Z"
}
```

##### GET /projects/{project_id}/status
Verificar status do processamento.

**Response:**
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 65,
  "current_step": "generating_audio",
  "steps": {
    "parsing": "completed",
    "summarizing": "completed", 
    "generating_images": "completed",
    "generating_audio": "in_progress",
    "creating_video": "pending"
  },
  "estimated_completion": "2024-01-15T10:25:00Z"
}
```

##### GET /projects/{project_id}/result
Obter resultado final.

**Response:**
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "video_url": "https://cdn.book2video.com/videos/project-id.mp4",
  "thumbnail_url": "https://cdn.book2video.com/thumbnails/project-id.jpg",
  "duration_seconds": 300,
  "file_size_mb": 45.2,
  "scenes_count": 12,
  "processing_time_seconds": 420,
  "cost_dollars": 3.45
}
```

##### GET /projects
Listar projetos do usuário.

**Query Parameters:**
- `page`: Número da página (default: 1)
- `limit`: Itens por página (default: 10)
- `status`: Filtrar por status (optional)

**Response:**
```json
{
  "projects": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "O Pequeno Príncipe",
      "status": "completed",
      "created_at": "2024-01-15T09:00:00Z",
      "duration_minutes": 5,
      "thumbnail_url": "https://cdn.book2video.com/thumbnails/project-id.jpg"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 3,
    "total_items": 25,
    "has_next": true,
    "has_prev": false
  }
}
```

#### **User Management**

##### GET /users/me
Obter dados do usuário atual.

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "João Silva",
  "subscription_tier": "pro",
  "usage_stats": {
    "videos_this_month": 8,
    "monthly_limit": 10,
    "total_videos": 45,
    "total_minutes_processed": 225
  },
  "created_at": "2024-01-01T00:00:00Z"
}
```

##### PUT /users/me
Atualizar dados do usuário.

**Request:**
```json
{
  "name": "João da Silva",
  "preferences": {
    "default_voice": "rachel",
    "default_style": "educational",
    "email_notifications": true
  }
}
```

#### **Subscription**

##### GET /subscription/plans
Listar planos disponíveis.

**Response:**
```json
{
  "plans": [
    {
      "id": "free",
      "name": "Gratuito",
      "price_monthly": 0,
      "features": {
        "videos_per_month": 1,
        "max_duration_minutes": 5,
        "watermark": true,
        "priority_processing": false
      }
    },
    {
      "id": "pro",
      "name": "Profissional",
      "price_monthly": 9.99,
      "features": {
        "videos_per_month": 10,
        "max_duration_minutes": 20,
        "watermark": false,
        "priority_processing": true,
        "custom_voices": true
      }
    }
  ]
}
```

### Códigos de Erro

| Código | Descrição |
|--------|-----------|
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Token inválido |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Recurso não encontrado |
| 422 | Unprocessable Entity - Validação falhou |
| 429 | Too Many Requests - Rate limit excedido |
| 500 | Internal Server Error - Erro interno |

### Rate Limits

| Endpoint | Limite |
|----------|---------|
| POST /auth/login | 5 req/min |
| POST /projects/upload | 2 req/min (free), 10 req/min (pro) |
| GET /projects/*/status | 30 req/min |
| API geral | 100 req/min |

---

## 👨‍💻 Guia do Desenvolvedor

### Estrutura do Projeto

```
book2video/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── config.py               # Configurações
│   │   ├── dependencies.py         # Dependências DI
│   │   ├── database.py             # Conexão DB
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   └── subscription.py
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   └── auth.py
│   │   ├── routes/                 # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   ├── users.py
│   │   │   └── subscriptions.py
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── project_service.py
│   │   │   ├── ai_service.py
│   │   │   └── storage_service.py
│   │   ├── workers/                # Celery tasks
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   ├── video_processor.py
│   │   │   └── ai_tasks.py
│   │   └── utils/                  # Utilities
│   │       ├── __init__.py
│   │       ├── file_parser.py
│   │       ├── video_editor.py
│   │       └── helpers.py
│   ├── tests/                      # Testes
│   ├── alembic/                    # Database migrations
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js 14 App Router
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── projects/
│   │   │   └── api/
│   │   ├── components/             # React components
│   │   │   ├── ui/                 # shadcn/ui
│   │   │   ├── forms/
│   │   │   ├── layout/
│   │   │   └── project/
│   │   ├── lib/                    # Utilities
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   ├── utils.ts
│   │   │   └── validations.ts
│   │   ├── stores/                 # Zustand stores
│   │   │   ├── auth.ts
│   │   │   ├── projects.ts
│   │   │   └── ui.ts
│   │   └── types/                  # TypeScript types
│   │       ├── api.ts
│   │       ├── user.ts
│   │       └── project.ts
│   ├── public/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── tsconfig.json
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       └── frontend-ci.yml
├── docs/
└── README.md
```

### Padrões de Código

#### **Backend (Python)**

##### Configuração
```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    redis_url: str
    
    # AI Services
    openai_api_key: str
    elevenlabs_api_key: str
    
    # Storage
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket_name: str
    aws_region: str = "us-east-1"
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Environment
    environment: str = "development"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

##### Models (SQLAlchemy)
```python
# app/models/project.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class VideoProject(Base):
    __tablename__ = "video_projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    style = Column(String(50), default="default")
    voice_id = Column(String(100), default="default")
    status = Column(String(50), default="pending")
    processing_progress = Column(Integer, default=0)
    result_url = Column(String(500))
    error_message = Column(Text)
    cost_dollars = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "progress": self.processing_progress,
            "duration_minutes": self.duration_minutes,
            "created_at": self.created_at.isoformat(),
            "result_url": self.result_url
        }
```

##### Schemas (Pydantic)
```python
# app/schemas/project.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict
from enum import Enum

class ProjectStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    duration_minutes: int = Field(..., ge=1, le=60)
    style: str = Field(default="default")
    voice_id: str = Field(default="default")

class ProjectResponse(BaseModel):
    id: str
    title: str
    status: ProjectStatus
    progress: int = Field(ge=0, le=100)
    duration_minutes: int
    created_at: datetime
    result_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class ProjectStatusUpdate(BaseModel):
    status: ProjectStatus
    progress: int
    current_step: str
    steps: Dict[str, str]
    estimated_completion: Optional[datetime] = None
```

##### Services
```python
# app/services/project_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import VideoProject
from app.schemas.project import ProjectCreate, ProjectResponse
from app.workers.video_processor import process_book_to_video
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_project(
        self, 
        user_id: int, 
        project_data: ProjectCreate,
        file_path: str,
        filename: str
    ) -> VideoProject:
        project = VideoProject(
            user_id=user_id,
            title=project_data.title,
            original_filename=filename,
            file_path=file_path,
            duration_minutes=project_data.duration_minutes,
            style=project_data.style,
            voice_id=project_data.voice_id
        )
        
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        
        logger.info(f"Project created: {project.id} for user {user_id}")
        return project
    
    async def start_processing(self, project_id: str) -> str:
        # Start Celery task
        task = process_book_to_video.delay(project_id)
        
        # Update project status
        project = await self.get_project(project_id)
        project.status = "processing"
        await self.db.commit()
        
        logger.info(f"Processing started for project {project_id}, task: {task.id}")
        return task.id
    
    async def get_project(self, project_id: str) -> Optional[VideoProject]:
        stmt = select(VideoProject).where(VideoProject.id == project_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_projects(
        self, 
        user_id: int, 
        page: int = 1, 
        limit: int = 10
    ) -> List[VideoProject]:
        offset = (page - 1) * limit
        stmt = (
            select(VideoProject)
            .where(VideoProject.user_id == user_id)
            .order_by(VideoProject.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
```

#### **Frontend (TypeScript/React)**

##### API Client
```typescript
// lib/api.ts
import axios, { AxiosResponse } from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

// Request interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor para tratar erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/auth/login'
    }
    return Promise.reject(error)
  }
)

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    current_page: number
    total_pages: number
    total_items: number
    has_next: boolean
    has_prev: boolean
  }
}
```

##### Types
```typescript
// types/project.ts
export enum ProjectStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export interface Project {
  id: string
  title: string
  status: ProjectStatus
  progress: number
  duration_minutes: number
  created_at: string
  result_url?: string
  thumbnail_url?: string
  error_message?: string
}

export interface ProjectCreate {
  title: string
  duration_minutes: number
  style?: string
  voice_id?: string
}

export interface ProcessingStatus {
  project_id: string
  status: ProjectStatus
  progress: number
  current_step: string
  steps: Record<string, string>
  estimated_completion?: string
}
```

##### Stores (Zustand)
```typescript
// stores/projects.ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { Project, ProjectCreate, ProcessingStatus } from '@/types/project'
import { projectsApi } from '@/lib/api/projects'

interface ProjectsState {
  projects: Project[]
  currentProject: Project | null
  processingStatus: ProcessingStatus | null
  isLoading: boolean
  error: string | null
  
  // Actions
  fetchProjects: () => Promise<void>
  createProject: (data: ProjectCreate, file: File) => Promise<string>
  startProcessing: (projectId: string) => Promise<void>
  checkProcessingStatus: (projectId: string) => Promise<void>
  setCurrentProject: (project: Project | null) => void
  clearError: () => void
}

export const useProjectsStore = create<ProjectsState>()(
  devtools(
    (set, get) => ({
      projects: [],
      currentProject: null,
      processingStatus: null,
      isLoading: false,
      error: null,
      
      fetchProjects: async () => {
        set({ isLoading: true, error: null })
        try {
          const projects = await projectsApi.getProjects()
          set({ projects, isLoading: false })
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Erro ao carregar projetos',
            isLoading: false 
          })
        }
      },
      
      createProject: async (data: ProjectCreate, file: File): Promise<string> => {
        set({ isLoading: true, error: null })
        try {
          const projectId = await projectsApi.uploadProject(data, file)
          await get().fetchProjects() // Refresh list
          set({ isLoading: false })
          return projectId
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Erro ao criar projeto',
            isLoading: false 
          })
          throw error
        }
      },
      
      checkProcessingStatus: async (projectId: string) => {
        try {
          const status = await projectsApi.getProcessingStatus(projectId)
          set({ processingStatus: status })
          
          // Update project in list if completed
          if (status.status === 'completed' || status.status === 'failed') {
            await get().fetchProjects()
          }
        } catch (error) {
          console.error('Erro ao verificar status:', error)
        }
      },
      
      setCurrentProject: (project) => set({ currentProject: project }),
      clearError: () => set({ error: null })
    }),
    { name: 'projects-store' }
  )
)
```

##### Components
```typescript
// components/project/ProjectUpload.tsx
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useProjectsStore } from '@/stores/projects'
import { FileUpload } from './FileUpload'

const projectSchema = z.object({
  title: z.string().min(1, 'Título é obrigatório').max(255, 'Título muito longo'),
  duration_minutes: z.number().min(1, 'Mínimo 1 minuto').max(60, 'Máximo 60 minutos'),
  style: z.string().default('default'),
  voice_id: z.string().default('rachel')
})

type ProjectFormData = z.infer<typeof projectSchema>

export function ProjectUpload() {
  const [file, setFile] = useState<File | null>(null)
  const { createProject, isLoading, error } = useProjectsStore()
  
  const form = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      title: '',
      duration_minutes: 5,
      style: 'default',
      voice_id: 'rachel'
    }
  })
  
  const onSubmit = async (data: ProjectFormData) => {
    if (!file) {
      form.setError('root', { message: 'Selecione um arquivo' })
      return
    }
    
    try {
      const projectId = await createProject(data, file)
      // Redirect to processing page
      window.location.href = `/projects/${projectId}`
    } catch (error) {
      console.error('Erro ao criar projeto:', error)
    }
  }
  
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Novo Projeto</h1>
      
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FileUpload onFileSelect={setFile} selectedFile={file} />
        
        <div>
          <label className="block text-sm font-medium mb-2">
            Título do Projeto
          </label>
          <Input
            {...form.register('title')}
            placeholder="Ex: O Pequeno Príncipe - Resumo"
          />
          {form.formState.errors.title && (
            <p className="text-red-500 text-sm mt-1">
              {form.formState.errors.title.message}
            </p>
          )}
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">
            Duração do Vídeo (minutos)
          </label>
          <Select
            value={form.watch('duration_minutes').toString()}
            onValueChange={(value) => form.setValue('duration_minutes', parseInt(value))}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1">1 minuto</SelectItem>
              <SelectItem value="3">3 minutos</SelectItem>
              <SelectItem value="5">5 minutos</SelectItem>
              <SelectItem value="10">10 minutos</SelectItem>
              <SelectItem value="20">20 minutos</SelectItem>
            </SelectContent>
          </Select>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Estilo Visual
            </label>
            <Select
              value={form.watch('style')}
              onValueChange={(value) => form.setValue('style', value)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="default">Padrão</SelectItem>
                <SelectItem value="cartoon">Cartoon</SelectItem>
                <SelectItem value="realistic">Realista</SelectItem>
                <SelectItem value="educational">Educacional</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">
              Voz da Narração
            </label>
            <Select
              value={form.watch('voice_id')}
              onValueChange={(value) => form.setValue('voice_id', value)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="rachel">Rachel (Feminina)</SelectItem>
                <SelectItem value="adam">Adam (Masculina)</SelectItem>
                <SelectItem value="bella">Bella (Jovem)</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}
        
        <Button 
          type="submit" 
          disabled={isLoading || !file}
          className="w-full"
        >
          {isLoading ? 'Criando Projeto...' : 'Criar Vídeo'}
        </Button>
      </form>
    </div>
  )
}
```

---

## 🎬 Pipeline de Processamento

### Fluxo Completo

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Worker
    participant AI Services
    participant Storage

    User->>Frontend: Upload arquivo
    Frontend->>API: POST /projects/upload
    API->>Storage: Salvar arquivo
    API->>Worker: Queue processing task
    API-->>Frontend: Project ID + Task ID
    
    Worker->>Worker: Parse arquivo (PDF/TXT/EPUB/MP3)
    Worker->>AI Services: Gerar resumo (GPT-4)
    Worker->>AI Services: Gerar prompts de imagem
    Worker->>AI Services: Gerar imagens (DALL-E)
    Worker->>AI Services: Gerar narração (ElevenLabs)
    Worker->>Worker: Montar vídeo (FFmpeg)
    Worker->>Storage: Salvar vídeo final
    Worker->>API: Update status = completed
    
    Frontend->>API: Poll status (WebSocket/HTTP)
    API-->>Frontend: Status updates
    Frontend->>User: Mostrar vídeo pronto
```

### Implementação dos Workers

#### Celery Configuration
```python
# workers/celery_app.py
from celery import Celery
from app.config import settings
import os

# Celery app configuration
celery_app = Celery(
    "book2video",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=['app.workers.video_processor']
)

# Configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    worker_send_task_events=True,
    task_send_sent_event=True,
    result_expires=3600,
    task_compression='gzip',
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
)

# Task routing
celery_app.conf.task_routes = {
    'app.workers.video_processor.*': {'queue': 'video_processing'},
    'app.workers.ai_tasks.*': {'queue': 'ai_processing'},
}
```

#### Main Processing Pipeline
```python
# workers/video_processor.py
from celery import current_task
from app.workers.celery_app import celery_app
from app.services.ai_service import AIService
from app.services.storage_service import StorageService
from app.utils.file_parser import FileParser
from app.utils.video_editor import VideoEditor
from app.database import get_db
from app.models.project import VideoProject
import logging
import asyncio

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_book_to_video(self, project_id: str):
    """
    Main task para processar um livro em vídeo
    """
    try:
        # Update task status
        self.update_state(
            state='PROGRESS',
            meta={
                'step': 'initializing',
                'progress': 0,
                'message': 'Iniciando processamento...'
            }
        )
        
        # Get project from database
        db = next(get_db())
        project = db.query(VideoProject).filter(VideoProject.id == project_id).first()
        
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Initialize services
        ai_service = AIService()
        storage_service = StorageService()
        file_parser = FileParser()
        video_editor = VideoEditor()
        
        # Step 1: Parse file
        self.update_state(
            state='PROGRESS',
            meta={
                'step': 'parsing',
                'progress': 10,
                'message': 'Extraindo texto do arquivo...'
            }
        )
        
        content = file_parser.parse_file(project.file_path)
        
        # Step 2: Generate summary
        self.update_state(
            state='PROGRESS',
            meta={
                'step': 'summarizing',
                'progress': 25,
                'message': 'Gerando resumo com IA...'
            }
        )
        
        summary_data = asyncio.run(
            ai_service.generate_summary(content, project.duration_minutes)
        )
        scenes = summary_data['scenes']
        
        # Step 3: Generate images
        self.update_state(
            state='PROGRESS',
            meta={
                'step': 'generating_images',
                'progress': 40,
                'message': f'Gerando {len(scenes)} imagens...'
            }
        )
        
        image_tasks = []
        for i, scene in enumerate(scenes):
            image_url = asyncio.run(
                ai_service.generate_scene_image(scene['description'])
            )
            scenes[i]['image_url'] = image_url
            
            # Update progress for each image
            progress = 40 + (i + 1) * (25 / len(scenes))
            self.update_state(
                state='PROGRESS',
                meta={
                    'step': 'generating_images',
                    'progress': int(progress),
                    'message': f'Imagem {i+1}/{len(scenes)} concluída'
                }
            )
        
        # Step 4: Generate audio narration
        self.update_state(
            state='PROGRESS',
            meta={
                'step': 'generating_audio',
                'progress': 65,
                'message': 'Gerando narração...'
            }
        )
        
        for i, scene in enumerate(scenes):
            audio_data = asyncio.run(
                ai_service.generate_narration(scene['text'], project.voice_id)
            )
            
            # Save audio file
            audio_path = f"temp/audio_{project_id}_{i}.mp3"
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
            
            scenes[i]['audio_path'] = audio_path
            
            # Update progress
            progress = 65 + (i + 1) * (15 / len(scenes))
            self.update_state(
                state='PROGRESS',
                meta={
                    'step': 'generating_audio',
                    'progress': int(progress),
                    'message': f'Narração {i+1}/{len(scenes)} concluída'
                }
            )
        
        # Step 5: Create video
        self.update_state(
            state='PROGRESS',
            meta={
                'step': 'creating_video',
                'progress': 80,
                'message': 'Montando vídeo final...'
            }
        )
        
        video_path = video_editor.create_video(scenes, project_id)
        
        # Step 6: Upload to storage
        self.update_state(
            state='PROGRESS',
            meta={
                'step': 'uploading',
                'progress': 90,
                'message': 'Fazendo upload do vídeo...'
            }
        )
        
        video_url = storage_service.upload_video(video_path, project_id)
        
        # Step 7: Update database
        project.status = 'completed'
        project.result_url = video_url
        project.processing_progress = 100
        db.commit()
        
        # Cleanup temporary files
        video_editor.cleanup_temp_files(project_id)
        
        return {
            'status': 'SUCCESS',
            'project_id': project_id,
            'video_url': video_url,
            'message': 'Vídeo criado com sucesso!'
        }
        
    except Exception as exc:
        logger.error(f"Error processing project {project_id}: {str(exc)}")
        
        # Update project status as failed
        try:
            project.status = 'failed'
            project.error_message = str(exc)
            db.commit()
        except:
            pass
        
        # Retry logic
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying task {self.request.id}, attempt {self.request.retries + 1}")
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        
        raise exc
```

#### AI Services Integration
```python
# services/ai_service.py
import openai
from elevenlabs import generate, Voice, VoiceSettings
import asyncio
import httpx
from typing import Dict, List
import json
import hashlib
from app.config import settings
from app.services.storage_service import StorageService

class AIService:
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self.storage = StorageService()
    
    async def generate_summary(self, content: str, duration_minutes: int) -> Dict:
        """
        Gera resumo estruturado do conteúdo
        """
        word_count = duration_minutes * 120  # 120 palavras por minuto
        scenes_count = max(1, duration_minutes // 2)  # 1 cena a cada 2 minutos
        
        prompt = f"""
        Você é um roteirista especializado em adaptar livros para vídeos curtos.
        
        Tarefas:
        1. Resuma o conteúdo em aproximadamente {word_count} palavras
        2. Divida em {scenes_count} cenas equilibradas
        3. Para cada cena, crie:
           - Texto narrativo (2-3 frases)
           - Descrição visual detalhada para geração de imagem
        
        Retorne em formato JSON:
        {{
            "title": "título da história",
            "scenes": [
                {{
                    "scene_number": 1,
                    "text": "texto da narração",
                    "description": "descrição visual detalhada",
                    "duration_estimate": "duração estimada em segundos"
                }}
            ]
        }}
        
        Conteúdo original:
        {content[:8000]}  # Limit content size
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "Você é um roteirista especializado."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=200