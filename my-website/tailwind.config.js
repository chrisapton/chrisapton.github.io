/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    // You can set defaults for the whole theme, or extend them
    extend: {
      colors: {
        // Add custom colors
        brandBlue: "#1DA1F2",
        brandDark: "#15202B",
        brandLight: "#E1E8ED",
      },
      fontFamily: {
        // Add custom fonts
        sans: ["Inter", "system-ui", "sans-serif"],
        heading: ["Poppins", "sans-serif"],
      },
      fontSize: {
        // Custom text sizes
        'xxs': '0.65rem',
        '4.5xl': '2.5rem',
      },
      spacing: {
        // Custom spacing scale
        '108': '27rem',
      },
      // You can add custom box shadows, transition durations, etc.
      boxShadow: {
        'brand': '0 4px 14px 0 rgba(29,161,242,0.39)',
      },
    },
  },
  plugins: [],
};


