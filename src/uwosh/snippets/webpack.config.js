const path = require("path");
const package_json = require("./package.json");
const patternslib_package_json = require("@patternslib/patternslib/package.json");
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
const webpack_config = require("@patternslib/dev/webpack/webpack.config").config;

module.exports = () => {
  let config = {
    entry: {
      snippets: path.resolve(__dirname, "browser/resources/snippets.js"),
    },
    output: {
      filename: "[name].js",
      path: path.resolve(__dirname, "browser/resources/build"),
    },
  };

  config = webpack_config({
    config,
    package_json,
  });

  config.plugins.push(
    mf_config({
      name: "uwosh_snippets",
      filename: "remote.snippets.js",
      remote_entry: config.entry.snippets,
      dependencies: {
        ...patternslib_package_json.dependencies,
        ...package_json.dependencies,
      },
      shared: {
        jquery: {
          singleton: true,
          requiredVersion: package_json.dependencies.jquery,
          eager: true,
        },
      },
    })
  );

  return config;
};
