import { useState } from 'react'
import styles from './ChatMessage.module.css'

function formatTime(date) {
  return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

export function ChatMessage({ role, content, toolActivity }) {
  const isNyx = role === 'nyx'
  // A mensagem monta uma única vez (key estável), então o horário de montagem é o de criação.
  const [time] = useState(() => formatTime(new Date()))

  return (
    <article className={`${styles.row} ${isNyx ? styles.nyx : styles.user}`}>
      <header className={styles.meta}>
        <span className={styles.origin}>{isNyx ? 'nyx' : 'você'}</span>
        <span className={styles.time}>{time}</span>
      </header>

      {toolActivity && (
        <div className={styles.toolBadge}>
          <span className={styles.toolDot} />
          {toolActivity}
        </div>
      )}

      <p className={styles.text}>{content}</p>
    </article>
  )
}
