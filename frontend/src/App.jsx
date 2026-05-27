import { useDashboard } from './hooks/useDashboard';
import { AlertCircle } from 'react-feather';
import DashboardLayout from './components/layout/DashboardLayout';
import Overview from './pages/Overview';
import Expectations from './pages/Expectations';
import Salary from './pages/Salary';
import Tenure from './pages/Tenure';
import Roles from './pages/Roles';
import Presentation from './pages/Presentation';
import Confidential from './pages/Confidential';
import Loader from './components/ui/Loader';

/**
 * Root application component.
 * Manages tab routing and delegates data to each page.
 */
export default function App() {
  const { tabs, activeTab, changeTab, data, loading, hasError } = useDashboard();

  const renderPage = () => {
    if (activeTab === 'confidential') {
      return <Confidential />;
    }
    
    switch (activeTab) {
      case 'overview':
        return <Overview data={data.overview} loading={loading.overview} />;
      case 'expectations':
        return <Expectations data={data.expectations} loading={loading.expectations} />;
      case 'salary':
        return <Salary data={data.salary} loading={loading.salary} />;
      case 'tenure':
        return <Tenure data={data.tenure} loading={loading.tenure} />;
      case 'roles':
        return <Roles data={data.roles} loading={loading.roles} />;
      case 'presentation':
        return <Presentation data={data.presentation} loading={loading.presentation} />;
      default:
        return <Overview data={data.overview} loading={loading.overview} />;
    }
  };

  return (
    <DashboardLayout tabs={tabs} activeTab={activeTab} onTabChange={changeTab}>
      {hasError && (
        <div style={{
          padding: 'var(--space-lg)',
          background: 'var(--negative-soft)',
          borderRadius: 'var(--radius-md)',
          marginBottom: 'var(--space-lg)',
          color: 'var(--negative)',
          fontSize: '0.875rem',
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-sm)'
        }}>
          <AlertCircle size={18} />
          <div>
            Erro ao carregar dados. Verifique se o backend está rodando em{' '}
            <code style={{ fontFamily: 'var(--font-mono)' }}>http://localhost:8000</code>.
          </div>
        </div>
      )}
      {renderPage()}
    </DashboardLayout>
  );
}
