import { useState, useCallback } from 'react';
import api from '../api/client';
import { useApi } from './useApi';

/**
 * Central dashboard state hook.
 * Manages active tab and provides data-fetching for each tab.
 */

const TABS = [
  { id: 'presentation', label: 'Apresentação', icon: 'Monitor' },
  { id: 'overview', label: 'Visão Geral', icon: 'BarChart2' },
  { id: 'expectations', label: 'Expectativas', icon: 'Target' },
  { id: 'salary', label: 'Salários', icon: 'DollarSign' },
  { id: 'tenure', label: 'Tempo & Carreira', icon: 'Clock' },
  { id: 'roles', label: 'Cargos', icon: 'Users' },
];

export function useDashboard() {
  const [activeTab, setActiveTab] = useState('presentation');

  const overview = useApi(api.getOverview);
  const expectations = useApi(api.getExpectations);
  const salary = useApi(api.getSalary);
  const tenure = useApi(api.getTenure);
  const roles = useApi(api.getRoles);
  const presentation = useApi(api.getPresentation);

  const changeTab = useCallback((tabId) => {
    setActiveTab(tabId);
  }, []);

  const isLoading = overview.loading || expectations.loading ||
    salary.loading || tenure.loading || roles.loading || presentation.loading;

  const hasError = overview.error || expectations.error ||
    salary.error || tenure.error || roles.error || presentation.error;

  return {
    tabs: TABS,
    activeTab,
    changeTab,
    isLoading,
    hasError,
    data: {
      overview: overview.data,
      expectations: expectations.data,
      salary: salary.data,
      tenure: tenure.data,
      roles: roles.data,
      presentation: presentation.data,
    },
    loading: {
      overview: overview.loading,
      expectations: expectations.loading,
      salary: salary.loading,
      tenure: tenure.loading,
      roles: roles.loading,
      presentation: presentation.loading,
    },
    errors: {
      overview: overview.error,
      expectations: expectations.error,
      salary: salary.error,
      tenure: tenure.error,
      roles: roles.error,
      presentation: presentation.error,
    },
  };
}

export { TABS };
