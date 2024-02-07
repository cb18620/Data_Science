const fakeCommands = [
    'Archivo recibido, preparando para guardar...',
    // ... resto de los comandos ficticios ...
];

let currentCommandIndex = 0;
let commandDisplayIndex = 0;

function typeCommand() {
    // ... lógica para mostrar los mensajes de comandos ficticios ...
}

document.getElementById('upload-btn').addEventListener('click', function() {
    currentCommandIndex = 0;
    commandDisplayIndex = 0;
    consoleLog.innerHTML = '';
    typeCommand();
});
