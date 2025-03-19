# Leer el contenido del archivo style.css y guardarlo en una variable
with open("style.css", "r", encoding="utf-8") as archivo_css:
    css_contenido = archivo_css.read()

# Imprimir para verificar (opcional)
print(css_contenido)