import React, { useState, useRef, useEffect } from 'react';

interface XYPadProps {
    x?: number;
    y?: number;
    label?: string;
    onUpdate: (x: number, y: number) => void;
    color?: string; // e.g., var(--color-part-a)
}

export const XYPad: React.FC<XYPadProps> = ({
    x = 0.5,
    y = 0.5,
    label = "Frequency / Amplitude",
    onUpdate,
    color = 'var(--color-text-primary)'
}) => {
    const padRef = useRef<HTMLDivElement>(null);
    const [isDragging, setIsDragging] = useState(false);

    // Local state for smooth interaction
    const [localX, setLocalX] = useState(x);
    const [localY, setLocalY] = useState(y);

    // Sync with props when not dragging
    useEffect(() => {
        if (!isDragging) {
            setLocalX(x);
            setLocalY(y);
        }
    }, [x, y, isDragging]);

    const handlePointer = (e: React.PointerEvent) => {
        if (!padRef.current) return;

        // Capture pointer to allow dragging outside container
        if (e.type === 'pointerdown') {
            setIsDragging(true);
            (e.target as Element).setPointerCapture(e.pointerId);
        }

        const rect = padRef.current.getBoundingClientRect();
        const clientX = e.clientX;
        const clientY = e.clientY;

        // Normalized coordinates (0.0 to 1.0)
        // Clamp to 0-1
        const rawX = (clientX - rect.left) / rect.width;
        const rawY = 1.0 - ((clientY - rect.top) / rect.height); // Y up is 1.0 usually in synths? Or down?
        // Let's assume standard UI: Top-Left is 0,0 usually? 
        // BUT for audio Y usually means Amplitude (Up = 1).
        // Let's implement Y=0 at Bottom, Y=1 at Top.

        const newX = Math.max(0, Math.min(1, rawX));
        const newY = Math.max(0, Math.min(1, rawY));

        setLocalX(newX);
        setLocalY(newY);

        onUpdate(newX, newY);
    };

    const handlePointerUp = (e: React.PointerEvent) => {
        setIsDragging(false);
        (e.target as Element).releasePointerCapture(e.pointerId);
    };

    return (
        <div
            style={{
                width: '100%',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.5rem'
            }}
        >
            <div
                ref={padRef}
                className="glass-panel"
                style={{
                    flex: 1,
                    position: 'relative',
                    cursor: 'crosshair',
                    touchAction: 'none', // Prevent scrolling
                    background: 'rgba(0,0,0,0.3)',
                    overflow: 'hidden'
                }}
                onPointerDown={handlePointer}
                onPointerMove={(e) => isDragging && handlePointer(e)}
                onPointerUp={handlePointerUp}
            >
                {/* Grid Lines */}
                <div style={{
                    position: 'absolute',
                    top: '50%', left: 0, right: 0, height: 1,
                    background: 'rgba(255,255,255,0.1)'
                }} />
                <div style={{
                    position: 'absolute',
                    left: '50%', top: 0, bottom: 0, width: 1,
                    background: 'rgba(255,255,255,0.1)'
                }} />

                {/* Cursor/Puck */}
                <div
                    style={{
                        position: 'absolute',
                        left: `${localX * 100}%`,
                        bottom: `${localY * 100}%`, // Bottom-up Y
                        width: '24px',
                        height: '24px',
                        borderRadius: '50%',
                        background: color,
                        boxShadow: `0 0 15px ${color}`,
                        transform: 'translate(-50%, 50%)', // Center it
                        pointerEvents: 'none',
                        transition: isDragging ? 'none' : 'all 0.1s ease-out'
                    }}
                />

                {/* Trail / Ghosting could go here */}
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--color-text-secondary)' }}>
                <span>X: Freq</span>
                <span>{label}</span>
                <span>Y: Amp</span>
            </div>
        </div>
    );
};
