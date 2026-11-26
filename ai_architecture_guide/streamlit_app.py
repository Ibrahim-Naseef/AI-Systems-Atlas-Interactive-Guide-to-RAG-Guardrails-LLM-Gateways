import html
import re
import textwrap

import streamlit as st


st.set_page_config(
    page_title="AI Systems Architecture Guide",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #e8eef8;
        --muted: #9cabc0;
        --panel: #111c2c;
        --panel-2: #17243a;
        --line: #2b3c55;
        --accent: #6ee7d2;
        --blue: #8db7ff;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 18% 0%, rgba(52, 94, 145, .20), transparent 38%),
            linear-gradient(160deg, #0b1220 0%, #0e1726 55%, #101a2b 100%);
        color: var(--ink);
    }
    [data-testid="stSidebar"] {
        background: #0c1523;
        border-right: 1px solid var(--line);
    }
    .block-container { max-width: 1440px; padding-top: 2rem; }
    .hero {
        padding: 1.6rem 1.8rem;
        border: 1px solid #30445e;
        border-radius: 22px;
        background: linear-gradient(120deg, rgba(28, 48, 74, .96), rgba(17, 29, 46, .94));
        margin-bottom: 1.4rem;
    }
    .hero-kicker {
        color: var(--accent);
        font-size: .76rem;
        font-weight: 750;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-bottom: .45rem;
    }
    .hero h1 { color: #f4f7fc; font-size: 2.25rem; margin: 0 0 .45rem 0; }
    .hero p { color: #b6c4d7; font-size: 1.04rem; margin: 0; max-width: 920px; }
    .eyebrow {
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: .12em;
        font-size: .72rem;
        font-weight: 750;
        margin-bottom: .25rem;
    }
    .info-card {
        height: 100%;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1rem 1.05rem;
        background: linear-gradient(150deg, rgba(23, 36, 58, .98), rgba(16, 27, 43, .96));
    }
    .info-card h3 { margin: 0 0 .5rem 0; color: #eff5ff; font-size: 1.03rem; }
    .info-card p { color: #b5c2d4; line-height: 1.5; margin: 0 0 .4rem 0; }
    .info-card .tag {
        display: inline-block;
        color: #8de5d3;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .04em;
        margin-bottom: .45rem;
    }
    .diagram {
        display: flex;
        align-items: stretch;
        gap: .55rem;
        overflow-x: auto;
        padding: .8rem .1rem 1rem;
    }
    .diagram-node {
        flex: 1 0 145px;
        min-width: 130px;
        border: 1px solid #30445e;
        border-radius: 14px;
        padding: .85rem;
        background: #111d2e;
        transition: border-color .2s, transform .2s, background .2s;
    }
    .diagram-node.active {
        border-color: var(--accent);
        background: linear-gradient(150deg, #193344, #14273a);
        transform: translateY(-3px);
        box-shadow: 0 8px 26px rgba(37, 211, 183, .10);
    }
    .diagram-node .step {
        color: var(--accent);
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
    }
    .diagram-node strong { display: block; color: #f0f5fc; margin: .35rem 0; font-size: .91rem; }
    .diagram-node span { display: block; color: #aebdd0; font-size: .78rem; line-height: 1.4; }
    .diagram-arrow {
        align-self: center;
        color: #7090b4;
        font-size: 1.15rem;
        padding: 0 .05rem;
    }
    .callout {
        border-left: 3px solid var(--accent);
        border-radius: 0 12px 12px 0;
        background: rgba(31, 56, 71, .58);
        padding: .8rem 1rem;
        color: #c4d2e3;
        margin: .5rem 0 1rem;
    }
    .small-note { color: var(--muted); font-size: .82rem; }
    .price-pill {
        display: inline-block;
        border: 1px solid #38506c;
        border-radius: 999px;
        padding: .2rem .55rem;
        color: #c1d7f0;
        font-size: .72rem;
        margin: .1rem .15rem .1rem 0;
    }
    @media (max-width: 760px) {
        .hero h1 { font-size: 1.75rem; }
        .diagram { flex-direction: column; }
        .diagram-node { flex: initial; width: auto; }
        .diagram-arrow { transform: rotate(90deg); align-self: center; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def hero(kicker: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <section class="hero">
            <div class="hero-kicker">{html.escape(kicker)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(description)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def cards(items: list[tuple[str, str, str, str]], columns: int = 3) -> None:
    for start in range(0, len(items), columns):
        row = st.columns(columns)
        for column, item in zip(row, items[start : start + columns]):
            tag, title, description, note = item
            column.markdown(
                f"""
                <article class="info-card">
                    <span class="tag">{html.escape(tag)}</span>
                    <h3>{html.escape(title)}</h3>
                    <p>{html.escape(description)}</p>
                    <p class="small-note">{html.escape(note)}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )


def diagram(
    nodes: list[tuple[str, str]],
    active_step: int,
    key: str,
) -> None:
    parts = ['<div class="diagram" role="img">']
    for index, (title, description) in enumerate(nodes):
        active = " active" if index == active_step else ""
        parts.append(
            f'<div class="diagram-node{active}">'
            f'<span class="step">{index + 1:02d} / {len(nodes):02d}</span>'
            f"<strong>{html.escape(title)}</strong>"
            f"<span>{html.escape(description)}</span></div>"
        )
        if index < len(nodes) - 1:
            parts.append('<div class="diagram-arrow" aria-hidden="true">→</div>')
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)
    options = [f"{i + 1}. {title}" for i, (title, _) in enumerate(nodes)]
    selected = st.selectbox("Explore a diagram step", options, key=key)
    st.caption(nodes[options.index(selected)][1])


def callout(text: str) -> None:
    st.markdown(
        f'<div class="callout">{html.escape(text)}</div>',
        unsafe_allow_html=True,
    )


def source_links(links: list[tuple[str, str]]) -> None:
    st.markdown("**Explore official docs**")
    st.markdown(" · ".join(f"[{label}]({url})" for label, url in links))


def split_preview(text: str, strategy: str, size: int, overlap: int) -> list[str]:
    text = text.strip()
    if not text:
        return []

    if strategy == "Fixed character windows":
        step = max(1, size - overlap)
        return [text[start : start + size].strip() for start in range(0, len(text), step)]

    if strategy == "Sentence bundles":
        units = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    else:
        units = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]

    chunks: list[str] = []
    current = ""
    for unit in units:
        while len(unit) > size:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(unit[:size].strip())
            unit = unit[size:].strip()
        candidate = f"{current}\n\n{unit}".strip() if current else unit
        if current and len(candidate) > size:
            chunks.append(current)
            current = unit
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def render_ingestion() -> None:
    hero(
        "01 / Data foundations",
        "Ingestion, embeddings & vector search",
        "Turn source files into searchable meaning. Follow the path from documents to chunks, vectors, retrieval, and a grounded answer.",
    )

    nodes = [
        ("Source data", "PDF, DOCX, HTML, text, databases, or APIs"),
        ("Parse & clean", "Extract text, normalize it, retain metadata"),
        ("Chunk", "Split content into retrieval-sized passages"),
        ("Embed", "Map each passage to a numeric vector"),
        ("Vector store", "Index vectors plus payload metadata"),
        ("Retrieve", "Embed the question, search, filter, rerank"),
        ("Generate", "Give relevant context to the LLM"),
    ]
    diagram(nodes, 0, "ingestion-step")

    callout(
        "In this project: files are parsed locally; the chunker groups paragraphs with an approximately 1,500-character target; Gemini embeddings are used when reachable; vectors are stored in Qdrant with cosine distance. A local sentence-transformer fallback exists if the initial Gemini probe fails."
    )

    st.subheader("Three building blocks")
    cards(
        [
            (
                "01 / Chunking",
                "A chunk is a passage",
                "Retrieval works on smaller passages instead of feeding an entire book into every prompt. Keep a little context around boundaries when useful.",
                "Common strategies: fixed-size, paragraph/recursive, semantic, and structure-aware (for example, sections or code blocks).",
            ),
            (
                "02 / Embeddings",
                "Meaning as numbers",
                "An embedding model maps text into a vector. Similar meanings tend to land near each other in vector space; the numbers are not human-readable labels.",
                "Common kinds: dense, sparse, hybrid, multimodal, and task-specific embeddings.",
            ),
            (
                "03 / Vector database",
                "Search the vectors",
                "A vector store indexes vectors and metadata, then finds likely-near matches. Filtering and hybrid keyword search improve control and recall.",
                "Approximate nearest-neighbor indexes trade a tiny amount of exactness for much faster search at scale.",
            ),
        ]
    )

    with st.expander("Interactive chunking playground", expanded=True):
        st.caption(
            "This is a local teaching demo, not a call to your production ingestion pipeline."
        )
        sample = (
            "Retrieval-augmented generation combines search with a language model. "
            "The search stage finds relevant evidence before generation.\n\n"
            "Chunk boundaries matter. A passage that is too large can include unrelated ideas; "
            "a passage that is too small can lose context.\n\n"
            "Metadata such as source, page, and document type can be stored alongside each vector."
        )
        demo_text = st.text_area(
            "Text to split",
            value=sample,
            height=130,
            key="chunk-demo-text",
        )
        c1, c2, c3 = st.columns(3)
        strategy = c1.selectbox(
            "Chunk strategy",
            [
                "Paragraph groups (this app's style)",
                "Fixed character windows",
                "Sentence bundles",
            ],
        )
        size = c2.slider("Target characters", 200, 1400, 500, step=100)
        overlap = c3.slider(
            "Overlap (fixed-window demo)",
            0,
            min(300, size // 2),
            min(60, size // 2),
            step=20,
            disabled=strategy != "Fixed character windows",
        )
        preview = split_preview(demo_text, strategy, size, overlap)
        st.metric("Preview chunks", len(preview))
        for index, chunk in enumerate(preview[:8], start=1):
            with st.expander(f"Chunk {index} · {len(chunk)} characters"):
                st.write(chunk)
        if len(preview) > 8:
            st.caption(f"Showing 8 of {len(preview)} chunks.")

    left, right = st.columns([1.1, 1])
    with left:
        st.subheader("Embedding model choice")
        model = st.selectbox(
            "Compare this project's embedding options",
            ["Gemini API · 3,072 dimensions", "Local all-mpnet-base-v2 · 768 dimensions"],
        )
        if model.startswith("Gemini"):
            st.info(
                "Hosted embedding service: convenient, no model server to operate, but requires network access and is subject to provider quota and usage terms."
            )
        else:
            st.info(
                "Open model running on your own machine: no per-request embedding API bill, but you operate the runtime and pay for EC2 CPU/RAM. Its 768-dimensional vectors need a matching Qdrant collection."
            )
        st.caption(
            "Illustration only: a real embedding has hundreds or thousands of values, not the few shown here."
        )
        st.code("text:  'network packet routing'\nvector: [0.12, -0.07, 0.81, ...]", language="text")
    with right:
        st.subheader("Vector database fit")
        database = st.selectbox(
            "Choose a deployment style",
            ["Qdrant (used here)", "PostgreSQL + pgvector", "Pinecone", "Weaviate", "FAISS"],
        )
        descriptions = {
            "Qdrant (used here)": "Open-source option to self-host; managed Qdrant Cloud is a separate hosted offering. Good fit for dedicated vector search and metadata filtering.",
            "PostgreSQL + pgvector": "Extension-based vector search in PostgreSQL. Good when relational data and vectors should share transactions and operations.",
            "Pinecone": "Managed vector database. Useful when a team prefers hosted operations; usage and plan terms are provider-controlled.",
            "Weaviate": "Open-source and managed deployment choices. Supports vector search with structured data and multiple integration patterns.",
            "FAISS": "Open-source similarity-search library, not a full managed database service. Useful for local or embedded search; persistence and service operations are yours.",
        }
        st.write(descriptions[database])

    st.subheader("Free vs. paid: what the labels really mean")
    cards(
        [
            (
                "Self-managed / open source",
                "No software license fee (often)",
                "Qdrant Community, pgvector, Weaviate Community, and FAISS are examples of open-source building blocks.",
                "You still pay for machines, storage, backups, networking, engineering, and any hosted embedding or LLM APIs.",
            ),
            (
                "Managed database",
                "Hosted service",
                "A provider operates availability, scaling, backups, and service upgrades under its plan.",
                "Usually billed by some combination of capacity, storage, requests, or usage. Free tiers and prices change; check current provider terms.",
            ),
            (
                "Enterprise",
                "Controls and support",
                "Organizations may need private networking, SSO, audit controls, support SLAs, or contractual terms.",
                "Often quote- or contract-based. Select based on requirements, not only on a demo's free tier.",
            ),
        ]
    )

    source_links(
        [
            ("Qdrant docs", "https://qdrant.tech/documentation/"),
            ("pgvector", "https://github.com/pgvector/pgvector"),
            ("Pinecone pricing", "https://www.pinecone.io/pricing/"),
            ("Weaviate docs", "https://weaviate.io/developers/weaviate"),
            ("FAISS", "https://github.com/facebookresearch/faiss"),
        ]
    )


def render_guardrails() -> None:
    hero(
        "02 / Safety & policy",
        "Guardrails",
        "Guardrails are checks around an AI system. They help enforce topic, safety, privacy, and business rules before or after a model responds.",
    )

    nodes = [
        ("User request", "Receive text, files, or a tool request"),
        ("Input checks", "Validate, classify, redact, apply policy"),
        ("Decision", "Allow, block, ask for review, or constrain"),
        ("LLM / tools", "Run only the permitted workflow"),
        ("Output checks", "Check format, grounding, safety, data"),
        ("Response", "Return, revise, redact, or escalate"),
    ]
    diagram(nodes, 0, "guardrails-step")

    callout(
        "In this project: NeMo Guardrails runs before the RAG workflow, uses a Groq chat model, and defines sample off-topic, greeting, farewell, and jailbreak-related flows. The app checks whether the returned text contains known refusal phrases. This is a useful demo gate, not a complete security boundary or a separate final-answer validator."
    )

    st.subheader("What can be guarded?")
    cards(
        [
            (
                "Input / topic",
                "Is this request in scope?",
                "Block disallowed topics, route to the right workflow, or ask a clarifying question.",
                "Use for support bots, internal knowledge assistants, and domain-specific agents.",
            ),
            (
                "Safety / abuse",
                "Is the request or answer unsafe?",
                "Apply policy checks to user input and model output. Use calibrated classifiers and human review for high-impact decisions.",
                "A model-based check can help, but should not be the only control for consequential actions.",
            ),
            (
                "Privacy / data",
                "Could sensitive data leak?",
                "Detect or redact sensitive information; enforce access controls before retrieval and before returning data.",
                "Authorization belongs in the application and data layer, not just in a prompt.",
            ),
            (
                "Tools / actions",
                "May the agent take this action?",
                "Constrain tool choices and validate arguments; require confirmation or approval for sensitive actions.",
                "Use least privilege, server-side checks, and auditable approval paths.",
            ),
            (
                "Format / quality",
                "Does the output meet requirements?",
                "Validate schemas, required fields, citations, policy language, or grounding expectations.",
                "Reject, repair, or escalate outputs that fail deterministic checks.",
            ),
        ]
    )

    st.subheader("Try a policy walkthrough")
    scenario = st.selectbox(
        "Choose a sample request",
        [
            "An in-scope Kubernetes question",
            "A clearly out-of-scope request",
            "A request that asks the assistant to ignore its rules",
            "A request asking for sensitive company data",
        ],
        key="guardrail-scenario",
    )
    walkthrough = {
        "An in-scope Kubernetes question": (
            "Illustrative route: input validation → topic policy allows → retrieval and answer generation → output checks.",
            "Allowed to continue",
        ),
        "A clearly out-of-scope request": (
            "Illustrative route: topic policy classifies the request as outside the assistant's scope → return a polite boundary message.",
            "Refuse or redirect",
        ),
        "A request that asks the assistant to ignore its rules": (
            "Illustrative route: instruction hierarchy and policy checks remain in force → do not follow the conflicting instruction.",
            "Block conflicting request",
        ),
        "A request asking for sensitive company data": (
            "Illustrative route: check user authorization at retrieval time → redact or deny protected data → log the policy outcome.",
            "Authorize, redact, or deny",
        ),
    }
    explanation, outcome = walkthrough[scenario]
    c1, c2 = st.columns([1, 2])
    c1.metric("Demo policy outcome", outcome)
    c2.info(explanation)
    st.caption(
        "This walkthrough is an educational simulation. It does not send the sample request to your NeMo service or test your live policies."
    )

    st.subheader("Deployment and cost patterns")
    cards(
        [
            (
                "Open-source framework",
                "Run guard logic yourself",
                "NVIDIA NeMo Guardrails is the framework used by this project; application teams host and configure it.",
                "No separate framework license fee under its open-source license; model inference, compute, and operations may cost money.",
            ),
            (
                "Hosted safety API",
                "Call a provider service",
                "Cloud safety APIs can provide content classification without operating a model server.",
                "Often metered by requests or text volume; availability, regions, and pricing depend on provider and plan.",
            ),
            (
                "Enterprise policy platform",
                "Central controls",
                "Teams may add policy management, audit workflows, dashboards, and support across applications.",
                "May be subscription, usage, or contract priced. Evaluate data handling, latency, coverage, and review needs.",
            ),
        ]
    )

    source_links(
        [
            ("NeMo Guardrails", "https://github.com/NVIDIA/NeMo-Guardrails"),
            ("NeMo docs", "https://docs.nvidia.com/nemo/guardrails/latest/"),
            ("AWS Bedrock Guardrails", "https://aws.amazon.com/bedrock/guardrails/"),
            ("Azure Content Safety pricing", "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/content-safety/"),
        ]
    )


def render_gateways() -> None:
    hero(
        "03 / Model access & routing",
        "LLM gateways",
        "A gateway gives applications one controlled interface to one or more model providers. It can centralize routing, credentials, retries, budgets, and observability.",
    )

    nodes = [
        ("Application", "Your API or agent asks for a model"),
        ("Gateway (optional)", "Authenticate, apply policy, select route"),
        ("Router", "Choose provider, model, or fallback"),
        ("Model provider", "Generate a response"),
        ("Gateway response", "Record usage, errors, latency, cost"),
        ("Application", "Continue the workflow"),
    ]
    diagram(nodes, 0, "gateway-step")

    callout(
        "In this project: Portkey routing and fallback are configured when PORTKEY_API_KEY is available. If it is absent, the planner and responder use Groq directly. Direct mode bypasses Portkey routing, gateway cache, and gateway analytics."
    )

    st.subheader("Common gateway patterns")
    cards(
        [
            (
                "Direct provider SDK",
                "Fewest moving parts",
                "The app calls a provider SDK directly. This is easy to start with and may be the right choice for one provider.",
                "Your app owns provider-specific code, retries, key rotation, and routing logic.",
            ),
            (
                "API-compatible proxy",
                "A shared endpoint",
                "An OpenAI-compatible endpoint can reduce application changes when switching model hosts.",
                "Verify feature compatibility, auth semantics, data handling, and vendor-specific extensions.",
            ),
            (
                "AI gateway / router",
                "Central model controls",
                "Route across providers; apply fallback, limits, caching, logging, and policy centrally.",
                "Adds a service dependency and possibly a hosted usage or subscription cost.",
            ),
        ]
    )

    st.subheader("Choose a routing pattern")
    requirement = st.selectbox(
        "What matters most?",
        [
            "Keep the architecture simple",
            "Recover from provider/model errors",
            "Centralize budgets, logs, and provider policies",
            "Keep a self-hosted control plane",
        ],
        key="gateway-requirement",
    )
    advice = {
        "Keep the architecture simple": (
            "Start with a direct provider SDK. Add a gateway when you have a clear cross-provider or governance requirement.",
            [
                ("App", "Calls one provider SDK"),
                ("Provider", "One model route"),
                ("Answer", "Return to app"),
            ],
        ),
        "Recover from provider/model errors": (
            "Use explicit retries and a tested fallback route. Keep retries bounded and avoid retrying non-retryable errors.",
            [
                ("App", "Sends request"),
                ("Primary", "Try preferred model"),
                ("Fallback", "Retry eligible failures"),
                ("App", "Return result or clear error"),
            ],
        ),
        "Centralize budgets, logs, and provider policies": (
            "Evaluate an AI gateway with per-team credentials, spend controls, routing, and audit support that match your requirements.",
            [
                ("App", "One integration"),
                ("Gateway", "Policy + budget + route"),
                ("Providers", "Approved model pool"),
                ("Logs", "Usage + outcomes"),
            ],
        ),
        "Keep a self-hosted control plane": (
            "Consider a self-hostable proxy/router. Your team then owns upgrades, availability, credential storage, and monitoring.",
            [
                ("App", "Sends request"),
                ("Self-hosted gateway", "Route + policy"),
                ("Provider(s)", "Model calls"),
                ("Team ops", "Own uptime + upgrades"),
            ],
        ),
    }
    explanation, chosen_nodes = advice[requirement]
    st.info(explanation)
    st.markdown("**Reference flow for this choice**")
    diagram(chosen_nodes, 0, "gateway-choice-step")

    st.subheader("Free vs. paid gateway options")
    cards(
        [
            (
                "Build it yourself",
                "Open source / self-host",
                "Examples include LiteLLM Proxy and other open-source proxies. Useful when you want control and can operate the service.",
                "Software may have no license fee; infrastructure, engineering, monitoring, and model-provider usage still cost money.",
            ),
            (
                "Managed gateway",
                "Hosted SaaS",
                "A provider operates the gateway and may offer analytics, policy features, and integrations.",
                "Plans may combine free tiers, usage billing, or subscriptions. Check current limits, retention, and data-processing terms.",
            ),
            (
                "Enterprise platform",
                "Contract and support",
                "May add organization controls, SSO, audit features, SLAs, and dedicated support.",
                "Often priced by usage or contract. Confirm which features are included before designing around them.",
            ),
        ]
    )
    source_links(
        [
            ("Portkey docs", "https://portkey.ai/docs"),
            ("Portkey pricing", "https://portkey.ai/pricing"),
            ("LiteLLM docs", "https://docs.litellm.ai/"),
            ("Groq pricing", "https://groq.com/pricing/"),
        ]
    )


with st.sidebar:
    st.markdown("## 🧭 AI Systems Guide")
    st.caption("An interactive field guide to the pieces behind a production AI app.")
    section = st.radio(
        "Choose a section",
        ["Ingestion", "Guardrails", "Gateways"],
        index=0,
        key="guide-section",
    )
    st.divider()
    st.markdown("### Your project, at a glance")
    st.caption("Ingestion: paragraph chunks → embeddings → Qdrant")
    st.caption("Safety: NeMo Guardrails + Groq")
    st.caption("Model calls: direct Groq if Portkey is not configured")
    st.markdown(
        '<span class="price-pill">Diagrams</span>'
        '<span class="price-pill">Interactive demos</span>'
        '<span class="price-pill">Cost models</span>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Provider plans, free tiers, and prices change. Use linked official pages for current terms."
    )

if section == "Ingestion":
    render_ingestion()
elif section == "Guardrails":
    render_guardrails()
else:
    render_gateways()

st.divider()
st.caption(
    "Architecture notes are educational, not vendor endorsements. Validate security, privacy, licensing, availability, and pricing against your organization's requirements."
)
