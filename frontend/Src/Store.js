import { writable, derived } from 'svelte/store';

const usuarioGuardado = JSON.parse(localStorage.getItem('user') || 'null');
const rolGuardado = localStorage.getItem('rol') || '';
const tokenGuardado = localStorage.getItem('token') || '';

export const user = writable(usuarioGuardado);
export const rol = writable(rolGuardado);
export const token = writable(tokenGuardado);

export const isAuthenticated = derived(user, ($user) => $user !== null);

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

export function cerrarSesion() {
    user.set(null);
    rol.set('');
    token.set('');
}