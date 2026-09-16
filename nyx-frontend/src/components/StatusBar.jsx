import styles from './StatusBar.module.css'

export function StatusBar({ connected, nyxState }) {
  return (
    <header className={styles.bar}>
      <div className={styles.identity}>
        <span className={styles.name}>NYX</span>
        <span className={styles.version}>v1.0</span>
      </div>

      <div className={styles.right}>
        <div className={`${styles.connection} ${connected ? styles.online : styles.offline}`}>
          <span className={styles.dot} />
          {connected ? 'conectado' : 'offline'}
        </div>
      </div>
    </header>
  )
}
