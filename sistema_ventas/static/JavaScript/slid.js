const desplazamiento = 150; 
const contenedorProductos = document.getElementsByClassName('productos')[0];

document.getElementById('derecha').addEventListener('click', function() {
  contenedorProductos.scrollLeft += desplazamiento;
});

document.getElementById('izquierda').addEventListener('click', function() {
  contenedorProductos.scrollLeft -= desplazamiento;
});
