import { useState, useEffect, useRef } from 'react'
import { NyxOrb } from '../components/NyxOrb'
import { ChatMessage } from '../components/ChatMessage'
import { InputBar } from '../components/InputBar'
import { StatusBar } from '../components/StatusBar'
import { sendMessage } from '../services/api'
import styles from './ChatScreen.module.css'

const WELCOME = {
  id: 'welcome',
  role: 'nyx',
  content: 'Olá. Estou pronta para ajudar.',
}

export function ChatScreen() {
  const [messages, setMessages] = useState([WELCOME])
  const [nyxState, setNyxState] = useState('idle')
  const [connected, setConnected] = useState(false)
  
  // 1. AQUI: Criamos o estado para guardar o ID da conversa ativa
  const [conversationId, setConversationId] = useState(null)
  
  const bottomRef = useRef(null)

  useEffect(() => {
    fetch(import.meta.env.VITE_API_URL || 'http://localhost:8000')
      .then(() => setConnected(true))
      .catch(() => setConnected(false))
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend(text) {
    const userMsg = { id: Date.now(), role: 'user', content: text }
    setMessages(prev => [...prev, userMsg])
    setNyxState('thinking')

    try {
      // 2. AQUI: Passamos o conversationId atual para a API
      const data = await sendMessage(text, conversationId)

      // 3. AQUI: Se o backend retornar um ID novo, salvamos no estado
      if (data?.conversation_id) {
        setConversationId(data.conversation_id)
      }

      const reply = data?.response ?? data?.message ?? data?.content ?? JSON.stringify(data)

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'nyx',
        content: reply,
      }])
      setNyxState('idle')

    } catch (err) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'nyx',
        content: 'Não consegui me conectar ao backend. Verifique se o servidor está rodando.',
      }])
      setNyxState('error')
      setTimeout(() => setNyxState('idle'), 3000)
    }
  }

  const isThinking = nyxState === 'thinking'

  return (
    <div className={styles.screen}>
      <StatusBar connected={connected} nyxState={nyxState} />

      <div className={styles.body}>
        <aside className={styles.sidebar}>
          <NyxOrb state={nyxState} />
        </aside>

        <main className={styles.chat}>
          <div className={styles.messages} role="log" aria-live="polite" aria-label="Conversa com NYX">
            {messages.map(msg => (
              <ChatMessage
                key={msg.id}
                role={msg.role}
                content={msg.content}
                toolActivity={msg.toolActivity}
              />
            ))}

            {isThinking && (
              <div className={styles.thinking} aria-live="assertive">
                <span />
                <span />
                <span />
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          <div className={styles.inputArea}>
            <InputBar onSend={handleSend} disabled={isThinking} />
          </div>
        </main>
      </div>
    </div>
  )
}