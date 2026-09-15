function Header() {
  return (
    <header className="topbar">
      <div>
        <h2>Document Intelligence</h2>

        <p>
          Ask questions and get answers grounded in
          your documents.
        </p>
      </div>

      <div className="status-badge">
        <span className="status-dot"></span>
        Ready
      </div>
    </header>
  );
}

export default Header;