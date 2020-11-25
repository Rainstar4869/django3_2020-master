module.exports = {
  "env": {
    "browser": true,
    "es6": true,
    "node": true
  },
  plugins: ['vue'],
  "extends": "eslint:recommended",
  "globals": {
    "Atomics": "readonly",
    "SharedArrayBuffer": "readonly"
  },
  // "parser": "babel-eslint",
  "parser": "vue-eslint-parser",
  "parserOptions": {
    "ecmaVersion": 2018,
    "sourceType": "module"
  },
  "rules": {
    "strict": 0,
    "indent": ["error", 4],                                  // インデント 半角スペース2
    "quotes": ["error", "single", {"avoidEscape": true}],  // ダブルクォート禁止
    "semi": ["error", "always"],
    "semi-spacing": ["error", {"after": true, "before": false}],
    "semi-style": ["error", "last"],
    "no-extra-semi": "error",
    "no-unexpected-multiline": "error",
    "no-unreachable": "error",                         // セミコロン禁止
    "comma-dangle": ["error", "never"]
  }
};