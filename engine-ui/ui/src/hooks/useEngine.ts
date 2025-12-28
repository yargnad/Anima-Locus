import { useEffect, useRef, useState } from 'react';

const SOCKET_URL = 'ws://localhost:8000/ws';

export type EnginePart = 'A' | 'B' | 'C' | 'D';

interface UseEngineReturn {
    isConnected: boolean;
    sendParam: (partId: EnginePart, param: string, value: number) => void;
}

export function useEngine(): UseEngineReturn {
    const [isConnected, setIsConnected] = useState(false);
    const wsRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        const ws = new WebSocket(SOCKET_URL);
        wsRef.current = ws;

        ws.onopen = () => {
            console.log('Connected to Engine');
            setIsConnected(true);
        };

        ws.onclose = () => {
            console.log('Disconnected from Engine');
            setIsConnected(false);
        };

        ws.onerror = (err) => {
            console.error('WebSocket Error:', err);
        };

        return () => {
            ws.close();
        };
    }, []);

    const sendParam = (partId: EnginePart, param: string, value: number) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({
                type: 'set_param',
                part_id: partId,
                engine: 'oscillator', // Hardcoded for now, could be dynamic
                param: param,
                value: value
            }));
        }
    };

    return { isConnected, sendParam };
}
