function abrirModalNomeUsuario() { var m=document.getElementById('modalNomeUsuario'); if(m){m.classList.add('active');document.body.style.overflow='hidden';} }
function fecharModalNomeUsuario() { var m=document.getElementById('modalNomeUsuario'); if(m){m.classList.remove('active');document.body.style.overflow='auto';} }
function abrirModalEditarPerfil() { var m=document.getElementById('modalEditarPerfil'); if(m){m.classList.add('active');document.body.style.overflow='hidden';} }
function fecharModalEditarPerfil() { var m=document.getElementById('modalEditarPerfil'); if(m){m.classList.remove('active');document.body.style.overflow='auto';} }
function abrirModalRemoverFoto() { var m=document.getElementById('modalRemoverFoto'); if(m){m.classList.add('active');document.body.style.overflow='hidden';} }
function fecharModalRemoverFoto() { var m=document.getElementById('modalRemoverFoto'); if(m){m.classList.remove('active');document.body.style.overflow='auto';} }
function confirmarRemoverFoto() { var f=document.getElementById('formRemoverFoto'); if(f) f.submit(); fecharModalRemoverFoto(); }
document.addEventListener('keydown',function(e){if(e.key==='Escape'){fecharModalNomeUsuario();fecharModalEditarPerfil();fecharModalRemoverFoto();}});
document.addEventListener('click',function(e){['modalNomeUsuario','modalEditarPerfil','modalRemoverFoto'].forEach(function(id){var m=document.getElementById(id);if(m&&e.target===m)m.classList.remove('active');});});
