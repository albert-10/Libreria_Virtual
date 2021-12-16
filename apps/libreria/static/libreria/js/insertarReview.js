/* Este script permite seleccionar la calificacion en forma de estrellas y que el numero de estrella seleccionada
sea el mismo que el elemento de la lista de seleccion*/

const PRIMERA_ESTRELLA = document.getElementById('primeraEstrella');
const SEGUNDA_ESTRELLA = document.getElementById('segundaEstrella');
const TERCERA_ESTRELLA = document.getElementById('terceraEstrella');
const CUARTA_ESTRELLA = document.getElementById('cuartaEstrella');
const QUINTA_ESTRELLA = document.getElementById('quintaEstrella');

const LISTA_ESTRELLAS = [PRIMERA_ESTRELLA, SEGUNDA_ESTRELLA, TERCERA_ESTRELLA, CUARTA_ESTRELLA, QUINTA_ESTRELLA]

/* La siguiente funcion recibe el id de un elemento estrella y permite que la estrella sea seleccionada
asi como las estrellas anteriores. Tambien permite el elemento equivalente de la lista de seleccion
que se encuentra occulta */

const SELECCION_ESTRELLA = (seleccionada) => {
    
    switch (seleccionada) {
        case 'primeraEstrella':
            PRIMERA_ESTRELLA.classList.add('checked');
            SEGUNDA_ESTRELLA.classList.remove('checked');
            TERCERA_ESTRELLA.classList.remove('checked');
            CUARTA_ESTRELLA.classList.remove('checked');
            QUINTA_ESTRELLA.classList.remove('checked');
            seleccionarCalificacion(0);            
            break;
        case 'segundaEstrella':
            PRIMERA_ESTRELLA.classList.add('checked');
            SEGUNDA_ESTRELLA.classList.add('checked');
            TERCERA_ESTRELLA.classList.remove('checked');
            CUARTA_ESTRELLA.classList.remove('checked');
            QUINTA_ESTRELLA.classList.remove('checked');
            seleccionarCalificacion(1); 
            break;
        case 'terceraEstrella':
            PRIMERA_ESTRELLA.classList.add('checked');
            SEGUNDA_ESTRELLA.classList.add('checked');
            TERCERA_ESTRELLA.classList.add('checked');
            CUARTA_ESTRELLA.classList.remove('checked');
            QUINTA_ESTRELLA.classList.remove('checked');
            seleccionarCalificacion(2); 
            break;
        case 'cuartaEstrella':
            PRIMERA_ESTRELLA.classList.add('checked');
            SEGUNDA_ESTRELLA.classList.add('checked');
            TERCERA_ESTRELLA.classList.add('checked');
            CUARTA_ESTRELLA.classList.add('checked');
            QUINTA_ESTRELLA.classList.remove('checked');
            seleccionarCalificacion(3); 
            break;            
        case 'quintaEstrella':
            PRIMERA_ESTRELLA.classList.add('checked');
            SEGUNDA_ESTRELLA.classList.add('checked');
            TERCERA_ESTRELLA.classList.add('checked');
            CUARTA_ESTRELLA.classList.add('checked');
            QUINTA_ESTRELLA.classList.add('checked');
            seleccionarCalificacion(4); 
            break;
    }
}

/* La siguiente funcion le agrega a cada elemento estrella una funcion manejadora de eventos, que permite
la seleccion de estrellas */

LISTA_ESTRELLAS.forEach( elemento => elemento.addEventListener('click', (event)=>{
    SELECCION_ESTRELLA(event.target.id);    
}));

// La siguient funcion permite seleccionar una opcion de la lista de seleccion

function seleccionarCalificacion(indice){
    document.getElementById('id_calificacion').selectedIndex = indice
}

// El siguiente metodo permite seleccionar la primera estrella, asi como el primer elemento de la lista de seleccion

function seleccionarPrimeraEstrella(){
    PRIMERA_ESTRELLA.classList.add('checked');
    SEGUNDA_ESTRELLA.classList.remove('checked');
    TERCERA_ESTRELLA.classList.remove('checked');
    CUARTA_ESTRELLA.classList.remove('checked');
    QUINTA_ESTRELLA.classList.remove('checked');
    seleccionarCalificacion(0); 
}

// Al iniciar se asigna la funcion manejadora del evento click sobre el boton reset, para poder reiniciar las 
// estrellas y la lista de seleccion

function iniciar(){
    document.getElementById('reset').addEventListener('click', seleccionarPrimeraEstrella);    
}

window.addEventListener('load', iniciar);