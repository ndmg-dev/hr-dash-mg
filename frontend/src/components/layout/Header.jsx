import React from 'react';
import TabNav from '../ui/TabNav';
import { TABS } from '../../hooks/useDashboard';

/**
 * Top header bar with tab navigation (visible on desktop in header area)
 */
export default function Header({ activeTab, onTabChange }) {
  return (
    <header
      id="header"
      style={{
        position: 'fixed',
        top: 0,
        left: 'var(--sidebar-width)',
        right: 0,
        height: 'var(--header-height)',
        background: 'rgba(10, 10, 15, 0.8)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        borderBottom: '1px solid var(--glass-border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 var(--space-8)',
        zIndex: 'var(--z-sticky)',
        transition: 'var(--transition)',
      }}
      className="header-bar"
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)', overflow: 'auto' }}>
        <TabNav tabs={TABS} activeTab={activeTab} onTabChange={onTabChange} />
      </div>

      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-3)',
      }}>
        {/* Status indicator */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '6px 12px',
          borderRadius: 'var(--border-radius-full)',
          background: 'var(--positive-bg)',
          border: '1px solid var(--positive-border)',
        }}>
          <div style={{
            width: '6px',
            height: '6px',
            borderRadius: '50%',
            background: 'var(--positive)',
            animation: 'pulse 2s ease-in-out infinite',
          }} />
          <span style={{
            fontSize: '0.7rem',
            fontWeight: 600,
            color: 'var(--positive)',
          }}>
            Live
          </span>
        </div>
      </div>

      <style>{`
        @media (max-width: 1024px) {
          .header-bar {
            left: 0 !important;
            padding: 0 var(--space-4) !important;
          }
        }
      `}</style>
    </header>
  );
}
