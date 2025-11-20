async function cargarDatos() {
    const res = await fetch("/datos");
    const datos = await res.json();

    const tbody = document.getElementById("tabla");
    tbody.innerHTML = "";

    datos.forEach(row => {
        tbody.innerHTML += `
            <tr>
                <td>${row.fecha}</td>
                <td>${row.uv}</td>
                <td>${row.temperatura}</td>
            </tr>
        `;
    });
}

async function cargarPrediccion() {
    const res = await fetch("/prediccion");
    const data = await res.json();

    document.getElementById("prediccion").innerText =
        "UV esperado: " + parseFloat(data.prediccion_uv).toFixed(2);
}

setInterval(() => {
    cargarDatos();
    cargarPrediccion();
}, 5000);

cargarDatos();
cargarPrediccion();
