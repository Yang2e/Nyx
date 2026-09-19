import { useEffect, useRef } from 'react'

import styles from './NyxOrb.module.css'

const STATE_CONFIG = {
  idle: {
    color: 'var(--state-idle)',
    label: 'em espera',
    pulse: false,
  },

  listening: {
    color: 'var(--state-listening)',
    label: 'ouvindo',
    pulse: true,
  },

  thinking: {
    color: 'var(--state-thinking)',
    label: 'processando',
    pulse: true,
  },

  tool: {
    color: 'var(--state-tool)',
    label: 'usando ferram.',
    pulse: true,
  },

  responding: {
    color: 'var(--state-responding)',
    label: 'respondendo',
    pulse: true,
  },

  error: {
    color: 'var(--state-error)',
    label: 'erro',
    pulse: false,
  },
}

export function NyxOrb({ state = 'idle' }) {
  const stateKey = STATE_CONFIG[state] ? state : 'idle'
  const config = STATE_CONFIG[stateKey]

  const orbRef = useRef(null)
  const eyeRef = useRef(null)
  const pupilWrapperRef = useRef(null)

  const requestRef = useRef(null)

  const targetPos = useRef({
    x: 0,
    y: 0,
  })

  const currentPos = useRef({
    x: 0,
    y: 0,
  })

  // Atualiza a cor do orb conforme o estado da NYX
  useEffect(() => {
    if (orbRef.current) {
      orbRef.current.style.setProperty(
        '--orb-color',
        config.color
      )
    }
  }, [config.color])

  // Rastreamento da pupila pelo mouse
  useEffect(() => {
    const reducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    )

    if (reducedMotion.matches) {
      return
    }

    const MAX_DISPLACEMENT = 12
    const LERP_FACTOR = 0.15
    const SMOOTH_FACTOR = 45

    const handleMouseMove = (event) => {
      if (!eyeRef.current) {
        return
      }

      const rect = eyeRef.current.getBoundingClientRect()

      const centerX = rect.left + rect.width / 2
      const centerY = rect.top + rect.height / 2

      const dx = event.clientX - centerX
      const dy = event.clientY - centerY

      let targetX = dx / SMOOTH_FACTOR
      let targetY = dy / SMOOTH_FACTOR

      const distance = Math.sqrt(
        targetX * targetX + targetY * targetY
      )

      if (distance > MAX_DISPLACEMENT) {
        targetX =
          (targetX / distance) * MAX_DISPLACEMENT

        targetY =
          (targetY / distance) * MAX_DISPLACEMENT
      }

      targetPos.current = {
        x: targetX,
        y: targetY,
      }
    }

    const handleMouseLeave = () => {
      targetPos.current = {
        x: 0,
        y: 0,
      }
    }

    const animate = () => {
      currentPos.current.x +=
        (targetPos.current.x - currentPos.current.x) *
        LERP_FACTOR

      currentPos.current.y +=
        (targetPos.current.y - currentPos.current.y) *
        LERP_FACTOR

      if (pupilWrapperRef.current) {
        pupilWrapperRef.current.style.setProperty(
          '--mouse-x',
          `${currentPos.current.x}px`
        )

        pupilWrapperRef.current.style.setProperty(
          '--mouse-y',
          `${currentPos.current.y}px`
        )
      }

      requestRef.current =
        requestAnimationFrame(animate)
    }

    window.addEventListener(
      'mousemove',
      handleMouseMove
    )

    document.addEventListener(
      'mouseleave',
      handleMouseLeave
    )

    requestRef.current =
      requestAnimationFrame(animate)

    return () => {
      window.removeEventListener(
        'mousemove',
        handleMouseMove
      )

      document.removeEventListener(
        'mouseleave',
        handleMouseLeave
      )

      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current)
      }
    }
  }, [])

  return (
    <div
      ref={orbRef}
      className={styles.wrapper}
      style={{
        '--orb-color': config.color,
      }}
    >
      <div
        className={`${styles.orb} ${styles[stateKey]} ${
          config.pulse ? styles.pulse : ''
        }`}
        aria-label={`NYX — ${config.label}`}
        role="status"
      >
        <div className={styles.glow} />

        <div className={styles.rail} />

        <div className={styles.marker} />

        <div className={styles.brackets} />

        <div
          className={styles.eye}
          ref={eyeRef}
        >
          <div className={styles.frame} />

          <div className={styles.cut} />

          <div
            className={styles.pupilWrapper}
            ref={pupilWrapperRef}
          >
            <div className={styles.pupil} />
          </div>

          <div className={styles.scan} />
        </div>
      </div>

      <span className={styles.label}>
        <span className={styles.labelDot} />

        {config.label}
      </span>
    </div>
  )
}