import './TabNav.css';

/**
 * Horizontal tab navigation with gold accent indicator.
 *
 * @param {object} props
 * @param {Array<{id: string, label: string, icon: string}>} props.tabs
 * @param {string} props.activeTab
 * @param {function} props.onTabChange
 */
export default function TabNav({ tabs, activeTab, onTabChange }) {
  return (
    <nav className="tab-nav" role="tablist" aria-label="Dashboard navigation">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          id={`tab-${tab.id}`}
          className={`tab-nav__item ${activeTab === tab.id ? 'active' : ''}`}
          role="tab"
          aria-selected={activeTab === tab.id}
          onClick={() => onTabChange(tab.id)}
        >
          <span className="tab-nav__icon">{tab.icon}</span>
          <span className="tab-nav__label">{tab.label}</span>
        </button>
      ))}
    </nav>
  );
}
