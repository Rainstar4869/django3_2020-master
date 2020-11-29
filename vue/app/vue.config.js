module.exports = {
  css: {
    loaderOptions: {
      css: {
        sourceMap: process.env.NODE_ENV !== "production" ? true : false
      }
    }
  },
    devServer: {
        port: 8080,
        disableHostCheck: true,
    },
};
