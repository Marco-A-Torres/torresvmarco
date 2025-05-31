document.addEventListener('DOMContentLoaded', () => {
    let db;
    let posiblesPersonajes = [];
    let preguntaActual = null;
    let faseAdivinanza = false;
    let nombreAdivinado = '';
    let preguntas = [];

    const request = indexedDB.open('AdivinaQuienDB', 1);

    request.onupgradeneeded = (event) => {
        const db = event.target.result;
        const store = db.createObjectStore('personajes', { keyPath: 'nombre' });

        const personajesIniciales = [
            {
                nombre: 'Juan',
                caracteristicas: {
                    gafas: 'sí',
                    'pelo corto': 'no',
                    sombrero: 'no',
                    'ojos claros': 'sí',
                    'piel clara': 'sí',
                    alto: 'no'
                }
            },
            {
                nombre: 'Maria',
                caracteristicas: {
                    gafas: 'no',
                    'pelo corto': 'sí',
                    sombrero: 'sí',
                    'ojos claros': 'no',
                    'piel clara': 'no',
                    alto: 'sí'
                }
            },
            {
                nombre: 'Carlos',
                caracteristicas: {
                    gafas: 'sí',
                    'pelo corto': 'sí',
                    sombrero: 'no',
                    'ojos claros': 'no',
                    'piel clara': 'sí',
                    alto: 'sí'
                }
            }
        ];

        personajesIniciales.forEach(personaje => store.add(personaje));
    };

    request.onsuccess = (event) => {
        db = event.target.result;
        cargarPersonajes();
    };

    function cargarPersonajes() {
        const transaction = db.transaction(['personajes'], 'readonly');
        const request = transaction.objectStore('personajes').getAll();

        request.onsuccess = (event) => {
            posiblesPersonajes = event.target.result;
            generarPreguntas();
            mostrarPreguntaAleatoria();
            imprimirTablaPersonajes();
        };
    }

    function imprimirTablaPersonajes() {
        console.table(
            posiblesPersonajes.map(personaje => ({
                Nombre: personaje.nombre,
                ...personaje.caracteristicas
            }))
        );
    }

    function generarPreguntas() {
        preguntas = [];
        posiblesPersonajes.forEach(personaje => {
            Object.keys(personaje.caracteristicas).forEach(attr => {
                if (!preguntas.some(p => p.clave === attr)) {
                    preguntas.push({
                        texto: `¿El personaje tiene ${attr}?`,
                        clave: attr
                    });
                }
            });
        });
    }

    function mostrarPreguntaAleatoria() {
        if (preguntas.length > 0) {
            const indicePregunta = Math.floor(Math.random() * preguntas.length);
            preguntaActual = preguntas[indicePregunta];
            document.getElementById('pregunta').innerText = preguntaActual.texto;
            preguntas.splice(indicePregunta, 1);
        } else {
            alert('Se han agotado las preguntas.');
            pedirNuevoPersonaje();
        }
    }

    window.manejarRespuesta = function manejarRespuesta(respuesta) {
        if (!preguntaActual) return;
    
        const claveCaracteristica = preguntaActual.clave;
        const valorEsperado = respuesta.toLowerCase() === 'sí' ? 'sí' : 'no';
    
        if (faseAdivinanza) {
            if (respuesta.toLowerCase() === 'no') {
                alert('No encontré coincidencias. Vamos a agregar un nuevo personaje.');
                pedirNuevoPersonaje(); // Muestra el formulario inmediatamente
                return;
            } else {
                alert(`¡Genial! Has adivinado, es ${nombreAdivinado}.`);
                reiniciarJuego();
                return;
            }
        }
    
        posiblesPersonajes = posiblesPersonajes.filter(personaje =>
            personaje.caracteristicas[claveCaracteristica] === valorEsperado
        );
    
        if (posiblesPersonajes.length === 1) {
            nombreAdivinado = posiblesPersonajes[0].nombre;
            document.getElementById('pregunta').innerText = `¿Es ${nombreAdivinado} tu personaje?`;
            faseAdivinanza = true; // Cambia a fase de adivinanza
        } else if (posiblesPersonajes.length === 0) {
            alert('No encontré coincidencias. Vamos a agregar un nuevo personaje.');
            pedirNuevoPersonaje(); // Muestra el formulario si no hay coincidencias
        } else {
            mostrarPreguntaAleatoria(); // Continúa con las preguntas
        }
    };
    

    function pedirNuevoPersonaje() {
        document.getElementById('juego-container').classList.add('oculto');
        document.getElementById('nuevo-personaje-form').classList.remove('oculto');
    }

    window.guardarNuevoPersonaje = function guardarNuevoPersonaje() {
        const nombre = document.getElementById('nombre-personaje').value.trim();
        const nuevaCaracteristica = document.getElementById('nueva-caracteristica-input').value.trim().toLowerCase();
        const tipoCaracteristica = document.querySelector('input[name="tipo-caracteristica"]:checked')?.value;

        if (!nombre || !nuevaCaracteristica || !tipoCaracteristica) {
            alert('Completa todos los campos.');
            return;
        }

        const claveCaracteristica = nuevaCaracteristica.replace(/\s+/g, '_');
        let nuevasCaracteristicas = generarAtributosParaNuevoPersonaje();

        nuevasCaracteristicas[claveCaracteristica] = 'sí';

        const nuevoPersonaje = { nombre, caracteristicas: nuevasCaracteristicas };

        agregarPersonajeABaseDatos(nuevoPersonaje)
            .then(() => actualizarPersonajesExistentes(claveCaracteristica))
            .then(() => {
                alert(`¡El personaje "${nombre}" se ha agregado con éxito!`);
                reiniciarJuego();
            })
            .catch((error) => {
                alert(`Error al agregar el personaje: ${error.message}`);
            });
    };

    function generarAtributosParaNuevoPersonaje() {
        let nuevasCaracteristicas = {};

        posiblesPersonajes.forEach(personaje => {
            Object.keys(personaje.caracteristicas).forEach(attr => {
                nuevasCaracteristicas[attr] = Math.random() < 0.5 ? 'sí' : 'no';
            });
        });

        return nuevasCaracteristicas;
    }

    function actualizarPersonajesExistentes(claveNueva) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['personajes'], 'readwrite');
            const objectStore = transaction.objectStore('personajes');

            objectStore.openCursor().onsuccess = function (event) {
                const cursor = event.target.result;
                if (cursor) {
                    const personaje = cursor.value;
                    personaje.caracteristicas[claveNueva] = Math.random() < 0.5 ? 'sí' : 'no';
                    cursor.update(personaje);
                    cursor.continue();
                } else {
                    resolve();
                }
            };

            transaction.onerror = (event) => reject(event.target.error);
        });
    }

    function agregarPersonajeABaseDatos(personaje) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['personajes'], 'readwrite');
            const store = transaction.objectStore('personajes');

            const request = store.add(personaje);
            request.onsuccess = () => resolve();
            request.onerror = (event) => reject(event.target.error);
        });
    }

    function reiniciarJuego() {
        document.getElementById('nuevo-personaje-form').classList.add('oculto');
        document.getElementById('juego-container').classList.remove('oculto');
        cargarPersonajes();
    }

    window.actualizarVistaPrevia = function actualizarVistaPrevia() {
        const nuevaCaracteristica = document.getElementById('nueva-caracteristica-input').value.trim();
        const tipoCaracteristica = document.querySelector('input[name="tipo-caracteristica"]:checked')?.value;
        let pregunta = '';

        if (nuevaCaracteristica && tipoCaracteristica) {
            switch (tipoCaracteristica) {
                case 'posesion':
                    pregunta = `¿El personaje tiene ${nuevaCaracteristica}?`;
                    break;
                case 'pertenencia':
                    pregunta = `¿El personaje es ${nuevaCaracteristica}?`;
                    break;
                case 'capacidad':
                    pregunta = `¿El personaje puede ${nuevaCaracteristica}?`;
                    break;
                default:
                    pregunta = `¿El personaje tiene ${nuevaCaracteristica}?`;
            }
        }

        document.getElementById('vista-previa-pregunta').innerText = pregunta;
    };
});
