function addLista() {
    const listaProductosC = document.getElementById("productos_l_l");
    const productN = document.createElement("li");
    const imgP = document.createElement("img");
    const marcaPrecio = document.getElementById("marca_total");
    const ex = document.createElement("li")
    const eliminar = document.createElement("button");
    const tarjeta = document.createElement("div");
    const precio = document.createElement("div");

    const boton = event.currentTarget;

    const codigoProducto = boton.getAttribute('data-producto-codigo');
    const precioProducto = boton.getAttribute('data-producto-precio');
    const imagenProducto = boton.getAttribute('data-producto-imagen');
    const existencias = boton.getAttribute('data-producto-existencia');
    const precioAct = parseFloat(marcaPrecio.innerText); 

    const textoBoton = boton.innerText;

    const jsonDat = {
        "codigo": codigoProducto,
        "precio": precioProducto
    };

    precio.id = "precio_ind";
    precio.innerText = precioProducto;
    productN.innerText = codigoProducto
    productN.id = "inf_p";
    imgP.src = imagenProducto
    imgP.className = "image_producto";
    imgP.id = "image_producto";
    ex.innerText = existencias;
    ex.id = "existencia"
    eliminar.id = "boton_eliminar";
    eliminar.onclick = eliminarArticulo;
    

    marcaPrecio.innerText = precioAct + parseFloat(precioProducto);
    ex.innerText = existencias;
    eliminar.innerText = "Eliminar del carrito"
    //ex.appendChild(eliminar);
    tarjeta.id = "tarjeta";
    tarjeta.appendChild(imgP);
    tarjeta.appendChild(productN);
    tarjeta.appendChild(ex);
    tarjeta.appendChild(eliminar);
    tarjeta.appendChild(precio);
    listaProductosC.appendChild(tarjeta);
    console.log(existencias)

}

function cobrar(){
    const aPagar = document.getElementById("a_pagar");
    const opcionesPago = document.getElementById("opciones_pago");
    aPagar.style.display = "none";
    opcionesPago.style.display = "block";

}

function realizarCobro(){
    const aPagar = document.getElementById("dinero_pagado");
    const totalDiv = document.getElementById("marca_total");
    const total = parseFloat(totalDiv.innerText);
    const pagado = parseFloat(aPagar.value);
    const avisoFaltante = document.getElementById("aviso_falta_dinero");
    const listaProductos = document.getElementById("productos_l_l");
    const avisoFaltaProducto = document.getElementById("aviso_falta_producto")

    var faltante = false
    let jsonPr = {}

    

    if(total > pagado){
        avisoFaltante.style.display = "block";        
    } else {
        for (let i = 0; i < listaProductos.children.length; i++) {
            const tarjeta = listaProductos.children[i];
            for (let j = 0; j < tarjeta.children.length; j++) {
                const liElement = tarjeta.children[j];

                if (liElement.id === "existencia") {
                    const existencia = liElement.innerText;
                    if (parseInt(existencia) <= 0) {
                        faltante = true;
                    }
                } else if (liElement.id === "image_producto") {
                    const imagen = liElement.id;
                    console.log(imagen);
                } else if (
                    liElement.id === "inf_p" &&
                    liElement.id !== "tarjeta" &&
                    liElement.id !== "boton_eliminar" &&
                    liElement.id !== "precio_ind"
                ) {
                    console.log(liElement.id);
                    jsonPr["producto " + i] = liElement.innerText;
                }
            }
        }

        if(faltante){
            avisoFaltaProducto.style.display = "block";
        }else{
            //////////
            const url = 'http://127.0.0.1:8000/cobro/comprar_carrito';
            
            
            const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

              fetch(url, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams(jsonPr),
                mode: 'cors', 
              })
                .then(response => response.json())
                .then(data => {
                  console.log(data);
                  datosj = data;  
                })
                .catch(error => console.error('Error:', error));
            /////////
        }
        
    }
    
}

function eliminarArticulo() {

    var tarjeta = document.getElementById('tarjeta');
    var precio = document.getElementById('precio_ind');
    const total = document.getElementById('marca_total');

  
    if (tarjeta) {
        total.innerText = parseFloat(total.innerText) - parseFloat(precio.innerText);
        tarjeta.remove();
    };


}