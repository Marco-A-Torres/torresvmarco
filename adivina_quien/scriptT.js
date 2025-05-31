document.addEventListener('DOMContentLoaded', () => {
    let db;
    let posiblesTelas = [];
    let preguntaActual = null;
    let faseAdivinanza = false;
    let telaAdivinada = '';
    let preguntas = [];
    let tiposAtributos = {};  // Aquí se guardarán los tipos de los atributos nuevos


    const request = indexedDB.open('AdivinaTelaDB', 1);

    request.onupgradeneeded = (event) => {
        const db = event.target.result;
        const store = db.createObjectStore('telas', { keyPath: 'nombre' });
    
        const telasIniciales = [
            {
                nombre: 'Algodón',
                caracteristicas: {
                    suave: { valor: 1, tipo: 'textura' },
                    resistente: { valor: 1, tipo: 'durabilidad' },
                    ligero: { valor: 1, tipo: 'peso' },
                    estampado: { valor: 0, tipo: 'apariencia' },
                    natural: { valor: 1, tipo: 'origen' },
                    flexible: { valor: 1, tipo: 'propiedad' }
                }
            },
            {
                nombre: 'Poliéster',
                caracteristicas: {
                    suave: { valor: 0, tipo: 'textura' },
                    resistente: { valor: 1, tipo: 'durabilidad' },
                    ligero: { valor: 1, tipo: 'peso' },
                    estampado: { valor: 1, tipo: 'apariencia' },
                    natural: { valor: 0, tipo: 'origen' },
                    flexible: { valor: 1, tipo: 'propiedad' }
                }
            },
            {
                nombre: 'Seda',
                caracteristicas: {
                    suave: { valor: 1, tipo: 'textura' },
                    resistente: { valor: 0, tipo: 'durabilidad' },
                    ligero: { valor: 1, tipo: 'peso' },
                    estampado: { valor: 0, tipo: 'apariencia' },
                    natural: { valor: 1, tipo: 'origen' },
                    flexible: { valor: 0, tipo: 'propiedad' }
                }
            }
        ];
    
        telasIniciales.forEach(tela => store.add(tela));
    };
    
    

    request.onsuccess = (event) => {
        db = event.target.result;
        cargarTelas();
    };

    function cargarTelas() {
        const transaction = db.transaction(['telas'], 'readonly');
        const request = transaction.objectStore('telas').getAll();
    
        request.onsuccess = (event) => {
            posiblesTelas = event.target.result;
            generarPreguntas();
            mostrarPreguntaAleatoria();
            imprimirTablaTelas();
        };
    }
    

    function imprimirTablaTelas() {
        const telasConValoresSimples = posiblesTelas.map(tela => {
            const caracteristicasSimplificadas = Object.fromEntries(
                Object.entries(tela.caracteristicas).map(([clave, data]) => [
                    clave,
                    data.valor === 1 || data.valor === 'sí' ? 'Sí' : 'No'
                ])
            );
    
            return {
                Nombre: tela.nombre,
                ...caracteristicasSimplificadas
            };
        });
    
        console.table(telasConValoresSimples);
    }
    
    
    

    function generarPreguntas() {
        preguntas = [];
        posiblesTelas.forEach(tela => {
            Object.entries(tela.caracteristicas).forEach(([clave, data]) => {
                if (!preguntas.some(p => p.clave === clave)) {
                    const tipoPregunta = determinarTipoDePregunta(clave, data.tipo);
                    preguntas.push({
                        texto: tipoPregunta,
                        clave: clave
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
            pedirNuevaTela();
        }
    }

    window.manejarRespuesta = function manejarRespuesta(respuesta) {
        if (!preguntaActual) return;
    
        const claveCaracteristica = preguntaActual.clave;
        const valorEsperado = respuesta === '1' ? 1 : 0;
    
        if (faseAdivinanza) {
            if (respuesta === '0') {
                alert('No encontré coincidencias. Vamos a agregar una nueva tela.');
                pedirNuevaTela();
                return;
            } else {
                alert(`¡Genial! Has adivinado, es ${telaAdivinada}.`);
                reiniciarJuego();
                return;
            }
        }
    
        posiblesTelas = posiblesTelas.filter(tela => {
            const valorCaracteristica = tela.caracteristicas[claveCaracteristica]?.valor;
            return valorCaracteristica === valorEsperado;
        });
    
        if (posiblesTelas.length === 1) {
            telaAdivinada = posiblesTelas[0].nombre;
            document.getElementById('pregunta').innerText = `¿Es ${telaAdivinada} tu tela?`;
            faseAdivinanza = true;
        } else if (posiblesTelas.length === 0) {
            alert('No encontré coincidencias. Vamos a agregar una nueva tela.');
            pedirNuevaTela();
        } else {
            mostrarPreguntaAleatoria();
        }
    };    
        
    
    
    

    function pedirNuevaTela() {
        document.getElementById('juego-container').classList.add('oculto');  // Esta línea ya es correcta
        document.getElementById('nuevo-tela-form').classList.remove('oculto');  // Cambia de 'nuevo-personaje-form' a 'nuevo-tela-form'
    }
    
    function reiniciarJuego() {
        faseAdivinanza = false;
        telaAdivinada = '';
        preguntaActual = null;
    
        posiblesTelas = [];
        preguntas = [];
    
        document.getElementById('nuevo-tela-form').classList.add('oculto');  // Cambia de 'nuevo-personaje-form' a 'nuevo-tela-form'
        document.getElementById('juego-container').classList.remove('oculto');  // Esta línea ya es correcta
    
        cargarTelas();
    }
    

    window.guardarNuevaTela = function guardarNuevaTela() {
        const nombre = document.getElementById('nombre-tela').value.trim();
        const nuevaCaracteristica = document.getElementById('nueva-caracteristica-input').value.trim().toLowerCase();
        const tipoCaracteristica = document.querySelector('input[name="tipo-caracteristica"]:checked')?.value;
    
        if (!nombre || !nuevaCaracteristica || !tipoCaracteristica) {
            alert('Completa todos los campos.');
            return;
        }
    
        const claveCaracteristica = nuevaCaracteristica.replace(/\s+/g, '_');
    
        const nuevasCaracteristicas = generarAtributosParaNuevaTela();
    
        nuevasCaracteristicas[claveCaracteristica] = {
            valor: 1,
            tipo: tipoCaracteristica
        };
    
        const nuevaTela = {
            nombre,
            caracteristicas: nuevasCaracteristicas
        };
    
        agregarTelaABaseDatos(nuevaTela)
            .then(() => actualizarTelasExistentes(claveCaracteristica, tipoCaracteristica))
            .then(() => {
                alert(`¡La tela "${nombre}" se ha agregado con éxito!`);
                reiniciarJuego();
            })
            .catch((error) => {
                alert(`Error al agregar la tela: ${error.message}`);
            });
    };
    
    
    

    function generarAtributosParaNuevaTela() {
        let nuevasCaracteristicas = {};
    
        const atributosConocidos = new Set();
        posiblesTelas.forEach(tela => {
            Object.keys(tela.caracteristicas).forEach(attr => {
                atributosConocidos.add(attr);
            });
        });
    
        atributosConocidos.forEach(attr => {
            nuevasCaracteristicas[attr] = {
                valor: Math.random() < 0.5 ? 1 : 0,
                tipo: 'desconocido'
            };
        });
    
        return nuevasCaracteristicas;
    }
        
    
    
    function actualizarTelasExistentes(claveNueva, tipoCaracteristica) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['telas'], 'readwrite');
            const objectStore = transaction.objectStore('telas');
    
            objectStore.openCursor().onsuccess = function (event) {
                const cursor = event.target.result;
                if (cursor) {
                    const tela = cursor.value;
    
                    if (!(claveNueva in tela.caracteristicas)) {
                        tela.caracteristicas[claveNueva] = {
                            valor: Math.random() < 0.5 ? 1 : 0,
                            tipo: tipoCaracteristica
                        };
                    }
    
                    cursor.update(tela);
                    cursor.continue();
                } else {
                    resolve();
                }
            };
    
            transaction.onerror = (event) => reject(event.target.error);
        });
    }
    
        
    
    function determinarTipoDePregunta(atributo, tipo) {
        const nombreAtributo = atributo.replace(/_/g, ' ');
    
        switch (tipo) {
            case 'textura':
                return `¿La tela es de textura ${nombreAtributo}?`;
            case 'durabilidad':
                return `¿La tela es ${nombreAtributo} en durabilidad?`;
            case 'peso':
                return `¿La tela es de peso ${nombreAtributo}?`;
            case 'apariencia':
                return `¿La tela tiene apariencia ${nombreAtributo}?`;
            case 'origen':
                return `¿La tela es de origen ${nombreAtributo}?`;
            case 'propiedad':
                return `¿La tela tiene propiedad ${nombreAtributo}?`;
            default:
                return `¿La tela es ${nombreAtributo}?`;
        }
    }
    
    
    

    function agregarTelaABaseDatos(tela) {
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['telas'], 'readwrite');
            const store = transaction.objectStore('telas');

            const request = store.add(tela);
            request.onsuccess = () => resolve();
            request.onerror = (event) => reject(event.target.error);
        });
    }

    function reiniciarJuego() {
        faseAdivinanza = false;
        telaAdivinada = '';
        preguntaActual = null;
    
        posiblesTelas = [];
        preguntas = [];
    
        // Verificar si los elementos existen antes de manipular classList
        const nuevoTelaForm = document.getElementById('nuevo-tela-form');
        const juegoContainer = document.getElementById('juego-container');
    
        if (nuevoTelaForm) {
            nuevoTelaForm.classList.add('oculto');  // Oculta el formulario de nueva tela si existe
        } else {
            console.error("Elemento 'nuevo-tela-form' no encontrado en el DOM.");
        }
    
        if (juegoContainer) {
            juegoContainer.classList.remove('oculto');  // Muestra el contenedor del juego si existe
        } else {
            console.error("Elemento 'juego-container' no encontrado en el DOM.");
        }
    
        // Recargar los personajes desde la base de datos
        cargarTelas();
    }
    
    

    window.actualizarVistaPrevia = function actualizarVistaPrevia() {
        const nuevaCaracteristica = document.getElementById('nueva-caracteristica-input').value.trim();
        const tipoCaracteristica = document.querySelector('input[name="tipo-caracteristica"]:checked')?.value;
        let pregunta = '';

        if (nuevaCaracteristica && tipoCaracteristica) {
            switch (tipoCaracteristica) {
                case 'textura':
                    pregunta = `¿La tela es de textura ${nuevaCaracteristica}?`;
                    break;
                case 'durabilidad':
                    pregunta = `¿La tela es ${nuevaCaracteristica} en durabilidad?`;
                    break;
                case 'peso':
                    pregunta = `¿La tela es de peso ${nuevaCaracteristica}?`;
                    break;
                case 'apariencia':
                    pregunta = `¿La tela tiene apariencia ${nuevaCaracteristica}?`;
                    break;
                case 'origen':
                    pregunta = `¿La tela es de origen ${nuevaCaracteristica}?`;
                    break;
                case 'propiedad':
                    pregunta = `¿La tela tiene propiedad ${nuevaCaracteristica}?`;
                    break;
                default:
                    pregunta = `¿La tela es ${nuevaCaracteristica}?`;
            }
        }

        document.getElementById('vista-previa-pregunta').innerText = pregunta;
    };
});
