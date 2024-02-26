const width = 640;
const height = 400;
const marginTop = 20;
const marginRight = 20;
const marginBottom = 30;
const marginLeft = 40;

var escala_maxima = 0;
const listaDeDias = document.getElementById('lista_de_dias');
const diasTotal = listaDeDias.children.length;
const listaFechas = [];
const listaGanancias = [];

for(let i = 0; i < diasTotal; i++){
    const dia = listaDeDias.children[i];
    const ganancia = parseFloat(dia.getAttribute('data-ganancias'))
    
    listaFechas.push('' + dia.getAttribute('data-year') + '-'
     + dia.getAttribute('data-mes') + '-' + dia.getAttribute('data-dia'));
    listaGanancias.push(dia.getAttribute('data-ganancias'))

    if(ganancia > escala_maxima){
        escala_maxima = ganancia;
        //console.log(escala_maxima);
    };

    
};
const listaFechasCorr = [...listaFechas].reverse()
const listaGananciasCorr = [...listaGanancias].reverse()
//console.log(listaGananciasCorr)

const ultimoElemento = listaDeDias.children[diasTotal-1] 
var fechaUltima = '' + ultimoElemento.getAttribute('data-year') + 
'-' + ultimoElemento.getAttribute('data-mes') + '-' + ultimoElemento.getAttribute('data-dia');

const primerElemento = listaDeDias.children[0];
var fechaPrimera = primerElemento.getAttribute('data-year') + 
'-' + primerElemento.getAttribute('data-mes') + '-' + primerElemento.getAttribute('data-dia');


const x = d3.scaleUtc()
    .domain([new Date(fechaPrimera), new Date(fechaUltima)])
    .range([marginLeft, width - marginRight]);


// Declare the y (vertical position) scale.
const y = d3.scaleLinear()
    .domain([0, escala_maxima])
    .range([height - marginBottom, marginTop]);

// Create the SVG container.
const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height);

// Add the x-axis.
svg.append("g")
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(d3.axisBottom(x));

// Add the y-axis.
svg.append("g")
    .attr("transform", `translate(${marginLeft},0)`)
    .call(d3.axisLeft(y));


//////
const fechas = [new Date(fechaPrimera), new Date(fechaUltima)]
//console.log("fechas: ")
//console.log(fechas)
const fecha1 = fechas[0];
const fecha2 = fechas[1];

const datos = [];

for(let i = 0; i < listaFechasCorr.length; i ++){
    console.log(listaGanancias[i]);
    datos.push({fecha: listaFechasCorr[i], ganancias: listaGananciasCorr[i]})
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
container.append(svg.node()); 