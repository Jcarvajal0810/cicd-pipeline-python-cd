# cicd-pipeline-python

Task CI/CD

## Integrantes

- Santiago Mesa Valencia
- Jose Manuel Carvajal Aristizabal
- Mateo Montoya Aristizabal

## Evidencias

-
-

## Respuestas a las preguntas

### 1.

Para un SDLC moderno se necesita un flujo rápido y continuo de trabajo, por eso un pipeline de CI nos permite:

- **Detectar errores temprano y de forma automática.** Corregir los errores en etapas tempranas cuesta menos tiempo y dinero, lo cual contribuye a la economía del software.
- **Hacer las validaciones repetibles y consistentes.** El pipeline corre siempre los mismos pasos, lo que estandariza el desarrollo de software.
- **Dar trazabilidad y retroalimentación visible.** Cada ejecución deja logs y artefactos (reporte de cobertura, reportes HTML de pruebas, reportes de Pylint y Flake8).

### 2.

- **Unitaria:** prueba una unidad mínima de código (una función o clase).
- **De componente:** prueba un componente completo (por ejemplo, la app web con sus rutas y plantillas).
- **De aceptación:** prueba el sistema desplegado desde el punto de vista del usuario final, de punta a punta.

### 3.

**Checkout**
- Qué hace: clona el repositorio en el runner con todo el historial.
- Para qué: tener el código.

**Set up Python**
- Qué hace: instala Python 3.13.
- Para qué: ejecutar todo con la misma versión fija que usa la imagen Docker.

**Install dependencies**
- Qué hace: actualiza pip e instala `requirements-dev.txt`.
- Para qué: tener las herramientas de prueba y análisis: pytest, Black, Pylint, Flake8, Selenium, etc.

**Run Black (`--check`)**
- Qué hace: verifica que el código de `app/` cumpla el formato, sin modificarlo.
- Para qué: mantener un estilo uniforme. Si no cumple, el pipeline falla.

**Run Pylint / Flake8 (`--exit-zero`)**
- Qué hace: analizan el código y guardan reportes en `.txt` sin romper el build.
- Para qué: detectar malas prácticas y errores potenciales. Los reportes los importa SonarCloud.

**Run Unit and Component Tests**
- Qué hace: ejecuta pytest, excepto las pruebas de aceptación, y exige cobertura de al menos 80 %.
- Para qué: validar la lógica y las rutas Flask antes de construir nada, y garantizar una cobertura mínima.

**Build Docker image**
- Qué hace: construye la imagen.
- Para qué: empaquetar la app tal como se va a ejecutar.

**Start container**
- Qué hace: arranca el contenedor en el puerto 8000 y espera hasta 30 s a que responda.
- Para qué: tener la app real (Gunicorn dentro de la imagen) lista para las pruebas de aceptación.

**Run Acceptance Tests**
- Qué hace: ejecuta Selenium contra `http://localhost:8000` y genera un reporte HTML.
- Para qué: validar el comportamiento de punta a punta.

**Show container logs on failure**
- Qué hace: si algo falló, imprime los logs del contenedor.
- Para qué: facilitar el diagnóstico.

**Upload Test Reports Artifacts (`always()`)**
- Qué hace: sube cobertura, reportes de pruebas y de linters como artefacto.
- Para qué: poder revisar evidencias aunque el job falle.

**SonarCloud Scan**
- Qué hace: envía el análisis (código, cobertura, reportes de linters) a SonarCloud y espera el Quality Gate.
- Para qué: análisis estático de calidad y seguridad. Si el gate falla, el pipeline falla.

**Login to Docker Hub**
- Qué hace: se autentica con el usuario.
- Para qué: tener permisos para publicar.

**Push Docker image**
- Qué hace: etiqueta la imagen también como `latest` y sube las dos etiquetas.
- Para qué: publicar el artefacto ya validado.

### 4.

- El seteo de SonarCloud algunas veces puede ser confuso. -> Mateo Montoya
- 

### 5.

Se prueba lo que realmente se despliega.

### 6.

Se agregaron 3 pruebas nuevas. Todas pasan, junto con las que ya existían (15 en total).

En `tests/test_calculadora.py` (pruebas unitarias):

1. **`test_operaciones_con_decimales`**: prueba las 4 operaciones con números decimales. Se usa `pytest.approx` porque en punto flotante `0.1 + 0.2` da `0.30000000000000004` y no exactamente `0.3`; con `approx` la comparación tolera esa pequeña diferencia. Ejemplos:
   - `sumar(0.1, 0.2) ≈ 0.3`
   - `dividir(1, 3) ≈ 0.3333333`
2. **`test_operaciones_con_dos_negativos`**: prueba las 4 operaciones cuando ambos números son negativos, un caso que las pruebas originales no cubrían. Ejemplos:
   - `sumar(-2, -3) == -5`
   - `multiplicar(-4, -2) == 8` (negativo por negativo da positivo)
   - `dividir(-10, -2) == 5.0`

En `tests/test_app.py` (prueba de componente):

3. **`test_index_post_un_numero_invalido`**: envía el formulario con un número válido (`num1='2'`) y otro inválido (`num2='abc'`). Verifica que la página responda bien (código 200) y muestre "Error: Introduce números válidos". La prueba original solo revisaba el caso en que ambos números eran inválidos.