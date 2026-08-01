# 🎬 Guion del vídeo de presentación (10 min) — Proyecto Big Data · Tokio Telecom
**Autor:** Juan David Collazos González · **Tema:** Predicción de bajas (churn) con PySpark

---

## Cómo usar este guion
- **Ritmo:** habla a ritmo natural (~130–135 palabras/min). Con las **pausas** para mostrar cada figura,
  el guion llega a **10 minutos** holgados. **No corras**: respira entre secciones y deja ver cada gráfica 2–3 s.
- **Formato de cada bloque:** `[tiempo] Título` → **EN PANTALLA** (qué se ve) + **NARRACIÓN** (lo que dices).
- **Graba por bloques** y únelos; así, si te equivocas, repites solo un bloque.
- Los **9 bloques** cubren TODAS las cuestiones de la defensa: 2 modelos, Grid Search + CV, train/test, AUC + curva ROC, y por qué la *accuracy* no vale.

**Mapa de material a mostrar (ten estas ventanas/figuras listas):**
1. Portada de la presentación · 2. `figuras/t3_churn_contract.png` · 3. `figuras/t5_matriz_correlacion.png`
4. Celdas 6.1–6.4 del notebook (Grid Search + CV) · 5. `figuras/t6_tabla_comparativa.png`
6. `figuras/t6_roc_train_test.png` · 7. `figuras/t6_matrices_confusion_v2.png` · 8. `figuras/t6_importancia_variables_v2.png`

---

### [0:00–0:40] 1 · Portada y objetivo
**EN PANTALLA:** Portada con título, tu nombre y el logo/idea de "Tokio Telecom".

**NARRACIÓN:**
> Hola, soy Juan David Collazos. En este vídeo presento mi proyecto final de Big Data: un sistema para
> **predecir qué clientes de la operadora Tokio Telecom se van a dar de baja** —lo que se conoce como
> *churn*—, usando **PySpark** de principio a fin. La idea es sencilla de decir y valiosa para el
> negocio: si somos capaces de anticipar quién se va a marchar, podemos actuar **antes** de perderlo.
> Voy a recorrer los datos, la arquitectura, el análisis y, sobre todo, el modelo de predicción, que
> es la parte que he **reforzado** en esta versión.

---

### [0:40–1:40] 2 · El problema de negocio y los datos
**EN PANTALLA:** Diapositiva del problema + tabla de las 12 variables (T1).

**NARRACIÓN:**
> Retener a un cliente siempre es más barato que captar uno nuevo, así que **cada baja que evitamos es
> ingreso recurrente que protegemos**. El dataset tiene **10.000 clientes** y **12 variables**: datos
> del cliente como la edad o el género; de su contrato, como el tipo de tarifa o la duración; y de su
> comportamiento, como la frecuencia de uso, las **llamadas a soporte**, el **retraso en los pagos** o
> el **gasto total**. La variable objetivo es `Churn`: si el cliente se dio de baja o no. Un dato
> importante: las clases están **bastante equilibradas**, un **56,7% de bajas** frente a un 43,3% que
> permanece. Recordad este equilibrio, porque será clave al elegir la métrica.

---

### [1:40–2:40] 3 · Arquitectura Big Data (Tareas 1 y 2)
**EN PANTALLA:** Diagrama simple: `CSV → Cassandra (Docker) → PySpark (análisis + ML)`. Muestra `comandos_cassandra.txt`.

**NARRACIÓN:**
> La arquitectura combina dos piezas del ecosistema Big Data. Primero, el **almacenamiento**: cargué
> los 10.000 registros en **Apache Cassandra**, una base de datos **NoSQL** distribuida, ejecutada en
> un contenedor **Docker** para que el entorno sea 100% reproducible. Sobre Cassandra definí el
> *keyspace*, la tabla y varios índices, y resolví las consultas de la Tarea 2. Segundo, el
> **procesamiento y la analítica**: todo el análisis y el aprendizaje automático están hechos con
> **PySpark**, el motor de cómputo distribuido de Apache Spark. Aunque aquí son 10.000 filas, **el
> mismo código escala a millones** sin cambios: esa es la gracia de trabajar con Spark.

---

### [2:40–4:00] 4 · Análisis exploratorio (Tareas 3, 4 y 5)
**EN PANTALLA:** `t3_churn_contract.png`, luego `t5_matriz_correlacion.png`.

**NARRACIÓN:**
> Antes de modelar, exploré los datos con Spark. El **análisis descriptivo** dibuja al cliente medio:
> unos 39 años, 31 meses de antigüedad y un gasto medio de 633 euros, pero con **mucha dispersión** —
> conviven perfiles de bajo y de alto valor—. Con eso en mente, el primer hallazgo es **contundente**:
> si miramos la **baja por duración de contrato**, el contrato **mensual tiene un 100% de baja**,
> frente a un 45–47% en los
> contratos trimestral y anual. El compromiso a largo plazo es, con diferencia, la mayor palanca de
> retención. En cambio, el tipo de tarifa —Basic, Standard o Premium— apenas distingue: todas rondan
> el 55–58%. Luego calculé la **matriz de correlación** con Spark. Frente a la baja destacan cuatro
> variables: las **llamadas a soporte**, con la correlación positiva más fuerte —más incidencias,
> más baja—; el **gasto total**, con correlación **negativa** —quien más gasta, más comprometido está
> y menos se va—; el **retraso en los pagos**; y la **edad**. Este análisis ya me anticipa **qué
> variables van a pesar** en el modelo.

---

### [4:00–4:45] 5 · Del análisis a la predicción · ¿por qué NO usar *accuracy*?
**EN PANTALLA:** Título "Aprendizaje supervisado" + bullet grande: "Métrica = AUC (no accuracy)".

**NARRACIÓN:**
> Predecir la baja es un problema de **clasificación binaria supervisada**: tenemos la etiqueta, así
> que entrenamos un modelo que aprenda a separar. Y aquí una decisión metodológica importante: **la
> métrica no es la *accuracy*, es el AUC**. ¿Por qué? Por dos razones. Una, el **coste es asimétrico**:
> no detectar a un cliente que se marcha —un falso negativo— es mucho más caro que ofrecer un incentivo
> de más. Y dos, en la práctica **ordenamos** a los clientes por riesgo y actuamos sobre los primeros;
> lo que importa es **cómo de bien ordena** el modelo, y eso es justo lo que mide el **área bajo la
> curva ROC**. La accuracy solo mira un umbral fijo del 50%; el AUC los evalúa **todos**.

---

### [4:45–6:20] 6 · Entrenamiento correcto · dos modelos + Grid Search + Cross Validation
**EN PANTALLA:** Celdas 6.1–6.4 del notebook (se ven `ParamGridBuilder` y `CrossValidator`).

**NARRACIÓN:**
> Esta es la parte que he reforzado respecto a la versión anterior. Antes el Random Forest se entrenaba
> con los **parámetros por defecto**; ahora hago una **selección rigurosa de hiperparámetros**.
> Comparo **dos modelos de árbol** —un **Árbol de Decisión**, que es interpretable y da reglas
> directas, y un **Random Forest**, que combina muchos árboles para reducir el error— y añado una
> **Regresión Logística** como referencia. A los tres les aplico **Grid Search con Validación Cruzada
> de 5 particiones**: es decir, pruebo muchas combinaciones de hiperparámetros —profundidad del árbol,
> número de árboles, criterio de división— y evalúo cada una en **cinco cortes distintos** de los datos
> de entrenamiento, quedándome con la que maximiza el **AUC** medio. Así el resultado **no depende de
> un único reparto afortunado**. En concreto, para los árboles exploro profundidades de 3 a 12 y
> distintos criterios de división, y para el Random Forest, de 50 a 120 árboles. Antes de entrenar,
> preparo las variables: las categóricas con *one-hot encoding* —convertirlas en columnas de ceros y
> unos— y, para la Regresión Logística, escalo las numéricas. Por último separo un **70% para entrenar
> y un 30% para test**, que el modelo **no verá hasta el final**, para que la evaluación sea honesta.

---

### [6:20–8:30] 7 · Resultados · tabla, curvas ROC y validación
**EN PANTALLA (por orden):** `t6_tabla_comparativa.png` → `t6_roc_train_test.png` → `t6_matrices_confusion_v2.png` → `t6_importancia_variables_v2.png`.

**NARRACIÓN:**
> Vamos a los resultados. En esta **tabla comparativa** tenéis, para cada modelo, el AUC en validación
> cruzada, en **train** y en **test**. El **Random Forest** es el mejor, con un **AUC en test de
> 0,9997**; el Árbol de Decisión queda muy cerca, en **0,998**, y es más interpretable; la Regresión
> Logística se queda en **0,958**, buena, pero claramente por debajo.
>
> *(Cambia a las curvas ROC.)* Estas son las **curvas ROC en train y en test**. Fijaos en lo
> importante: los dos paneles son **casi idénticos**. Como el rendimiento en entrenamiento y en test
> es prácticamente el mismo, podemos afirmar que **no hay sobreajuste**. Si el modelo hubiera
> "memorizado", el test caería, y no cae.
>
> Ahora bien, un AUC tan alto obliga a preguntarse: *¿es demasiado bueno?* La respuesta honesta es que
> **este dataset es sintético y contiene reglas casi deterministas**: por ejemplo, el contrato mensual
> siempre acaba en baja, o más de veinte días de retraso en el pago llevan siempre a la baja. Con
> patrones tan limpios, hasta un árbol sencillo alcanza casi el máximo. Es una propiedad **de los
> datos**, no un truco del modelo, y por eso me aseguro con la validación cruzada y el test.
>
> *(Cambia a las matrices de confusión.)* En las **matrices de confusión** se ve el impacto de negocio:
> el Random Forest solo confunde una veintena de casos de casi tres mil, mientras que la Regresión
> Logística **deja escapar 171 bajas** sin detectar. En churn, cada uno de esos 171 es un cliente que
> perderíamos sin avisar.
>
> *(Cambia a la importancia de variables.)* Y por último, **qué mira el modelo para decidir**: las
> variables más importantes son las **llamadas a soporte**, el **gasto total**, la **edad** y el
> **retraso en los pagos** —exactamente lo que anticipaba la correlación—. El modelo es coherente con
> el análisis exploratorio.

---

### [8:30–9:30] 8 · Conclusiones de negocio y próximos pasos
**EN PANTALLA:** Diapositiva de conclusiones (3 acciones) + lista de próximos pasos.

**NARRACIÓN:**
> ¿Qué haría la empresa con esto? Tres acciones concretas. Primero, **migrar a los clientes del
> contrato mensual** hacia trimestral o anual con incentivos, porque el mensual es una fuga segura.
> Segundo, **vigilar a quien acumula llamadas a soporte y retrasos de pago**, que son las señales de
> alarma más tempranas. Y tercero, **priorizar la retención por probabilidad de baja**: el modelo nos
> da un ranking, y actuamos primero sobre los de más riesgo. Como **próximos pasos** propongo:
> una **validación temporal** para estimar el rendimiento real en producción, **recalibrar el umbral
> según el coste** de cada acción, probar modelos de *boosting*, y **llevar el scoring al CRM** de
> forma automática, con monitorización por si los datos cambian con el tiempo.

---

### [9:30–10:00] 9 · Cierre
**EN PANTALLA:** Diapositiva final: "Gracias" + resumen de una línea.

**NARRACIÓN:**
> En resumen: he construido un pipeline **Big Data completo** —almacenamiento en Cassandra y analítica
> en PySpark— y un modelo de predicción de baja **entrenado correctamente**, con selección de
> hiperparámetros, validación cruzada, comparación de dos modelos y evaluación por **AUC y curva ROC**
> en train y test. El Random Forest predice la baja de forma fiable y, más importante, **sin
> sobreajuste**. Gracias por vuestra atención.

---

## ✅ Checklist de la defensa (verifica que el vídeo lo cubre)
- [x] **Dos modelos comparados:** Árbol de Decisión + Random Forest (+ baseline Regresión Logística) → bloques 6–7.
- [x] **Entrenamiento correcto:** Grid Search + Cross Validation optimizando AUC → bloque 6.
- [x] **Resultados en train y test** → tabla + curvas ROC, bloque 7.
- [x] **AUC y curva ROC reportadas** → bloque 7.
- [x] **Por qué accuracy no es buena métrica** → bloque 5.
- [x] **Justificación del AUC ~1 (sin sobreajuste)** → bloque 7.
