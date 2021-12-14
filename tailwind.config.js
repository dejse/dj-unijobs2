module.exports = {
  content: ["Backend/templates/**/*.{html, js}",],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
  ],
}
