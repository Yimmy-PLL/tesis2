const URL_API = "https://tesis2.onrender.com";

// ----------------------------
// Cargar datos en tiempo real
// ----------------------------
async function cargarDatos() {
    try {
        const res = await fetch(URL_API + "/datos");
        const datos = await res.json();

        if (datos.length === 0) return;

        const ultimo = datos[0];

        document.getElementById("uv_actual").textContent = ultimo.uv;
        document.getElementById("temp_actual").textContent = ultimo.temperatura;

        actualizarGrafico(datos.reverse());

    } catch (err) {
        console.log("Error cargando datos:", err);
    }
}

// ----------------------------
// Predicción desde el servidor
// ----------------------------
async function cargarPrediccion() {
    try {
        const res = await fetch(URL_API + "/prediccion");
        const data = await res.json();

        document.getElementById("uv_prediccion").textContent =
            data.prediccion_uv !== undefined ? data.prediccion_uv.toFixed(2) : "--";

    } catch (err) {
        console.log("Error predicción:", err);
    }
}

// ----------------------------
//    Gráfico de UV
// ----------------------------
let grafico = null;

function actualizarGrafico(datos) {
    const ctx = document.getElementById("grafico_uv").getContext("2d");

    const labels = datos.map(d => d.fecha.slice(11, 16));  
    const uv_values = datos.map(d => d.uv);

    if (grafico) grafico.destroy();

    grafico = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "UV",
                data: uv_values,
                borderWidth: 2
            }]
        }
    });
}

// ----------------------------
// Ejecutar cada 3 segundos
// ----------------------------
setInterval(() => {
    cargarDatos();
    cargarPrediccion();
}, 3000);

// correr al inicio
cargarDatos();
cargarPrediccion();
