# 🧠 MedGPT

# 🧠 MedGPT – AI Assistant for Medical Research

![Build](https://img.shields.io/github/actions/workflow/status/vrajbhatt27/mygpt/.github/workflows/ci-cd.yml?branch=main)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![Lint](https://img.shields.io/badge/linting-ruff-blue?logo=python)
![Last Commit](https://img.shields.io/github/last-commit/vrajbhatt27/mygpt)
![Issues](https://img.shields.io/github/issues/vrajbhatt27/mygpt)

## 📑 Table of Contents

- [Introduction](#-introduction)
- [Project Overview](#-project-overview)
  - [Tech Stack](#-tech-stack)
  - [System Overview](#-system-overview)
- [Project Status](#-project-status)
  - [MVP Delivered: Phase 1 + Phase 2](#-mvp-delivered-phase-1--phase-2)
    - [Phase 1 – MVP Foundation](#-phase-1--mvp-foundation-backend--frontend--claude-integration)
    - [Phase 2 – RAG Pipeline Implementation & Document Uploads](#-phase-2--rag-pipeline-implementation--document-uploads)
  - [Phase 3 – System Refinement & User-Centric RAG](#-phase-3--system-refinement--user-centric-rag-️-in-progress)
  - [Phase 4 – Identity, Access & Session Management](#-phase-4--identity-access--session-management)
  - [Phase 5 – Knowledge Corpus Integration & Smart Training](#-phase-5--knowledge-corpus-integration--smart-training)
  - [Phase 6 – Security, Privacy & Compliance](#-phase-6--security-privacy--compliance)
  - [Phase 7 – Chat UX & Session Management](#-phase-7--chat-ux--session-management)
  - [Phase 8 – Production Deployment & Scaling](#-phase-8--production-deployment--scaling)

## 📌 Introduction

MedGPT is an enterprise-grade, domain-specific generative AI assistant built to serve the specialized needs of the pharmaceutical and healthcare sectors. It is designed with a medical company’s real-world research workflows, compliance requirements, and knowledge hierarchies in mind — helping transform scattered internal documents into structured, accessible, and intelligent knowledge.

What sets MedGPT apart is its ability to adapt to roles and responsibilities within an organization, ensuring that information is not only accurate but also securely scoped to each user’s access level. Whether it’s a research scientist diving into regulatory data, a medical advisor summarizing clinical trials, or an operations team referencing study protocols — MedGPT offers a context-aware, secure, and collaborative research experience.

Unlike general-purpose AI tools, MedGPT is engineered to:

🌟 Provide role-based access control, where only authorized personnel can upload, manage, or access specific knowledge sources based on department, project, or clearance.

🌟 Include a dedicated training mode, accessible only to authorized roles, enabling ingestion and tagging of curated datasets for department- or team-specific use.

🌟 Serve as a secure and compliant AI research companion, usable by employees at all levels — from data scientists to clinicians and administrative staff.

🌟 Offer all the advanced capabilities of modern GenAI systems — chat, summarization, document search, multi-turn memory — refined specifically for high-stakes medical use cases.

🌟 Enable real-time document synchronization, pulling content from both local uploads and cloud-based knowledge systems like Confluence, SharePoint, and internal portals, ensuring always-fresh context during retrieval and generation.

🌟 Maintain session-aware context, implement data expiry, and support audit logging to align with industry-grade security and governance protocols.

🌟 Scale seamlessly across teams while preserving data isolation, document encryption, and compliance guardrails — making it enterprise-ready from day one.

---

## 🔧 Project Overview

---

### 🧱 Tech Stack

| Layer                      | Technology                                                    |
| -------------------------- | ------------------------------------------------------------- |
| **Frontend**               | Streamlit (Dockerized)                                        |
| **Backend API**            | FastAPI (Dockerized), Celery (async task queue)               |
| **LLM / Embeddings**       | Claude Sonnet (LLM), OpenAI Embeddings                        |
| **Vector Store**           | Pinecone (namespaced, metadata-filtered)                      |
| **Storage & DB**           | PostgreSQL (user/session data), Cloud File Storage            |
| **Auth & Access Control**  | JWT-based Authentication, Role-Based Access Control (RBAC)    |
| **Document Sync**          | Confluence, SharePoint                                        |
| **Structured Data Source** | Snowflake (Cortex AI)                                         |
| **Security**               | Guardrails, PII scanner and filtering                         |
| **Deployment & DevOps**    | Docker, GitHub Actions CI/CD, AWS (ECS), Monitoring & Logging |

---

### 📐 System Overview

MedGPT is built on a modular, containerized architecture designed to support scalable document processing, role-specific AI-driven interactions, and secure deployment for high-stakes medical environments.

The **frontend**, built with Streamlit, provides a ChatGPT-style interface that supports document uploads, chat input, model switching (Claude/OpenAI), and interaction modes (Training, Research, Normal). It includes secure authentication and displays responses in real time.

Each session is authenticated through a JWT-based system, and user metadata (role, team, permissions) is used to dynamically configure both the frontend and backend access policies.

The **backend**, powered by FastAPI, coordinates the system’s RAG pipeline and business logic. When a user uploads documents, they are processed asynchronously using Celery workers — parsed, chunked, embedded using OpenAI’s embedding API, and stored in Pinecone with rich metadata. Queries are normalized for clarity, then used to retrieve relevant vector chunks which, along with the user’s question, are embedded into a prompt sent to Claude Sonnet for answer generation.

**Pinecone** acts as the vector database, structured into multiple namespaces:

- **User-level namespaces** for ephemeral sessions, with automatic expiry or deletion.
- **Team-level namespaces** for documents trained/uploaded in Training Mode.
- **Org-wide knowledge bases** containing standard institutional information.

Documents are sourced from local uploads and automatically synchronized from external systems like **Confluence and SharePoint**. These files are processed and embedded into the appropriate namespace with access control based on user role and department.

Structured enterprise data is accessible via **Snowflake**, using Cortex AI to enable secure LLM-powered querying alongside unstructured document search.

For compliance, a **PII scanning and redaction layer** ensures sensitive information is filtered before reaching the LLM. Prompt Guardrails are enforced to monitor inputs and maintain alignment with enterprise usage policies.

**PostgreSQL** is used to persist user profiles, session metadata, chat history, and audit logs. All services are containerized using Docker, deployed via GitHub Actions to AWS infrastructure. Monitoring and logging services are integrated to ensure reliability and observability across the platform.

---

## 📈 Project Status

---

### ✅ MVP Delivered: Phase 1 + Phase 2

The following phases represent the foundation of the MedGPT platform and are fully implemented and containerized as an MVP.

---

### 🔹 Phase 1 – MVP Foundation (Backend + Frontend + Claude Integration)

**🎯 Goal:** Build a ChatGPT-style MVP with API-layer Claude integration and a basic frontend.

- Modular backend (FastAPI) and frontend (Streamlit) setup with Docker.
- `/ask` API created to send user queries + context to Claude Sonnet.
- `call_claude()` integrated using Anthropic's API.
- Basic Streamlit UI with question input + answer rendering.
- Manual and Postman-based testing of Claude response pipeline.
- Dockerfiles with EXPOSE/CMD best practices applied.
- Engineering practices: `.env` secrets, port binding, isolated services.

---

### 🔹 Phase 2 – RAG Pipeline Implementation & Document Uploads

**🎯 Goal:** Enable file-aware Q&A using Claude + OpenAI Embeddings + Pinecone.

- File upload in Streamlit with support for PDF/CSV.
- Document chunking using LangChain (recursive splitter).
- Embedding via OpenAI (`text-embedding-3-small`) and stored in Pinecone.
- Vector search + Top-k chunk retrieval implemented.
- Prompt engineering to combine user query and context chunks into structured Claude inputs.
- Display responses in chat-style interface.
- Namespace protection to prevent duplicate uploads.
- CI (Github Actions) with Ruff, modular RAG services, Docker build validations.

> ✅ Phase 2 marks the completion of the MVP — enabling secure, document-aware Q&A using Claude, embeddings, and a modular RAG pipeline.

---

### 🏗️ Phase 3 – System Refinement & User-Centric RAG _(🚧 In Progress)_

**🎯 Goal:** Improve reliability, answer quality, and user experience.

- Add fallback and retry mechanisms.
- Auto-summarization if no question is asked.
- Improve prompts and clean user queries with normalization.
- Display parsed document content via `st.expander`.
- Add semantic filters to control retrieval by date, section, or topic.
- Implement chat memory across turns + model switching (Claude/OpenAI).
- Avoid reprocessing same files through memory/session cache.

---

### 🔐 Phase 4 – Identity, Access & Session Management

**🎯 Goal:** Enable secure, role-aware multi-user access.

- Implement JWT-based login/signup with RBAC.
- Role-based indexing and session-aware Pinecone namespaces.
- Auto-expire ephemeral data or allow manual deletion.
- Dynamically render features in UI based on role (Trainer, Admin, Employee).
- Secrets managed securely with `.env` and runtime loaders.

---

### 🧠 Phase 5 – Knowledge Corpus Integration & Smart Training

**🎯 Goal:** Expand the assistant into a collaborative training and knowledge base.

- Ingest content from PDF/HTML/Confluence → chunk → embed → store.
- Add “Smart Search Mode” (User → Team → Org hierarchy).
- Connect with Confluence and SharePoint pages for syncing knowledge.
- Add Snowflake (Cortex AI) for structured data search.
- Add Celery to asynchronously process and embed synced documents and queries.
- Design a Trainer Dashboard for dataset management and upload.

---

### 🔒 Phase 6 – Security, Privacy & Compliance

**🎯 Goal:** Ensure compliance with medical data governance.

- Encrypt sensitive files before storage/transmission.
- Implement PII scanner with redaction before LLM access.
- Add Guardrails for prompt safety + abuse detection.
- Maintain audit logs for moderation and traceability.
- Implement GDPR-style expiry of user/vector data.

---

### 💬 Phase 7 – Chat UX & Session Management

**🎯 Goal:** Polish chat interface into a full ChatGPT-style session system.

- Multi-chat threads saved with timestamps.
- Store chat history in PostgreSQL/local storage.
- Sidebar-based chat picker with rename/delete features.
- Maintain turn-level memory across sessions.
- Apply UI polish — avatars, markdown support, loader animations.

---

### 🚀 Phase 8 – Production Deployment & Scaling

**🎯 Goal:** Productionize MedGPT with DevOps, CI/CD, and scalable infra.

- Optimize Dockerfiles with multi-stage builds and health checks.
- Set up config environments for dev, UAT, and prod.
- Use GitHub Actions to test/lint/build/deploy backend + frontend.
- Deploy on AWS ECS with logging and health monitoring.
- Set up observability (Prometheus/Sentry) and add optional autoscaling.

---

## 📩 Contact

Designed and engineered by Vraj Bhatt | AI/ML Systems • Full-Stack Development • DevOps
📫 Email: vrajbhatt.it@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/vrajbhatt27ß)

---

## © Copyright

© 2025 Vraj Bhatt. All rights reserved.  
This project is intended for portfolio and educational purposes only. Commercial use is prohibited without permission.
