# Simulador de manejo de memoria en Python

Este repositorio contiene una prueba de concepto de un simulador del sistema de manejo de memoria del lenguaje C (`malloc`, `realloc`, `free`) escrito en Python. El simulador está pensado con fines educativos para poder probar distintas situaciones (pérdidas de memoria, arítmetica de punteros, reinterpretación) en un lenguaje de más alto nivel.

El simulador provee las mismas operaciones sobre memoria que el lenguaje C:

- Pedir, redimensionar o liberar un bloque de memoria
- Reinterpretar un bloque de memoria a un tipo distinto
- Acceder a una direccion de memoria
- Leer valores no inicializados
- Generar un segmentation fault al leer o escribir fuera de un bloque

La idea es ejecutar un programa que administra memoria de manera manual controlando el entorno para poder ver qué pasa cuando el entorno responde de distintas maneras (ej: generar o no un segmentation fault ante una lectura o escritura inválida) y poder observar con claridad
qué fue lo que causó el problema. Como próximos pasos, se quiere poder proveer una "visión general del heap" del programa, con el fin de poder entender otros conceptos como fragmentación.

Al finalizar el programa, el simulador da un resumen de todas las asignaciones de memoria que no fueron liberadas.

## Ejemplos

Los distintos ejemplos muestran como usar el simulador y explican algunos conceptos básicos. Cada uno de los ejemplos en Python viene acompañado del código equivalente que está simulando en C en la carpeta `examples-c`. Uno de los objetivos del simulador es que el código C y el código Python se vean idénticos salvo cuestiones de sintáxis.
