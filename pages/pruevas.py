# 1. Importamos la clase FPDF de la librería fpdf
from fpdf import FPDF

# 2. Creamos una instancia del objeto FPDF
# Por defecto, el formato es A4, la unidad de medida es milímetros y la orientación es Vertical (Portrait).
pdf = FPDF()

# 3. Añadimos una página al documento
# Es obligatorio añadir al menos una página antes de intentar escribir texto.
pdf.add_page()

# 4. Establecemos la fuente inicial (Arial, tamaño 12)
pdf.set_font("Arial", size=12)

# 5. Cambiamos la fuente para el título (Arial, Negrita "B", tamaño 16)
pdf.set_font("Arial", style="B", size=16)

# 6. Creamos una celda para el título
# w=200: Ancho de la celda.
# h=10: Alto de la celda.
# txt: El texto que se mostrará.
# ln=True: Indica que después de esta celda debe haber un salto de línea.
# align="C": Alinea el texto al Centro.
pdf.cell(200, 10, txt="My First PDF in Python", ln=True, align="C")

# 7. Volvemos a cambiar la fuente para el cuerpo del texto (Arial, normal, tamaño 12)
pdf.set_font("Arial", size=12)

# 8. Creamos una multi-celda para el contenido
# w=0: Al poner 0, la celda se extiende hasta el margen derecho de la página.
# h=10: Alto de cada línea.
# txt: El texto del párrafo.
pdf.multi_cell(0, 10, txt="Prueba creacion de pdf con python")

# 9. Generamos y guardamos el archivo físico
# El nombre del archivo será "Prueva_creacion_PDF.pdf" y se guardará en la misma carpeta que el script.
pdf.output("Prueva_creacion_PDF.pdf")

# 10. Mensaje de confirmación en la consola
print("PDF creado con exito!")