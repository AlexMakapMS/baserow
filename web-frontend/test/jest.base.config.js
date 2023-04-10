// Allow to transform some ESM installed modules
const esModules = ['@nuxtjs/i18n'].join('|')

module.exports = {
  rootDir: '../../../',
  testEnvironment: 'node',
  moduleNameMapper: {
    '^@baserow/(.*)$': '<rootDir>/web-frontend/$1',
    '^@/(.*)$': '<rootDir>/web-frontend/$1',
    '^~/(.*)$': '<rootDir>/web-frontend/$1',
    '^vue$': '<rootDir>/web-frontend/node_modules/vue/dist/vue.common.js',
  },
  moduleFileExtensions: ['js', 'vue', 'json'],
  transform: {
    '^.+\\.js$': ['babel-jest', { configFile: __dirname + '/../babel.config.js' }],
    '.*\\.(vue)$': '<rootDir>/web-frontend/node_modules/@vue/vue2-jest',
    '^.+\\.svg$': '<rootDir>/web-frontend/test/helpers/stubSvgTransformer.js',
  },
  transformIgnorePatterns: [
    `<rootDir>/web-frontend/node_modules/(?!${esModules})`,
  ],
}
