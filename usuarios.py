import streamlit as st
from db import connect_db

def gestionar_usuarios():
    st.subheader("👤 Gestión de Usuarios")

    # Mostrar mensajes de éxito almacenados en session_state
    if "msg_success" in st.session_state:
        st.success(st.session_state["msg_success"])
        del st.session_state["msg_success"]

    tab1, tab2 = st.tabs(["➕ Crear Usuario", "🧾 Lista de Usuarios"])

    # --- TAB 1: Crear Usuario ---
    with tab1:
        st.markdown("### ➕ Crear nuevo usuario")
        with st.form("crear_usuario_form"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre completo")
                usuario = st.text_input("Usuario")
                password = st.text_input("Contraseña", type="password")
                departamento = st.text_input("Departamento")
            with col2:
                email = st.text_input("Correo electrónico")
                rol = st.selectbox("Rol", ["admin", "tecnico", "usuario"])
                estado = st.selectbox("Estado", ["activo", "inactivo"])
                confirmar_creacion = st.checkbox("Confirmo que deseo crear este usuario")
            submitted = st.form_submit_button("Crear Usuario")

            if submitted:
                if not confirmar_creacion:
                    st.warning("⚠️ Debes confirmar la creación del usuario.")
                elif nombre and usuario and password and email and departamento:
                    try:
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO Usuarios (nombre, usuario, password, email, rol, departamento, estado)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (nombre, usuario, password, email, rol, departamento, estado))
                        conn.commit()
                        st.session_state["msg_success"] = "✅ Usuario creado exitosamente"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error al crear el usuario: {e}")
                    finally:
                        conn.close()
                else:
                    st.warning("⚠️ Por favor completa todos los campos")
    # --- TAB 2: Lista de Usuarios ---
    with tab2:
        st.markdown("### 🧾 Usuarios registrados")

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, usuario, email, rol, departamento, estado FROM Usuarios")
            rows = cursor.fetchall()

            for row in rows:
                user_id = row.id_usuario
                st.markdown(f"**ID Usuario: {user_id}**")

                with st.expander(f"👤 {row.nombre} - {row.usuario}"):
                    nombre_edit = st.text_input("Nombre", row.nombre, key=f"nombre_{user_id}")
                    usuario_edit = st.text_input("Usuario", row.usuario, key=f"usuario_{user_id}")
                    email_edit = st.text_input("Correo", row.email, key=f"email_{user_id}")
                    rol_edit = st.selectbox("Rol", ["admin", "tecnico"], index=["admin", "tecnico"].index(row.rol), key=f"rol_{user_id}")
                    departamento_edit = st.text_input("Departamento", row.departamento, key=f"depto_{user_id}")
                    estado_edit = st.selectbox("Estado", ["activo", "inactivo"], index=["activo", "inactivo"].index(row.estado), key=f"estado_select_{user_id}")

                    col1, col2, col3 = st.columns(3)

                    # ACTUALIZAR USUARIO
                    with col1:
                        if st.checkbox("Confirmar actualización", key=f"confirm_update_{user_id}"):
                            if st.button("💾 Actualizar", key=f"btn_actualizar_{user_id}"):
                                try:
                                    cursor.execute("""
                                        UPDATE Usuarios 
                                        SET nombre = ?, usuario = ?, email = ?, rol = ?, departamento = ?, estado = ?
                                        WHERE id_usuario = ?
                                    """, (nombre_edit, usuario_edit, email_edit, rol_edit, departamento_edit, estado_edit, user_id))
                                    conn.commit()
                                    st.session_state["msg_success"] = "✅ Usuario actualizado exitosamente"
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error al actualizar: {e}")

                    # CAMBIAR ESTADO
                    with col2:
                        nuevo_estado = "inactivo" if row.estado == "activo" else "activo"
                        if st.button(f"🔁 Cambiar a {nuevo_estado}", key=f"btn_cambiar_estado_{user_id}"):
                            try:
                                cursor.execute("UPDATE Usuarios SET estado = ? WHERE id_usuario = ?", (nuevo_estado, user_id))
                                conn.commit()
                                st.session_state["msg_success"] = f"✅ Estado cambiado a {nuevo_estado}"
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error al cambiar estado: {e}")

                    # ELIMINAR USUARIO
                    with col3:
                        if st.checkbox("Confirmar eliminación", key=f"confirm_delete_{user_id}"):
                            if st.button("🗑️ Eliminar", key=f"btn_eliminar_{user_id}"):
                                try:
                                    cursor.execute("DELETE FROM Usuarios WHERE id_usuario = ?", (user_id,))
                                    conn.commit()
                                    st.session_state["msg_success"] = "✅ Usuario eliminado correctamente"
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error al eliminar: {e}")

        except Exception as e:
            None#st.error(f"❌ Error al obtener usuarios: {e}")
        finally:
            conn.close()
