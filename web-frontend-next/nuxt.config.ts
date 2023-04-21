// https://nuxt.com/docs/api/configuration/nuxt-config

import en from "./locales/en.json";
import fr from "./locales/fr.json";
import nl from "./locales/nl.json";
import de from "./locales/de.json";
import es from "./locales/es.json";
import it from "./locales/it.json";
import pl from "./locales/pl.json";

const locales = [
    { code: "en", name: "English", file: "en.json" },
    { code: "fr", name: "Français", file: "fr.json" },
    { code: "nl", name: "Nederlands", file: "nl.json" },
    { code: "de", name: "Deutsch", file: "de.json" },
    { code: "es", name: "Español", file: "es.json" },
    { code: "it", name: "Italiano", file: "it.json" },
    { code: "pl", name: "Polski (Beta)", file: "pl.json" },
];

export default defineNuxtConfig({
    css: ["@/assets/sass/main.scss"],
    modules: ["@nuxtjs/i18n"],
    i18n: {
        strategy: "no_prefix",
        defaultLocale: "en",
        detectBrowserLanguage: {
            useCookie: true,
            cookieKey: "i18n-language",
        },
        locales,
        langDir: "locales",
    },
});
