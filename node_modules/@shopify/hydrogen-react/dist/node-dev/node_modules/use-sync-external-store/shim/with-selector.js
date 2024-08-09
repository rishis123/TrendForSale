"use strict";
Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const withSelector = require("../../../_virtual/with-selector.js");
const withSelector_production_min = require("../cjs/use-sync-external-store-shim/with-selector.production.min.js");
const withSelector_development = require("../cjs/use-sync-external-store-shim/with-selector.development.js");
if (process.env.NODE_ENV === "production") {
  withSelector.__module.exports = withSelector_production_min.__require();
} else {
  withSelector.__module.exports = withSelector_development.__require();
}
var withSelectorExports = withSelector.__module.exports;
exports.withSelectorExports = withSelectorExports;
//# sourceMappingURL=with-selector.js.map
