module.exports = {
  content: ["src/Backend/templates/**/*.{html, js}",],
  theme: {
    extend: {},
  },
  mode: ["jit"],
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
  ],
}
