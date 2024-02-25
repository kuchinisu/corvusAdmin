const ancho = 640;
const alto = 400;
const marginUp = 20;
const marginR = 20;
const marginDown = 30;
const marginL = 40; 

var escala_maxima_ = 0;
const listaDeDias_c = document.getElementById('lista_de_dias_clientes');
const diasTotal = listaDeDias_c.children.length;
const listaFechas = [];
const listaGanancias = [];

for(let i = 0; i < diasTotal; i++){
    const dia = listaDeDias_c.children[i];
    const ganancia = parseFloat(dia.getAttribute('data-clientes'))
    
    if(ganancia > escala_maxima_){
        escala_maxima_ = ganancia;
        console.log(escala_maxima_);
    };

    listaFechas.push('' + dia.getAttribute('data-year') + '-'
     + dia.getAttribute('data-mes') + '-' + dia.getAttribute('data-dia'));
    listaGanancias.push(dia.getAttribute('data-clientes'))
    
};

const ultimoElemento = listaDeDias_c.children[diasTotal-1]
var fechaUltima = '' + ultimoElemento.getAttribute('data-year') + 
'-' + ultimoElemento.getAttribute('data-mes') + '-' + ultimoElemento.getAttribute('data-dia');

const primerElemento = listaDeDias_c.children[0];
var fechaPrimera = primerElemento.getAttribute('data-year') + 
'-' + primerElemento.getAttribute('data-mes') + '-' + primerElemento.getAttribute('data-dia');


const x = d3.scaleUtc()
    .domain([new Date(fechaPrimera), new Date(fechaUltima)])
    .range([marginL, ancho - marginR]);

console.log([new Date(fechaPrimera), new Date(fechaUltima)]);

// Declare the y (vertical position) scale. width
const y = d3.scaleLinear()
    .domain([0, escala_maxima_])
    .range([alto - marginDown, marginUp]);

// Create the SVG container.
const svg = d3.create("svg")
    .attr("width", ancho)
    .attr("height", alto);

// Add the x-axis.
svg.append("g")
    .attr("transform", `translate(0,${alto - marginDown})`)
    .call(d3.axisBottom(x));

// Add the y-axis.
svg.append("g")
    .attr("transform", `translate(${marginL},0)`)
    .call(d3.axisLeft(y));


//////
const fechas = [new Date(fechaPrimera), new Date(fechaUltima)]
const fecha1 = fechas[0];
const fecha2 = fechas[1];
  
const datos = [];

for(let i = 0; i < listaFechas.length; i ++){
    console.log(listaGanancias[i]);
    datos.push({fecha: listaFechas[i], ganancias: listaGanancias[i]})
};
  
svg.selectAll("circle")
    .data(datos)  
    .enter()
    .append("circle")
    .attr("cx", d => x(new Date(d.fecha)))  
    .attr("cy", d => y(d.ganancias))
    .attr("r", 5)  
    .attr("fill", "red");  
// ...


///////

// Append the SVG element.
container_c.append(svg.node());