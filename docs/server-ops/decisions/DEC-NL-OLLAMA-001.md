# DEC-NL-OLLAMA-001 - Runtime LLM Local para Nortiqa

Estado: propuesta aprobada operativamente por Gio, pendiente de canon Notion  
Fecha: 2026-06-18  
Alcance: Nortiqa Lab / VPS SC2027  

## Decision

Nortiqa usara **Ollama nativo en el VPS** como runtime LLM local principal.

No se dockeriza Ollama por ahora. La PC local de Gio queda como laboratorio
opcional, no como entorno productivo ni fuente oficial de ejecucion.

## Contexto

El VPS ya tiene Ollama instalado y operativo:

- Binario: `/usr/local/bin/ollama`
- Version verificada: `0.30.8`
- API local: `http://127.0.0.1:11434`
- Modelos presentes:
  - `mistral:latest`
  - `phi3:mini`

El objetivo es mantener baja la complejidad operacional mientras Nortiqa avanza
con agentes, n8n, consola y staging.

## Arquitectura Elegida

```text
Agentes / n8n / Nortiqa Console
        |
        v
Ollama nativo en VPS
        |
        v
Modelos locales: mistral, phi3, futuros modelos
```

## Reglas Operativas

- Ollama no debe exponerse publicamente a internet.
- El endpoint autorizado por defecto es `http://127.0.0.1:11434`.
- Los agentes deben consumir Ollama desde el VPS o red interna controlada.
- Los modelos nuevos se prueban primero en staging o entorno controlado.
- La PC local puede usarse para experimentar prompts/modelos, pero no reemplaza
  el runtime del servidor.
- Docker para Ollama queda diferido hasta que exista necesidad real de
  reproducibilidad, migracion o multi-nodo.

## Alternativas Consideradas

### Ollama en PC local

Ventajas:

- Buen entorno de laboratorio.
- Permite pruebas offline sin tocar el servidor.

Desventajas:

- No sirve como runtime productivo de agentes.
- Depende del hardware y disponibilidad de la PC.
- Puede fragmentar modelos/configuracion.

Decision: permitido solo como laboratorio.

### Ollama en Docker

Ventajas:

- Aislamiento.
- Reproducibilidad.
- Facil migracion futura.

Desventajas:

- Agrega complejidad ahora.
- Requiere mas cuidado con volumenes, GPU/drivers y red.
- No aporta valor inmediato porque Ollama ya funciona nativo en el VPS.

Decision: diferido.

### Ollama nativo en VPS

Ventajas:

- Ya esta instalado y probado.
- Menos capas operativas.
- Integracion directa con agentes y servicios locales.
- Mantiene el puerto privado/local.

Desventajas:

- Reproducibilidad menor que Docker.
- Requiere documentar instalacion y backup de modelos/configuracion.

Decision: opcion elegida.

## Validacion Actual

Comandos verificados el 2026-06-18:

```bash
ollama --version
curl -fsS http://127.0.0.1:11434/api/tags
```

Resultado:

- Ollama responde.
- Modelos `mistral:latest` y `phi3:mini` disponibles.

## Siguiente Paso

1. Documentar healthcheck Ollama en el kit OPS.
2. Agregar variable estandar para agentes: `OLLAMA_HOST=http://127.0.0.1:11434`.
3. Mantener Ollama fuera de exposicion publica.
4. Evaluar Docker solo en una fase posterior de estandarizacion.

