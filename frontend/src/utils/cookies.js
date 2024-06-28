import Cookies from 'js-cookie';

export function setCookie(name, value) {
  const jsonString = JSON.stringify(value);
  Cookies.set(name, jsonString, { expires: 7 });
}

export function getCookie(name) {
  const value = Cookies.get(name);
  if (value) {
    console.log(value, value.replace('|', ',').replace(/\\/g, ''));
    return JSON.parse(value.replace('|', ',').replace(/\\/g, ''));
  }
  return null;
}

export function removeCookie(name) {
  Cookies.remove(name);
}
