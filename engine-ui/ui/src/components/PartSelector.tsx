import React from 'react';

interface PartSelectorProps {
    activePart: 'A' | 'B' | 'C' | 'D';
    onSelect: (part: 'A' | 'B' | 'C' | 'D') => void;
}

const PARTS = [
    { id: 'A', color: 'var(--color-part-a)', label: 'Lead' },
    { id: 'B', color: 'var(--color-part-b)', label: 'Pad' },
    { id: 'C', color: 'var(--color-part-c)', label: 'Bass' },
    { id: 'D', color: 'var(--color-part-d)', label: 'Tex' },
] as const;

export const PartSelector: React.FC<PartSelectorProps> = ({ activePart, onSelect }) => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {PARTS.map((part) => {
                const isActive = activePart === part.id;
                return (
                    <button
                        key={part.id}
                        onClick={() => onSelect(part.id)}
                        style={{
                            padding: '1rem',
                            background: isActive
                                ? `linear-gradient(90deg, ${part.color}22, transparent)`
                                : 'transparent',
                            border: `1px solid ${isActive ? part.color : 'rgba(255,255,255,0.1)'}`,
                            borderLeft: `4px solid ${part.color}`,
                            borderRadius: '8px',
                            color: 'var(--color-text-primary)',
                            cursor: 'pointer',
                            textAlign: 'left',
                            transition: 'all 0.2s ease',
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                        }}
                    >
                        <span style={{ fontWeight: 700, fontSize: '1.2rem' }}>{part.id}</span>
                        <span style={{ color: 'var(--color-text-secondary)', fontSize: '0.9rem' }}>{part.label}</span>
                    </button>
                );
            })}
        </div>
    );
};
