function UploadDocument({
  file,
  uploading,
  uploadMessage,
  onFileChange,
  onUpload,
}) {
  return (
    <section className="card upload-card">

      <div className="section-heading">
        <div className="section-icon">
          ↑
        </div>

        <div>
          <h3>Upload a document</h3>

          <p>
            Add a PDF to your knowledge base.
          </p>
        </div>
      </div>

      <div className="upload-area">

        <div className="upload-icon">
          ↑
        </div>

        <div className="upload-text">
          <strong>
            Choose a PDF document
          </strong>

          <span>
            Your document will be processed and
            indexed for questions.
          </span>
        </div>

        <div className="upload-controls">

          <label className="file-button">
            Choose PDF

            <input
              type="file"
              accept=".pdf"
              onChange={onFileChange}
            />
          </label>

          <button
            className="primary-button"
            onClick={onUpload}
            disabled={uploading}
          >
            {uploading
              ? "Processing..."
              : "Upload"}
          </button>

        </div>

      </div>

      {file && (
        <div className="selected-file">
          <span>📄</span>
          <span>{file.name}</span>
        </div>
      )}

      {uploadMessage && (
        <div className="upload-message">
          {uploadMessage}
        </div>
      )}

    </section>
  );
}

export default UploadDocument;