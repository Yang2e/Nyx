from enum import Enum

class NyxState(str, Enum):
    STARTING = "STARTING"
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    RESPONDING = "RESPONDING"
    ERROR = "ERROR"
    SHUTTING_DOWN = "SHUTTING_DOWN"

# Mapeamento oficial backend -> estado visual do NyxOrb.jsx
STATE_TO_ORB_MAP = {
    NyxState.STARTING: "idle",
    NyxState.IDLE: "idle",
    NyxState.LISTENING: "listening",
    NyxState.THINKING: "thinking",
    NyxState.RESPONDING: "responding",
    NyxState.ERROR: "error",
    NyxState.SHUTTING_DOWN: "idle"
}

def get_orb_state(state: NyxState) -> str:
    return STATE_TO_ORB_MAP.get(state, "idle")