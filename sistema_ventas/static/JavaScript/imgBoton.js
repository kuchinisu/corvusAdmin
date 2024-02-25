$(document).ready(function () {
    
    $(".imagen-botón").on("click", function () {
        if ($(this).attr("src") === '/static/img/enhw.jpg') {
            window.location.href = '/cobro/estilo coreano';
        } else if ($(this).attr("src") === '/static/img/alize.jpeg') {
            window.location.href = '/cobro/estilo francés';
        } else if ($(this).attr("src") === '/static/img/pokemomo.jpg') {
            window.location.href = '/cobro';
        }
    });
});