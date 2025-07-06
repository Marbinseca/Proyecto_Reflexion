import streamlit as st
import plotly.graph_objects as go
import numpy as np
import string

# --- Función para la reflexión de puntos ---
def reflect_point(x, y, reflection_type, custom_value=0):
    """
    Refleja un punto (x, y) según el tipo de reflexión especificada.

    Args:
        x (float): Coordenada x del punto original.
        y (float): Coordenada y del punto original.
        reflection_type (str): Tipo de reflexión ('eje_x', 'eje_y', 'origen', 'y_igual_x', 'y_igual_menos_x', 'linea_horizontal', 'linea_vertical').
        custom_value (float, optional): Valor para reflexiones sobre líneas personalizadas (k para y=k, h para x=h).

    Returns:
        tuple: Coordenadas (x_reflejado, y_reflejado) del punto reflejado.
    """
    if reflection_type == 'eje_x':
        return x, -y
    elif reflection_type == 'eje_y':
        return -x, y
    elif reflection_type == 'origen':
        return -x, -y
    elif reflection_type == 'y_igual_x':
        return y, x
    elif reflection_type == 'y_igual_menos_x':
        return -y, -x
    elif reflection_type == 'linea_horizontal':  # y = k
        return x, 2 * custom_value - y
    elif reflection_type == 'linea_vertical':  # x = h
        return 2 * custom_value - x, y
    else:
        return x, y  # No reflection

# --- Página de la Aplicación Principal ---
def app_page():
    st.markdown("<h1 style='text-align: center;'>Reflexiones de Figuras en el Plano Cartesiano</h1>", unsafe_allow_html=True)

    st.markdown("""
    Esta aplicación te permite introducir puntos en el plano cartesiano, conectarlos para formar una figura
    y observar cómo esta figura se refleja según diferentes ejes o líneas.
    """)

    # Inicializar el estado de la sesión para los puntos si no existe
    if 'points' not in st.session_state:
        st.session_state.points = [{'x': 1.0, 'y': 1.0}, {'x': 3.0, 'y': 1.0}, {'x': 2.0, 'y': 3.0}] # Ejemplo de triángulo inicial
        # Aseguramos que haya al menos un punto inicial si se borran todos y se vuelve a cargar la app
        if not st.session_state.points:
            st.session_state.points.append({'x': 0.0, 'y': 0.0})

    # Definir dos columnas para la interfaz principal: una para inputs y otra para el gráfico
    col_inputs, col_graph = st.columns([1, 2]) # 1 para inputs (más estrecho), 2 para el gráfico (más ancho)

    with col_inputs:
        st.header("Entrada de Vértices y Opciones")

        st.markdown("### Introduce los vértices de tu figura (x, y)")
        st.info("Para dibujar una figura cerrada, asegura que el último punto sea el mismo que el primero. Puedes borrar vértices con el botón 'X'.")

        alphabet_letters = list(string.ascii_uppercase)

        # Mostrar inputs para cada punto en st.session_state.points
        # Ahora con un botón para eliminar cada punto
        points_to_remove = [] # Lista para guardar los índices de los puntos a eliminar

        for i, point in enumerate(st.session_state.points):
            if i < len(alphabet_letters):
                label_prefix = f"Vértice {alphabet_letters[i]}"
            else:
                label_prefix = f"Vértice {i+1}"

            # Usamos columnas para alinear x, y y el botón de cerrar
            col_x_input, col_y_input, col_close_button = st.columns([0.4, 0.4, 0.2]) # Ajusta las proporciones
            with col_x_input:
                st.session_state.points[i]['x'] = st.number_input(f"{label_prefix} (x)", value=point['x'], key=f"x_{i}")
            with col_y_input:
                st.session_state.points[i]['y'] = st.number_input(f"{label_prefix} (y)", value=point['y'], key=f"y_{i}")
            with col_close_button:
                # El botón de eliminar se coloca al lado, ligeramente alineado
                # Usamos un espacio en blanco arriba para alinearlo verticalmente
                st.write("") # Pequeño hack para centrar verticalmente el botón
                if st.button("X", key=f"remove_point_{i}"):
                    if len(st.session_state.points) > 1: # No permitir eliminar si solo queda un punto
                        points_to_remove.append(i)
                    else:
                        st.warning("Debe haber al menos un vértice.")


        # Procesar los puntos a eliminar después de iterar para evitar problemas de índices
        if points_to_remove:
            # Eliminar los puntos en orden inverso para no afectar los índices de los elementos restantes
            for index_to_remove in sorted(points_to_remove, reverse=True):
                del st.session_state.points[index_to_remove]
            st.rerun() # Fuerza una nueva ejecución para actualizar la UI

        # Botón para añadir más puntos
        if st.button("Añadir Vértice"):
            st.session_state.points.append({'x': 0.0, 'y': 0.0})
            st.rerun() # Fuerza una nueva ejecución para mostrar el nuevo input

        st.markdown("### Selecciona el tipo de reflexión")
        reflection_type = st.selectbox(
            "Tipo de Reflexión",
            (
                'Reflexión sobre el Eje X',
                'Reflexión sobre el Eje Y',
                'Reflexión sobre el Origen',
                'Reflexión sobre la línea y = x',
                'Reflexión sobre la línea y = -x',
                'Reflexión sobre una línea horizontal (y = k)',
                'Reflexión sobre una línea vertical (x = h)'
            ),
            key="reflection_type_main_page"
        )

        custom_line_value = 0.0
        if 'línea horizontal' in reflection_type:
            custom_line_value = st.number_input("Valor de k (para y = k)", value=0.0, step=0.1, key="custom_k_main")
        elif 'línea vertical' in reflection_type:
            custom_line_value = st.number_input("Valor de h (para x = h)", value=0.0, step=0.1, key="custom_h_main")


    with col_graph:
        st.markdown("<h2 style='text-align: center;'>Visualización de la Reflexión</h2>", unsafe_allow_html=True)

        # Procesar los puntos
        original_points_data = []
        reflected_points_data = []
        x_coords_orig = []
        y_coords_orig = []
        x_coords_reflected = []
        y_coords_reflected = []
        point_labels = []

        # Asegúrate de que haya al menos un punto para evitar errores si la lista está vacía
        if st.session_state.points:
            for i, point in enumerate(st.session_state.points):
                x = point['x']
                y = point['y']
                original_points_data.append((x, y))
                x_coords_orig.append(x)
                y_coords_orig.append(y)

                reflection_func_type = ''
                if reflection_type == 'Reflexión sobre el Eje X':
                    reflection_func_type = 'eje_x'
                elif reflection_type == 'Reflexión sobre el Eje Y':
                    reflection_func_type = 'eje_y'
                elif reflection_type == 'Reflexión sobre el Origen':
                    reflection_func_type = 'origen'
                elif reflection_type == 'Reflexión sobre la línea y = x':
                    reflection_func_type = 'y_igual_x'
                elif reflection_type == 'Reflexión sobre la línea y = -x':
                    reflection_func_type = 'y_igual_menos_x'
                elif 'línea horizontal' in reflection_type:
                    reflection_func_type = 'linea_horizontal'
                elif 'línea vertical' in reflection_type:
                    reflection_func_type = 'linea_vertical'

                rx, ry = reflect_point(x, y, reflection_func_type, custom_line_value)
                reflected_points_data.append((rx, ry))
                x_coords_reflected.append(rx)
                y_coords_reflected.append(ry)

                if i < len(alphabet_letters):
                    point_labels.append(alphabet_letters[i])
                else:
                    point_labels.append(str(i+1))

        # El gráfico solo se dibuja si hay al menos un punto
        if original_points_data:
            # Si la figura debe ser cerrada, duplicamos el primer punto al final
            if len(original_points_data) > 1 and original_points_data[0] != original_points_data[-1]:
                x_coords_orig.append(x_coords_orig[0])
                y_coords_orig.append(y_coords_orig[0])
                x_coords_reflected.append(x_coords_reflected[0])
                y_coords_reflected.append(y_coords_reflected[0])


            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=x_coords_orig,
                y=y_coords_orig,
                mode='lines+markers+text',
                name='Figura Original',
                line=dict(color='blue', width=2),
                marker=dict(size=8, color='blue'),
                text=[f'{point_labels[i]} ({p[0]}, {p[1]})' for i, p in enumerate(original_points_data)],
                textposition="top right"
            ))

            fig.add_trace(go.Scatter(
                x=x_coords_reflected,
                y=y_coords_reflected,
                mode='lines+markers+text',
                name='Figura Reflejada',
                line=dict(color='red', width=2, dash='dash'),
                marker=dict(size=8, color='red'),
                text=[f'{point_labels[i]}\' ({p[0]}, {p[1]})' for i, p in enumerate(reflected_points_data)],
                textposition="bottom left"
            ))

            all_x = x_coords_orig + x_coords_reflected
            all_y = y_coords_orig + y_coords_reflected

            x_min_data = min(all_x) if all_x else -5
            x_max_data = max(all_x) if all_x else 5
            y_min_data = min(all_y) if all_y else -5
            y_max_data = max(all_y) if all_y else 5

            padding = 1.5
            x_range = [x_min_data - padding, x_max_data + padding]
            y_range = [y_min_data - padding, y_max_data + padding]

            if reflection_type == 'Reflexión sobre el Eje X':
                fig.add_shape(type="line", x0=x_range[0], y0=0, x1=x_range[1], y1=0,
                              line=dict(color="green", width=2, dash="dot"), name="Eje X")
                fig.add_annotation(x=x_range[1] * 0.9, y=0.5, text="Eje X", showarrow=False, font=dict(color="green"))
            elif reflection_type == 'Reflexión sobre el Eje Y':
                fig.add_shape(type="line", x0=0, y0=y_range[0], x1=0, y1=y_range[1],
                              line=dict(color="green", width=2, dash="dot"), name="Eje Y")
                fig.add_annotation(x=0.5, y=y_range[1] * 0.9, text="Eje Y", showarrow=False, font=dict(color="green"))
            elif reflection_type == 'Reflexión sobre la línea y = x':
                x_line = np.linspace(min(x_range[0], y_range[0]), max(x_range[1], y_range[1]), 100)
                fig.add_trace(go.Scatter(x=x_line, y=x_line, mode='lines', name='y = x',
                                         line=dict(color='green', width=2, dash='dot')))
                fig.add_annotation(x=x_line[-1], y=x_line[-1], text="y = x", showarrow=False, font=dict(color="green"))
            elif reflection_type == 'Reflexión sobre la línea y = -x':
                x_line = np.linspace(min(x_range[0], y_range[0]), max(x_range[1], y_range[1]), 100)
                fig.add_trace(go.Scatter(x=x_line, y=-x_line, mode='lines', name='y = -x',
                                         line=dict(color='green', width=2, dash='dot')))
                fig.add_annotation(x=x_line[0], y=-x_line[0], text="y = -x", showarrow=False, font=dict(color="green"))
            elif 'línea horizontal' in reflection_type:
                fig.add_shape(type="line", x0=x_range[0], y0=custom_line_value, x1=x_range[1], y1=custom_line_value,
                              line=dict(color="green", width=2, dash="dot"), name=f"y = {custom_line_value}")
                fig.add_annotation(x=x_range[1] * 0.9, y=custom_line_value + 0.5, text=f"y = {custom_line_value}", showarrow=False, font=dict(color="green"))
            elif 'línea vertical' in reflection_type:
                fig.add_shape(type="line", x0=custom_line_value, y0=y_range[0], x1=custom_line_value, y1=y_range[1],
                              line=dict(color="green", width=2, dash="dot"), name=f"x = {custom_line_value}")
                fig.add_annotation(x=custom_line_value + 0.5, y=y_range[1] * 0.9, text=f"x = {custom_line_value}", showarrow=False, font=dict(color="green"))

            fig.update_layout(
                title_text='Figuras Original y Reflejada con Vértices',
                title_x=0.5,
                xaxis_title='Eje X',
                yaxis_title='Eje Y',
                hovermode='closest',
                showlegend=True,
                xaxis=dict(
                    zeroline=True, zerolinecolor='lightgray', zerolinewidth=1,
                    gridcolor='lightgray', gridwidth=1,
                    range=x_range
                ),
                yaxis=dict(
                    zeroline=True, zerolinecolor='lightgray', zerolinewidth=1,
                    gridcolor='lightgray', gridwidth=1,
                    range=y_range
                ),
                template='plotly_white',
                width=800,
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Añade al menos dos puntos para ver la figura y su reflexión. La figura se cerrará automáticamente.")


    st.markdown("---")
    st.header("Explicación de las Reflexiones")

    if reflection_type == 'Reflexión sobre el Eje X':
        st.markdown("""
        Al **reflejar un punto (x, y) sobre el Eje X**, la coordenada $x$ permanece igual, mientras que la coordenada $y$ cambia de signo.
        La fórmula de transformación es: $(x, y) \\rightarrow (x, -y)$.
        Imagina que el Eje X es un espejo; el punto reflejado estará a la misma distancia del eje, pero en el lado opuesto.
        """)
    elif reflection_type == 'Reflexión sobre el Eje Y':
        st.markdown("""
        Al **reflejar un punto (x, y) sobre el Eje Y**, la coordenada $y$ permanece igual, mientras que la coordenada $x$ cambia de signo.
        La fórmula de transformación es: $(x, y) \\rightarrow (-x, y)$.
        Piensa en el Eje Y como un espejo; el punto reflejado estará a la misma distancia del eje, pero al lado contrario.
        """)
    elif reflection_type == 'Reflexión sobre el Origen':
        st.markdown("""
        Al **reflejar un punto (x, y) sobre el Origen (0,0)**, ambas coordenadas, $x$ e $y$, cambian de signo.
        La fórmula de transformación es: $(x, y) \\rightarrow (-x, -y)$.
        Es como realizar una reflexión sobre el Eje X y luego otra sobre el Eje Y (o viceversa).
        """)
    elif reflection_type == 'Reflexión sobre la línea y = x':
        st.markdown("""
        Al **reflejar un punto (x, y) sobre la línea $y = x$**, las coordenadas $x$ e $y$ simplemente se intercambian.
        La fórmula de transformación es: $(x, y) \\rightarrow (y, x)$.
        Esta línea verde punteada en el gráfico es la línea $y=x$, sirviendo como el eje de reflexión.
        """)
    elif reflection_type == 'Reflexión sobre la línea y = -x':
        st.markdown("""
        Al **reflejar un punto (x, y) sobre la línea $y = -x$**, las coordenadas $x$ e $y$ se intercambian y ambas cambian de signo.
        La fórmula de transformación es: $(x, y) \\rightarrow (-y, -x)$.
        La línea verde punteada en el gráfico es la línea $y=-x$, actuando como el eje de reflexión.
        """)
    elif 'línea horizontal' in reflection_type: # y = k
        st.markdown(f"""
        Al **reflejar un punto (x, y) sobre una línea horizontal $y = k$** (donde $k$ es un valor constante), la coordenada $x$ permanece igual, y la nueva coordenada $y$ se calcula como $2k - y$.
        La fórmula de transformación es: $(x, y) \\rightarrow (x, 2k - y)$.
        En este caso, la línea de reflexión es $y = {custom_line_value}$. El punto reflejado estará a la misma distancia vertical de esta línea que el punto original.
        """)
    elif 'línea vertical' in reflection_type: # x = h
        st.markdown(f"""
        Al **reflejar un punto (x, y) sobre una línea vertical $x = h$** (donde $h$ es un valor constante), la coordenada $y$ permanece igual, y la nueva coordenada $x$ se calcula como $2h - x$.
        La fórmula de transformación es: $(x, y) \\rightarrow (2h - x, y)$.
        En este caso, la línea de reflexión es $x = {custom_line_value}$. El punto reflejado estará a la misma distancia horizontal de esta línea que el punto original.
        """)
    else:
        st.markdown("""
        Selecciona un tipo de reflexión del menú desplegable para ver su explicación y cómo transforma los puntos.
        """)

    st.markdown("---")
    st.markdown("Desarrollado con Streamlit y Plotly por tu programador Python amigo.")

# --- Página de Teoría sobre Reflexión ---
def theory_page():
    st.markdown("<h1 style='text-align: center;'>Teoría de la Reflexión Geométrica</h1>", unsafe_allow_html=True)
    st.markdown("""
    ---
    ¡Hola, futuros genios de las matemáticas! Hoy vamos a explorar un concepto fascinante en geometría: la **reflexión**.
    """)

    st.header("¿Qué es una Reflexión?")
    st.markdown("""
    Imagina que tienes un espejo. Cuando te miras en él, ves una imagen de ti mismo que es exactamente igual, pero invertida. En matemáticas, la reflexión funciona de manera muy similar.
    Una **reflexión** (o simetría axial) es una **transformación geométrica** que "voltea" una figura o un punto sobre una línea, llamada **eje de reflexión**. Es como si doblaras el papel por el eje y la figura original coincidiera exactamente con su imagen reflejada.

    **Características clave de una reflexión:**
    * **Forma y tamaño:** La figura reflejada tiene la misma forma y el mismo tamaño que la figura original. No se estira ni se encoge.
    * **Orientación:** La orientación de la figura se invierte. Si la figura original se leía de izquierda a derecha, la reflejada se leerá de derecha a izquierda.
    * **Distancia:** Cada punto de la figura original está a la misma distancia del eje de reflexión que su punto correspondiente en la figura reflejada.
    """)

    st.header("Tipos Comunes de Reflexiones en el Plano Cartesiano")
    st.markdown("""
    En el plano cartesiano (donde usamos coordenadas $x$ e $y$), hay varios ejes de reflexión que son muy comunes:
    """)

    st.subheader("1. Reflexión sobre el Eje X")
    st.markdown("""
    Cuando reflejamos un punto $(x, y)$ sobre el **Eje X**, la coordenada $x$ se mantiene igual, y la coordenada $y$ cambia de signo.
    * **Fórmula:** $(x, y) \\rightarrow (x, -y)$
    * **Ejemplo:** Si el punto original es $(2, 3)$, su reflexión sobre el Eje X será $(2, -3)$.
    """)

    st.subheader("2. Reflexión sobre el Eje Y")
    st.markdown("""
    Cuando reflejamos un punto $(x, y)$ sobre el **Eje Y**, la coordenada $y$ se mantiene igual, y la coordenada $x$ cambia de signo.
    * **Fórmula:** $(x, y) \\rightarrow (-x, y)$
    * **Ejemplo:** Si el punto original es $(2, 3)$, su reflexión sobre el Eje Y será $(-2, 3)$.
    """)

    st.subheader("3. Reflexión sobre el Origen")
    st.markdown("""
    Cuando reflejamos un punto $(x, y)$ sobre el **Origen (0,0)**, ambas coordenadas (x e y) cambian de signo.
    * **Fórmula:** $(x, y) \\rightarrow (-x, -y)$
    * **Ejemplo:** Si el punto original es $(2, 3)$, su reflexión sobre el Origen será $(-2, -3)$.
    """)

    st.subheader("4. Reflexión sobre la línea $y = x$")
    st.markdown("""
    Cuando reflejamos un punto $(x, y)$ sobre la **línea $y = x$**, las coordenadas $x$ e $y$ simplemente se intercambian.
    * **Fórmula:** $(x, y) \\rightarrow (y, x)$
    * **Ejemplo:** Si el punto original es $(2, 3)$, su reflexión sobre la línea $y=x$ será $(3, 2)$.
    """)

    st.subheader("5. Reflexión sobre la línea $y = -x$")
    st.markdown("""
    Cuando reflejamos un punto $(x, y)$ sobre la **línea $y = -x$**, las coordenadas $x$ e $y$ se intercambian y ambas cambian de signo.
    * **Fórmula:** $(x, y) \\rightarrow (-y, -x)$
    * **Ejemplo:** Si el punto original es $(2, 3)$, su reflexión sobre la línea $y=-x$ será $(-3, -2)$.
    """)

    st.subheader("6. Reflexión sobre una Línea Horizontal ($y = k$)")
    st.markdown("""
    Cuando reflejamos un punto $(x, y)$ sobre una **línea horizontal $y = k$** (donde $k$ es un número), la coordenada $x$ permanece igual. La nueva coordenada $y$ se calcula como el doble de $k$ menos la $y$ original.
    * **Fórmula:** $(x, y) \\rightarrow (x, 2k - y)$.
    * **Ejemplo:** Si el punto original es $(2, 3)$ y la línea de reflexión es $y = 5$ (es decir, $k=5$), la reflexión será $(2, 2*5 - 3) = (2, 10 - 3) = (2, 7)$.
    """)

    st.subheader("7. Reflexión sobre una Línea Vertical ($x = h$)")
    st.markdown("""
    Cuando reflejamos un punto $(x, y)$ sobre una **línea vertical $x = h$** (donde $h$ es un número), la coordenada $y$ permanece igual. La nueva coordenada $x$ se calcula como el doble de $h$ menos la $x$ original.
    * **Fórmula:** $(x, y) \\rightarrow (2h - x, y)$.
    * **Ejemplo:** Si el punto original es $(2, 3)$ y la línea de reflexión es $x = 5$ (es decir, $h=5$), la reflexión será $(2*5 - 2, 3) = (10 - 2, 3) = (8, 3)$.
    """)

    st.markdown("""
    ---
    ¡Esperamos que esta teoría te ayude a comprender mejor las reflexiones! Ahora, puedes volver a la aplicación interactiva para poner en práctica lo aprendido.
    """)
    st.markdown("---")
    st.markdown("Contenido diseñado para estudiantes de bachillerato/educación media.")


# --- Configuración de la página global ---
# Añade el parámetro 'page_icon' con el emoji de tu elección
st.set_page_config(layout="wide", page_title="Reflexiones Geométricas", page_icon="📐") # O usa "✨" o el que prefieras

# --- Implementación del Navbar con st.tabs en la parte superior ---
tab_app, tab_theory = st.tabs(["Aplicación Interactiva", "Teoría de la Reflexión"])

with tab_app:
    app_page() # Llama a la función que renderiza la página de la aplicación

with tab_theory:
    theory_page() # Llama a la función que renderiza la página de teoría

# Pie de página opcional y global si se desea
# st.markdown("---")
# st.markdown("Desarrollado con Streamlit y Plotly por tu programador Python amigo.")