// Allow to transform some ESM installed modules
const esModules = ['@nuxtjs/i18n'].join('|')
module.exports = {
  rootDir: '../../../../',
  moduleDirectories: ['<rootDir>/web-frontend/node_modules/'],
  modulePaths: ['<rootDir>/web-frontend/node_modules/'],
  moduleNameMapper: {
    '^@baserow/(.*)$': '<rootDir>/web-frontend/$1',
    '^@baserow_enterprise/(.*)$':
      '<rootDir>/enterprise/web-frontend/modules/baserow_enterprise/$1',
    '^@baserow_enterprise_test/(.*)$':
      '<rootDir>/enterprise/web-frontend/test/$1',
    '^@/(.*)$': '<rootDir>/web-frontend/$1',
    '^~/(.*)$': '<rootDir>/web-frontend/$1',
    '^vue$': '<rootDir>/web-frontend/node_modules/vue/dist/vue.common.js',
  },
  moduleFileExtensions: ['js', 'vue', 'json'],
  transform: {
    '^.+\\.js$': [
      'babel-jest',
      { configFile: __dirname + '/../../../web-frontend/babel.config.js' },
    ],
    '.*\\.(vue)$': '<rootDir>/web-frontend/node_modules/@vue/vue2-jest',
    '^.+\\.svg$': '<rootDir>/web-frontend/test/helpers/stubSvgTransformer.js',
  },
  transformIgnorePatterns: [
    `<rootDir>/web-frontend/node_modules/(?!(baserow|${esModules})/)`,
  ],
}
