with open("templates/index.html", "r") as f:
    content = f.read()

# Add a warning badge inside the result card if IA failed
old_result = """                    const card = document.getElementById('resultadoCard');
                    card.classList.add('active');
                    document.getElementById('resFolio').innerText = `FOLIO: ${res.folio} (${res.estado_hash})`;"""

new_result = """                    const card = document.getElementById('resultadoCard');
                    card.classList.add('active');
                    if (res.ia_disponible === false) {
                        document.getElementById('resSeveridad').parentElement.innerHTML += '<br><span style="color:#ef4444; font-size:0.8rem; font-weight:bold;">⚠️ IA Offline: Requiere Inspección Humana</span>';
                    }
                    document.getElementById('resFolio').innerText = `FOLIO: ${res.folio} (${res.estado_hash})`;"""

content = content.replace(old_result, new_result)

with open("templates/index.html", "w") as f:
    f.write(content)
