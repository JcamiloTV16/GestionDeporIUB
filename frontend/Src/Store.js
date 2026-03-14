import { writable, derived } from 'svelte/store';

// --- BLOQUE: RECUPERACIÓN DE SESIÓN ---
const usuarioGuardado = JSON.parse(localStorage.getItem('user') || 'null');
const rolGuardado = localStorage.getItem('rol') || '';
const tokenGuardado = localStorage.getItem('token') || '';

// --- BLOQUE: STORES DE ESTADO ---
export const user = writable(usuarioGuardado);
export const rol = writable(rolGuardado);
export const token = writable(tokenGuardado);

// -- NUEVO: Estado de autenticación (se calcula automáticamente si hay un usuario)
export const isAuthenticated = derived(user, ($user) => $user !== null);

// --- BLOQUE: PERSISTENCIA (LocalStorage) ---
rol.subscribe(valor => {
    if (valor) localStorage.setItem('rol', valor);
    else localStorage.removeItem('rol');
});

user.subscribe(valor => {
    if (valor) localStorage.setItem('user', JSON.stringify(valor));
    else localStorage.removeItem('user');
});

token.subscribe(valor => {
    if (valor) localStorage.setItem('token', valor);
    else localStorage.removeItem('token');
});

// --- BLOQUE: FUNCIONES GLOBALES ---
export function cerrarSesion() {
    user.set(null);
    rol.set('');
    token.set('');
    // Al limpiar los stores, el suscribe borrará automáticamente el LocalStorage
}