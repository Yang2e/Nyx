import styles from './ChatMessage.module.css'

export function ChatMessage({ role, content, toolActivity }) {
  const isNyx = role === 'nyx'

  return (
    <div className={`${styles.row} ${isNyx ? styles.nyx : styles.user}`}>
      {isNyx && <div className={styles.avatar} aria-hidden="true">N</div>}

      <div className={styles.bubble}>
        {toolActivity && (
          <div className={styles.toolBadge}>
            <span className={styles.toolDot} />
            {toolActivity}
          </div>
        )}
        <p className={styles.text}>{content}</p>
      </div>
    </div>
  )
}
