# 📝 Correcciones del proyecto — texto listo para pegar en los 3 entregables
**Proyecto Big Data · Tokio Telecom · Churn** — Juan David Collazos González

Este documento responde punto por punto al feedback. Contiene: (1) resumen de lo corregido,
(2) los resultados nuevos, (3) texto listo para pegar en el **informe científico**, (4) mejoras del
**informe técnico**, (5) qué añadir a la **presentación**, (6) banco de preguntas de defensa y
(7) cómo re-ejecutar el notebook.

---

## 1. Qué se ha corregido (resumen)

| Feedback | Acción realizada |
|---|---|
| RF entrenado solo con parámetros por defecto | **Grid Search + Cross Validation (5-fold)** para Árbol de Decisión **y** Random Forest, optimizando **AUC** |
| Faltan métricas en *train* y *test* | Tabla comparativa con AUC/F1/recall/precision **en train y test** |
| Faltan curvas ROC | **Curvas ROC en train y test** para los 3 modelos (`figuras/t6_roc_train_test.png`) |
| Comparar **dos modelos** | **Árbol de Decisión + Random Forest** (+ Regresión Logística como baseline) |
| *Accuracy* no es buena métrica | Métrica de referencia = **AUC**; se explica el porqué y se reporta recall de la clase baja |
| Falta tabla `test-train-modelos` (presentación) | `figuras/t6_tabla_comparativa.png` |
| Faltan próximos pasos (científico) | Sección **"Próximos pasos"** redactada (abajo) |
| Informe técnico poco estructurado | Índice propuesto + criterio "código con contexto" (abajo) |

**Notebook actualizado:** `churn_pyspark_colab.ipynb` (Tarea 6 rehecha). Copia del anterior en
`churn_pyspark_colab_ORIGINAL_backup.ipynb`.
**Figuras nuevas** en `figuras/`: `t6_roc_train_test.png`, `t6_tabla_comparativa.png`,
`t6_auc_train_vs_test.png`, `t6_matrices_confusion_v2.png`, `t6_importancia_variables_v2.png`.

---

## 2. Resultados nuevos (cifras reales de la ejecución)

Partición: **train = 7.104** clientes (70%) · **test = 2.896** (30%). Métrica optimizada: **AUC**.

| Modelo | Hiperparámetros (Grid Search) | AUC CV | AUC train | AUC test | Recall baja (test) | Accuracy test |
|---|---|---|---|---|---|---|
| Árbol de Decisión | maxDepth=12, entropy | 0,9943 | 0,9996 | 0,9982 | 0,997 | 0,995 |
| **Random Forest** ⭐ | numTrees=120, maxDepth=12, subset=1/3 | 0,9994 | 1,0000 | **0,9997** | 0,990 | 0,992 |
| Regresión Logística | regParam=0, sin L1/L2 | 0,9599 | 0,9602 | 0,9583 | 0,896 | 0,895 |

**Lecturas clave:**
- **Mejor modelo: Random Forest** (AUC test 0,9997). El Árbol de Decisión queda a un pelo (0,9982) y es más interpretable.
- **No hay sobreajuste:** AUC en train ≈ test en los tres modelos (RF: 1,0000 vs 0,9997).
- **La Regresión Logística** (lineal) es peor: en test deja **171 bajas sin detectar** (falsos negativos).
- **Variables más importantes (RF):** Support Calls (0,31), Total Spend (0,22), Age (0,13), Payment Delay (0,12).

---

## 3. INFORME CIENTÍFICO — texto listo para pegar

### 3.1 Metodología (sección de modelado)

> **Planteamiento.** Predecir la baja es un problema de clasificación binaria supervisada (etiqueta
> `Churn_YesNo`). Definimos la baja como clase positiva (`label = 1`) por ser el evento a detectar.
>
> **Preprocesado.** Las variables categóricas (`Gender`, `Subscription Type`, `Contract Length`) se
> transforman con `StringIndexer` + `OneHotEncoder`; las numéricas se ensamblan con `VectorAssembler`.
> Para la Regresión Logística se aplica además `StandardScaler`. `CustomerID` se excluye por ser un
> identificador.
>
> **Partición y validación.** Separamos 70% train / 30% test con semilla fija. Sobre el train
> aplicamos **selección de hiperparámetros con Grid Search y Validación Cruzada de 5 particiones**
> (`ParamGridBuilder` + `CrossValidator` de Spark ML), optimizando el **AUC**.
>
> **Elección de la métrica.** Reportamos y optimizamos el **AUC (área bajo la curva ROC)**, no la
> *accuracy*. En un problema de baja el coste de los errores es **asimétrico** (no detectar a un cliente
> que se marcha es más caro que un incentivo innecesario) y, sobre todo, interesa **ordenar** a los
> clientes por riesgo para actuar sobre los de mayor probabilidad; el AUC mide precisamente esa calidad
> de ordenación a lo largo de todos los umbrales, mientras que la *accuracy* se ata a un único umbral
> del 0,5. Complementamos con el **recall de la clase baja** (qué porcentaje de bajas capturamos).
>
> **Modelos.** Comparamos un **Árbol de Decisión** (interpretable), un **Random Forest** (ensemble, el
> más potente) y una **Regresión Logística** (baseline lineal).

### 3.2 Resultados (pegar la tabla del punto 2 y estas figuras)

> Insertar `figuras/t6_tabla_comparativa.png`, `figuras/t6_roc_train_test.png` y
> `figuras/t6_matrices_confusion_v2.png`.
>
> El **Random Forest** obtiene el mejor rendimiento (**AUC test = 0,9997**), seguido muy de cerca por
> el Árbol de Decisión (0,9982); la Regresión Logística queda en 0,958. Las **curvas ROC en train y
> test son prácticamente idénticas**, lo que descarta sobreajuste: el modelo generaliza. El elevado
> AUC se explica porque el dataset (sintético) contiene **patrones casi deterministas** —p. ej., el
> contrato mensual conlleva un 100% de baja y un retraso de pago superior a 20 días también—, de modo
> que el "techo" del problema es muy alto. Las variables más determinantes (llamadas a soporte, gasto
> total, edad y retraso de pago) coinciden con el análisis de correlación, lo que da **coherencia** al
> modelo.

### 3.3 Próximos pasos (esto es lo que faltaba)

> **Próximos pasos / trabajo futuro.**
> 1. **Validación temporal (out-of-time):** entrenar con un periodo y validar con el siguiente para
>    estimar el rendimiento real en despliegue, más exigente que el *split* aleatorio.
> 2. **Recalibración y umbral por coste:** ajustar el umbral de decisión a partir de una matriz de
>    coste real (valor del cliente frente a coste del incentivo), en lugar del 0,5 por defecto.
> 3. **Más modelos:** probar *Gradient-Boosted Trees* (Spark) o XGBoost y comparar.
> 4. **Explicabilidad:** valores SHAP para justificar cada predicción ante el equipo de retención.
> 5. **Ingeniería de variables:** ratios (gasto/antigüedad), tendencias de uso, incidencias por mes.
> 6. **Industrialización:** *pipeline* Spark reentrenable y programado, *scoring* por lotes exportado
>    al CRM y monitorización de *data drift*.
> 7. **Validación de negocio (A/B):** medir si la campaña de retención sobre el top-N de riesgo reduce
>    realmente la baja.

---

## 4. INFORME TÉCNICO — cómo estructurarlo mejor

El feedback pide **más estructura y descripción** (es el documento para que otro continúe el proyecto).
Propuesta de índice, con **texto entre los bloques de código** (no solo código):

1. **Portada, índice y resumen ejecutivo** (1 párrafo: problema, datos, resultado principal).
2. **Arquitectura y entorno** — versiones exactas (Spark 3.5.3, Java 17, Cassandra 5.0 en Docker,
   Python 3.x) + diagrama `CSV → Cassandra → PySpark`.
3. **Tarea 1 — Estructura del dato** — tabla campo/tipo y decisiones (p. ej., `CustomerID` como
   categórica).
4. **Tarea 2 — Cassandra** — por qué NoSQL, modelo de datos, y **cada comando explicado** (qué hace y
   por qué), no solo pegado.
5. **Tareas 3–5 — EDA en PySpark** — para cada tarea: *objetivo → código → salida → interpretación*.
6. **Tarea 6 — Machine Learning** — planteamiento, preprocesado, **validación (Grid Search + CV)**,
   resultados train/test, curvas ROC, importancia de variables.
7. **Reproducibilidad** — cómo ejecutar (dependencias, comando), semillas y rutas.
8. **Limitaciones y próximos pasos.**

**Regla práctica:** cada bloque de código va **precedido** de una frase "qué hace y por qué" y
**seguido** de otra "qué observamos". Eso convierte un cuaderno de código en documentación técnica.

---

## 5. PRESENTACIÓN — qué diapositivas añadir

En la sección de **Resultados**, añade (lo pide el feedback):
1. **Diapositiva "Tabla comparativa test–train–modelos"** → imagen `figuras/t6_tabla_comparativa.png`.
2. **Diapositiva "Curvas ROC (train y test)"** → imagen `figuras/t6_roc_train_test.png`.
3. (Recomendado) **Diapositiva "Sin sobreajuste"** → `figuras/t6_auc_train_vs_test.png`, con una frase:
   "AUC train ≈ AUC test ⇒ el modelo generaliza".
4. (Recomendado) Sustituir la antigua gráfica de métricas por `figuras/t6_matrices_confusion_v2.png`
   para enseñar que la Regresión Logística deja escapar 171 bajas.

Añade también una frase en la diapositiva de método: **"Métrica de referencia: AUC (no accuracy)"**.

---

## 6. Banco de preguntas de defensa (con respuesta breve)

- **¿Por qué comparáis Árbol de Decisión y Random Forest?** El árbol da interpretabilidad directa
  (reglas); el Random Forest, al promediar muchos árboles, reduce la varianza y mejora el AUC.
  Comparamos ambos + un baseline logístico.
- **¿Qué es Grid Search + Cross Validation?** Grid Search prueba combinaciones de hiperparámetros; la
  validación cruzada de k=5 evalúa cada combinación en 5 particiones del train para no depender de un
  único reparto. Elegimos la que maximiza el AUC medio.
- **¿Por qué optimizáis por AUC y no accuracy?** Coste asimétrico (un falso negativo = cliente perdido)
  y necesidad de **ordenar** por riesgo; la accuracy solo mira un umbral fijo. (ver punto 3.1).
- **Vuestro AUC es casi 1, ¿no es sospechoso / hay fuga de datos?** No: el AUC en **train ≈ test** y
  coincide con la validación cruzada (si hubiera sobreajuste, el test caería). El valor alto viene de
  que el dataset **sintético** tiene reglas casi deterministas (contrato mensual → 100% baja; retraso
  de pago > 20 → 100%; gasto ≤ 500 → 100%). Es una propiedad de los datos.
- **¿Por qué la baja es la clase positiva?** Porque es el evento que queremos detectar; así el recall y
  la curva ROC se leen sobre "capturar bajas".
- **¿Cómo se usaría en la empresa?** *Scoring* por lotes → ranking de riesgo → campaña sobre el top-N →
  medir la reducción de baja (A/B).
- **¿Es "big data" con 10.000 filas?** El volumen es didáctico, pero el pipeline (Cassandra + Spark +
  ML distribuido) **escala a millones de filas sin cambiar el código**.
- **¿Por qué Contract Length casi no aparece en la importancia si el mensual es 100% baja?** Porque los
  clientes con contrato mensual son pocos y su baja ya queda explicada por variables numéricas (gasto,
  soporte); el Random Forest reparte la importancia hacia esas variables más generales.

---

## 7. Cómo re-ejecutar el notebook (Google Colab)

1. Sube `churn_pyspark_colab.ipynb` y `customer_churn_10k.csv` a Colab.
2. Ejecuta las celdas en orden. La Tarea 6 tarda unos minutos (Grid Search + CV).
3. Las figuras se muestran en línea. Para exportarlas, añade `plt.savefig('nombre.png')` antes de
   `plt.show()` en la celda correspondiente.

> Nota: el notebook usa `pyspark`, `scikit-learn`, `matplotlib` y `pandas` (todas preinstaladas en
> Colab salvo `pyspark`, que instala la primera celda).
