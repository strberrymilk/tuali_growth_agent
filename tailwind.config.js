import daisyui from "daisyui"
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {} },
  plugins: [daisyui],
  daisyui: {
    themes: [
      {
        tuali: {
          "primary": "#E4002B",
          "primary-content": "#ffffff",
          "secondary": "#F16321",
          "secondary-content": "#ffffff",
          "accent": "#FFB800",
          "neutral": "#1A1A1A",
          "base-100": "#FFFFFF",
          "base-200": "#F5F5F5",
          "base-300": "#E8E8E8",
          "info": "#3B82F6",
          "success": "#22C55E",
          "warning": "#FFB800",
          "error": "#E4002B",
        },
      },
    ],
  },
}

