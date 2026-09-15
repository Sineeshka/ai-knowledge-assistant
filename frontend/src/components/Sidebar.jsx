function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">✦</div>

        <div>
          <h1>AI Assistant</h1>
          <span>Knowledge workspace</span>
        </div>
      </div>

      <div className="sidebar-section">
        <p className="sidebar-label">
          DOCUMENTS
        </p>

        <div className="sidebar-item active">
          <span>▣</span>
          Document Q&A
        </div>
      </div>

      <div className="sidebar-bottom">
        <div className="status-dot"></div>
        <span>AI system ready</span>
      </div>
    </aside>
  );
}

export default Sidebar;