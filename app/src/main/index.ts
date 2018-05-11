import path from 'path';
import url from 'url';

import { app, BrowserWindow } from 'electron';

let win: BrowserWindow;
const createWindow = () => {
  if (win !== undefined) return;
  win = new BrowserWindow({ width: 900, height: 700 });
  // win.webContents.openDevTools();

  if (process.env.NODE_ENV !== 'production') {
    win.loadURL(`http://localhost:${process.env.ELECTRON_WEBPACK_WDS_PORT}`);
  } else {
    win.loadURL(url.format({
      pathname: path.join(__dirname, 'index.html'),
      protocol: 'file:',
      slashes: true,
    }));
  }
};

app.on('ready', createWindow);
app.on('activate', createWindow);

app.on('window-all-closed', ()=>app.quit());