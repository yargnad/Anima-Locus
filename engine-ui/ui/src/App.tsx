import { useState, useCallback } from 'react';
import './index.css';
import { PartSelector } from './components/PartSelector';
import { XYPad } from './components/XYPad';
import { useEngine } from './hooks/useEngine';

function App() {
  const [activePart, setActivePart] = useState<'A' | 'B' | 'C' | 'D'>('A');
  const { isConnected, sendParam } = useEngine();

  const handleXYUpdate = useCallback((x: number, y: number) => {
    // Map X to Frequency (Exponential 50Hz - 2000Hz)
    // Formula: min * (max/min)^x
    const minFreq = 50;
    const maxFreq = 2000;
    const freq = minFreq * Math.pow(maxFreq / minFreq, x);

    // Map Y to Amplitude (Linear 0.0 - 1.0)
    const amp = y;

    sendParam(activePart, 'frequency', freq);
    sendParam(activePart, 'amplitude', amp);
  }, [activePart, sendParam]);

  return (
    <div style={{ padding: '2rem', height: '100%', boxSizing: 'border-box' }}>
      <header style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 className="title-text">ANIMA LOCUS <span style={{ opacity: 0.5, fontSize: '0.8em' }}>CONDUCTOR</span></h1>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            onClick={() => fetch('http://localhost:8000/api/v1/panic', { method: 'POST' })}
            style={{
              background: 'rgba(255, 51, 102, 0.2)',
              border: '1px solid #ff3366',
              color: '#ff3366',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: 'bold',
              letterSpacing: '1px',
              textTransform: 'uppercase',
              transition: 'all 0.2s ease',
              display: 'flex', alignItems: 'center', gap: '8px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#ff3366';
              e.currentTarget.style.color = '#fff';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(255, 51, 102, 0.2)';
              e.currentTarget.style.color = '#ff3366';
            }}
          >
            <span>STOP</span>
          </button>

          <div style={{
            color: isConnected ? '#00eeff' : 'var(--color-text-secondary)',
            display: 'flex', alignItems: 'center', gap: '8px',
            fontWeight: isConnected ? 'bold' : 'normal',
            textShadow: isConnected ? '0 0 10px rgba(0,238,255,0.5)' : 'none'
          }}>
            <div style={{
              width: 8, height: 8, borderRadius: '50%',
              background: isConnected ? '#00eeff' : '#555',
              boxShadow: isConnected ? '0 0 10px #00eeff' : 'none'
            }} />
            {isConnected ? 'LIVE' : 'Connecting...'}
          </div>
        </div>
      </header>

      <main style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '2rem', height: 'calc(100% - 100px)' }}>

        {/* Left Sidebar: Part Selector & Macros */}
        <aside className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <div>
            <h3 style={{ marginBottom: '1rem', marginTop: 0 }}>Select Part</h3>
            <PartSelector activePart={activePart} onSelect={setActivePart} />
          </div>

          <div style={{ color: 'var(--color-text-secondary)', fontSize: '0.9rem' }}>
            <p><strong>Controls</strong></p>
            <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '0.5rem', alignItems: 'center' }}>
              <span>X-Axis:</span> <span>Frequency (Exp)</span>
              <span>Y-Axis:</span> <span>Amplitude</span>
            </div>
          </div>
        </aside>

        {/* Main Stage: XY Pad & Visualizer */}
        <section className="glass-panel" style={{ padding: '2rem', display: 'flex', flexDirection: 'column' }}>
          <XYPad
            color={`var(--color-part-${activePart.toLowerCase()})`}
            onUpdate={handleXYUpdate}
            label={`Part ${activePart} Control`}
          />
        </section>

      </main>
    </div>
  );
}

export default App;
