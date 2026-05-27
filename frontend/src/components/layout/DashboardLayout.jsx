import Sidebar from './Sidebar';
import './DashboardLayout.css';

/**
 * Main dashboard layout with fixed sidebar and scrollable content area.
 */
export default function DashboardLayout({ tabs, activeTab, onTabChange, children }) {
  const activeLabel = activeTab === 'confidential' 
    ? 'Área Restrita' 
    : (tabs.find(t => t.id === activeTab)?.label || '');

  return (
    <div className="dashboard-layout">
      <Sidebar tabs={tabs} activeTab={activeTab} onTabChange={onTabChange} />

      <div className="dashboard-main">
        <header className="dashboard-header">
          <h2 className="dashboard-header__title">{activeLabel}</h2>
        </header>

        <main className="dashboard-content" role="tabpanel">
          {children}
        </main>
      </div>
    </div>
  );
}
