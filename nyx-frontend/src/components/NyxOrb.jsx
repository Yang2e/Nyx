import { useEffect, useRef } from 'react'
import styles from './NyxOrb.module.css'

const STATE_CONFIG = {
  idle:       { color: 'var(--state-idle)',       label: 'em espera',     pulse: false },
  listening:  { color: 'var(--state-listening)',  label: 'ouvindo',       pulse: true  },
  thinking:   { color: 'var(--state-thinking)',   label: 'processando',   pulse: true  },
  tool:       { color: 'var(--state-tool)',       label: 'usando ferram.', pulse: true  },
  responding: { color: 'var(--state-responding)', label: 'respondendo',   pulse: true  },
  error:      { color: 'var(--state-error)',      label: 'erro',          pulse: false },
}

export function NyxOrb({ state = 'idle' }) {
  const config = STATE_CONFIG[state] ?? STATE_CONFIG.idle
  const orbRef = useRef(null)

  // Atualiza a variável CSS do orb sem re-renderizar
  useEffect(() => {
    if (orbRef.current) {
      orbRef.current.style.setProperty('--orb-color', config.color)
    }
  }, [config.color])

  return (
    <div className={styles.wrapper}>
      <div
        ref={orbRef}
        className={`${styles.orb} ${config.pulse ? styles.pulse : ''}`}
        style={{ '--orb-color': config.color }}
        aria-label={`NYX — ${config.label}`}
        role="status"
      >
        <div className={styles.inner} />
      </div>
      <span className={styles.label}>{config.label}</span>
    </div>
  )
}
