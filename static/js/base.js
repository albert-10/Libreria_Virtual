// El siguiente script permite mostrar y ocultar el header de la pagina, al hacer click al boton
// del navbar o al redimencionar la ventana

// Dependiendo de su valor se mostrara u ocultara el header

headerOculto = false;

// La siguiente funcion permite ocultar el header

function ocultarHeader() {
  header = document.getElementById('headerSitio');
  contenedorSitio = document.getElementById('contenedorSitio');
  header.style.display = 'none';
  contenedorSitio.style.setProperty('grid-template-rows','repeat(1, 1fr)') 
  navBar = document.getElementById('navbar');
  navBar.style.setProperty('grid-row-start','1');
  navBar.style.setProperty('grid-row-end','2');
  headerOculto = true;
}

// La siguiente funcion permite mostrar el header

function mostrarHeader() {
  header = document.getElementById('headerSitio');
  contenedorSitio = document.getElementById('contenedorSitio');
  header.style.display = 'block';
  contenedorSitio.style.setProperty('grid-template-rows','repeat(6, 1fr)');
  navBar = document.getElementById('navbar');
  navBar.style.setProperty('grid-row-start','6');
  navBar.style.setProperty('grid-row-end','7');
  headerOculto = false;
}

// La siguiente funcion permitira mostrar u ocultar el header, dependiendo de si esta oculto o no

function ocultarMostrarHeader(){
    if(headerOculto){
        mostrarHeader();        
    }

    else{
        ocultarHeader();
    }
}

/* Al redimencionar la ventana a un mayor tamano que 992px se va a mostrar el header. Tambien
se a plegar el menu del navbar */

function cambiarTamano(event){    
    if(event.matches && headerOculto){      
            mostrarHeader();
            botonNabBar = document.getElementById('navbar-toggler-button');            
            document.getElementById("navbarNav").classList.remove("show");
    }  
}

/* La siguiente funcion se invocara al cargarse la ventana. Aqui se le asigna una funcion manejadora
del evento change a la ventana. Tambien se le asinga uan funcion manejadora del evento click la boton
del navbar*/

function iniciar(){
    const mediaQuery = window.matchMedia('(min-width: 992px)');
    mediaQuery.addEventListener('change', cambiarTamano);
    toogleButton = document.getElementById('navbar-toggler-button');
    toogleButton.addEventListener('click', ocultarMostrarHeader)

}

window.addEventListener('load', iniciar)