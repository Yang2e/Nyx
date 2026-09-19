import styles from './StatusBar.module.css'

export function StatusBar({ connected, nyxState }) {
  return (
    <header className={styles.bar} data-state={nyxState}>
      <div className={styles.identity}>
        <img
          className={styles.mark}
          src="/assets/nyx-eye.png"
          alt=""
          aria-hidden="true"
          draggable="false"
        />
        <span className={styles.name}>NYX</span>
        <span className={styles.version}>v1.0</span>
      </div>

      <div className={styles.right}>
        <div
          className={`${styles.connection} ${connected ? styles.online : styles.offline}`}
          role="status"
        >
          <span className={styles.dot} />
          {connected ? 'conectado' : 'offline'}
        </div>
      </div>
    </header>
  )
}
