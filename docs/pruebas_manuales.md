# Pruebas manuales desde Swagger

Ejecuta `uvicorn app.main:app --reload` desde la raíz y abre
http://127.0.0.1:8000/docs. En cada operación pulsa **Try it out**, completa los
parámetros y el cuerpo si corresponde, y pulsa **Execute**.

Empieza con un servidor recién iniciado. Guarda el ID devuelto por el POST de
la prueba 2 (normalmente 4) y úsalo donde se indica `{id}`. `99999` representa
un usuario inexistente. Las direcciones de correo son texto normal, sin enlaces
Markdown. GET y DELETE no llevan cuerpo JSON.

## 1. GET /users

No completes filtros. Esperado: **200**, tres usuarios iniciales.

## 2. POST /users válido

```json
{
  "name": "Samir Acosta",
  "email": "samir@example.com",
  "role": "user",
  "is_active": true
}
```

Esperado: **201**, devuelve estos datos y un `id` generado. Anota ese ID.

## 3. POST con email repetido

```json
{
  "name": "Samir Repetido",
  "email": "SAMIR@EXAMPLE.COM",
  "role": "user",
  "is_active": true
}
```

Esperado: **400**, `{"detail":"El correo electrónico ya está registrado"}`.

## 4. POST con email inválido

```json
{
  "name": "Samir Acosta",
  "email": "correo-invalido",
  "role": "user",
  "is_active": true
}
```

Esperado: **422**, error de validación en `email`.

## 5. GET /users/{id}

En `user_id` escribe el ID de la prueba 2. Esperado: **200**, usuario creado.

## 6. GET usuario inexistente

En `user_id` escribe `99999`. Esperado: **404**, `{"detail":"Usuario no encontrado"}`.

## 7. PUT válido

En `user_id` escribe el ID de la prueba 2 y pega:

```json
{
  "name": "Samir Acosta Peña",
  "email": "samir@example.com",
  "role": "support",
  "is_active": true
}
```

Esperado: **200**, todos los campos actualizados, mismo ID. Se permite conservar
el correo propio. Si omites cualquiera de los cuatro campos, debe responder 422.

## 8. PUT usuario inexistente

Usa `user_id=99999` y el mismo JSON completo de la prueba 7.
Esperado: **404**, `{"detail":"Usuario no encontrado"}`.

## 9. PATCH solo role

Usa el ID de la prueba 2 y pega:

```json
{
  "role": "user"
}
```

Esperado: **200**, cambia el rol de support a user y mantiene nombre, correo,
estado e ID. También puedes enviar `{"role":"support"}` para volver al rol anterior.

## 10. PATCH vacío

Usa el ID de la prueba 2:

```json
{}
```

Esperado: **400**, `{"detail":"Debe enviar al menos un campo para actualizar"}`.

## 11. DELETE válido

Usa el ID de la prueba 2. Esperado: **204**, sin cuerpo de respuesta.

## 12. DELETE usuario inexistente

Vuelve a eliminar el mismo ID o usa `99999`.
Esperado: **404**, `{"detail":"Usuario no encontrado"}`.

## 13. GET filtrado por role

En GET `/users`, escribe `admin` en `role` y deja `is_active` sin enviar.
Esperado: **200**, solo el administrador. Repite con `support`: solo soporte.

## 14. GET filtrado por is_active

Quita el filtro `role`. Envía `is_active=false`: debe retornar el usuario inactivo
con ID 3. Con `true`: los usuarios activos. Esperado: **200**.
Combina `role=admin` e `is_active=true`: solo el administrador.

## Comprobaciones adicionales

- En POST, usa el JSON de la prueba 2 cambiando `role` a `technician`: **400**,
  `{"detail":"Rol no permitido"}`.
- En PATCH `/users/1`, pega `{"email":"SUPPORT@DEVICESYSTEMS.COM"}`: **400**, correo duplicado.
- En PATCH `/users/1`, pega `{"name":null}`: **422**.
- Revisa **Response headers**: `x-app-name: device_systems` y
  `x-api-version: 2.0.0`, también en errores y en DELETE 204.
- Abre `/redoc` y `/openapi.json`. Comprueba los seis endpoints agrupados como `Users`.

Guarda capturas reales en `docs/images/`; consulta los marcadores del README.
