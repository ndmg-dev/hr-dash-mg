import * as Icons from 'react-feather';
import './Sidebar.css';

/**
 * Vertical sidebar navigation with logo, title, and Feather icon links.
 */
export default function Sidebar({ tabs, activeTab, onTabChange }) {
  const getIcon = (iconName) => {
    const Icon = Icons[iconName];
    return Icon ? <Icon size={18} strokeWidth={1.8} /> : null;
  };

  return (
    <aside className="sidebar" role="navigation" aria-label="Menu principal">
      {/* Brand */}
      <div className="sidebar__brand">
        <img src="/logo.png" alt="Mendonça Galvão" className="sidebar__logo" />
        <div className="sidebar__title-group">
          <h1 className="sidebar__title">HR Analytics</h1>
          <span className="sidebar__subtitle">Painel de Expectativas</span>
        </div>
      </div>

      <div className="sidebar__divider" />

      {/* Navigation */}
      <nav className="sidebar__nav">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            id={`nav-${tab.id}`}
            className={`sidebar__item ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => onTabChange(tab.id)}
            aria-current={activeTab === tab.id ? 'page' : undefined}
          >
            <span className="sidebar__item-icon">
              {getIcon(tab.icon)}
            </span>
            <span className="sidebar__item-label">{tab.label}</span>
            {activeTab === tab.id && <span className="sidebar__item-indicator" />}
          </button>
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar__footer">
        <div className="sidebar__divider" style={{ margin: '0 0 var(--space-md) 0' }} />
        
        <button
          className={`sidebar__confidential-btn ${activeTab === 'confidential' ? 'active' : ''}`}
          onClick={() => onTabChange('confidential')}
        >
          <Icons.Lock size={14} strokeWidth={2} />
          <span>Área Restrita</span>
        </button>

        <div className="sidebar__footer-text">
          <Icons.Shield size={14} strokeWidth={1.5} />
          <span>Mendonça Galvão</span>
        </div>
      </div>
    </aside>
  );
}
