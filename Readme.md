# 📐 Reflexiones Geométricas Interactivas

Una aplicación web interactiva construida con Streamlit para visualizar la reflexión de figuras geométricas en el plano cartesiano. Diseñada como una herramienta educativa, permite a los usuarios definir polígonos, elegir diferentes ejes de reflexión y observar la transformación en tiempo real, junto con explicaciones teóricas detalladas.


## 🎬 Demostración

**¡Puedes probar la aplicación en vivo en el siguiente enlace!**

### ➡️ [reflexion.streamlit.app](https://proyecto-reflexion.streamlit.app) ⬅️

## ✨ Características Principales

*   **Definición de Figuras Personalizadas**: Introduce los vértices de cualquier polígono para visualizarlo.
*   **Gestión Dinámica de Vértices**: Añade o elimina vértices fácilmente para modificar la figura sobre la marcha.
*   **Múltiples Tipos de Reflexión**: Soporte para una amplia variedad de reflexiones:
    *   Sobre el Eje X (`y=0`)
    *   Sobre el Eje Y (`x=0`)
    *   Sobre el Origen `(0,0)`
    *   Sobre la línea `y = x`
    *   Sobre la línea `y = -x`
    *   Sobre una línea horizontal personalizable (`y = k`)
    *   Sobre una línea vertical personalizable (`x = h`)
*   **Visualización Interactiva**: Gráficos claros y dinámicos generados con Plotly que muestran la figura original, la figura reflejada y el eje de reflexión.
*   **Componente Educativo**: Una pestaña dedicada a la "Teoría de la Reflexión" que explica los conceptos matemáticos detrás de cada transformación con fórmulas y ejemplos.
*   **Interfaz Intuitiva**: Diseño limpio y fácil de usar gracias a Streamlit, con controles separados para la entrada de datos y la visualización.

---

## 🛠️ Tecnologías Utilizadas

*   **Python**: Lenguaje de programación principal.
*   **Streamlit**: Framework para la creación de la aplicación web.
*   **Plotly**: Biblioteca para la generación de gráficos interactivos.
*   **NumPy**: Para cálculos numéricos y la generación de rangos para las líneas de reflexión.

---

## 🚀 Instalación y Ejecución Local

Para ejecutar esta aplicación en tu máquina local, sigue estos pasos:

1.  **Clona el repositorio** (o descarga los archivos en un directorio local).
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2.  **Crea y activa un entorno virtual** (recomendado):
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala las dependencias**:
    Crea un archivo `requirements.txt` con el siguiente contenido:
    ```txt
    streamlit
    plotly
    numpy
    ```
    Luego, instálalas usando pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación**:
    Una vez instaladas las dependencias, ejecuta el siguiente comando en tu terminal:
    ```bash
    streamlit run app.py
    ```

5.  Abre tu navegador web y ve a la URL local que te indica la terminal (generalmente `http://localhost:8501`).

---

## 📖 ¿Cómo Usar la Aplicación?

1.  **Navega a la pestaña "Aplicación Interactiva"**.
2.  **Introduce las coordenadas** de los vértices de tu figura en los campos de entrada `(x, y)`. La aplicación comienza con un triángulo de ejemplo.
3.  Usa el botón **"Añadir Vértice"** para agregar más puntos o el botón **"X"** junto a un vértice para eliminarlo.
4.  **Selecciona el tipo de reflexión** que deseas visualizar en el menú desplegable.
5.  Si eliges una reflexión sobre una línea horizontal o vertical, **introduce el valor de `k` o `h`** en el campo numérico que aparecerá.
6.  Observa el gráfico para ver la figura original (azul), la figura reflejada (roja) y el eje de reflexión (verde punteado).
7.  Para aprender más sobre los conceptos matemáticos, visita la pestaña **"Teoría de la Reflexión"**.

---

## 👨‍💻 Autor

Desarrollado con ❤️ por tu programador Python amigo.