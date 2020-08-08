const webpack = require("webpack"),
    merge = require("webpack-merge"),
    dotenv = require("dotenv"),
    common = require("./webpack.common.js"),
    BundleTracker = require("webpack-bundle-tracker");


const env = dotenv.config().parsed;
const envKeys = Object.keys(env).reduce((prev, next) => {
    prev[`process.env.${next}`] = JSON.stringify(env[next]);
    return prev;
}, {});

module.exports = merge(common, {
    context: __dirname,
    mode: "development",
    devtool: "inline-source-map",
    plugins: [
        new webpack.DefinePlugin(envKeys),
        new BundleTracker({
            path: __dirname,
            filename: "webpack-stats.json",
            indent: 4
        })
    ]
});
