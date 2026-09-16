import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

/**
 * POST /chat/ (ou /api/chat/ conforme configurado no backend)
 * Envia uma mensagem para a NYX e retorna a resposta.
 */
export async function sendMessage(message, conversationId = null) {
  try {
    const response = await client.post('/chat/', {
      message: message,
      conversation_id: conversationId,
    })
    return response.data
  } catch (error) {
    throw new Error('Erro na comunicação com o backend')
  }
}

/**
 * POST /api/tools/execute
 * Executa uma ferramenta modular.
 */
export async function executeTool(toolName, args) {
  const response = await client.post('/api/tools/execute', {
    tool_name: toolName,
    arguments: args,
  })
  return response.data
}

export default client