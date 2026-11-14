# cicd-pipeline-python

CI/CD - EAFIT 

## Integrantes

- Santiago Mesa Valencia
- Jose Manuel Carvajal Aristizabal
- Mateo Montoya Aristizabal

## Evidencias

- https://github.com/mate2000/cicd-pipeline-python/pull/1
- https://github.com/mate2000/cicd-pipeline-python/actions/runs/43615272317

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

### Mateo Montoya Aristizabal

**Dificultad:** La configuración de SonarCloud fue confusa. El análisis fallaba con el error `Not authorized or organization not found`, aunque el token estaba bien configurado como secreto en GitHub.

**Solución:** Activamos el log de debug del scanner y vimos que SonarCloud respondía 404 al buscar la organización. En `sonar-project.properties` habíamos puesto el nombre visible de la organización (`mate2000`) en lugar de su key (`mate2000-1`). Al corregir `sonar.organization` con la key, el análisis corrió bien.


### Santiago Mesa Valencia

**Dificultad:** Mi principal problema fue configurar SonarCloud, sobre todo crear la cuenta y vincularla con mi cuenta de GitHub para que pudiera analizar el repositorio.

**Solución:** Con ayuda del profesor configuré el nuevo proyecto en SonarCloud y lo vinculé con el repositorio de GitHub, para que el análisis se ejecutara desde el pipeline.

**Aprendizaje:** SonarCloud detecta problemas de calidad en el código, como errores, vulnerabilidades, código duplicado o poca cobertura de pruebas, antes de llegar al despliegue. Así se evita que esos errores lleguen a producción, y por eso es una parte importante de un pipeline de CI/CD.

### Jose Manuel Carvajal Aristizabal

**Dificultad:** El entendimiento o la profundización de conceptos, debido a que hay muchas cosas de estas que se habían visto pero no tan a profundidad entonces interiorizar esos conceptos y aplicarlos fue una parte complicada, entonces tuve que leer muy bien cada paso y buscar información por fuera para comprender mejor todo, y ya personalmente no me gusto sonarcloud, me parece que podrían de haber herramientas mas interesantes.

**Solución:**

**Aprendizaje:**

### 5.

- Se prueba lo que realmente se despliega.
- Paridad entre entornos.

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