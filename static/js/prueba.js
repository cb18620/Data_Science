// document.addEventListener('DOMContentLoaded', function () {
//     const consoleLog = document.getElementById('console-log');
//     const initialCommands = [
//       'Inicializando sistema de carga de archivos...',
//       'Esperando a que el usuario cargue un archivo...'
//     ];
  
//     // Función para agregar mensajes iniciales a la consola
//     function addInitialMessageToConsole(index) {
//       if (index < initialCommands.length) {
//         consoleLog.innerHTML += initialCommands[index] + "\n";
//         consoleLog.scrollTop = consoleLog.scrollHeight;
//       }
//     }
  
//     // Iniciar con los mensajes iniciales
//     addInitialMessageToConsole(0); // Inicializar sistema
//     setTimeout(() => addInitialMessageToConsole(1), 1000); // Esperar un segundo y luego esperar al usuario
//   });
  
//   // Resto de tus mensajes que se mostrarán después de presionar el botón "Cargar"
//   const fakeCommands = [
//     // ... resto de los comandos ficticios ...
//   'Archivo recibido, preparando para guardar...',
//     'Guardando archivo en el servidor...',
//     'Archivo guardado exitosamente. Procesando...',
//     'Leyendo archivo con pandas...',
//     'Aplicando transformaciones al DataFrame...',
//     'Guardando el archivo transformado...',
//     'Archivo transformado con éxito. Listo para descarga.',
//     'Proceso completado. Archivo listo para ser descargado por el usuario.'
//   ];

//   let currentCommandIndex = 0;
// let commandDisplayIndex = 0;

// function typeCommand() {
//   if (currentCommandIndex < fakeCommands.length) {
//     let command = fakeCommands[currentCommandIndex];
//     if (commandDisplayIndex < command.length) {
//       consoleLog.innerHTML += command.charAt(commandDisplayIndex);
//       commandDisplayIndex++;
//       setTimeout(typeCommand, Math.random() * 16); // Retardo aleatorio para simular escritura
//     } else {
//       consoleLog.innerHTML += '\n';
//       consoleLog.scrollTop = consoleLog.scrollHeight; // Auto-scroll
//       currentCommandIndex++;
//       commandDisplayIndex = 0;
//       setTimeout(typeCommand, 25); // Espera un poco antes del siguiente comando
//     }
//   } else {
//     consoleLog.innerHTML += '<span class="console-typing"></span>'; // Cursor parpadeante al final
//   }
// }

// document.getElementById('upload-btn').addEventListener('click', function() {
//   // Vacía la consola antes de comenzar
//   consoleLog.innerHTML = '';
//   currentCommandIndex = 0;  // Reiniciar el índice del comando actual
  
//   // Iniciar la simulación de la consola
//   typeCommand();
// });
