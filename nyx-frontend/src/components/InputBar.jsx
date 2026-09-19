import { useState, useRef, useEffect } from 'react'
import styles from './InputBar.module.css'

export function InputBar({ onSend, disabled }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)
  const hasSentRef = useRef(false)

  // Quando a resposta chega, o campo é reabilitado e perde o foco — devolve ao console.
  useEffect(() => {
    if (!disabled && hasSentRef.current) {
      textareaRef.current?.focus()
    }
  }, [disabled])

  function handleSend() {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    hasSentRef.current = true
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

  const canSend = Boolean(value.trim()) && !disabled

  return (
    <div className={styles.wrap}>
      <div className={`${styles.bar} ${disabled ? styles.busy : ''}`}>
        <span className={styles.prompt} aria-hidden="true">&gt;</span>

        <textarea
          ref={textareaRef}
          className={styles.input}
          value={value}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder={disabled ? 'NYX está processando...' : 'Fale com a NYX...'}
          rows={1}
          disabled={disabled}
          aria-label="Campo de mensagem"
        />

        <button
          className={`${styles.send} ${canSend ? styles.active : ''}`}
          onClick={handleSend}
          disabled={!canSend}
          aria-label="Enviar mensagem"
        >
          <span className={styles.sendLabel}>enviar</span>
          <svg className={styles.sendIcon} width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <path d="M14 8L2 2l2.5 6L2 14l12-6z" fill="currentColor"/>
          </svg>
        </button>
      </div>

      <p className={styles.hint} aria-hidden="true">
        <span>enter</span> envia
        <span className={styles.hintGap}>shift + enter</span> nova linha
      </p>
    </div>
  )
}
