import { useState, useRef } from 'react'
import styles from './InputBar.module.css'

export function InputBar({ onSend, disabled }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)

  function handleSend() {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setValue('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  function handleInput(e) {
    setValue(e.target.value)
    // Auto-resize
    const ta = textareaRef.current
    if (ta) {
      ta.style.height = 'auto'
      ta.style.height = Math.min(ta.scrollHeight, 140) + 'px'
    }
  }

  return (
    <div className={styles.bar}>
      <textarea
        ref={textareaRef}
        className={styles.input}
        value={value}
        onChange={handleInput}
        onKeyDown={handleKeyDown}
        placeholder="Fale com a NYX..."
        rows={1}
        disabled={disabled}
        aria-label="Campo de mensagem"
      />
      <button
        className={`${styles.send} ${value.trim() && !disabled ? styles.active : ''}`}
        onClick={handleSend}
        disabled={!value.trim() || disabled}
        aria-label="Enviar mensagem"
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M14 8L2 2l2.5 6L2 14l12-6z" fill="currentColor"/>
        </svg>
      </button>
    </div>
  )
}
