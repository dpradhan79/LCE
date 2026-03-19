# Learn Challenge & Evolve — Full Stack Architecture

## Folder Structure

```
lce/                                              # project root (Learn Challenge & Evolve)
├── docker-compose.yml                            # all services wired together
├── pyproject.toml                                # Python deps: fastapi, langgraph, langchain, celery, pydantic
├── package.json                                  # JS workspace root (Turborepo)
├── turbo.json                                    # Turborepo pipeline config
├── .env.example                                  # all env vars: LLM_PROVIDER, DB_URL, REDIS_URL, etc.
├── Makefile                                      # dev, test, lint, docker-up shortcuts
└── README.md
│
│
├── frontend/                                     # UI layer (Phase 3)
│   │
│   ├── apps/
│   │   │
│   │   ├── mobile/                               # React Native + Expo (iOS + Android)
│   │   │   ├── app.json                          # Expo config
│   │   │   ├── App.tsx                           # root component, navigation setup
│   │   │   ├── app/                              # Expo Router file-based navigation
│   │   │   │   ├── (tabs)/
│   │   │   │   │   ├── index.tsx                 # home tab
│   │   │   │   │   └── profile.tsx               # profile tab
│   │   │   │   └── _layout.tsx                   # root layout
│   │   │   ├── assets/                           # fonts, images, icons
│   │   │   └── package.json
│   │   │
│   │   └── web/                                  # Next.js (web browser)
│   │       ├── next.config.js                    # Next.js config, transpiles shared packages
│   │       ├── app/                              # App Router
│   │       │   ├── layout.tsx                    # root layout, providers
│   │       │   ├── page.tsx                      # home page (SSG)
│   │       │   ├── chat/
│   │       │   │   └── page.tsx                  # chat page (CSR)
│   │       │   └── api/                          # Next.js API routes (BFF layer)
│   │       │       └── chat/
│   │       │           └── route.ts              # proxies to FastAPI /chat
│   │       ├── public/                           # static assets
│   │       └── package.json
│   │
│   └── packages/                                 # shared across mobile + web
│       │
│       ├── ui/                                   # shared component library
│       │   ├── package.json                      # name: @lce/ui
│       │   ├── index.ts                          # exports all components
│       │   ├── components/
│       │   │   ├── Button.tsx                    # react-native-web compatible
│       │   │   ├── TextInput.tsx
│       │   │   ├── ChatBubble.tsx
│       │   │   ├── Avatar.tsx
│       │   │   └── Card.tsx
│       │   └── tokens/
│       │       ├── colors.ts                     # brand colors: teal, coral, purple
│       │       ├── typography.ts                 # font sizes, weights
│       │       └── spacing.ts                    # spacing scale
│       │
│       ├── api-client/                           # shared HTTP + WebSocket client
│       │   ├── package.json                      # name: @lce/api-client
│       │   ├── index.ts
│       │   ├── chat.ts                           # chat endpoint calls, streaming
│       │   └── ingest.ts                         # document ingest calls
│       │
│       ├── store/                                # shared Zustand state
│       │   ├── package.json                      # name: @lce/store
│       │   ├── index.ts
│       │   ├── chatStore.ts                      # messages, session state
│       │   └── userStore.ts                      # auth, preferences
│       │
│       └── config/                               # shared constants + types
│           ├── package.json                      # name: @lce/config
│           └── index.ts                          # API_URL, shared TypeScript types
│
│
├── backend/                                      # all server-side Python code
│   ├── __init__.py
│   │
│   ├── ai/                                       # AI layer (Phase 1) — pure Python, no HTTP
│   │   ├── __init__.py
│   │   │
│   │   ├── graph/                                # LangGraph definitions
│   │   │   ├── __init__.py                       # exports: build_graph
│   │   │   ├── state.py                          # TypedDict: messages, context, metadata
│   │   │   ├── nodes.py                          # pure functions: retrieve, generate, validate
│   │   │   ├── edges.py                          # conditional routing logic between nodes
│   │   │   └── graph.py                          # assembles StateGraph, compiles runnable
│   │   │
│   │   ├── llm/                                  # switchable LLM adapter
│   │   │   ├── __init__.py                       # exports: get_llm
│   │   │   ├── base.py                           # BaseLLM protocol / abstract interface
│   │   │   ├── factory.py                        # reads LLM_PROVIDER env var, returns instance
│   │   │   ├── ollama.py                         # Ollama adapter (local, default)
│   │   │   ├── openai.py                         # OpenAI-compatible adapter (vLLM or hosted)
│   │   │   └── anthropic.py                      # Anthropic adapter (optional)
│   │   │
│   │   ├── rag/                                  # retrieval-augmented generation pipeline
│   │   │   ├── __init__.py
│   │   │   ├── embeddings.py                     # HuggingFace sentence-transformers setup
│   │   │   ├── vectorstore.py                    # Chroma client, collection init
│   │   │   ├── retriever.py                      # similarity search, reranking
│   │   │   └── ingest.py                         # load docs, chunk, embed, store
│   │   │
│   │   ├── tools/                                # LangGraph tool nodes
│   │   │   ├── __init__.py                       # exports tool registry list
│   │   │   ├── search.py                         # RAG retriever exposed as a tool
│   │   │   └── calculator.py                     # example deterministic tool
│   │   │
│   │   ├── prompts/                              # all prompt templates
│   │   │   ├── __init__.py                       # exports: SYSTEM_PROMPT, RAG_PROMPT
│   │   │   ├── system.py                         # base system prompt
│   │   │   └── rag.py                            # RAG context injection template
│   │   │
│   │   └── memory/                               # conversation and long-term memory
│   │       ├── __init__.py
│   │       ├── short_term.py                     # in-graph message window
│   │       └── long_term.py                      # Postgres persistence via LangGraph checkpointer
│   │
│   ├── api/                                      # API layer (Phase 2) — FastAPI, HTTP/WebSocket
│   │   ├── __init__.py
│   │   ├── main.py                               # FastAPI app init, router registration, lifespan
│   │   ├── deps.py                               # FastAPI Depends: db session, current user, llm
│   │   │
│   │   ├── routers/                              # HTTP endpoints only, no business logic
│   │   │   ├── __init__.py
│   │   │   ├── chat.py                           # POST /chat, WebSocket /chat/stream
│   │   │   ├── ingest.py                         # POST /ingest (triggers Celery job)
│   │   │   └── health.py                         # GET /health, GET /ready
│   │   │
│   │   ├── services/                             # business logic, no HTTP concerns
│   │   │   ├── __init__.py
│   │   │   ├── chat_service.py                   # calls ai/graph, formats response
│   │   │   └── ingest_service.py                 # orchestrates document pipeline
│   │   │
│   │   ├── schemas/                              # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── chat.py                           # ChatRequest, ChatResponse, StreamChunk
│   │   │   └── ingest.py                         # IngestRequest, IngestStatus
│   │   │
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py                           # JWT decode, user injection
│   │       └── logging.py                        # structlog request logging
│   │
│   ├── workers/                                  # Celery async job workers
│   │   ├── __init__.py
│   │   ├── celery_app.py                         # Celery init, broker = Valkey
│   │   └── tasks.py                              # ingest_document, batch_embed tasks
│   │
│   └── core/                                     # shared across ai/, api/, workers/
│       ├── __init__.py                           # exports: settings
│       ├── config.py                             # pydantic-settings: all env vars typed
│       ├── database.py                           # SQLAlchemy async engine, session factory
│       ├── exceptions.py                         # domain exceptions, HTTP error mapping
│       └── logging.py                            # structlog config, JSON output
│
│
├── infra/                                        # Infrastructure layer
│   │
│   ├── docker/                                   # per-service Dockerfiles
│   │   ├── Dockerfile.api                        # FastAPI app image
│   │   ├── Dockerfile.worker                     # Celery worker image
│   │   └── Dockerfile.web                        # Next.js web image
│   │
│   ├── postgres/
│   │   ├── init.sql                              # schema creation, pgvector extension
│   │   └── migrations/                           # Alembic migration scripts
│   │       ├── env.py
│   │       ├── alembic.ini
│   │       └── versions/                         # auto-generated migration files
│   │
│   ├── valkey/
│   │   └── valkey.conf                           # Valkey config: maxmemory, persistence
│   │
│   ├── chroma/
│   │   └── config.yaml                           # Chroma server config, persistence path
│   │
│   ├── ollama/
│   │   └── modelfile                             # default model pull config (llama3)
│   │
│   └── nginx/
│       └── nginx.conf                            # reverse proxy: / → Next.js, /api → FastAPI
│
│
├── tests/                                        # mirrors backend/ package structure
│   ├── __init__.py
│   ├── conftest.py                               # fixtures: mock LLM, test DB, sample docs
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── test_graph.py                         # unit test LangGraph nodes in isolation
│   │   └── test_rag.py                           # retrieval quality tests
│   └── api/
│       ├── __init__.py
│       └── test_api.py                           # FastAPI TestClient integration tests
│
└── docs/
    ├── ARCHITECTURE.md                           # this file
    ├── setup.md                                  # local dev setup guide
    └── api.md                                    # API endpoint reference
```

---

## Layer Responsibilities

### `frontend/apps/mobile/` — iOS + Android
React Native + Expo. File-based routing via Expo Router. Consumes all
shared packages from `frontend/packages/`. Builds to native iOS and
Android via `expo build` or EAS Build.

### `frontend/apps/web/` — Web browser
Next.js with App Router. Statically generated pages for SEO (landing,
docs), client-side rendering for interactive chat. Uses the same
`@lce/ui`, `@lce/store`, and `@lce/api-client` packages as mobile.
The `app/api/` routes act as a thin BFF (backend-for-frontend) proxy
to FastAPI — useful for hiding the backend URL from the browser.

### `frontend/packages/` — Shared code
All packages are workspace packages consumed by both apps. `react-native-web`
makes `@lce/ui` components render correctly in the browser. No platform-
specific code lives here — if something needs to differ between mobile and
web it uses platform-aware file extensions (`.native.ts` / `.web.ts`).

| Package | Purpose |
|---|---|
| `@lce/ui` | Shared components, design tokens |
| `@lce/api-client` | HTTP + WebSocket calls to FastAPI |
| `@lce/store` | Zustand global state (chat, user) |
| `@lce/config` | Shared constants, TypeScript types |

### `backend/ai/` — AI layer (Phase 1)
Pure Python. No dependency on FastAPI or any web framework. The entire
LangGraph agent — state, nodes, tools, RAG pipeline, and LLM adapter —
lives here and is independently testable. The LLM is switchable via a
single env var (`LLM_PROVIDER`).

### `backend/api/` — API layer (Phase 2)
FastAPI application exposing the AI layer over HTTP and WebSocket.
Routers handle only request/response. Business logic lives in `services/`.

### `backend/workers/` — Async job workers
Celery workers for long-running tasks: document ingestion, batch
embedding. Uses Valkey as message broker and result backend.

### `backend/core/` — Shared Python foundation
Typed config, async database session, structured logging, and domain
exceptions shared across all Python packages.

### `infra/` — Infrastructure
All infrastructure config in one place — Dockerfiles, database migrations,
Valkey tuning, Chroma persistence, Nginx reverse proxy. Nothing here
contains business logic; it is purely operational config.

---

## Data Flow

```
Mobile / Web client
  └── @lce/api-client
        └── POST /api/chat  (Next.js BFF)  — web only
        └── POST /chat      (FastAPI direct) — mobile
              └── backend/api/routers/chat.py
                    └── backend/api/services/chat_service.py
                          └── backend/ai/graph/graph.py
                                ├── backend/ai/llm/factory.py     # Ollama / vLLM / OpenAI
                                ├── backend/ai/tools/search.py    # Chroma RAG retrieval
                                └── backend/ai/prompts/rag.py     # prompt assembly
                          └── StreamingResponse → WebSocket → UI
```

---

## LLM Switching

```bash
# .env

# Local development (default)
LLM_PROVIDER=ollama
MODEL_NAME=llama3

# GPU server / self-hosted
LLM_PROVIDER=openai
OPENAI_BASE_URL=http://vllm-server:8000/v1
MODEL_NAME=mistral-7b

# Hosted fallback
LLM_PROVIDER=anthropic
MODEL_NAME=claude-3-5-sonnet
```

---

## Tech Stack

| Layer | Technology | License |
|---|---|---|
| Mobile | React Native + Expo | MIT |
| Web | Next.js + App Router | MIT |
| Shared UI | react-native-web | MIT |
| State | Zustand | MIT |
| Server state | TanStack Query | MIT |
| Monorepo | Turborepo | MIT |
| API | FastAPI | MIT |
| Auth | python-jose / Keycloak | MIT / Apache 2.0 |
| Job queue | Celery | BSD |
| AI orchestration | LangGraph + LangChain | Apache 2.0 |
| LLM (local) | Ollama + Llama 3 / Mistral | MIT |
| LLM (GPU scale) | vLLM | Apache 2.0 |
| Embeddings | HuggingFace sentence-transformers | Apache 2.0 |
| Vector DB | Chroma | Apache 2.0 |
| Database | PostgreSQL + pgvector | PostgreSQL License |
| Cache / broker | Valkey | BSD |
| Reverse proxy | Nginx | BSD |
| Containers | Docker + Compose | Apache 2.0 |
