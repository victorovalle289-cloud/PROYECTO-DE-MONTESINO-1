// =====================================================================
//  Gestor de contraseñas - Frontend (consume la API Flask)
// =====================================================================
const BASE_URL = 'http://127.0.0.1:5000'; // Dirección del backend

// Pinta los registros recibidos en la tabla de index.html
function visualizar(data) {
  let tabla = '';
  data.baul.forEach(item => {
    tabla += `<tr data-id="${item.id_baul}">
      <td>${item.id_baul}</td>
      <td>${item.Plataforma}</td>
      <td>${item.usuario}</td>
      <td>********</td>
      <td><button class="btn btn-primary" onclick="location.href='edit.html?variable1=${item.id_baul}'">
          <img src="imagenes/edit.png" height="30" width="30" alt=""> Editar</button></td>
      <td><button class="btn btn-danger" onclick="eliminar(${item.id_baul})">
          <img src="imagenes/delete.png" height="30" width="30" alt=""> Eliminar</button></td>
    </tr>`;
  });
  document.getElementById('data').innerHTML = tabla;
}

// Consulta general (GET)
function consulta_general() {
  fetch(`${BASE_URL}/`)                                        // Solicitud GET
    .then(response => {
      if (!response.ok) throw new Error(`Error: ${response.status}`); // Manejo de errores HTTP
      return response.json();                                  // Convierte a JSON
    })
    .then(data => visualizar(data))                            // Muestra los datos
    .catch(error => console.error('Error:', error));
}

// Eliminar un registro (DELETE)
function eliminar(id) {
  fetch(`${BASE_URL}/eliminar/${id}`, { method: 'DELETE' })
    .then(response => {
      if (!response.ok) throw new Error(`Error: ${response.status}`);
      return response.json();
    })
    .then(res => {
      actualizarDOM(id);                                       // Quita la fila sin recargar
      swal("Mensaje", `Registro ${res.mensaje} exitosamente`, "success");
    })
    .catch(error => console.error('Error:', error));
}

// Quita del DOM la fila eliminada
function actualizarDOM(id) {
  const row = document.querySelector(`tr[data-id="${id}"]`);
  if (row) row.remove();
}

// Registrar un nuevo elemento (POST)
function registrar() {
  const plat = document.getElementById('plataforma').value;
  const usua = document.getElementById('usuario').value;
  const clav = document.getElementById('clave').value;
  if (!plat || !usua || !clav) {                               // Validación simple
    swal("Mensaje", "Todos los campos son obligatorios", "warning");
    return;
  }
  fetch(`${BASE_URL}/registro/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plataforma: plat, usuario: usua, clave: clav })
  })
    .then(response => response.json())
    .then(res => {
      if (res.mensaje === 'Error') {
        swal("Mensaje", "Error en el registro", "error");
      } else {
        swal("Mensaje", "Registro agregado exitosamente", "success")
          .then(() => location.href = 'index.html');
      }
    })
    .catch(error => console.error('Error:', error));
}

// Consulta individual: llena el formulario de edit.html (GET)
function consulta_individual() {
  const id = new URLSearchParams(window.location.search).get('variable1'); // Lee el id de la URL
  fetch(`${BASE_URL}/consulta_individual/${id}`)
    .then(response => response.json())
    .then(res => {
      if (!res.baul) { swal("Mensaje", res.mensaje, "error"); return; }
      document.getElementById('id_baul').value = res.baul.id_baul;
      document.getElementById('plataforma').value = res.baul.Plataforma;
      document.getElementById('usuario').value = res.baul.usuario;
    })
    .catch(error => console.error('Error:', error));
}

// Actualizar un registro (PUT)
function modificar() {
  const id = document.getElementById('id_baul').value;
  const plat = document.getElementById('plataforma').value;
  const usua = document.getElementById('usuario').value;
  const clav = document.getElementById('clave').value;
  if (!plat || !usua || !clav) {
    swal("Mensaje", "Todos los campos son obligatorios", "warning");
    return;
  }
  fetch(`${BASE_URL}/actualizar/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plataforma: plat, usuario: usua, clave: clav })
  })
    .then(response => response.json())
    .then(res => {
      if (res.mensaje === 'Error') {
        swal("Mensaje", "Error al actualizar", "error");
      } else {
        swal("Mensaje", "Registro actualizado exitosamente", "success")
          .then(() => location.href = 'index.html');
      }
    })
    .catch(error => console.error('Error:', error));
}
