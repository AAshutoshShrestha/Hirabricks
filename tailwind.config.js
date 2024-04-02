/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.{html,js}",
        "./statics/**/*.{html,js}",
        "./staticfiles_build/**/*.{html,js}",
    ],
    theme: {
      extend: {
        animation: {
          'spin-slow': 'spin 8s linear infinite',
        },
        colors: {
          primary: '#b53721',
          secondary: '#7d1c0b',
        },
      },
    },
    plugins: [],
  }