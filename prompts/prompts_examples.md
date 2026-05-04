### Estructura Básica
- Zero-shot: Consiste en dar una instrucción directa y pedir una respuesta inmediata, sin proporcionar ningún ejemplo previo al modelo.

- Few-shot: Implica incluir unos pocos ejemplos de lo que esperas (pares de pregunta y respuesta o entrada y salida) dentro del prompt para que el modelo entienda el patrón, formato o estilo deseado antes de resolver tu petición real.

- Role-Prompting: Se trata de pedirle al modelo que asuma un rol, profesión o personaje específico (por ejemplo, "Actúa como un analista de datos senior") para que su respuesta adopte la terminología, el tono y la perspectiva adecuados para ese perfil.

### Razonamiento
- Chain of thought: Invita al modelo a desglosar su razonamiento paso a paso antes de llegar a la conclusión final mostrando ejemplos previos de cómo deducir la respuesta. Es muy útil para problemas matemáticos o lógicos complejos.

- Zero-Shot Chain of Thought: Es una variante donde simplemente se añade una frase estructurada como "Pensemos en esto paso a paso" al final del prompt, forzando al modelo a razonar su proceso lógico sin necesidad de darle ejemplos de resolución previos.

- Tree of Thoughts: Plantea el problema de manera que el modelo explore múltiples caminos o ramas de pensamiento de forma paralela, evalúe la viabilidad de cada uno de esos pasos intermedios y luego elija la mejor ruta para llegar a la solución, simulando un árbol de decisiones.

- Self-consistency: Genera varias rutas de razonamiento diferentes para un mismo problema y luego selecciona la respuesta que más se repite o la conclusión más consistente entre todas las opciones generadas, aumentando la probabilidad de acierto.

### Refinamiento
- Self-refinement: Pide al modelo que genere un primer borrador de la respuesta, que luego él mismo evalúe y critique para detectar errores o áreas de mejora, y finalmente reescriba una versión optimizada basándose en su propia autoevaluación.

- Expert Ensemble: Simula un panel donde varios agentes o expertos virtuales con diferentes especialidades discuten el problema, aportan sus puntos de vista particulares y debaten hasta llegar a un consenso para ofrecer una respuesta mucho más robusta y multidisciplinar.

- Meta prompting: Utiliza el modelo para reflexionar sobre el propio proceso de creación de instrucciones. Se le pide a la IA que escriba un prompt mejorado para una tarea específica, o que actúe como un ingeniero de prompts para evaluar y refinar las instrucciones antes de ejecutarlas.