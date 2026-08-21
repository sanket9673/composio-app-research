# Composio App Readiness Research Agent

An enterprise-grade research pipeline and interactive dashboard auditing **100 popular SaaS applications** for AI agent buildability, authentication methods, gating parameters, and Model Context Protocol (MCP) server support.

* **Live Deployed Dashboard**: [https://composio-app.netlify.app/](https://composio-app.netlify.app/)
* **Source Code Repository**: [https://github.com/sanket9673/composio-app-research](https://github.com/sanket9673/composio-app-research)

---

## 📌 Project Overview

This repository demonstrates a complete dual-pass verification loop:
1. **Pass 1 (Raw Research)**: An automated research run retrieving app metadata and document URLs using Google Search Grounding with Gemini.
2. **Pass 2 (Verification Sweep)**: Applies corrections from a manual 15-app audit sample and executes a dataset-wide validation sweep to eliminate hallucinations, correcting the Model Context Protocol (MCP) adoption rate from 96% down to a realistic, grounded **14%**.

---

## 📊 Dashboard Preview & Features

The repository includes a single-page interactive dashboard (`index.html`) deployed live on Netlify:
* **Top Metric Analytics**: Overview of OAuth2 dominance (70%), overall self-serve percentage (74%), category rankings, and primary integration blockers.
* **Strategic Opportunity Matrix**: Dedicated breakdown contrasting 5 concrete **Easy Wins** (*Supabase, Linear, Notion, GitHub, Stripe*) against 5 **Needs Outreach** platforms (*PitchBook, DealCloud, Brex, Ramp, Paygent Connect*).
* **Interactive Findings Matrix**: Search, filter, and browse all 100 apps with color-coded badges, `⚡ Composio Native` tags, and direct documentation links.
* **Verification Proof Table**: Full audit history showing Pass 1 claims vs Pass 2 actuals for 15 representative applications (yielding an 80% to 100% accuracy delta).
* **Structured Data**: Embedded JSON-LD schema (`TechArticle`) for machine consumption and automated agents.

---

## 🏗️ Architecture & Request Pipeline

```mermaid
graph TD;
    classDef client fill:#1e293b,stroke:#475569,stroke-width:1px,color:#94a3b8;
    classDef security fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#c7d2fe;
    classDef api fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#38bdf8;
    classDef service fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#a7f3d0;
    classDef storage fill:#581c87,stroke:#a855f7,stroke-width:2px,color:#f3e8ff;
    classDef external fill:#451a03,stroke:#f97316,stroke-width:2px,color:#ffedd5;

    CLI["CLI / Terminal Entrypoint<br>(python research_agent.py)"]:::client
    EnvCheck["Environment & Config Parser<br>(API Keys & Offline Fallback Check)"]:::security

    subgraph PipelineCore ["Core Research Pipeline"]
        AgentEngine["Gemini Search Grounding Engine<br>(Google GenAI SDK & Live Web Search)"]:::service
        ComposioRegistry["Composio ToolSet SDK Registry<br>(Native Toolkit Verification Loop)"]:::service
        PydanticValidator["Pydantic Runtime Schema Validator<br>(AppMetadata Model Enforcement)"]:::service
    end

    subgraph VerificationEngine ["Dual-Pass Verification Engine"]
        AuditLogger["15-App Manual Audit Logger<br>(data/verification.csv Sample Audit)"]:::service
        SanitizationSweep["Dataset Sanitization Sweep<br>(Domain Grounding & MCP De-hallucination)"]:::service
    end

    subgraph DataPersistence ["Data Persistence Layer"]
        RawOutput[("Pass 1 Raw Data<br>data/results_v1.json")]:::storage
        VerifiedOutput[("Pass 2 Verified Data<br>data/results_v2_verified.json")]:::storage
    end

    subgraph PresentationLayer ["Frontend Presentation Layer"]
        SyncEngine["Dashboard Sync Engine<br>(results_v2 -> index.html Data Binding)"]:::external
        NetlifyDashboard[("Netlify Live Web Dashboard<br>composio-app.netlify.app")]:::external
    end

    CLI --> EnvCheck
    EnvCheck --> AgentEngine
    AgentEngine --> ComposioRegistry
    ComposioRegistry --> PydanticValidator
    PydanticValidator --> RawOutput
    RawOutput --> AuditLogger
    AuditLogger --> SanitizationSweep
    SanitizationSweep --> VerifiedOutput
    VerifiedOutput --> SyncEngine
    SyncEngine --> NetlifyDashboard
```

---

## 📁 Repository Data Layout

* [`research_agent.py`](research_agent.py): Asynchronous research pipeline script supporting Gemini search grounding, Pydantic validation, Composio SDK tool registry lookup, and manual audit correction sweeps.
* [`requirements.txt`](requirements.txt): Declared Python package requirements (google-genai, composio-core, pydantic, pandas, beautifulsoup4).
* [`data/results_v1.json`](data/results_v1.json): Raw Pass 1 output containing the initial automated research dataset (including initial hallucinations and unverified claims).
* [`data/results_v2_verified.json`](data/results_v2_verified.json): Grounded, verified Pass 2 dataset with corrected documentation domains and realistic MCP mapping.
* [`data/verification.csv`](data/verification.csv): 15-app audit sample tracking the verification delta (yielding 80.0% Pass 1 accuracy scaling to 100% in Pass 2).
* [`index.html`](index.html): Highly interactive single-page Tailwind CSS glassmorphic dashboard deployed live on Netlify.

---

## ⚡ Quick Start Guide

### Prerequisites
* Python 3.9 or higher
* Pip package manager

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/sanket9673/composio-app-research.git
cd composio-app-research
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the project root to configure credentials:
```env
GEMINI_API_KEY=your_gemini_api_key_here
COMPOSIO_API_KEY=your_composio_api_key_here
```
*Note: If no API key is found, the script automatically executes in offline simulator mode utilizing the cached dataset to ensure the pipeline runs successfully without requiring external credentials.*

### 3. Running the Pipeline

#### Execute Pass 1 (Raw Research)
Generates the raw dataset `data/results_v1.json` based on the search grounding loop:
```bash
python research_agent.py --run
```

#### Execute Pass 2 (Apply Verification Sweep)
Applies the audit corrections from `data/verification.csv`, runs a sanitization sweep across all 100 apps to clean up hallucinated MCP servers/fake URLs, validates records using Pydantic, and writes to `data/results_v2_verified.json`:
```bash
python research_agent.py --verify
```

---

## 🔬 Verification Methodology & Grounding

The initial automated research run suffered from typical LLM decay, incorrectly claiming a **96% MCP server adoption rate** with hallucinated subdomains like `mcp.podio.com`.

Our verification loop addresses this through:
1. **Manual Audit Sampling**: A 15-app representative sample (`data/verification.csv`) evaluated across all 10 categories to catch systematic errors (e.g., classifying Basic Authentication as plain API key, or command-line utilities as REST APIs).
2. **Dataset-wide Sanitization Loop**: Programmatic rules correcting domains, whitelisting only the 14 apps with verified MCP servers (GitHub, Supabase, Stripe, Linear, Notion, Slack, Apify, Firecrawl, Datadog, Sentry, Cloudflare, MongoDB Atlas, Airtable, Jira), and formatting evidence URLs.

---

## 🛡️ Human-in-the-Loop & Gating Analysis

Automated agents are blocked by platform-level gating. We flag apps as `needs_human_review` for:
* **Enterprise paywalls**: Gated behind direct corporate contact (e.g., PitchBook).
* **Corporate whitelists**: Restricted to business bank accounts or verified IRS EIN submissions (e.g., Brex, Ramp).
* **Developer Review queues**: Scopes restricted until brand verification and OAuth walkthrough videos are audited by platform reviews (e.g., Google Ads, Meta Ads).