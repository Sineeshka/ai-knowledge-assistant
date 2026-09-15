function SourceList({ sources }) {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <section className="card sources-card">

      <div className="result-heading">

        <div>
          <span className="result-label">
            SOURCES
          </span>

          <h3>
            Referenced documents
          </h3>
        </div>

        <span className="source-count">
          {sources.length}
        </span>

      </div>

      <div className="sources-list">

        {sources.map((source) => (
          <div
            className="source-item"
            key={source.chunk_id}
          >

            <div className="source-icon">
              📄
            </div>

            <div className="source-info">

              <strong>
                {source.filename}
              </strong>

              <span>
                Page {source.page_number}
              </span>

            </div>

          </div>
        ))}

      </div>

    </section>
  );
}

export default SourceList;