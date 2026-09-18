# Pruebas funcionales en Swagger

1. Desde la raíz del proyecto, con el entorno virtual activo, inicia la API con `python -m uvicorn app.main:app --reload` y abre `/docs`.
2. En POST /users, pulsa **Try it out** y crea
   `{"name":"Samir Acosta","email":"samir@example.com","role":"user","is_active":true}`.
   Espera 201 y guarda el ID. Si ya existe ese correo, usa otro para esta ejecución.
3. Repite el POST: espera 400 por correo duplicado.
4. Ejecuta GET /users: espera 200 y el usuario creado.
5. Ejecuta GET /users/{user_id} con el ID guardado: espera 200.
6. Consulta un ID que no exista: espera 404.
7. En GET /users, usa role=user: verifica el filtro.
8. Usa is_active=true: verifica que todos estén activos.
9. Prueba sort_by=name y created_at con order=asc y desc.
10. Ejecuta PUT con los cuatro campos y cambia role a support: espera 200.
11. Ejecuta PATCH con `{"is_active":false}`: espera 200 y los demás campos conservados.
12. Reinicia Uvicorn y consulta el ID: el usuario sigue presente e inactivo.
13. Prueba role=invalid, email sin formato y name=ab: espera 422.
14. Ejecuta DELETE del ID guardado: espera 204 sin contenido.
15. Consulta el ID eliminado: espera 404.
16. Intenta PUT, PATCH y DELETE sobre el ID eliminado: espera 404 con cuerpos válidos.

Guarda capturas de los resultados de tu ejecución. El README ya incluye las
capturas generadas automáticamente y `resultados.json` conserva 17 respuestas
HTTP reales. Las pruebas automatizadas comprueban además la persistencia y
las restricciones directamente en SQLite.
