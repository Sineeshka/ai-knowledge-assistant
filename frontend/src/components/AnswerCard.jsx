function AnswerCard({ answer }) {
  if (!answer) {
    return null;
  }

  return (
    <section className="card answer-card">

      <div className="result-heading">
        <div>
          <span className="result-label">
            ANSWER
          </span>

          <h3>AI Response</h3>
        </div>
      </div>

      <div className="answer-content">
        {answer}
      </div>

    </section>
  );
}

export default AnswerCard;