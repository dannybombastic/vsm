"""Seed default Mermaid diagrams for existing projects."""
from django.core.management.base import BaseCommand
from vsm.models import Project, Diagram


# The original hardcoded diagram from index.html
ATHINA_DELIVERY_DIAGRAM = """\
graph LR
    CLIENT["🏛️ End Client<br/>HADEA"]
    MGT["📋 Management"]
    AGILE["🔄 Agile / Scrum"]
    DEV["💻 Developers"]
    QA["🧪 QA / Testing"]
    UX["🎨 UX / Design"]
    DATA["📊 Data / Analytics"]
    DEVOPS["⚙️ DevOps / Platform"]
    FELIPE["👤<br/>Tech Lead"]

    CLIENT -->|Requirements| MGT
    MGT -->|Priorities| AGILE
    AGILE -->|Stories| DEV
    AGILE -->|Stories| QA
    AGILE -->|Stories| UX
    AGILE -->|Stories| DATA
    DEV -->|Builds| QA
    UX -->|Designs| DEV
    QA -->|Results| AGILE
    DATA -->|Reports| MGT
    DEV -->|Artifacts| DEVOPS
    DEVOPS -->|Deployments| QA
    DEVOPS -.->|Enables| DEV
    DEVOPS -.->|Enables| QA
    DEVOPS -.->|Enables| DATA
    DEV -->|Deliverables| FELIPE
    FELIPE -->|Validation| MGT
    MGT -->|Releases| CLIENT

    style CLIENT fill:#f59e0b,stroke:#d97706,color:#000
    style MGT fill:#dc2626,stroke:#b91c1c,color:#fff
    style AGILE fill:#16a34a,stroke:#15803d,color:#fff
    style DEV fill:#2563eb,stroke:#1d4ed8,color:#fff
    style QA fill:#9333ea,stroke:#7e22ce,color:#fff
    style UX fill:#ea580c,stroke:#c2410c,color:#fff
    style DATA fill:#0891b2,stroke:#0e7490,color:#fff
    style DEVOPS fill:#4f46e5,stroke:#4338ca,color:#fff
    style FELIPE fill:#64748b,stroke:#475569,color:#fff

    click DEV "/questionnaire/developers/" _self
    click QA "/questionnaire/qa-testing/" _self
    click UX "/questionnaire/ux-design/" _self
    click DATA "/questionnaire/data-analytics/" _self
    click AGILE "/questionnaire/agile-scrum/" _self
    click MGT "/questionnaire/management/" _self
    click DEVOPS "/questionnaire/devops-platform/" _self"""

LOT2_ANALYTICS_DIAGRAM = """\
graph TD
    subgraph Ingestion
        SRC["📁 Data Sources"]
        ETL["⚙️ ETL Pipeline"]
        LAKE["🗄️ Data Lake"]
    end
    subgraph Processing
        SYNAPSE["📊 Synapse Analytics"]
        PURVIEW["🔍 Purview Catalog"]
        SEARCH["🔎 AI Search"]
    end
    subgraph Presentation
        PBI["📈 Power BI"]
        API["🌐 REST API"]
        DASH["📋 Dashboard"]
    end

    SRC -->|Raw data| ETL
    ETL -->|Cleaned| LAKE
    LAKE --> SYNAPSE
    LAKE --> PURVIEW
    SYNAPSE --> PBI
    SYNAPSE --> API
    PURVIEW --> SEARCH
    SEARCH --> DASH
    API --> DASH

    style SRC fill:#0891b2,stroke:#0e7490,color:#fff
    style ETL fill:#4f46e5,stroke:#4338ca,color:#fff
    style LAKE fill:#2563eb,stroke:#1d4ed8,color:#fff
    style SYNAPSE fill:#9333ea,stroke:#7e22ce,color:#fff
    style PURVIEW fill:#16a34a,stroke:#15803d,color:#fff
    style SEARCH fill:#ea580c,stroke:#c2410c,color:#fff
    style PBI fill:#f59e0b,stroke:#d97706,color:#000
    style API fill:#dc2626,stroke:#b91c1c,color:#fff
    style DASH fill:#64748b,stroke:#475569,color:#fff"""

GLOBAL_OVERVIEW_DIAGRAM = """\
graph TB
    subgraph ATHINA["🏗️ ATHINA Platform"]
        LOT1["LOT1<br/>Development"]
        LOT2["LOT2<br/>Analytics"]
    end
    subgraph Services["☁️ Azure Services"]
        AKS["AKS"]
        PG["PostgreSQL"]
        SYNAPSE["Synapse"]
        KV["Key Vault"]
    end
    subgraph DevOps["⚙️ DevOps"]
        ADO["Azure DevOps"]
        ACR["Container Registry"]
        PIPE["CI/CD Pipelines"]
    end

    LOT1 --> AKS
    LOT1 --> PG
    LOT2 --> SYNAPSE
    LOT2 --> PG
    AKS --> ACR
    ADO --> PIPE
    PIPE --> ACR
    PIPE --> AKS
    KV -.->|Secrets| AKS
    KV -.->|Secrets| SYNAPSE

    style ATHINA fill:#fff,stroke:#dc2626,color:#000
    style Services fill:#fff,stroke:#2563eb,color:#000
    style DevOps fill:#fff,stroke:#4f46e5,color:#000
    style LOT1 fill:#dc2626,stroke:#b91c1c,color:#fff
    style LOT2 fill:#0891b2,stroke:#0e7490,color:#fff
    style AKS fill:#2563eb,stroke:#1d4ed8,color:#fff
    style PG fill:#16a34a,stroke:#15803d,color:#fff
    style SYNAPSE fill:#9333ea,stroke:#7e22ce,color:#fff
    style KV fill:#f59e0b,stroke:#d97706,color:#000
    style ADO fill:#4f46e5,stroke:#4338ca,color:#fff
    style ACR fill:#ea580c,stroke:#c2410c,color:#fff
    style PIPE fill:#64748b,stroke:#475569,color:#fff"""


class Command(BaseCommand):
    help = "Seed default Mermaid diagrams for projects"

    def handle(self, *args, **options):
        created = 0

        # Global overview diagram (no project)
        _, was_created = Diagram.objects.get_or_create(
            slug="athina-overview",
            defaults={
                "name": "ATHINA Platform Overview",
                "description": "Vista general de la plataforma ATHINA con sus LOTs y servicios Azure.",
                "mermaid_code": GLOBAL_OVERVIEW_DIAGRAM,
                "is_default": True,
                "project": None,
            },
        )
        if was_created:
            created += 1

        # ATHINA LOT1 delivery diagram
        athina = Project.objects.filter(slug="athina").first()
        if athina:
            _, was_created = Diagram.objects.get_or_create(
                slug="athina-delivery-chain",
                defaults={
                    "name": "ATHINA Delivery Chain",
                    "description": "Cadena de entrega del equipo de desarrollo ATHINA LOT1.",
                    "mermaid_code": ATHINA_DELIVERY_DIAGRAM,
                    "is_default": True,
                    "project": athina,
                },
            )
            if was_created:
                created += 1

        # ATHINA LOT2 analytics diagram
        lot2 = Project.objects.filter(slug="athina-lot2").first()
        if lot2:
            _, was_created = Diagram.objects.get_or_create(
                slug="athina-lot2-analytics-flow",
                defaults={
                    "name": "LOT2 Analytics Flow",
                    "description": "Flujo de datos y analytics de ATHINA LOT2.",
                    "mermaid_code": LOT2_ANALYTICS_DIAGRAM,
                    "is_default": True,
                    "project": lot2,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} diagrams seeded."))
