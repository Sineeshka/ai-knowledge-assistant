function QuestionBox({
  question,
  loading,
  onQuestionChange,
  onAsk,
  onKeyDown,
}) {
  return (
    <section className="card ask-card">

      <div className="section-heading">
        <div className="section-icon">
          ?
        </div>

        <div>
          <h3>Ask your documents</h3>

          <p>
            Ask a question using natural language.
          </p>
        </div>
      </div>

      <div className="question-box">

        <textarea
          value={question}
          onChange={onQuestionChange}
          onKeyDown={onKeyDown}
          placeholder="What would you like to know?"
          rows="2"
        />

        <button
          className="ask-button"
          onClick={onAsk}
          disabled={loading || !question.trim()}
        >
          {loading ? (
            "Thinking..."
          ) : (
            <>
              Ask
              <span>→</span>
            </>
          )}
        </button>

      </div>

      <div className="hint">
        Press <strong>Enter</strong> to ask
      </div>

    </section>
  );
}

export default QuestionBox;