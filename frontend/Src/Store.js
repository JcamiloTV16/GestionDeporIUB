import { writable } from 'svelte/store';

// Intentar recuperar la sesión de localStorage
const savedUser = JSON.parse(localStorage.getItem('user') || 'null');
const savedRol = localStorage.getItem('rol') || '';

export const rol = writable(savedRol);
export const user = writable(savedUser);

// Suscribirse para guardar cambios en localStorage
rol.subscribe(value => {
    if (value) localStorage.setItem('rol', value);
    else localStorage.removeItem('rol');
});

user.subscribe(value => {
    if (value) localStorage.setItem('user', JSON.stringify(value));
    else localStorage.removeItem('user');
});