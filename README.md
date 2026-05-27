# Mendonça Galvão - HR Analytics Dashboard 🏢✨

> Dashboard Executivo de Inteligência de Recursos Humanos com foco em análise macroestrutural, retenção de talentos e política salarial.

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

---

## 🎯 Sobre o Projeto

O **Mendonça Galvão HR Analytics** é uma ferramenta gerencial desenhada para diretoria e liderança. O projeto transforma dados brutos de RH (em planilhas Excel) em visualizações ricas e insights estratégicos através de uma interface premium no estilo *Dark Glassmorphism*.

### Principais Funcionalidades
- 📊 **Visão Geral Macro:** KPIs instantâneos de retenção, salários e força de trabalho.
- 🎯 **Expectativas e Retenção:** Análise preditiva de risco baseada no "Índice de Confiança" da base corporativa.
- 💰 **Inteligência Salarial:** Mapeamento de folha de pagamento, fricção de compensação e faixas salariais (Junior a Especialista).
- ⏱️ **Tempo & Carreira:** Demografia corporativa baseada no tempo de vínculo empregatício.
- 🎬 **Modo Apresentação:** Experiência cinematográfica *fullscreen* automatizada (Storytelling de Dados) para reuniões executivas.
- 🔒 **Área Restrita (Confidencial):** Acesso estrito por senha para detalhamento nominal, protegendo dados sensíveis do RH.

---

## 🛠️ Stack Tecnológica

O sistema foi arquitetado de forma desacoplada para máxima performance e flexibilidade.

**Frontend (Client-side):**
- **React.js 19 + Vite** (Single Page Application super rápida)
- **Framer Motion** (Micro-interações e animações físicas/spring)
- **Recharts** (Visualização de dados SVG)
- **React Feather** (Iconografia consistente)
- Estilização pura focada em *CSS Variables*, *Glassmorphism* (Backdrop Filters) e Acessibilidade Visual.

**Backend (Server-side & Data Engine):**
- **Python 3.12 + FastAPI** (API Assíncrona, robusta e tipada)
- **Pandas** (Motor de ETL: Leitura, higienização, mapeamento e agregação dos dados Excel)
- **Pydantic** (Validação e serialização severa dos esquemas de dados JSON)
- **Uvicorn** (Servidor Web ASGI)

---

## 📁 Estrutura do Repositório

```text
DASH - MG/
├── backend/               # Motor Python
│   ├── app/               # Lógica de negócio FastAPI
│   │   ├── api/           # Rotas / Endpoints REST
│   │   ├── analytics/     # Motor de cálculos de RH
│   │   ├── etl/           # Tratamento de dados da Planilha
│   │   ├── models/        # Schemas Pydantic
│   │   └── config.py      # Gestor de Variáveis e Settings
│   ├── data/              # Bases de dados locais (.xlsx)
│   └── requirements.txt   # Dependências do Backend
│
├── frontend/              # Interface React
│   ├── public/            # Assets estáticos (Logo, Fonts)
│   ├── src/               # Código-fonte SPA
│   │   ├── components/    # Componentes reutilizáveis UI/Gráficos
│   │   ├── hooks/         # Custom Hooks de orquestração de dados
│   │   ├── pages/         # Páginas / Abas principais do Dashboard
│   │   └── utils/         # Formatadores (Moeda, Porcentagem)
│   └── package.json       # Dependências do Frontend
│
├── .env.example           # Exemplo de Variáveis de Ambiente
├── .dockerignore          # Arquivos ignorados no Build (nuvem)
└── Dockerfile             # Multi-stage build para Deploy Unificado
```

---

## 🚀 Desenvolvimento Local

Para rodar este projeto na sua própria máquina, você precisará ter o Node.js e o Python instalados. Siga os dois passos simultaneamente (em terminais separados).

### 1. Subindo o Backend (API)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # (No Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Subindo o Frontend (Interface)
```bash
cd frontend
npm install
npm run dev
```
O Frontend estará rodando em `http://localhost:5173` consumindo automaticamente a API na porta `8000`.

---

## ☁️ Deploy em Produção (Coolify / Docker)

O projeto já está 100% otimizado para deploy em orquestradores de contêineres como o **Coolify**, usando o arquivo `Dockerfile` (Multi-estágio) incluído na raiz.

Em produção, o Frontend é construído de forma estática e embutido no Backend FastAPI, unificando toda a plataforma numa única porta (`8000`), extinguindo problemas de CORS.

### Passos de Configuração:
1. Conecte este repositório no seu Coolify como **Dockerfile Service**.
2. Defina as **Environment Variables** obrigatórias (veja o `.env.example`), garantindo que:
   - `HR_ENVIRONMENT=production`
   - `HR_CONFIDENTIAL_PASSWORD=[SUA_SENHA]`
3. Exponha a porta interna **8000**.
4. Realize o Deploy. O Coolify tratará do download do Node/Python, construção e serving de forma automática!

---

> Desenvolvido de forma cuidadosa e estratégica, unindo inteligência de dados à sofisticação de design. 🚀
