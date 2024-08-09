import { __module as withSelector } from "../../../_virtual/with-selector.mjs";
import { __require as requireWithSelector_production_min } from "../cjs/use-sync-external-store-shim/with-selector.production.min.mjs";
import { __require as requireWithSelector_development } from "../cjs/use-sync-external-store-shim/with-selector.development.mjs";
if (process.env.NODE_ENV === "production") {
  withSelector.exports = requireWithSelector_production_min();
} else {
  withSelector.exports = requireWithSelector_development();
}
var withSelectorExports = withSelector.exports;
export {
  withSelectorExports as w
};
//# sourceMappingURL=with-selector.mjs.map
