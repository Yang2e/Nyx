const { app, BrowserWindow, ipcMain, globalShortcut } = require("electron");
const path = require("path");
// Assumindo que os caminhos para as funções estão corretos
const { transcribeAudio } = require("./src/functions/transcriber.js");
const { chatGptRequest } = require("./src/functions/openia.js");
const { listening } = require("./src/functions/listening.js");

let win;

const createWindow = () => {
    win = new BrowserWindow({
        title: 'J.A.R.V.I.S',
        width: 370,
        height: 500,
        // CORREÇÃO: Usando path.join para garantir o caminho correto em todos os SOs.
        icon: path.join(__dirname, "src", "assets", "img", "jarvis-logo.png"),
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            // CORREÇÃO DE SEGURANÇA CRÍTICA:
            // nodeIntegration deve ser 'false' para evitar que o frontend execute código Node.js.
            nodeIntegration: false,
            // contextIsolation deve ser 'true' para isolar o ambiente de execução do frontend do Node.js.
            contextIsolation: true,
        },
    });

    win.loadFile("./src/html/index.html");
};

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});

ipcMain.on("transcribe-audio", async (event, audioPath) => {
    try {
        // Transcreve o áudio para texto
        const transcription = await transcribeAudio(audioPath);
        console.log('### transcription: ', transcription)

        // Envia o resultado da transcrição
        event.reply("transcription-result", transcription);
        
        const listen = await listening(transcription);
        console.log('### result for listen: ', listen)

        // Chama o ChatGPT com o texto transcrito
        const { text, audioPath: generatedAudioPath } = await chatGptRequest(listen);

        // Retorna o texto e o áudio para o frontend
        event.reply("chatgpt-response", { text, audioPath: generatedAudioPath });
    } catch (error) {
        console.error("Erro na transcrição/chat:", error);
        // Resposta de erro para o frontend
        event.reply("chatgpt-response", { text: "Erro ao processar resposta.", audioPath: null });
    }
});

ipcMain.on("toggle-always-on-top", (event, isAlwaysOnTop) => {
    win.setAlwaysOnTop(isAlwaysOnTop);
});

// Nota: A função 'win' foi definida globalmente com 'let win',
// garantindo que ela esteja disponível para 'ipcMain.on("toggle-always-on-top", ...)'