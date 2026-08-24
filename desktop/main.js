const { app, BrowserWindow, clipboard, globalShortcut } = require('electron');
const path = require('path');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 700,
    height: 800,
    minWidth: 500,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#0a0a0f',
    icon: path.join(__dirname, 'icon.png')
  });

  mainWindow.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  // Global shortcut: CmdOrCtrl+Shift+U to sanitize clipboard
  globalShortcut.register('CommandOrControl+Shift+U', () => {
    const text = clipboard.readText();
    if (text) {
      // Send to renderer for processing
      mainWindow.webContents.send('clipboard-text', text);
    }
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
