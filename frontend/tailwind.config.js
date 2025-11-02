/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        dark: "#1E1E2E",      // фон, шапка, карточки
        light: "#F8FAFC",     // основной светлый фон
        accent: "#7C3AED",    // акцент (фиолетовый)
        grayish: "#9CA3AF",   // второстепенный текст, бордеры
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false
  }
}
