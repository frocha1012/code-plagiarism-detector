import { useEffect, useState } from "react";
import { getMeta } from "../services/api";

const PIPELINE_STEPS = [
  {
    title: "Upload Files / ZIP / GitHub Repositories",
    detail: "Submit individual source files, a ZIP archive, or two public repositories.",
  },
  {
    title: "Source Code Processing",
    detail: "Files are validated, decoded, and prepared for analysis.",
  },
  {
    title: "CodeBERT Embeddings",
    detail: "Each file is encoded into a semantic vector representation.",
  },
  {
    title: "Lexical Similarity Analysis",
    detail: "Token- and identifier-level overlap is measured.",
  },
  {
    title: "Hybrid Similarity Scoring",
    detail: "Semantic and lexical signals are combined into a single score.",
  },
  {
    title: "Risk Classification",
    detail: "Each pair is labelled high, medium, or low risk.",
  },
  {
    title: "AI Explanation (Ollama)",
    detail: "An optional model summarises why two files appear related.",
  },
  {
    title: "Analysis Results",
    detail: "Findings are presented for human review and export.",
  },
];

const TECH_STACK = [
  {
    group: "Frontend",
    accent: "blue",
    items: ["React", "Vite", "Tauri"],
  },
  {
    group: "Backend",
    accent: "green",
    items: ["FastAPI", "Python"],
  },
  {
    group: "AI",
    accent: "purple",
    items: ["CodeBERT", "Ollama"],
  },
  {
    group: "Analysis",
    accent: "cyan",
    items: ["Cosine Similarity", "Hybrid Scoring"],
  },
  {
    group: "Reports",
    accent: "amber",
    items: ["ReportLab"],
  },
];

const FUTURE_WORK = [
  {
    title: "Additional Embedding Models",
    detail: "Support alternative and newer code embedding models for richer analysis.",
  },
  {
    title: "Cross-Language Detection",
    detail: "Detect plagiarism across different programming languages.",
  },
  {
    title: "Teacher Dashboard",
    detail: "A dedicated workspace to manage cohorts and review submissions at scale.",
  },
  {
    title: "Authentication",
    detail: "User accounts and role-based access for institutional deployment.",
  },
  {
    title: "Large-Scale Repository Analysis",
    detail: "Batch comparison across many repositories and submissions.",
  },
  {
    title: "Enhanced AI-Assisted Review",
    detail: "Deeper, more structured AI insights to speed up manual review.",
  },
];

const LIMITATIONS = [
  "Similarity scores are indicators only.",
  "Common programming patterns may produce similarities.",
  "Small source files may generate less reliable results.",
  "Human review is always recommended.",
  "The system is designed to assist academic review rather than replace it.",
];

function SectionHeader({ eyebrow, title, lead }) {
  return (
    <div className="about-section-head">
      <p className="eyebrow">{eyebrow}</p>
      <h2 className="about-section-title">{title}</h2>
      {lead && <p className="about-section-lead">{lead}</p>}
    </div>
  );
}

export default function AboutPage() {
  const [meta, setMeta] = useState(null);
  const [metaError, setMetaError] = useState(false);

  useEffect(() => {
    let active = true;
    getMeta()
      .then((data) => {
        if (active) setMeta(data);
      })
      .catch(() => {
        if (active) setMetaError(true);
      });
    return () => {
      active = false;
    };
  }, []);

  // Thresholds come from backend config.py (HIGH/MEDIUM_SIMILARITY_THRESHOLD).
  // Fall back to documented defaults only if the API is unreachable.
  const high = meta?.thresholds?.high ?? 85;
  const medium = meta?.thresholds?.medium ?? 78;
  const fmt = (n) => `${Number(n).toFixed(Number.isInteger(n) ? 0 : 1)}%`;

  const stats = meta?.statistics;

  return (
    <section className="page-card about-page">
      {/* SECTION 1 — PROJECT OVERVIEW */}
      <header className="about-hero">
        <p className="eyebrow">About &amp; Methodology</p>
        <h1>Code Plagiarism Detector</h1>
        <p className="about-subtitle">
          AI-powered source code similarity analysis using semantic embeddings
          and hybrid scoring techniques.
        </p>
        <div className="about-overview">
          <p>
            The Code Plagiarism Detector analyses source code submissions to
            surface meaningful similarities between them. It combines
            transformer-based semantic embeddings with lexical analysis to
            produce a hybrid similarity score, then classifies each comparison
            by risk level so reviewers can focus their attention where it
            matters most.
          </p>
          <p>
            The tool exists to make academic integrity reviews faster and more
            consistent. In coursework and lab settings, manually comparing many
            submissions is slow and error-prone — this application highlights
            the pairs most worth a closer look.
          </p>
          <p className="about-disclaimer-line">
            Crucially, this system <strong>assists human reviewers</strong> and
            does <strong>not</strong> automatically determine plagiarism. Every
            result is an indicator intended to support — never replace — a
            human judgement.
          </p>
        </div>
        <div className="feature-chips about-hero-chips">
          <span>Semantic Embeddings</span>
          <span>Hybrid Scoring</span>
          <span>Risk Classification</span>
          <span>AI Explanations</span>
        </div>
      </header>

      {/* SECTION 2 — HOW ANALYSIS WORKS */}
      <div className="about-section">
        <SectionHeader
          eyebrow="The Pipeline"
          title="How Analysis Works"
          lead="Every comparison moves through the same transparent sequence of stages."
        />
        <ol className="pipeline-flow">
          {PIPELINE_STEPS.map((step, index) => (
            <li className="pipeline-block" key={step.title}>
              <div className="pipeline-card">
                <span className="pipeline-index">{index + 1}</span>
                <div>
                  <h3>{step.title}</h3>
                  <p>{step.detail}</p>
                </div>
              </div>
              {index < PIPELINE_STEPS.length - 1 && (
                <span className="pipeline-arrow" aria-hidden="true">
                  ↓
                </span>
              )}
            </li>
          ))}
        </ol>
      </div>

      {/* SECTION 3 — SIMILARITY LEVELS */}
      <div className="about-section">
        <SectionHeader
          eyebrow="Risk Levels"
          title="Similarity Levels"
          lead={
            metaError
              ? "Thresholds reflect documented defaults (backend unavailable)."
              : "Thresholds are read live from the backend configuration."
          }
        />
        <div className="risk-grid">
          <article className="risk-level-card high">
            <div className="risk-level-top">
              <span className="risk-badge high">High Risk</span>
              <span className="risk-threshold">{fmt(high)}+</span>
            </div>
            <p>
              Strong semantic and lexical similarity detected. Manual review
              strongly recommended.
            </p>
          </article>
          <article className="risk-level-card medium">
            <div className="risk-level-top">
              <span className="risk-badge medium">Medium Risk</span>
              <span className="risk-threshold">
                {fmt(medium)} – {fmt(high)}
              </span>
            </div>
            <p>
              Partial structural or logical similarity detected. Manual review
              recommended.
            </p>
          </article>
          <article className="risk-level-card low">
            <div className="risk-level-top">
              <span className="risk-badge low">Low Risk</span>
              <span className="risk-threshold">Below {fmt(medium)}</span>
            </div>
            <p>
              Limited similarity detected. Likely unrelated implementations.
            </p>
          </article>
        </div>
      </div>

      {/* SECTION 4 — SCORING METHODOLOGY */}
      <div className="about-section">
        <SectionHeader
          eyebrow="Methodology"
          title="Scoring Methodology"
          lead="Two complementary signals are combined for a more reliable result."
        />
        <div className="method-grid">
          <article className="method-card">
            <span className="method-step">1</span>
            <h3>CodeBERT Semantic Analysis</h3>
            <p className="method-tag">Semantic Similarity</p>
            <p>Measures similarity of logic and structure.</p>
          </article>
          <article className="method-card">
            <span className="method-step">2</span>
            <h3>Lexical Similarity Analysis</h3>
            <p className="method-tag">Lexical Similarity</p>
            <p>Measures similarity of code tokens and identifiers.</p>
          </article>
          <article className="method-card">
            <span className="method-step">3</span>
            <h3>Hybrid Similarity Scoring</h3>
            <p className="method-tag">Hybrid Score</p>
            <p>Combines both approaches to improve reliability.</p>
          </article>
        </div>
        <div className="info-callout">
          <span className="info-callout-icon" aria-hidden="true">
            i
          </span>
          <p>
            Similarity scores are <strong>indicators</strong> and{" "}
            <strong>not proof of plagiarism</strong>. They are designed to guide
            a reviewer toward submissions that deserve closer inspection.
          </p>
        </div>
      </div>

      {/* SECTION 5 — AI EXPLANATIONS */}
      <div className="about-section">
        <SectionHeader
          eyebrow="Explainability"
          title="AI Explanations"
          lead="An optional Ollama model adds human-readable context to each comparison."
        />
        <div className="about-prose">
          <p>
            When enabled, the application integrates a locally-run{" "}
            <strong>Ollama</strong> language model to generate plain-language
            explanations of why two files appear similar. This runs on demand
            and keeps source code on your own machine.
          </p>
        </div>
        <div className="ai-feature-grid">
          <div className="ai-feature">
            <h3>AI-Generated Explanations</h3>
            <p>Concise, readable summaries of each flagged comparison.</p>
          </div>
          <div className="ai-feature">
            <h3>Structural Similarity Detection</h3>
            <p>Highlights shared control flow and code organisation.</p>
          </div>
          <div className="ai-feature">
            <h3>Variable Renaming Detection</h3>
            <p>Spots logic that has been preserved despite renamed identifiers.</p>
          </div>
          <div className="ai-feature">
            <h3>Logic Preservation Detection</h3>
            <p>Identifies equivalent algorithms expressed in different ways.</p>
          </div>
        </div>
        <div className="info-callout warning">
          <span className="info-callout-icon" aria-hidden="true">
            !
          </span>
          <p>
            AI explanations assist reviewers and should not be treated as
            definitive conclusions.
          </p>
        </div>
      </div>

      {/* SECTION 6 — TECHNOLOGY STACK */}
      <div className="about-section">
        <SectionHeader
          eyebrow="Built With"
          title="Technology Stack"
          lead="A modern, fully local-capable toolchain across the whole pipeline."
        />
        <div className="tech-grid">
          {TECH_STACK.map((category) => (
            <article
              className={`tech-group-card accent-${category.accent}`}
              key={category.group}
            >
              <h3>{category.group}</h3>
              <div className="tech-badges">
                {category.items.map((item) => (
                  <span className="tech-badge" key={item}>
                    {item}
                  </span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </div>

      {/* SECTION 7 — LIMITATIONS */}
      <div className="about-section">
        <SectionHeader
          eyebrow="Honest Boundaries"
          title="Limitations"
          lead="Understanding what the system cannot do is part of using it responsibly."
        />
        <div className="limitations-grid">
          {LIMITATIONS.map((item) => (
            <div className="limitation-card" key={item}>
              <span className="limitation-icon" aria-hidden="true">
                !
              </span>
              <p>{item}</p>
            </div>
          ))}
        </div>
      </div>

      {/* SECTION 8 — FUTURE WORK */}
      <div className="about-section">
        <SectionHeader
          eyebrow="Roadmap"
          title="Future Improvements"
          lead="Directions we would explore to extend the project further."
        />
        <div className="roadmap-grid">
          {FUTURE_WORK.map((item) => (
            <article className="roadmap-card" key={item.title}>
              <span className="roadmap-dot" aria-hidden="true" />
              <h3>{item.title}</h3>
              <p>{item.detail}</p>
            </article>
          ))}
        </div>
      </div>

      {/* SECTION 9 — PROJECT STATISTICS */}
      <div className="about-section">
        <SectionHeader
          eyebrow="By The Numbers"
          title="Project Statistics"
          lead="Aggregated from your saved analysis history on this machine."
        />
        <div className="stats-grid">
          <article className="stat-card">
            <span className="stat-label">Total Analyses Performed</span>
            <strong className="stat-value">
              {stats ? stats.total_analyses.toLocaleString() : "—"}
            </strong>
          </article>
          <article className="stat-card">
            <span className="stat-label">Total Files Analyzed</span>
            <strong className="stat-value">
              {stats ? stats.total_files.toLocaleString() : "—"}
            </strong>
          </article>
          <article className="stat-card optional">
            <span className="stat-label">
              Total Reports Generated
              <span className="stat-optional-tag">Optional</span>
            </span>
            <strong className="stat-value">—</strong>
            <span className="stat-note">Not currently tracked</span>
          </article>
        </div>
        {metaError && (
          <p className="stats-fallback-note">
            Live statistics are unavailable — the backend could not be reached.
          </p>
        )}
      </div>

      <footer className="about-footer">
        <p>
          This tool is an academic aid. Final decisions about academic integrity
          always rest with a human reviewer.
        </p>
      </footer>
    </section>
  );
}
