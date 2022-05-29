const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  chainWebpack: (config) => {
    config.plugin("html").tap((args) => {
      args[0].title = "Battle Royale de culture générale";
      return args;
    });
  },
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === "production" ? "/~quizz/" : "/",
  productionSourceMap: false,
});
