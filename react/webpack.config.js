const path = require("path");
const webpack = require("webpack");
const HtmlWebPackPlugin = require("html-webpack-plugin");

const PATH = path.resolve(__dirname + "/build");

module.exports = {
  entry: "./src/index.js",
  output: {
    filename: "bundle.js",
    path: PATH,
  },
  devServer: {
    static: PATH,
    compress: true,
    historyApiFallback: true,
    proxy: {
      "/api/v1/*": {
        target: "https://127.0.0.1",
        secure: false,
      },
      "/api/v0/*": {
        target: "https://127.0.0.1",
        secure: false,
      },
    },
    liveReload: false,
    hot: false,
    port: 3000,
  },
  mode: "development",
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: "/node_modules",
        use: ["babel-loader"],
      },
      { test: /\.css$/i, use: ["css-loader"] },
      {
        test: /\.html$/,
        exclude: [/node_modules/],
        use: [
          {
            loader: "html-loader",
            options: { minimize: true },
          },
        ],
      },
      {
        test: /\.svg$/,
        use: [
          {
            loader: "@svgr/webpack",
          },
        ],
      },
    ],
  },
  plugins: [
    new HtmlWebPackPlugin({
      template: path.join(__dirname, "public", "index.html"),
      filename: "index.html",
    }),
    new webpack.ProvidePlugin({
      React: "react",
    }),
  ],
  stats: { children: true },
};
