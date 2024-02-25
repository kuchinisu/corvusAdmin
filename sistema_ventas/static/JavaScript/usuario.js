const usuario = document.getElementById("nombre_usuario");
const contra = document.getElementById("contrase");
const boton = document.getElementById("iniciar_sesion");

boton.addEventListener("click", function(){ 
    //window.alert("Hello World!");
    const n_usuario = usuario.value;
    const n_contra = contra.value;

    var datos = {
        "usuario": n_usuario,
        "contrase": n_contra,
    };

    url = "http://127.0.0.1:8000/usuario/entrar"
    fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken,
        },
        body: new URLSearchParams(datos),
        mode: 'cors', 
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          datosj = data;  
        })
        .catch(error => console.error('Error:', error));


});