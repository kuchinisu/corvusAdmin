const elementos = document.getElementById("lista_servicios");

const ancho = 640;
const alto = 400;
const marginUp = 20;
const marginR = 20;
const marginDown = 30;
const marginL = 40; 

//const plot = Plot.rectY({length: 1}, Plot.binX({y: "count"}, {x: 0.5})).plot();


const dineroReunido = 100;
const meta = 1000;

// Crea el gráfico de barras
const plot = Plot.plot({
  marginTop: 60,
  marginRight: 60,
  marginBottom: 60,
  marginLeft: 60,
  grid: true,
  marks: [
    Plot.barY(
      [
        { meta, label: "Meta" },
        { dineroReunido, label: "Dinero Reunido" }
      ],
      {
        x: "label",
        y: d => d.meta,
        fill: d => (d.label === "Dinero Reunido" ? "green" : "lightblue")
      }
    ),
    Plot.frame()
  ],
  y: { domain: [0, meta] } // Establece el dominio del eje y
});

// Agrega el gráfico al contenedor
document.querySelector("#plot_serv").appendChild(plot);

