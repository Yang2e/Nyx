import { useEffect, useRef, useCallback } from 'react'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'

/**
 * Hook de WebSocket para eventos em tempo real da NYX.
 * Fica inativo até o backend expor o endpoint /ws.
 *
 * Eventos esperados do backend:
 *   { type: 'thinking' }
 *   { type: 'tool_started', tool_name: '...' }
 *   { type: 'tool_finished', tool_name: '...' }
 *   { type: 'response_chunk', content: '...' }
 *   { type: 'response_finished' }
 *   { type: 'error', message: '...' }
 */
export function useWebSocket(onEvent, enabled = false) {
  const wsRef = useRef(null)
  const onEventRef = useRef(onEvent)
  onEventRef.current = onEvent

  const connect = useCallback(() => {
    if (!enabled) return

    try {
      const ws = new WebSocket(WS_URL)
      wsRef.current = ws

      ws.onopen = () => onEventRef.current({ type: 'connected' })

      ws.onmessage = (e) => {
        try {
          const data = JSON.parse(e.data)
          onEventRef.current(data)
        } catch {
          console.warn('[NYX WS] Mensagem não-JSON recebida:', e.data)
        }
      }

      ws.onerror = () => onEventRef.current({ type: 'error', message: 'Falha na conexão WebSocket' })
      ws.onclose = () => onEventRef.current({ type: 'disconnected' })
    } catch (err) {
      console.warn('[NYX WS] WebSocket não disponível ainda:', err.message)
    }
  }, [enabled])

  useEffect(() => {
    connect()
    return () => wsRef.current?.close()
  }, [connect])

  const send = useCallback((data) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }, [])

  return { send }
}
