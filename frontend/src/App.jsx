import { useMemo, useState } from "react";
import "./App.css";

const initialCases = [
  {
    id: "KYC-1001",
    name: "Arben Krasniqi",
    type: "Individual",
    purpose: "Personal account",
    status: "In Review",
    risk: "Medium",
    updated: "12 Oct 2026",
    missing: 1,
  },
  {
    id: "KYC-1002",
    name: "Elira Berisha",
    type: "Individual",
    purpose: "Salary payments",
    status: "Pending",
    risk: "Low",
    updated: "12 Oct 2026",
    missing: 2,
  },
  {
    id: "KYC-1003",
    name: "Dardan Gashi",
    type: "Individual",
    purpose: "Business activity",
    status: "In Review",
    risk: "High",
    updated: "11 Oct 2026",
    missing: 0,
  },
  {
    id: "KYC-1004",
    name: "Lira Studio LLC",
    type: "Business",
    purpose: "Business account",
    status: "Completed",
    risk: "Low",
    updated: "10 Oct 2026",
    missing: 0,
  },
  {
    id: "KYC-1005",
    name: "Besnik Hoxha",
    type: "Individual",
    purpose: "International transfers",
    status: "Pending",
    risk: "Medium",
    updated: "09 Oct 2026",
    missing: 3,
  },
];

const navigation = [
  { label: "Dashboard", icon: "◫" },
  { label: "Cases", icon: "▤" },
  { label: "Review Checklist", icon: "☑" },
  { label: "Knowledge Base", icon: "▧" },
];

function App() {
  const [cases, setCases] = useState(initialCases);
  const [activePage, setActivePage] = useState("Dashboard");
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [selectedCase, setSelectedCase] = useState(null);

  const filteredCases = useMemo(() => {
    return cases.filter((item) => {
      const query = search.toLowerCase();

      const matchesSearch =
        item.name.toLowerCase().includes(query) ||
        item.id.toLowerCase().includes(query) ||
        item.purpose.toLowerCase().includes(query);

      const matchesStatus =
        statusFilter === "All" || item.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [cases, search, statusFilter]);

  const stats = [
    {
      label: "Total cases",
      value: cases.length,
      detail: "All registered cases",
      icon: "▤",
      color: "blue",
    },
    {
      label: "Pending reviews",
      value: cases.filter((item) => item.status === "Pending").length,
      detail: "Awaiting review",
      icon: "◷",
      color: "amber",
    },
    {
      label: "Missing information",
      value: cases.filter((item) => item.missing > 0).length,
      detail: "Cases requiring attention",
      icon: "!",
      color: "red",
    },
    {
      label: "Completed",
      value: cases.filter((item) => item.status === "Completed").length,
      detail: "Reviews marked complete",
      icon: "✓",
      color: "green",
    },
  ];

  function changeStatus(caseId, status) {
    setCases((previous) =>
      previous.map((item) =>
        item.id === caseId ? { ...item, status } : item,
      ),
    );

    setSelectedCase((previous) =>
      previous?.id === caseId ? { ...previous, status } : previous,
    );
  }

  function navigate(page) {
    setActivePage(page);
    setSelectedCase(null);
    setStatusFilter("All");
    setSearch("");
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">C</div>
          <div className="brand-copy">
            <strong>Compliance</strong>
            <span>Copilot</span>
          </div>
        </div>

        <div className="workspace-label">WORKSPACE</div>

        <nav className="navigation">
          {navigation.map((item) => (
            <button
              key={item.label}
              className={`nav-item ${
                activePage === item.label ? "active" : ""
              }`}
              onClick={() => navigate(item.label)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
              {item.label === "Cases" && (
                <span className="nav-count">{cases.length}</span>
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="environment-card">
            <span className="environment-dot" />
            <div>
              <strong>Development mode</strong>
              <span>Fictional data only</span>
            </div>
          </div>

          <button
            className={`nav-item ${
              activePage === "Settings" ? "active" : ""
            }`}
            onClick={() => navigate("Settings")}
          >
            <span className="nav-icon">⚙</span>
            <span>Settings</span>
          </button>

          <div className="profile">
            <div className="avatar">CC</div>
            <div className="profile-info">
              <strong>Compliance User</strong>
              <span>Local workspace</span>
            </div>
            <span className="profile-menu">···</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> {selectedCase ? selectedCase.id : activePage}
          </div>

          <div className="topbar-right">
            <span className="demo-badge">
              <span /> DEMO ENVIRONMENT
            </span>
            <div className="top-avatar">CC</div>
          </div>
        </header>

        <div className="page-content">
          {selectedCase ? (
            <CaseDetail
              selectedCase={selectedCase}
              onBack={() => setSelectedCase(null)}
              onChangeStatus={changeStatus}
            />
          ) : activePage === "Dashboard" || activePage === "Cases" ? (
            <>
              <section className="page-heading">
                <div>
                  <div className="eyebrow">COMPLIANCE WORKSPACE</div>
                  <h1>
                    {activePage === "Dashboard"
                      ? "Review overview"
                      : "KYC case management"}
                  </h1>
                  <p>
                    {activePage === "Dashboard"
                      ? "Monitor review progress and identify cases requiring attention."
                      : "Search, filter, and inspect your KYC review cases."}
                  </p>
                </div>

                <button
                  className="primary-button"
                  onClick={() => {
                    const newCase = {
                      id: `KYC-${1001 + cases.length}`,
                      name: "New fictional client",
                      type: "Individual",
                      purpose: "Not specified",
                      status: "Pending",
                      risk: "Unassessed",
                      updated: "12 Oct 2026",
                      missing: 5,
                    };

                    setCases((previous) => [...previous, newCase]);
                    setActivePage("Cases");
                    setSelectedCase(newCase);
                  }}
                >
                  <span>＋</span> New case
                </button>
              </section>

              {activePage === "Dashboard" && (
                <section className="stats-grid">
                  {stats.map((stat) => (
                    <div className="stat-card" key={stat.label}>
                      <div className="stat-top">
                        <span>{stat.label}</span>
                        <span className={`stat-icon ${stat.color}`}>
                          {stat.icon}
                        </span>
                      </div>
                      <div className="stat-value">{stat.value}</div>
                      <div className="stat-detail">{stat.detail}</div>
                    </div>
                  ))}
                </section>
              )}

              <section className="section-heading">
                <div>
                  <h2>
                    {activePage === "Dashboard"
                      ? "Recent cases"
                      : "All cases"}
                  </h2>
                  <p>
                    {filteredCases.length} case
                    {filteredCases.length !== 1 ? "s" : ""} shown
                  </p>
                </div>

                <button
                  className="text-button"
                  onClick={() => navigate("Cases")}
                >
                  View all cases <span>→</span>
                </button>
              </section>

              <section className="case-panel">
                <div className="table-toolbar">
                  <div className="search-box">
                    <span>⌕</span>
                    <input
                      value={search}
                      onChange={(event) => setSearch(event.target.value)}
                      placeholder="Search by client or case ID..."
                      aria-label="Search cases"
                    />
                    {search && (
                      <button onClick={() => setSearch("")}>×</button>
                    )}
                  </div>

                  <select
                    value={statusFilter}
                    onChange={(event) => setStatusFilter(event.target.value)}
                    aria-label="Filter by status"
                  >
                    <option value="All">All statuses</option>
                    <option value="Pending">Pending</option>
                    <option value="In Review">In Review</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>

                <div className="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>CLIENT / CASE ID</th>
                        <th>PURPOSE</th>
                        <th>STATUS</th>
                        <th>RISK</th>
                        <th>MISSING INFO</th>
                        <th>LAST UPDATED</th>
                        <th />
                      </tr>
                    </thead>

                    <tbody>
                      {filteredCases.map((item) => (
                        <tr key={item.id}>
                          <td>
                            <button
                              className="client-cell"
                              onClick={() => setSelectedCase(item)}
                            >
                              <span className="client-avatar">
                                {item.name
                                  .split(" ")
                                  .map((part) => part[0])
                                  .slice(0, 2)
                                  .join("")}
                              </span>
                              <span>
                                <strong>{item.name}</strong>
                                <small>{item.id}</small>
                              </span>
                            </button>
                          </td>
                          <td>
                            <span className="purpose-text">
                              {item.purpose}
                            </span>
                          </td>
                          <td>
                            <StatusBadge status={item.status} />
                          </td>
                          <td>
                            <RiskBadge risk={item.risk} />
                          </td>
                          <td>
                            {item.missing > 0 ? (
                              <span className="missing-count">
                                {item.missing} item
                                {item.missing !== 1 ? "s" : ""}
                              </span>
                            ) : (
                              <span className="none-missing">None</span>
                            )}
                          </td>
                          <td className="date-cell">{item.updated}</td>
                          <td>
                            <button
                              className="row-action"
                              onClick={() => setSelectedCase(item)}
                              aria-label={`Open ${item.id}`}
                            >
                              →
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>

                  {filteredCases.length === 0 && (
                    <div className="empty-state">
                      <div>⌕</div>
                      <strong>No matching cases</strong>
                      <p>Try changing your search or status filter.</p>
                    </div>
                  )}
                </div>

                <div className="table-footer">
                  <span>
                    Showing {filteredCases.length} of {cases.length} cases
                  </span>
                  <span>Fictional sample data</span>
                </div>
              </section>

              <div className="notice">
                <span className="notice-icon">i</span>
                <p>
                  <strong>Decision support only.</strong> Risk labels and
                  statuses are fictional examples. All actual compliance
                  decisions require evidence and authorized human review.
                </p>
              </div>
            </>
          ) : (
            <PlaceholderPage page={activePage} />
          )}
        </div>
      </main>
    </div>
  );
}

function StatusBadge({ status }) {
  const className = status.toLowerCase().replace(" ", "-");

  return (
    <span className={`status-badge ${className}`}>
      <span />
      {status}
    </span>
  );
}

function RiskBadge({ risk }) {
  const className = risk.toLowerCase();

  return (
    <span className={`risk-badge ${className}`}>
      <span />
      {risk}
    </span>
  );
}

function CaseDetail({ selectedCase, onBack, onChangeStatus }) {
  const [notes, setNotes] = useState("");
  const [savedNotes, setSavedNotes] = useState("");

  const checklist = [
    "Identity information verified",
    "Occupation and account purpose documented",
    "Source of funds assessed",
    "Screening results reviewed",
    "Expected account activity documented",
  ];

  const [checkedItems, setCheckedItems] = useState([]);

  return (
    <>
      <section className="page-heading">
        <div>
          <button className="back-button" onClick={onBack}>
            ← Back to cases
          </button>
          <div className="eyebrow">CASE REVIEW / {selectedCase.id}</div>
          <h1>{selectedCase.name}</h1>
          <p>Fictional client · {selectedCase.type}</p>
        </div>

        <StatusBadge status={selectedCase.status} />
      </section>

      <div className="detail-grid">
        <section className="detail-card">
          <h2>Case information</h2>
          <p className="card-subtitle">Basic case details</p>

          <DetailRow label="Case ID" value={selectedCase.id} />
          <DetailRow label="Client type" value={selectedCase.type} />
          <DetailRow label="Account purpose" value={selectedCase.purpose} />
          <DetailRow label="Current status" value={selectedCase.status} />
          <DetailRow label="Risk assessment" value={selectedCase.risk} />
          <DetailRow
            label="Missing information"
            value={`${selectedCase.missing} item(s)`}
          />

          <div className="detail-divider" />

          <label className="field-label" htmlFor="case-status">
            Update case status
          </label>
          <select
            id="case-status"
            className="full-select"
            value={selectedCase.status}
            onChange={(event) =>
              onChangeStatus(selectedCase.id, event.target.value)
            }
          >
            <option value="Pending">Pending</option>
            <option value="In Review">In Review</option>
            <option value="Completed">Completed</option>
          </select>
          <p className="field-help">
            Status changes are stored in local page state only.
          </p>
        </section>

        <section className="detail-card">
          <h2>Review checklist</h2>
          <p className="card-subtitle">
            Track evidence reviewed for this case.
          </p>

          <div className="checklist">
            {checklist.map((item, index) => (
              <label className="checklist-item" key={item}>
                <input
                  type="checkbox"
                  checked={checkedItems.includes(index)}
                  onChange={() =>
                    setCheckedItems((previous) =>
                      previous.includes(index)
                        ? previous.filter((value) => value !== index)
                        : [...previous, index],
                    )
                  }
                />
                <span>{item}</span>
              </label>
            ))}
          </div>

          <div className="checklist-progress">
            <div>
              <span>Checklist progress</span>
              <strong>{checkedItems.length}/5</strong>
            </div>
            <div className="progress-track">
              <div
                style={{ width: `${(checkedItems.length / 5) * 100}%` }}
              />
            </div>
          </div>
        </section>

        <section className="detail-card notes-card">
          <h2>Review notes</h2>
          <p className="card-subtitle">
            Record observations supported by available evidence.
          </p>

          <textarea
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
            placeholder="Enter fictional review notes..."
            rows={5}
          />

          <div className="notes-actions">
            {savedNotes && <span>Notes saved locally in this view.</span>}
            <button
              className="primary-button"
              onClick={() => setSavedNotes(notes)}
            >
              Save notes
            </button>
          </div>

          {savedNotes && (
            <div className="saved-note">
              <strong>Saved note</strong>
              <p>{savedNotes || "No note content entered."}</p>
            </div>
          )}
        </section>
      </div>
    </>
  );
}

function DetailRow({ label, value }) {
  return (
    <div className="detail-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function PlaceholderPage({ page }) {
  const descriptions = {
    "Review Checklist":
      "A reusable checklist for consistent KYC and AML reviews.",
    "Knowledge Base":
      "A future home for approved procedures, guidance, and internal reference material.",
    Settings:
      "Application preferences and environment configuration.",
  };

  return (
    <section className="placeholder-page">
      <div className="placeholder-icon">▧</div>
      <div className="eyebrow">COMPLIANCE WORKSPACE</div>
      <h1>{page}</h1>
      <p>
        {descriptions[page] || "This workspace is being prepared."}
      </p>
      <span className="coming-soon">PLANNED FEATURE</span>
    </section>
  );
}

export default App;