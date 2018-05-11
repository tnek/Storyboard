"use strict";
exports.__esModule = true;
var path_1 = require("path");
var url_1 = require("url");
var electron_1 = require("electron");
var win;
var createWindow = function () {
    if (win !== undefined)
        return;
    win = new electron_1.BrowserWindow({ width: 900, height: 700 });
    // win.webContents.openDevTools();
    if (process.env.NODE_ENV !== 'production') {
        win.loadURL("http://localhost:" + process.env.ELECTRON_WEBPACK_WDS_PORT);
    }
    else {
        win.loadURL(url_1["default"].format({
            pathname: path_1["default"].join(__dirname, 'index.html'),
            protocol: 'file:',
            slashes: true
        }));
    }
};
electron_1.app.on('ready', createWindow);
electron_1.app.on('activate', createWindow);
electron_1.app.on('window-all-closed', function () { return electron_1.app.quit(); });
