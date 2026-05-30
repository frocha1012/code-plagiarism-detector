const steps = [
  "Uploading files",
  "Generating embeddings",
  "Comparing submissions",
  "Calculating similarity scores",
  "Preparing results",
];

export default function AnalysisLoader({ currentStep = 0, progress = 0 }) {
  const visibleProgress = Math.min(Math.max(progress, 0), 100);

  return (
    <section className="page-card analysis-screen" role="status" aria-live="polite">
      <div className="analysis-loader">
        <div
          className="progress-ring progress-ring-fill"
          style={{ "--progress": `${visibleProgress}%` }}
          aria-hidden="true"
        >
          <span>{Math.round(visibleProgress)}%</span>
        </div>
        <div>
          <p className="eyebrow">AI analysis running</p>
          <h1>Analyzing submissions</h1>
          <p>
            CodeBERT is generating embeddings and comparing uploaded source
            files. Results will appear automatically.
          </p>
        </div>
      </div>

      <ol className="analysis-steps">
        {steps.map((step, index) => {
          const status =
            index < currentStep ? "completed" : index === currentStep ? "active" : "pending";

          return (
            <li className={status} key={step}>
              <span>{index < currentStep ? "✓" : index + 1}</span>
              {step}
            </li>
          );
        })}
      </ol>
    </section>
  );
}
