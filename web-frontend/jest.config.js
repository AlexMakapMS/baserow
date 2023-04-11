const esModules = ['@nuxtjs/i18n'].join('|')

module.exports = {
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['js', 'json', 'vue'],
  transform: {
    '^.+\\.js$': 'babel-jest',
    '^.+\\.vue$': '@vue/vue2-jest',
    '^.+\\.svg$': '<rootDir>/test/helpers/stubSvgTransformer.js',
  },
  moduleNameMapper: {
    '^@baserow/(.*)$': '<rootDir>/$1',
    '^@/(.*)$': '<rootDir>/$1',
    '^~/(.*)$': '<rootDir>/$1',
    '^vue$': '<rootDir>/node_modules/vue/dist/vue.common.js',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  transformIgnorePatterns: [
    `<rootDir>/web-frontend/node_modules/(?!${esModules})`,
  ],
  testMatch: ['<rootDir>/test/unit/**/*.spec.js'],
}
